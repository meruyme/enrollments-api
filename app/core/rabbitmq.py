from pika import URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from app.core.settings import Settings

settings = Settings()


class RabbitMQProvider:
    __connection: BlockingConnection

    @staticmethod
    def get_queue_name() -> str:
        return settings.rabbit_queue_name

    def get_channel(self) -> BlockingChannel:
        self.__connection = BlockingConnection(URLParameters(settings.rabbit_host))
        channel = self.__connection.channel()
        channel.queue_declare(queue=self.get_queue_name(), durable=True)

        return channel

    def close_connection(self):
        if self.__connection:
            self.__connection.close()

    def publish_message(self, message_data: str):
        channel = self.get_channel()
        channel.basic_publish(
            exchange="",
            routing_key=self.get_queue_name(),
            body=message_data.encode("utf-8"),
        )
        self.close_connection()
