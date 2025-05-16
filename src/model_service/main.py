import json
import os
from typing import Any, Dict

import pika
from dotenv import load_dotenv

from src.model_service.infrastructure.models.inference import Inference

load_dotenv()

inference = Inference()


def on_request(ch, method, properties, body):
    data: Dict[str, Any] = json.loads(body.decode())

    print(data)
    model_name = data.get("model_name", "")
    prompt: str = data.get("prompt", "")
    max_length: int = data.get("max_length", 100)
    temperature: float = data.get("temperature", 0.5)
    top_k: int = data.get("top_k", 100)
    top_p: float = data.get("top_p", 0.95)

    result = inference.generate_text(model_name, prompt, max_length, temperature, top_k, top_p)
    print(result)

    generated_text = result["text"]
    token_count = int(result["token_count"])

    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=json.dumps({"text": generated_text, "token_count": token_count}).encode(),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    message_broker_host_url = os.environ.get("MESSAGE_BROKER_HOST_URL", "")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=message_broker_host_url, credentials=pika.PlainCredentials("guest", "guest"))
    )
    channel = connection.channel()
    channel.queue_declare(queue="text_generation_queue")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="text_generation_queue", on_message_callback=on_request)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
