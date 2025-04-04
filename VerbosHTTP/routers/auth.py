from fastapi.responses import JSONResponse
from modelsPydantic import modelAuth
from tokenGen import createToken
from fastapi import APIRouter

routerAuth= APIRouter()

#endpoint para generar un token
@routerAuth.post('/auth', tags=['Autentificación'])
def login(autorizado:modelAuth):
    if autorizado.correo == 'carlos@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {'Aviso':'Usuario no autorizado'}