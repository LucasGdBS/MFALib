import jwt
import datetime
from decouple import config
from .jwt_exceptions import TokenExpiredError, InvalidTokenError

# Variáveis de ambiente usando decouple
SECRET_KEY = config("JWT_SECRET", default="chave_padrao_teste")
ALGORITHM = config("JWT_ALGORITHM", default="HS256")
EXP_MINUTES = config("JWT_EXP_MINUTES", cast=int, default=60)

class JWTHandler:
    """Classe responsável por gerar e validar tokens JWT."""
    @staticmethod
    def _get_permissions(role: str) -> list[str]:
        """Define as permissões de acordo com o papel do usuário."""
        if role == "admin":
            return ["read", "write", "manage_permissions"]
        elif role == "escritor":
            return ["read", "write"]
        elif role == "leitor":
            return ["read"]
        else:
            return []


    @staticmethod
    def create_token(user_id: int, email: str, role: str = "leitor") -> str:
        """
        Cria um token JWT contendo o payload(email, role, permission e uma data de expiração).
        Retorna o token gerado como string.
        """
        permissions = JWTHandler._get_permissions(role)
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=EXP_MINUTES)

        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "permissions": permissions,
            "exp": expiration
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token


    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decodifica e valida o token JWT.
        Retorna o payload se o token for válido.
        """
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("O token JWT expirou.")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Token JWT inválido ou corrompido.")
