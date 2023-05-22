from typing import List
from pydantic import BaseModel
from datetime import date


class UsuarioBase(BaseModel):
    nome: str
    email: str
    codigo_pessoa: int


class UsuarioCreate(UsuarioBase):
    senha: str


class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True


class UsuarioLoginSchema(BaseModel):
    codigo_pessoa: int
    senha: str


class PaginatedUsuario(BaseModel):
    limit: int
    offset: int
    data: List[Usuario]


class PedidoBase(BaseModel):
    id_usuario: int
    valor_total: float
    data_pedido: date

class PedidoUpdate(BaseModel):
    pass


class PedidoCreate(PedidoBase):
    pass


class Pedido(PedidoBase):
    id: int
    usuario: Usuario = {}

    class Config:
        orm_mode = True


class PaginatedPedido(BaseModel):
    limit: int
    offset: int
    data: List[Pedido]


class PedidoItensBase(BaseModel):
    id_pedido: int
    id_estoque: int
    quantidade: int


class PedidoItensCreate(PedidoItensBase):
    pass


class PedidoItens(PedidoItensBase):
    id: int

    class Config:
        orm_mode = True


class PaginatedPedidoItens(BaseModel):
    limit: int
    offset: int
    data: List[PedidoItens]


class EstoqueBase(BaseModel):
    nome: str
    quantidade: int
    preco: float
    validade: date


class EstoqueCreate(EstoqueBase):
    pass


class EstoqueUpdate(EstoqueBase):
    pass


class EstoquePatch(BaseModel):
    nome: str = None
    quantidade: int = None
    preco: float = None
    validade: date = None

    class Config:
        schema_extra = {
            "example": {
                "nome": "Coca Cola",
                "quantidade": 10,
                "preco": 5.0,
                "validade": "2021-12-31"
            }
        }


class EstoquePatchList(BaseModel):
    data: List[EstoquePatch]

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "nome": "Coca Cola",
                        "quantidade": 10,
                        "preco": 5.0,
                        "validade": "2021-12-31"
                    },
                    {
                        "nome": "Pepsi",
                        "quantidade": 10,
                        "preco": 5.0,
                        "validade": "2021-12-31"
                    }
                ]
            }
        }


class Estoque(EstoqueBase):
    id: int

    class Config:
        orm_mode = True


class PaginatedEstoque(BaseModel):
    limit: int
    offset: int
    data: List[Estoque]
