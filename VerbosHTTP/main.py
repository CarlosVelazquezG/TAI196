from fastapi import FastAPI, HTTPException
from typing import Optional

app= FastAPI(
    title='Mi primer API',
    description='Carlos Velázquez',
    version='1.0.'

)

usuarios = [
    {"id":1,"nombre":"alondra", "edad":22},
    {"id":2,"nombre":"carlos", "edad":22},
    {"id":3,"nombre":"antonio", "edad":23},
    {"id":4,"nombre":"danna", "edad":21}
]



@app.get('/',tags=['Inicio'])
def main():
    return{'hello FastAPI':'Carlos Velázquez'}

#endpoint para consultar datos 
@app.get('/usuarios',tags=['Operaciones CRUD'])
def ConsultarTodos():
    return{"Usuarios Registrados": usuarios}

#endpoint para agregar usuarios
@app.post('/usuarios/',tags=['Operaciones CRUD'])
def AgregarUsuarios(usuarionuevo: dict):
        for usr in usuarios:
            if usr ["id"] == usuarionuevo.get("id"):
                raise HTTPException(status_code=400, detail="El id ya está registrado")
            
        usuarios.append(usuarionuevo)
        return usuarionuevo
            
#endpoint para actualizar usuario
@app.put('/usuarios/{id}', tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: dict):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(usuario_actualizado)
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#endpoint para eliminar usuario 
@app.delete('/usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")