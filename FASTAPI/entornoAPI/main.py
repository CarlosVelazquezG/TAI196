from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title = 'Mi primer API 196', 
    description = 'Carlos Velázquez Govea',
    version = '1.0.1'
)

#modelo para validación de datos
class modelUsuario(BaseModel):
    id:int
    nombre:str
    edad:int
    correo:str

usuarios = [
    {"id":1,"nombre":"alondra", "edad":22,"correo":"alondra@ejemplo.com"},
    {"id":2,"nombre":"carlos", "edad":22,"correo":"carlos@ejemplo.com"},
    {"id":3,"nombre":"antonio", "edad":23,"correo":"antonio@ejemplo.com"},
    {"id":4,"nombre":"danna", "edad":21,"correo":"danna@ejemplo.com"}
]

@app.get('/',tags=['Inicio'])
def main():
    return {'Hola FastAPI':'CarlosVelazquez'}

@app.get('/promedio', tags=['Mi calificación TAI'])
def promedio():
    promedio = 20.20
    return {promedio}

#Endpoint Parámetro Obligatorio
@app.get('/usuario/{id}',tags=['Parámetro obligatorio'])
def consultaUsuario(id:int):
    #ConnectDB
    #Query
    return{"Se encontró el usuario": id}

#Endoint Parámetro Opcional
@app.get('/usuario/',tags=['Parámetro opcional'])
def consultaUsuario2(id:Optional[int]= None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id:
                return {"mensaje":"Usuario encontrado","usuario":usuario}
        return{"mensaje":f"No se encontró el id: {id}"}
    else:
        return {"mensaje":"No se proporcionó un Id"}
    
#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}