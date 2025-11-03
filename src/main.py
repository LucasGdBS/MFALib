'''Exemplo de código completo (no README)'''
import asyncio
from decouple import config as env
from src.otp.otp_email_handler import OtpEmailHandler
from src.otp.totp_handler import TOTPHandler, generate_secret_key
from src.email.email_sender import SmtpEmailSender
from src.email.smtp_servers import SMTPServer
from src.jwt.jwt_handler import JWTHandler
from src.jwt.jwt_exceptions import JWTException

async def exemplo_opt():
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
        to_adress= env('LOGIN_GMAIL'),
        subject='Código de Verificação - MeuApp'
    )
    print(f"Código OTP enviado: {otp_code}")

    # Simular verificação do código OTP
    while True:
        codigo_inserido = input("Digite o código recebido por email: ")
        if codigo_inserido == otp_code:
            print("✅ Código OTP correto!")
            break
        else:
            print("❌ Código OTP incorreto. Tente novamente.")

async def exemplo_totp():
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
    while True: 
        codigo_totp = input("Digite o código do seu app authenticator: ")
        if totp_handler.verify_totp(codigo_totp):
            print("✅ Código TOTP válido!")
            break
        else:
            print("❌ Código TOTP inválido!")

async def exemplo_jwt():
    print("\n🔑 Exemplo de Autenticação JWT com permissão")

    email_env = env("LOGIN_GMAIL")

    flag = True

    while flag:
        print(f"\nE-mail selecionado: {email_env}")

        # escolher o papel
        print("\nEscolha o papel (role) do usuário:")
        print("   • admin     → pode ler, escrever e gerenciar permissões")
        print("   • escritor  → pode ler e escrever")
        print("   • leitor    → pode apenas ler")
        role = input("\nPapel (role): ").strip().lower()

        if role not in ["admin", "escritor", "leitor"]:
            print("⚠️ Papel inválido! Digite apenas admin, escritor ou leitor.")
            continue

        token = JWTHandler.create_token(user_id= 1, email=email_env, role=role)
        print(f"\n✅ Token JWT gerado para {email_env} com o papel '{role}':\n{token}")

        # Decodificar token 
        print("\n🕐 Decodificando token JWT...")
        try:
            decoded = JWTHandler.decode_token(token)
            print("Payload decodificado:")
            for key, value in decoded.items():
                print(f"   • {key}: {value}")
            flag = False
        except JWTException as e:
            print(f"❌ Erro ao decodificar token: {str(e)}")
    

async def main():
    while(True):
        print("\n##### Sistema de Teste de Autenticação ######")
        print("Digite 1: Testar OPT")
        print("Digite 2: Testar TOTP")
        print("Digite 3: Testar JWT")
        print("Digite 0: Sair")

        escolha = input("\nEscolha uma opção: ")
    
        if escolha == "1":
            await exemplo_opt()
        elif escolha == "2":
            await exemplo_totp()
        elif escolha == "3":
            await exemplo_jwt()
        else:
            print("👋 Encerrando execução...")
            break
        
if __name__ == "__main__":
    asyncio.run(main())

