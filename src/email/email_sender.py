from email.message import EmailMessage
from typing import List
from dataclasses import dataclass

import aiosmtplib
from loguru import logger

from src.email.smtp_servers import SMTPServer, SmtpServerConfig

@dataclass
class EmailBody:
    text: str
    subtype: str

class SmtpEmailSender:
    """
    Asynchronous SMTP email sender.
    
    Handles sending emails through various SMTP servers using async/await pattern.
    Supports both single and multiple recipients.
    """
    
    def __init__(self, smtp_server: SMTPServer | SmtpServerConfig, username: str, password: str):
        """
        Initialize the SMTP email sender.
        
        Args:
            smtp_server: SMTP server configuration (from SMTPServer enum)
            username: Email account username/address
            password: Email account password or app-specific password
        """
        self.smtp_server = str(smtp_server)
        self.smtp_port = smtp_server.port
        self.username = username
        self.password = password

    async def send_email(self, to_address: List[str] | str, subject: str, body: EmailBody | str) -> None:
        """
        Send an email asynchronously.
        
        Args:
            to_address: Single recipient email or list of recipient emails
            subject: Email subject line
            body: Email body content (plain text)
            
        Raises:
            Exception: If email sending fails (logged and re-raised)
        """
        to_address = to_address if isinstance(to_address, list) else [to_address]

        msg = EmailMessage()
        msg['From'] = self.username
        msg['To'] = ", ".join(to_address)
        msg['Subject'] = subject

        if isinstance(body, EmailBody) and body.subtype.lower() == "html":
            msg.set_content("Seu cliente de email não suporta HTML")
            msg.add_alternative(body.text, subtype="html")
        else:
            msg.set_content(body if isinstance(body, str) else body.text)


        try: 
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.username,
                password=self.password,
                start_tls=True
            )
            logger.debug(f"Email sent to {to_address} with subject '{subject}'")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise

# Example usage:
# import asyncio

# smtp = SMTPServer.GMAIL
# email_sender = SmtpEmailSender(smtp, "your_email@gmail.com", PASSWORD_GMAIL)
# asyncio.run(email_sender.send_email(
#     to_address="friend_mail@anymail.com",
#     subject="Test Email",
#     body="This is a test email sent using SmtpEmailSender."
# ))