from fastapi import FastAPI, HTTPException
from typing import Optional, List
from modelsPydantic import modelEnvios

app = FastAPI(
    title='Mi Examen 2do Parcial',
)

envios = [
    {"cp": "76168", "destino":"Queretaro", "peso": 5},
    {"cp": "76000", "destino":"Queretaro", "peso": 10},
    {"cp": "76200", "destino":"Queretaro", "peso": 20}
]

@app.get('/',tags=['Inicio'])
def main():
    return{'hello FastAPI':'Carlos Velázquez'}

#endpoint para consultar un envío
@app.get('/envios/',response_model= List[modelEnvios] ,tags=['Mostrar todos los envíos'])
def consultaEnvios():
    return envios

#endpoint para eliminar un envío por código postal
@app.delete('/envios/{cp}', tags=['Eliminar un envío'])
def eliminarEnvio(cp:str):
    for envio in envios:
        if envio["cp"] == cp:
            envios.remove(envio)
            return {"Mensaje:":"El envío fue eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Envío no encontrado")

