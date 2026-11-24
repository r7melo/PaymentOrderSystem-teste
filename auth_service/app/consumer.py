import json
import time
import pika
from app.config import settings
from app.repository import UserRepository
from app.publisher import EventPublisher
from app.erros import AuthError
from app.acoes.registrar import executar_registro
from app.acoes.autenticar import executar_login


class AuthConsumer:
    def __init__(self):
        self.repo = UserRepository()

    def _handle_message(self, ch, method, props, body):
        publisher = EventPublisher(ch)

        try:
            message = json.loads(body.decode("utf-8"))
            action = message.get("action")
            payload = message.get("payload", {})

            if action == "register":
                result = executar_registro(payload, self.repo, publisher)
                response = {"status": 201, "data": result}
            elif action == "login":
                result = executar_login(payload, self.repo)
                response = {"status": 200, "data": result}
            else:
                response = {"status": 400, "error": f"Ação RPC não suportada: {action}"}

        except AuthError as err:
            response = {"status": err.status_code, "error": err.message}
        except Exception as exc:
            response = {"status": 500, "error": f"Erro interno no auth_service: {str(exc)}"}

        publisher.publish_rpc_reply(
            reply_to=props.reply_to,
            correlation_id=props.correlation_id,
            response=response,
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
                )
                channel = connection.channel()
                channel.queue_declare(queue=settings.RPC_QUEUE, durable=True)
                channel.exchange_declare(
                    exchange=settings.EVENTS_EXCHANGE,
                    exchange_type="topic",
                    durable=True,
                )
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(
                    queue=settings.RPC_QUEUE,
                    on_message_callback=self._handle_message,
                )
                print(f"[auth_service] Aguardando mensagens RPC na fila '{settings.RPC_QUEUE}'...")
                channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                print("[auth_service] RabbitMQ indisponível. Reconectando em 3s...")
                time.sleep(3)