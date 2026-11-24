class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class DadosInvalidosError(AuthError):
    def __init__(self, message: str = "Dados obrigatórios ausentes ou inválidos."):
        super().__init__(message, status_code=400)


class EmailJaCadastradoError(AuthError):
    def __init__(self, message: str = "E-mail já cadastrado na plataforma."):
        super().__init__(message, status_code=409)


class CredenciaisInvalidasError(AuthError):
    def __init__(self, message: str = "E-mail ou senha inválidos."):
        super().__init__(message, status_code=401)