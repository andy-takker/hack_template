from email.message import EmailMessage

from aiosmtplib import SMTP


class SMTPSender:
    __smtp_client: SMTP
    __from_email: str

    def __init__(self, smtp_client: SMTP, from_email: str) -> None:
        self.__smtp_client = smtp_client
        self.__from_email = from_email

    async def send(self, to_email: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self.__from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)
        async with self.__smtp_client:
            await self.__smtp_client.send_message(message)
