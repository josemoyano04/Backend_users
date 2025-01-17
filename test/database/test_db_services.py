import pytest
from fixture_bd import bd_test
from fixture_usuario import usuario_test, usuario_modificado_test

def test_registrar_usuario(bd_test, usuario_test):
    bd_test.registrar_usuario(usuario= usuario_test)
    usuario = bd_test.obtener_usuario(id_usuario= 1) # Al ser el único usuario en una prueba controlada, 
                                                     # su id siempre va a ser 1
    
    #Pruebas:
    assert usuario is not None
    assert usuario.nombre == usuario_test.nombre
    assert usuario.apellido == usuario_test.apellido
    assert usuario.nombre_usuario == usuario_test.nombre_usuario
    assert usuario.correo == usuario_test.correo
    assert usuario.hashed_password == usuario_test.hashed_password

def test_obtener_usuario(bd_test):
    user1 = bd_test.obtener_usuario(999)
    user2 = bd_test.obtener_usuario(-1)
    
    assert user1 is None
    assert user2 is None
    
def test_modificar_usuario(bd_test, usuario_modificado_test):
    
    bd_test.modificar_usuario(id_usuario= 1, usuario_modificado= usuario_modificado_test )
    usuario = bd_test.obtener_usuario(1)
    
    #Pruebas:
    assert usuario is not None
    assert usuario.nombre == usuario_modificado_test.nombre
    assert usuario.apellido == usuario_modificado_test.apellido
    assert usuario.nombre_usuario == usuario_modificado_test.nombre_usuario
    assert usuario.correo == usuario_modificado_test.correo
    assert usuario.hashed_password == usuario_modificado_test.hashed_password
    
def test_eliminar_usuario(bd_test):
    bd_test.eliminar_usuario(id_usuario= 1)
    usuario = bd_test.obtener_usuario(1)
    
    assert usuario is None