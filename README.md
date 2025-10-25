# MFALib 🔐

Uma biblioteca Python para autenticação multi-fator (MFA) com suporte a OTP (One-Time Password) via email e TOTP (Time-based One-Time Password).

## 📋 Funcionalidades

- ✅ Envio de códigos OTP por email
- ✅ Geração e validação de códigos TOTP
- ✅ Suporte a múltiplos provedores SMTP (Gmail, Outlook, etc.)
- ✅ Templates HTML customizáveis para emails
- ✅ Configuração flexível via variáveis de ambiente
- ✅ Logging integrado

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com suas credenciais:

```env
LOGIN_GMAIL=seu_email@gmail.com
PASSWORD_GMAIL=sua_senha_de_app
```

> **Nota**: Para Gmail, use uma [senha de app](https://support.google.com/accounts/answer/185833) em vez da sua senha normal.

## 📚 Como Usar

### 🔐 OTP via Email

Envie códigos de verificação únicos por email:

```python
import asyncio
from decouple import config as env
from src.otp.otp_email_handler import OtpEmailHandler
from src.email.email_sender import SmtpEmailSender
from src.email.smtp_servers import SMTPServer

async def exemplo_otp_email():
    # Configurar o handler de OTP
    handler = OtpEmailHandler(
        sender=SmtpEmailSender(
            SMTPServer.GMAIL,
            env('LOGIN_GMAIL'),
            env('PASSWORD_GMAIL')
        )
    )

    # Enviar código OTP
    otp_code = await handler.send_otp_email(
        to_adress='usuario@exemplo.com',
        subject='Seu código de verificação'
    )

    print(f"Código OTP enviado: {otp_code}")

    # Simular verificação do código
    while True:
        codigo_inserido = input("Digite o código recebido: ")
        if codigo_inserido == otp_code:
            print("✅ Código correto! Acesso liberado.")
            break
        else:
            print("❌ Código incorreto. Tente novamente.")

# Executar o exemplo
asyncio.run(exemplo_otp_email())
```

### 🕐 TOTP (Time-based OTP)

Para códigos baseados em tempo (como Google Authenticator):

```python
from src.otp.totp_handler import TOTPHandler, generate_secret_key

# Gerar uma nova chave secreta
secret_key = generate_secret_key()
totp_handler = TOTPHandler(secret_key)
print(f"Chave secreta: {secret_key}")

# Gerar QR Code para configurar no app
totp_handler.generate_totp_qrcode(
    user_identifier="usuario@exemplo.com",
    app_name="MeuApp",
    ascii=True
)

# Verificar um código TOTP
codigo_inserido = input("Digite o código do seu app: ")
if totp_handler.verify_totp(codigo_inserido):
    print("✅ Código TOTP válido!")
else:
    print("❌ Código TOTP inválido!")
```

### 📧 Configuração de Email Personalizada

Você pode usar diferentes provedores de email:

```python
from src.email.email_sender import SmtpEmailSender
from src.email.smtp_servers import SMTPServer

# Gmail
gmail_sender = SmtpEmailSender(SMTPServer.GMAIL, "seu_email@gmail.com", "sua_senha")

# Outlook/Hotmail
outlook_sender = SmtpEmailSender(SMTPServer.OUTLOOK, "seu_email@outlook.com", "sua_senha")

# Servidor SMTP customizado
from src.email.smtp_servers import SmtpServerConfig

custom_server = SmtpServerConfig("smtp.seuservidor.com", 587, True)
custom_sender = SmtpEmailSender(custom_server, "seu_email@seudominio.com", "sua_senha")
```

### 🎨 Template HTML Customizado

O email OTP usa um template HTML que pode ser personalizado em `src/otp/templates/otp_email.html`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Código de Verificação</title>
  </head>
  <body>
    <h2>Seu código de verificação</h2>
    <p>Use o código abaixo para completar sua autenticação:</p>
    <h1 style="color: #4CAF50; font-size: 32px;">{otp_code}</h1>
    <p>Este código expira em 5 minutos.</p>
  </body>
</html>
```

## 🏗️ Estrutura do Projeto

```bash
src/
├── __init__.py
├── logging_config.py          # Configuração de logs
├── main.py                   # Exemplos de uso
├── email/
│   ├── __init__.py
│   ├── email_sender.py       # Cliente SMTP
│   └── smtp_servers.py       # Configurações de servidores
└── otp/
    ├── __init__.py
    ├── otp_email_handler.py   # Handler para OTP via email
    ├── totp_handler.py        # Handler para TOTP
    └── templates/
        └── otp_email.html     # Template do email OTP
```

## 🔧 Exemplo Completo

```python
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
        to_adress='usuario@exemplo.com',
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
        user_identifier="usuario@exemplo.com",
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
```

## 📝 Requisitos

- Python 3.12+
- Dependências listadas em `requirements.txt`
