from pydantic import model_validator
from models.usuario import Usuario
from services.HashContraseña import HashContraseña

class UsuarioBD(Usuario):
    hashed_password: str #Contraseña hasheada-
    
    @model_validator(mode= "before")
    def validacion_pass(cls, values):
        hashed_password = values.get("hashed_password")
        if hashed_password is None:
            raise ValueError("La contraseña no puede ser nula")
        
        if len(hashed_password) < 8:
            raise ValueError("El tamaño de la contraseña debe ser como minimo de 8 caracteres.")
                
        values["hashed_password"] = HashContraseña().hashear_contraseña(hashed_password)
        
        return values
    
    