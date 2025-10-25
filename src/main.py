'''Exemplo de código completo (no README)'''
import asyncio
from decouple import config as env
from src.otp.otp_email_handler import OtpEmailHandler
from src.otp.totp_handler import TOTPHandler, generate_secret_key
from src.email.email_sender import SmtpEmailSender
from src.email.smtp_servers import SMTPServer

async def exemplo_mfa_completo():
    print("🔐 Exemplo de MFA Completo")

    # 1. OTP via Email
    print("\n📧 Enviando OTP via email...")
    email_handler = OtpEmailHandler(
        sender=SmtpEmailSender(
            SMTPServer.GMAIL,
            env('LOGIN_GMAIL'),
            env('PASSWORD_GMAIL')
        )
    )

    otp_code = await email_handler.send_otp_email(
        to_adress='lucas_gabrielbrito@hotmail.com',
        subject='Código de Verificação - MeuApp'
    )
    print(f"Código OTP enviado: {otp_code}")

    # Simular verificação do código OTP
    while True:
        codigo_inserido = input("Digite o código recebido por email: ")
        if codigo_inserido == otp_code:
            print("✅ Código OTP correto! Prosseguindo...")
            break
        else:
            print("❌ Código OTP incorreto. Tente novamente.")

    # 2. TOTP Setup
    print("\n🕐 Configurando TOTP...")
    secret_key = generate_secret_key()
    totp_handler = TOTPHandler(secret_key)
    print(f"Chave secreta: {secret_key}")

    # Gerar QR Code para configurar no app
    totp_handler.generate_totp_qrcode(
        user_identifier=env('LOGIN_GMAIL'),
        app_name="MeuApp",
        ascii=True
    )

    # Verificar código TOTP
    codigo_totp = input("Digite o código do seu app authenticator: ")
    if totp_handler.verify_totp(codigo_totp):
        print("✅ Código TOTP válido! MFA completo com sucesso!")
    else:
        print("❌ Código TOTP inválido!")

# Executar exemplo
asyncio.run(exemplo_mfa_completo())