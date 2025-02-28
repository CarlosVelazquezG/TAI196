
from pydantic import BaseModel, Field, EmailStr

#modelo para validación de datos
class modelUsuario(BaseModel):
    id:int = Field(..., gt=0, description="Id Único y sólo números positivos")
    nombre:str = Field(..., min_length=3, max_length=15, description="Nombre debe contener sólo letras y espacios", example="Jon Doe")
    edad:int = Field(..., gt=0, le=130, description="La edad debe ser mayor a 0 y menor a 130")
    correo:str = Field(..., pattern=r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$',description="Correo válido", example="usuario@example.com")

class modelAuth(BaseModel):
    correo:EmailStr
    passw:str = Field(..., min_lenght=8,strip_whitespace=True, description="Contraseña mínimo 8 caractéres")
    