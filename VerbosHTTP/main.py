from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from middlewares import bearerJWT
from DB.conexion import Session, engine, Base
from models.modelsDB import User

app= FastAPI(
    title='Mi primer API',
    description='Carlos Velázquez',
    version='1.0.'
)

#Levantamiento de las tablas definidas en los modelos
Base.metadata.create_all(bind=engine)

@app.get('/',tags=['Inicio'])
def main():
    return{'hello FastAPI':'Carlos Velázquez'}

#dependencies= [Depends(bearerJWT())]

#endpoint para consultar datos 
@app.get('/usuarios', tags=['Operaciones CRUD'])
def ConsultarTodos():
    db = Session()
    try:
        consulta= db.query(User).all()
        return JSONResponse(content= jsonable_encoder(consulta))
    
    except Exception as x:
        return JSONResponse(status_code=500,content={"mensaje":"NO fue posible consultar","Excepcion":str(x)})
    
    finally:
        db.close()

#endpoint para consultar datos por id
@app.get('/usuarios/{id}', tags=['Operaciones CRUD'])
def ConsultarUno(id:int):
    db = Session()
    try:
        consulta= db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code = 404, content= {"mensaje":"Usuario no encontrado"})
        return JSONResponse(content= jsonable_encoder(consulta))
    
    except Exception as x:
        return JSONResponse(status_code=500,content={"mensaje":"NO fue posible consultar","Excepcion":str(x)})
    
    finally:
        db.close()

#endpoint para agregar usuarios
@app.post('/usuarios/', response_model=modelUsuario, tags=['Operaciones CRUD'])
def AgregarUsuarios(usuarionuevo: modelUsuario):
    db= Session()
    try:
        db.add(User(**usuarionuevo.model_dump()))
        db.commit()
        return JSONResponse(status_code=201,content={"mensaje":"Usuario Guardado","usuario":usuarionuevo.model_dump()})
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,content={"mensaje":"NO Guardado","Excepcion":str(e)})

    finally:
        db.close()
        
#endpoint para actualizar usuario
@app.put('/usuarios/{id}', response_model=modelUsuario, tags=['Operaciones CRUD'])
def actualizarUsuario(id: int, usuario_actualizado: modelUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"mensaje": "Usuario no encontrado"})
        
        for key, value in usuario_actualizado.model_dump().items():
            setattr(usuario, key, value)
        
        db.commit()
        return JSONResponse(content={"mensaje": "Usuario actualizado", "usuario": jsonable_encoder(usuario)})
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"mensaje": "No se pudo actualizar", "Excepcion": str(e)})
    
    finally:
        db.close()

#endpoint para eliminar usuario 
@app.delete('/usuarios/{id}', tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"mensaje": "Usuario no encontrado"})
        
        db.delete(usuario)
        db.commit()
        return JSONResponse(content={"mensaje": "Usuario eliminado correctamente"})
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"mensaje": "No se pudo eliminar", "Excepcion": str(e)})
    
    finally:
        db.close()

#endpoint para generar un token
@app.post('/auth', tags=['Autentificación'])
def login(autorizado:modelAuth):
    if autorizado.correo == 'carlos@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {'Aviso':'Usuario no autorizado'}