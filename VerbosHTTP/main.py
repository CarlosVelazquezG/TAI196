from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from middlewares import bearerJWT

app= FastAPI(
    title='Mi primer API',
    description='Carlos Velázquez',
    version='1.0.'
)

usuarios = [
    {"id":1,"nombre":"alondra", "edad":22,"correo":"alondra@ejemplo.com"},
    {"id":2,"nombre":"carlos", "edad":22,"correo":"carlos@ejemplo.com"},
    {"id":3,"nombre":"antonio", "edad":23,"correo":"antonio@ejemplo.com"},
    {"id":4,"nombre":"danna", "edad":21,"correo":"danna@ejemplo.com"}
]

@app.get('/',tags=['Inicio'])
def main():
    return{'hello FastAPI':'Carlos Velázquez'}

#endpoint para generar un token
@app.post('/auth', tags=['Autentificación'])
def login(autorizado:modelAuth):
    if autorizado.correo == 'carlos@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {'Aviso':'Usuario no autorizado'}

#endpoint para consultar datos 
@app.get('/usuarios', dependencies= [Depends(bearerJWT())],response_model= List[modelUsuario], tags=['Operaciones CRUD'])
def ConsultarTodos():
    return usuarios

#endpoint para agregar usuarios
@app.post('/usuarios/', response_model=modelUsuario, tags=['Operaciones CRUD'])
def AgregarUsuarios(usuarionuevo: modelUsuario):
        for usr in usuarios:
            if usr ["id"] == usuarionuevo.id:
                raise HTTPException(status_code=400, detail="El id ya está registrado")
            
        usuarios.append(usuarionuevo)
        return usuarionuevo
            
#endpoint para actualizar usuario
@app.put('/usuarios/{id}', response_model=modelUsuario,tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: modelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index]=usuario_actualizado.model_dump()
            return usuarios[index]
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#endpoint para eliminar usuario 
@app.delete('/usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#