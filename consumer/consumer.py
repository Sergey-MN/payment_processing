import asyncio
import json
import logging
import random
from uuid import UUID

from aio_pika import IncomingMessage

from consumer.consumer_repository import update_status, save_idempotency_key
from consumer.utils import send_webhook
from messaging.rabbitmq import RabbitBroker
from payments.database import session
from payments.models import Status

MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_message(message: IncomingMessage):
    async with message.process(requeue=False):
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                pay_data = json.loads(message.body.decode())

                payment_id = pay_data.get('id')
                idempotency_key = pay_data.get('idempotency_key')
                webhook_url = pay_data.get('payload').get('webhook_url')

                if attempt == 1:
                    async with session() as local_session:
                        if not await save_idempotency_key(local_session, UUID(idempotency_key)):
                            raise Exception("Duplicate idempotency key")

                async with session() as local_session:
                    async with local_session.begin():
                        await asyncio.sleep(random.uniform(2, 5))

                        status = Status.FAILED if random.random() < 0.10 else Status.SUCCEEDED

                        await update_status(local_session, payment_id, status)

                        if status == Status.FAILED:
                            raise Exception("Processing message failed")

                        await send_webhook(
                            webhook_url,
                            {
                                'payment_id': payment_id,
                                'idempotency_key': idempotency_key,
                                'status': status
                            }
                        )
                        return

            except Exception as e:
                logger.error(e)
                if attempt == MAX_RETRIES:
                    await send_webhook(
                        webhook_url,
                        {
                            'payment_id': payment_id,
                            'idempotency_key': idempotency_key,
                            'status': status
                        }
                    )
                    raise
                await asyncio.sleep(2 ** attempt)


async def start_consuming(broker: RabbitBroker):
    try:
        await broker.queue.consume(process_message, robust=True)
        await asyncio.Future()

    except KeyboardInterrupt:
        logger.info("Consumer stopped")
        raise

    finally:
        await broker.close()


async def main():
    broker = RabbitBroker()
    await broker.connect()
    await start_consuming(broker)


if __name__ == '__main__':
    asyncio.run(main())
