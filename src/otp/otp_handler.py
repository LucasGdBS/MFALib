from io import BytesIO

from loguru import logger
import pyotp
import qrcode

class OTPHandler:
    def __init__(self, secret_key: str):
        self.totp = pyotp.TOTP(secret_key)

    @logger.catch
    def generate_otp_qrcode(self, user_identifier: str, app_name: str, ascii: bool = False) -> BytesIO | None:
        """
        Generate a QR code for OTP (TOTP) setup and either print an ASCII representation
        or return a PNG image buffer suitable for embedding or saving.
        Parameters
        ----------
        user_identifier : str
            The identifier for the user (for example, their email). This is used as the
            account name in the otpauth URI.
        app_name : str
            The name of the application (issuer) shown in authenticator apps.
        ascii : bool
            If True, prints an ASCII representation of the QR code to stdout and
            returns None. If False, returns an io.BytesIO containing the QR code as a
            PNG image (the buffer is seeked to position 0 and ready for reading).
        Returns
        -------
        io.BytesIO or None
            - If ascii is False: an io.BytesIO object containing the PNG image bytes.
              The buffer is positioned at the beginning (buffer.seek(0) has been called).
            - If ascii is True: None (QR printed to stdout).
        """

        otpauth_url = self.totp.provisioning_uri(
            name=user_identifier,
            issuer_name=app_name
        )
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(otpauth_url)
        qr.make(fit=True)
        if ascii:
            qr.print_ascii()
            logger.debug("Displayed ASCII QR code for OTP setup.")
        else:
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            logger.debug("Generated PNG QR code for OTP setup.")
            return buffer

    @logger.catch
    def verify_otp(self, otp_code: str) -> bool:
        """
        Verify the provided OTP code.

        Args:
            otp_code (str): The OTP code to verify.

        Returns:
            bool: True if the OTP code is valid, False otherwise.
        """
        return self.totp.verify(otp_code)

def generate_secret_key(length:int=32) -> str:
    """Generate a random base32 secret key for OTP.

    Args:
        length (int): Length of the secret key. Default is 32.
    """
    return pyotp.random_base32(length)