import aio_pika
from aio_pika import RobustConnection, RobustChannel, ExchangeType
from aio_pika.abc import AbstractRobustQueue, AbstractRobustExchange

from config import settings


class RabbitBroker:
    def __init__(self):
        self.url = settings.RABBITMQ_URL
        self.connection: RobustConnection | None = None
        self.channel: RobustChannel | None = None
        self.exchange: AbstractRobustExchange | None = None
        self.dlx: AbstractRobustQueue | None = None
        self.queue: AbstractRobustQueue | None = None
        self.dlq: AbstractRobustQueue | None = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel(publisher_confirms=True)
        await self.channel.set_qos(prefetch_count=10)

        self.exchange = await self.channel.declare_exchange(name=settings.RABBITMQ_EXCHANGE,
                                                            type=ExchangeType.DIRECT, durable=True)
        self.dlx = await self.channel.declare_exchange(name='dlx', type=ExchangeType.DIRECT, durable=True)

        self.dlq = await self.channel.declare_queue(name='dlq', durable=True)
        self.queue = await self.channel.declare_queue(name=settings.RABBITMQ_QUEUE, durable=True,
                                                      arguments={'x-dead-letter-exchange': 'dlx',
                                                                 'x-dead-letter-routing-key': 'dlq'})

        await self.queue.bind(self.exchange, routing_key=settings.RABBITMQ_ROUTING_KEY)
        await self.dlq.bind(self.dlx, routing_key='dlq')

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
