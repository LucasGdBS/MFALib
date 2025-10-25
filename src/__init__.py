"""MFALib - Multi-Factor Authentication Library

A comprehensive Python library for implementing multi-factor authentication (MFA) 
with support for email-based OTP and TOTP (Time-based One-Time Password) authentication.

This library provides:
- Email-based OTP (One-Time Password) generation and delivery
- TOTP (Time-based One-Time Password) support compatible with authenticator apps
- SMTP email sending with support for multiple providers
- HTML and plain text email templates
- Secure random code generation using cryptographically secure methods

Main Components:
    SmtpEmailSender: Handles email sending via SMTP with SSL/TLS support
    SMTPServer: Pre-configured SMTP server settings for popular email providers
    OtpEmailHandler: Generates and sends OTP codes via email
    TOTPHandler: Manages TOTP tokens for authenticator app integration

Example:
    >>> from mfalib import SmtpEmailSender, OtpEmailHandler, TOTPHandler
    >>> 
    >>> # Setup email sender
    >>> sender = SmtpEmailSender("smtp.gmail.com", 587, "user@gmail.com", "password")
    >>> 
    >>> # Send OTP via email
    >>> otp_handler = OtpEmailHandler(sender)
    >>> otp_code = await otp_handler.send_otp_email(
    ...     to_address="user@example.com",
    ...     subject="Your verification code"
    ... )
    >>> 
    >>> # Generate TOTP secret and QR code
    >>> totp_handler = TOTPHandler()
    >>> secret = totp_handler.generate_secret()
    >>> qr_code = totp_handler.generate_qr_code(secret, "user@example.com", "MyApp")

Security Features:
- Uses secrets module for cryptographically secure random generation
- Supports time-based token validation with configurable time windows
- HTML email templates with security warnings
- Comprehensive logging for security auditing

Version: 0.0.1
"""

from .email.email_sender import SmtpEmailSender, EmailBody
from .email.smtp_servers import SMTPServer, SmtpServerConfig
from .otp.otp_email_handler import OtpEmailHandler
from .otp.totp_handler import TOTPHandler

__version__ = "0.0.1"
__description__ = "Multi-Factor Authentication Library for Python"

__all__ = [
    "SmtpEmailSender",
    "SMTPServer", 
    "OtpEmailHandler",
    "TOTPHandler",
    "EmailBody",
    "SmtpServerConfig",
    "__version__",
    "__description__",
]