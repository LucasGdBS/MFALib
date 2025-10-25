from pathlib import Path
from typing import List
import string
import secrets

from jinja2 import Template
from loguru import logger

from src.email.email_sender import SmtpEmailSender, EmailBody

class OtpEmailHandler:
    """Handler for sending OTP codes via email.
    
    This class is responsible for generating OTP (One-Time Password) codes and
    sending them via email using HTML templates or plain text.
    
    Args:
        sender: SmtpEmailSender instance for sending emails.
    """
    
    def __init__(self, sender: SmtpEmailSender):
        self.sender = sender

    def generate_otp(self, length: int = 6) -> str:
        """Generates a random numeric OTP code.
        
        Args:
            length: Length of the OTP code. Default is 6 digits.
            
        Returns:
            String containing the generated OTP code.
            
        Example:
            >>> handler = OtpEmailHandler(sender)
            >>> otp = handler.generate_otp(8)
            >>> len(otp)
            8
        """
        digits = string.digits
        otp = ''.join(secrets.choice(digits) for _ in range(length))
        return otp
    
    def _get_html_template(self, otp_code: str, expiry_minutes: int = 10) -> str | None:
        """Loads and renders the HTML template for OTP email.
        
        Searches for a template file at 'templates/otp_email.html' and renders
        it with the provided parameters using Jinja2.
        
        Args:
            otp_code: OTP code to be inserted into the template.
            expiry_minutes: Expiration time for the code in minutes.
            
        Returns:
            String containing the rendered HTML or None if template doesn't exist.
        """
        template_path = Path(__file__).parent/"templates"/"otp_email.html"

        if template_path.exists():
            template = Template(template_path.read_text(encoding='utf-8'))

            return template.render(
                otp_code=otp_code,
                expiry_minutes=expiry_minutes,
            )
        return None
    
    def _get_text_template(self, otp_code: str, expiry_minutes: int = 10) -> str | None:
        """Generates the plain text content for the OTP email.
        
        Creates a plain text version of the email as fallback when
        the HTML template is not available.
        
        Args:
            otp_code: OTP code to be inserted into the text.
            expiry_minutes: Expiration time for the code in minutes.
            
        Returns:
            String containing the formatted email text.
        """
        text_content = f"""           
        Olá,
        
        Você solicitou um código de verificação para acessar sua conta.
        
        Seu código: {otp_code}
        
        Este código expira em {expiry_minutes} minutos.
        
        Se você não solicitou este código, ignore este email.
        """
        return text_content
    
    @logger.catch
    async def send_otp_email(
        self,
        to_adress: str,
        subject: str, 
        otp_code: str | None = None,
        expiry_minutes: int = 10
    ) -> str:
        """Sends an email containing OTP code to the specified recipients.
        
        Automatically generates an OTP code if not provided and sends the email
        using HTML template (if available) or plain text as fallback.
        
        Args:
            to_adress: Email address of the recipient.
            subject: Email subject line.
            otp_code: Specific OTP code. If None, will be generated automatically.
            expiry_minutes: Code expiration time in minutes. Default is 10.
            
        Returns:
            String containing the OTP code that was sent.
            
        Raises:
            Email sending related exceptions are captured by the @logger.catch decorator.
            
        Example:
            >>> handler = OtpEmailHandler(smtp_sender)
            >>> otp_sent = await handler.send_otp_email(
            ...     to_adress="user@example.com",
            ...     subject="Your verification code",
            ...     expiry_minutes=15
            ... )
            >>> print(f"OTP sent: {otp_sent}")
        """
        if otp_code is None:
            otp_code = self.generate_otp()
        
        body = EmailBody(
            text=self._get_html_template(otp_code, expiry_minutes),
            subtype='html'
        )

        await self.sender.send_email(
            to_address=to_adress,
            subject=subject,
            body=body if body else self._get_text_template(otp_code, expiry_minutes)
        )
        
        logger.debug(f"Email enviado! otp: {otp_code}")
        return otp_code
