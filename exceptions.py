class UsuarioException(Exception):
    ...

class UsuarioNotFoundError(UsuarioException):
    def __init__(self):
        self.status_code = 404
        self.detail = "USUARIO_NAO_ENCONTRADO"


class UsuarioAlreadyExistError(UsuarioException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_DUPLICADO"

class PedidoException(Exception):
    ...

class PedidoNotFoundError(PedidoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "PEDIDO_NAO_ENCONTRADO"

class PedidoItensException(Exception):
    ...

class PedidoItensNotFoundError(PedidoItensException):
    def __init__(self):
        self.status_code = 404
        self.detail = "PEDIDO_ITENS_NAO_ENCONTRADO"

class EstoqueException(Exception):
    ...

class EstoqueNotFoundError(EstoqueException):
    def __init__(self):
        self.status_code = 404
        self.detail = "ESTOQUE_NAO_ENCONTRADO"

class EstoqueAlreadyExistError(EstoqueException):
    def __init__(self):
        self.status_code = 409
        self.detail = "ESTOQUE_DUPLICADO"