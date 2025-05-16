import os
from typing import Any

import pika
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "")
MESSAGE_BROKER_HOST_URL = os.environ.get("MESSAGE_BROKER_HOST_URL", "")


# Initialize DB utils
class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# RabbitMQ
responses: dict[str, Any] = {}

connection_parameters = pika.ConnectionParameters(
    host=MESSAGE_BROKER_HOST_URL,
    credentials=pika.PlainCredentials("guest", "guest"),
)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

result = channel.queue_declare(queue="", exclusive=True)
callback_queue = result.method.queue


def on_response(ch, method, properties, body):
    responses[properties.correlation_id] = body


channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)
