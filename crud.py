from sqlalchemy.orm import Session
from exceptions import UsuarioAlreadyExistError, UsuarioNotFoundError, PedidoNotFoundError, PedidoItensNotFoundError
import bcrypt, models, schemas

# usuário
def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuario_by_codigo_pessoa(db: Session, codigo_pessoa: int):
    return db.query(models.Usuario).filter(models.Usuario.codigo_pessoa == codigo_pessoa).first()

def get_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).get(usuario_id)
    if db_usuario is None:
        raise UsuarioNotFoundError
    return db_usuario

def get_all_usuarios(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).offset(offset).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_email(db, usuario.email)
    if db_usuario is not None:
        raise UsuarioAlreadyExistError
    db_usuario = models.Usuario(**usuario.dict())
    db_usuario.senha = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def check_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_codigo_pessoa(db, usuario.codigo_pessoa)
    if db_usuario is None:
        raise UsuarioNotFoundError
    if not bcrypt.checkpw(usuario.senha.encode("utf-8"), db_usuario.senha.encode("utf-8")):
        raise UsuarioNotFoundError
    return True

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db_usuario.nome = usuario.nome
    db_usuario.email = usuario.email
    db_usuario.codigo_pessoa = usuario.codigo_pessoa
    db_usuario.senha = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt())
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db.delete(db_usuario)
    db.commit()
    return

# pedido
def get_pedido_by_id(db: Session, pedido_id: int):
    db_pedido = db.query(models.Pedido).get(pedido_id)
    if db_pedido is None:
        raise PedidoNotFoundError
    return db_pedido

def get_all_pedidos(db: Session, offset: int, limit: int):
    return db.query(models.Pedido).offset(offset).limit(limit).all()

def create_pedido(db: Session, pedido: schemas.PedidoCreate):
    db_pedido = models.Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def update_pedido(db: Session, pedido_id: int, pedido: schemas.PedidoUpdate):
    db_pedido = get_pedido_by_id(db, pedido_id)
    db_pedido.valor_total = pedido.valor_total
    db_pedido.data_pedido = pedido.data_pedido
    db_pedido.id_usuario = pedido.id_usuario
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def delete_pedido_by_id(db: Session, pedido_id: int):
    db_pedido = get_pedido_by_id(db, pedido_id)
    db.delete(db_pedido)
    db.commit()
    return

# pedido_itens
def get_pedido_itens_by_id(db: Session, pedido_itens_id: int):
    db_pedido_itens = db.query(models.PedidoItens).get(pedido_itens_id)
    if db_pedido_itens is None:
        raise PedidoItensNotFoundError
    return db_pedido_itens

def get_all_pedido_itens(db: Session, offset: int, limit: int):
    return db.query(models.PedidoItens).offset(offset).limit(limit).all()

def create_pedido_itens(db: Session, pedido_itens: schemas.PedidoItensBase):
    db_pedido_itens = models.PedidoItens(**pedido_itens.dict())
    db.add(db_pedido_itens)
    db.commit()
    db.refresh(db_pedido_itens)
    return db_pedido_itens

def update_pedido_itens(db: Session, pedido_itens_id: int, pedido_itens: schemas.PedidoItensBase):
    db_pedido_itens = get_pedido_itens_by_id(db, pedido_itens_id)
    db_pedido_itens.pedido_id = pedido_itens.pedido_id
    db_pedido_itens.produto_id = pedido_itens.produto_id
    db_pedido_itens.quantidade = pedido_itens.quantidade
    db.commit()
    db.refresh(db_pedido_itens)
    return db_pedido_itens

def delete_pedido_itens_by_id(db: Session, pedido_itens_id: int):
    db_pedido_itens = get_pedido_itens_by_id(db, pedido_itens_id)
    db.delete(db_pedido_itens)
    db.commit()
    return

# estoque

def get_estoque_by_id(db: Session, estoque_id: int):
    db_estoque = db.query(models.Estoque).get(estoque_id)
    if db_estoque is None:
        raise EstoqueNotFoundError
    return db_estoque

def get_all_estoques(db: Session, offset: int, limit: int):
    return db.query(models.Estoque).offset(offset).limit(limit).all()

def create_estoque(db: Session, estoque: schemas.EstoqueBase):
    db_estoque = models.Estoque(**estoque.dict())
    db.add(db_estoque)
    db.commit()
    db.refresh(db_estoque)
    return db_estoque

def update_estoque(db: Session, estoque_id: int, estoque: schemas.EstoqueBase):
    db_estoque = get_estoque_by_id(db, estoque_id)
    db_estoque.nome = estoque.nome
    db_estoque.quantidade = estoque.quantidade
    db_estoque.preco = estoque.preco
    db_estoque.validade = estoque.validade
    db.commit()
    db.refresh(db_estoque)
    return db_estoque

def delete_estoque_by_id(db: Session, estoque_id: int):
    db_estoque = get_estoque_by_id(db, estoque_id)
    db.delete(db_estoque)
    db.commit()
    return