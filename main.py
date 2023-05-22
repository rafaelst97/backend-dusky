from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from exceptions import UsuarioException, PedidoException, PedidoItensException
from database import get_db, engine
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# signup
@app.post("/api/signup", tags=["usuario"])
async def user_signup(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        usuario = crud.create_usuario(db, usuario)
        return signJWT(usuario.codigo_pessoa)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

# login
@app.post("/api/login", tags=["usuario"])
async def user_login(usuario: schemas.UsuarioLoginSchema = Body(...), db: Session = Depends(get_db)):
    if crud.check_usuario(db, usuario):
        return signJWT(usuario.codigo_pessoa)
    raise HTTPException(status_code=400, detail="USUARIO_INCORRETO")

# usuário
@app.get("/api/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def get_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/usuarios", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedUsuario)
def get_all_usuarios(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_usuarios = crud.get_all_usuarios(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_usuarios}
    return response

@app.post("/api/usuarios", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        usuario = crud.update_usuario(db, usuario_id, usuario)
        return usuario
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())])
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_usuario(db, usuario_id)
        return {"Usuário Deletado!"}
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

# pedido
@app.get("/api/pedidos/{pedido_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Pedido)
def get_pedido_by_id(pedido_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_pedido_by_id(db, pedido_id)
    except PedidoException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/pedidos", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedPedido)
def get_all_pedidos(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_pedidos = crud.get_all_pedidos(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_pedidos}
    return response

@app.post("/api/pedidos", dependencies=[Depends(JWTBearer())], response_model=schemas.Pedido)
def create_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_pedido(db, pedido)
    except PedidoException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/pedidos/{pedido_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Pedido)
def update_pedido(pedido_id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_pedido(db, pedido_id, pedido)
    except PedidoException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/pedidos/{pedido_id}", dependencies=[Depends(JWTBearer())])
def delete_pedido_by_id(pedido_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_pedido_by_id(db, pedido_id)
        return "Pedido Deletado!"
    except PedidoException as cie:
        raise HTTPException(**cie.__dict__)

# pedido_itens
@app.get("/api/pedido_itens/{pedido_itens_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.PedidoItens)
def get_pedido_itens_by_id(pedido_itens_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_pedido_itens_by_id(db, pedido_itens_id)
    except PedidoItensException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/pedido_itens", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedPedidoItens)
def get_all_pedido_itens(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_pedido_itens = crud.get_all_pedido_itens(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_pedido_itens}
    return response

@app.post("/api/pedido_itens", dependencies=[Depends(JWTBearer())], response_model=schemas.PedidoItens)
def create_pedido_itens(pedido_itens: schemas.PedidoItensCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_pedido_itens(db, pedido_itens)
    except PedidoItensException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/pedido_itens/{pedido_itens_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.PedidoItens)
def update_pedido_itens(pedido_itens_id: int, pedido_itens: schemas.PedidoItensCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_pedido_itens(db, pedido_itens_id, pedido_itens)
    except PedidoItensException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/pedido_itens/{pedido_itens_id}", dependencies=[Depends(JWTBearer())])
def delete_pedido_itens_by_id(pedido_itens_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_pedido_itens_by_id(db, pedido_itens_id)
    except PedidoItensException as cie:
        raise HTTPException(**cie.__dict__)

# estoque
@app.get("/api/estoques/{estoque_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Estoque)
def get_estoque_by_id(estoque_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_estoque_by_id(db, estoque_id)
    except EstoqueException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/estoques", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedEstoque)
def get_all_estoques(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_estoques = crud.get_all_estoques(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_estoques}
    return response

@app.post("/api/estoques", dependencies=[Depends(JWTBearer())], response_model=schemas.Estoque)
def create_estoque(estoque: schemas.EstoqueCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_estoque(db, estoque)
    except EstoqueException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/estoques/{estoque_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.Estoque)
def update_estoque(estoque_id: int, estoque: schemas.EstoqueUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_estoque(db, estoque_id, estoque)
    except EstoqueException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/estoques/{estoque_id}", dependencies=[Depends(JWTBearer())])
def delete_estoque_by_id(estoque_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_estoque_by_id(db, estoque_id)
        return "Excluído com sucesso!"
    except EstoqueException as cie:
        raise HTTPException(**cie.__dict__)
