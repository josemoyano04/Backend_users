from pytest import fixture
from models.usuario_db import UsuarioBD


@fixture(scope= "module")
def usuario_test():
     return UsuarioBD(
         id= 1, #AutoAsignado en la base de datos como autoincremental
         nombre= "Jose",
         apellido= "Moyano",
         nombre_usuario= "josemoyano04",
         correo= "josemoyano059@gmail.com",
         hashed_password= "contraseña"
     )
@fixture(scope= "module")
def usuario_modificado_test():
     return UsuarioBD(
         id= 1, #El id no se tiene en cuenta para la modificacion #TODO crear logica de reasignacion de id's (No recomendado)
         nombre= "Jose_MODIFICADO",
         apellido= "Moyano_MODIFICADO",
         nombre_usuario= "josemoyano04_MODIFICADO",
         correo= "josemoyano059@gmail.com",
         hashed_password= "contraseña_MODIFICADO"
     )