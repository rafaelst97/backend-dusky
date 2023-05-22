from sqlalchemy import Column, Integer, String, SmallInteger, Date, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    senha = Column(String(255))
    codigo_pessoa = Column(Integer, unique=True, index=True)
    pedidos = relationship("Pedido", back_populates='usuario')

class Estoque(Base):
    __tablename__ = 'estoque'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    quantidade = Column(Integer)
    preco = Column(Float)
    validade = Column(Date)
    itens = relationship("PedidoItens", back_populates='estoque')

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    valor_total = Column(Float)
    data_pedido = Column(Date)
    usuario = relationship("Usuario", back_populates='pedidos')
    itens = relationship("PedidoItens", back_populates='pedido', foreign_keys='PedidoItens.id_pedido')

class PedidoItens(Base):
    __tablename__ = 'pedido_itens'

    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id'))
    id_estoque = Column(Integer, ForeignKey('estoque.id'))
    quantidade = Column(Integer)
    pedido = relationship("Pedido", back_populates='itens')
    estoque = relationship("Estoque", back_populates='itens')