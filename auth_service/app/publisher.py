import json
from datetime import datetime, timezone
import pika
from app.config import settings


class EventPublisher:
    def __init__(self, channel):
        self.channel = channel

    def publish_domain_event(self, routing_key: str, payload: dict):
        message = {
            "event": routing_key,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload,
        }
        self.channel.basic_publish(
            exchange=settings.EVENTS_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message, default=str),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def publish_rpc_reply(self, reply_to: str, correlation_id: str, response: dict):
        if not reply_to:
            return
        self.channel.basic_publish(
            exchange="",
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=json.dumps(response, default=str),
        )