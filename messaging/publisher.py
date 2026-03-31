import asyncio
import json
import logging

from aio_pika import Message

from config import settings
from messaging.rabbitmq import RabbitBroker
from outbox.models import PaymentOutbox
from outbox.schemas import OutboxSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitPublisher:
    MAX_RETRIES = 3

    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def send_message(self, record: PaymentOutbox):
        serializable_data = OutboxSchema.model_validate(record).model_dump(mode='json')
        payload = json.dumps(serializable_data).encode()
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                await self.broker.exchange.publish(Message(body=payload, delivery_mode=2),
                                                   routing_key=settings.RABBITMQ_ROUTING_KEY)
                return True

            except Exception as e:
                if attempt == self.MAX_RETRIES:
                    logger.error(f"RabbitPublisher failed to publish message: {e}")
                    return False
                delay = 2 ** attempt
                await asyncio.sleep(delay)
