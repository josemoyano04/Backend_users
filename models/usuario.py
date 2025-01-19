#Usuario_DB
from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int]
    nombre: str
    apellido: str
    nombre_usuario: str
    correo: EmailStr
    
    model_config = ConfigDict(arbitrary_types_allowed= True)
    
    @model_validator(mode= "before")
    def validacion_general(cls, values):
        id = values.get("id")
        if id is None or id < 0:
            raise ValueError(f"El id del usuario no puede ser negativo. Id ingresado:{id}")

        nombre = values.get("nombre")
        if nombre is None:
            raise ValueError(f"El nombre no nulo.")
        
        apellido = values.get("apellido")
        if apellido is None:
            raise ValueError(f"El apellido no puede ser nulo")
        
        correo = values.get("correo")
        if correo is None:
            raise ValueError(f"El correo no puede ser nulo")
        
        return  values