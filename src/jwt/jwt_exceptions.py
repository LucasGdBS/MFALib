
class JWTException(Exception):
    """Exceção base para erros relacionados ao JWT."""
    pass


class TokenExpiredError(JWTException):
    """Token expirou."""
    pass


class InvalidTokenError(JWTException):
    """Token inválido ou malformado."""
    pass