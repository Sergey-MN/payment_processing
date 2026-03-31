import asyncio
import logging

from messaging.publisher import RabbitPublisher
from messaging.rabbitmq import RabbitBroker
from outbox.repository import OutboxRepository
from payments.database import session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutboxProducer:

    def __init__(self, publisher: RabbitPublisher, batch_size: int = 10):
        self.publisher = publisher
        self.batch_size = batch_size

    async def run(self):
        try:
            while True:
                async with session() as local_session:
                    repo = OutboxRepository(local_session)
                    async with local_session.begin():
                        records = await repo.get_new(limit=self.batch_size)

                        for record in records:
                            try:
                                await self.publisher.send_message(record)
                                await repo.mark_sent(record.id)

                            except Exception as e:
                                logger.error(f'Error record_id {record.id}: {e}')

                await asyncio.sleep(5)

        except KeyboardInterrupt:
            logger.info("Producer stopped")
            raise
        except Exception as e:
            logger.error(e)
        finally:
            await self.publisher.broker.close()


async def main():
    broker = RabbitBroker()
    await broker.connect()
    publisher = RabbitPublisher(broker)
    producer = OutboxProducer(publisher=publisher)
    await producer.run()


if __name__ == '__main__':
    asyncio.run(main())
