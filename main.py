from services.HashContraseña import HashContraseña
from models.usuario_db import UsuarioBD

user = UsuarioBD(
    id= 1,
    nombre= "Jose",
    apellido= "Moyano",
    correo= "josemoyano059@gmail.com",
    nombre_usuario= "josemoyano04",
    hashed_password= "45543871"
)
pas = user.hashed_password
print(pas)

print(HashContraseña().validar_contraseña(contraseña="45543871", hashed= user.hashed_password))