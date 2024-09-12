from faststream.rabbit import RabbitRouter

AMQPSenderController = RabbitRouter()


@AMQPSenderController.subscriber("send_message")
async def send_message() -> None: ...
