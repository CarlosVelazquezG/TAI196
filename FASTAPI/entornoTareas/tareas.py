from fastapi import FastAPI, HTTPException
from typing import Optional

app= FastAPI(
    title='Gestión de Tareas - To do List',
    description='Carlos Velázquez',
    version='1.0.0'
)

tareas = [
    {
        "id": 1,
        "titulo": "Estudiar para el examen",
        "descripcion": "Repasar los apuntes de TAI",
        "vencimiento": "10-03-2025",
        "Estado": "completada" 
    },
    {
        "id": 2,
        "titulo": "Práctica 4",
        "descripcion": "Repasar todos los temas vistos de FastAPI",
        "vencimiento": "19-02-2025",
        "Estado": "No completada" 
    },
    {
        "id": 3,
        "titulo": "Práctica 3",
        "descripcion": "Verbos HTTP",
        "vencimiento": "08-02-2025",
        "Estado": "completada" 
    }
]

@app.get('/',tags=['Inicio'])
def main():
    return{'To DO List':'Carlos Velázquez'}

#endpoint para consultar todas las tareas 
@app.get('/tarea',tags=['Mostrar todas las tareas'])
def consultarTodaTarea():
    return{"Lista de tareas": tareas}


#endpoint para consultar una tarea por su id
@app.get('/tarea/{id}',tags=['Mostrar tarea por ID'])
def consultaTarea(id:int):
    for tarea in tareas:
            if tarea["id"]== id:
                return {"mensaje":"Tarea encontrada","Tarea":tarea}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

#endpoint para agregar una tarea
@app.post('/tarea/', tags=['Agregar tarea'])
def agregarTarea(tareanueva: dict):
    for nTarea in tareas:
          if nTarea["id"] == tareanueva.get("id"):
               raise HTTPException(status_code=400, detail="Ya existe una tarea con este ID")
    tareas.append(tareanueva)
    return tareanueva    

     