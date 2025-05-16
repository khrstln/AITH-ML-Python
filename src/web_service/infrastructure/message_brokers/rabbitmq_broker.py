import json
import uuid
from typing import Any, Dict, Optional

import pika

from src.web_service.core.message_brokers import IMessageBroker
from src.web_service.utils import (callback_queue, channel, connection,
                                   responses)


class RabbitmqBroker(IMessageBroker):
    @staticmethod
    async def generate_text(
        model_name: str,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
        username: str,
    ) -> Optional[Dict[str, Any]]:

        correlation_id = str(uuid.uuid4())

        message = json.dumps(
            {
                "model_name": model_name,
                "prompt": prompt,
                "max_length": max_length,
                "temperature": temperature,
                "top_k": top_k,
                "top_p": top_p,
                "username": username,
            }
        )

        responses[correlation_id] = None
        channel.basic_publish(
            exchange="",
            routing_key="text_generation_queue",
            properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=correlation_id),
            body=message,
        )
        while responses[correlation_id] is None:
            connection.process_data_events()

        try:
            response: Dict[str, Any] = json.loads(responses[correlation_id])
            return response
        except Exception:
            return None
