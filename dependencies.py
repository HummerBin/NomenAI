import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from sqlalchemy.ext.asyncio import AsyncSession
from models import AsyncSessionFactory
import settings


async def  get_session()->AsyncSession: # type: ignore
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        session.close
    


class Mailer:
    @staticmethod
    async def send(to_addr: str, subject: str, body: str, is_html: bool = False):
        msg = MIMEMultipart()
        msg["From"] = settings.MAIL_FROM
        msg["To"] = to_addr
        msg["Subject"] = Header(subject, "utf-8").encode()
        subtype = "html" if is_html else "plain"
        msg.attach(MIMEText(body, subtype, "utf-8"))

        await aiosmtplib.send(
            msg,
            hostname=settings.MAIL_SERVER,
            port=settings.MAIL_PORT,
            username=settings.MAIL_USERNAME,
            password=settings.MAIL_PASSWORD,
            starttls=True,
        )

def get_mailer() -> Mailer:
    return Mailer()