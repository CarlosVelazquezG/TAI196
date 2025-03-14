from pydantic import BaseModel,Field

class modelEnvios(BaseModel):
    cp: str = Field(..., min_length=5, max_length=5, example="76000")
    destino: str = Field(..., min_length=6, example="Querétaro, Querétaro")
    peso: int = Field(..., gt=0, le=130, description="El peso debe ser mayor a 0 y menor a 500", example="200")

