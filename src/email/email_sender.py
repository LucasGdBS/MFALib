from email.message import EmailMessage
from typing import List

import aiosmtplib
from loguru import logger

from smtp_servers import SMTPServer

class SmtpEmailSender:
    """
    Asynchronous SMTP email sender.
    
    Handles sending emails through various SMTP servers using async/await pattern.
    Supports both single and multiple recipients.
    """
    
    def __init__(self, smtp_server: SMTPServer, username: str, password: str):
        """
        Initialize the SMTP email sender.
        
        Args:
            smtp_server: SMTP server configuration (from SMTPServer enum)
            username: Email account username/address
            password: Email account password or app-specific password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_server.port
        self.username = username
        self.password = password

    async def send_email(self, to_address: List[str] | str, subject: str, body: str) -> None:
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
        msg.set_content(body)

        try: 
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_server.value,
                port=self.smtp_port,
                username=self.username,
                password=self.password,
                start_tls=True
            )
            logger.info(f"Email sent to {to_address} with subject '{subject}'")
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