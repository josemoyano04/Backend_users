import os
import gc
import pytest
from config.config import RUTA_BD__TEST
from database.BD_services import BaseDeDatos

@pytest.fixture(scope= "module")
def bd_test():
    print("/Incializacion de base de datos para test./")
    base_de_datos = BaseDeDatos()
    base_de_datos.activar_test()
    print(f"/Modo test activo: {base_de_datos.modo_test}/")
    print(f"/Incio de creacion de base de datos y tablas./")
    base_de_datos.iniciar_creacion() #Creacion de archivo de base de datos y tablas para pruebas.
    print(f"/Fin de creacion de base de datos y tablas./")
    
    yield base_de_datos
    
    #Cierre de conexiones
    base_de_datos.cerrar_conexiones()
    
    # Limpieza de base de datos y eliminacion de las mismas una vez finalizadas las pruebas:
    if os.path.exists(RUTA_BD__TEST):
        base_de_datos.desactivar_test() #Desactivacion de modo test en clase BaseDeDatos
        base_de_datos = None #Eliminacion de referencia a base de datos
        gc.collect() #Forzado de recoleccion de basura
        os.remove(RUTA_BD__TEST)
