import os
import sqlite3
from typing import Optional
from models.usuario_db import UsuarioBD, Usuario
from services.HashContraseña import HashContraseña
from errors.codigo_incorrecto import CodigoIncorrecto
from config.config import RUTA_BD, RUTA_BD__TEST, HASH_CODIGO_CONFIRMACION_ELIMINACION_BD

class BaseDeDatos:
    """
    Clase singleton encargada de la creacion de la base de datos del proyecto.
    """
    # Singleton
    __instancia = None

    def __new__(cls, *args, **kwargs):
        if cls.__instancia is None:
            cls.__instancia = super(BaseDeDatos, cls).__new__(cls)
        return cls.__instancia

    def __init__(self):
        if not hasattr(self, "__inicializado"):
            self.__inicializado = True
            self.ruta_bd = RUTA_BD
            self.__conexion = None  # Nueva variable para mantener la conexión

    # Control de habilitacion de pruebas. (Las pruebas se realizan en una base de datos simulada a fin de no afectar
    # la real en caso de que la misma ya tenga datos almacenados.)
    __modo_test = False

    @property
    def modo_test(self):
        return self.__modo_test

    def activar_test(self):
        self.__modo_test = True
        print("Modo test: ACTIVADO")

    def desactivar_test(self):
        self.__modo_test = False
        print("Modo test: DESACTIVADO")

    # Métodos
    def __crear_archivo_bd(self) -> None:
        """
        Crea el archivo vacio de la base de datos luego de verificar si el archivo no existe.
        Solo crea el archivo si aún no se creó.
        """
        # Control de creación de base de datos real o de prueba.
        self.ruta_bd = RUTA_BD if not self.__modo_test else RUTA_BD__TEST

        if not os.path.exists(self.ruta_bd):
            with open(self.ruta_bd, 'w'):
                print(f"La base de datos se creo correctamente. Ruta del archivo: {RUTA_BD}")

    def __conexion_bd(self) -> sqlite3.Connection:
        """
        Retorna la conexion a la base de datos.
        Produce error si la base de datos no esta creada.
        """
        try:
            if self.__conexion is None:  # Si no hay una conexión activa, crea una nueva
                self.__conexion = sqlite3.connect(self.ruta_bd)
            return self.__conexion
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al conectar la base de datos: {e}")

    def __crear_tablas_bd(self) -> None:
        """
        Crea las tablas si estas no existen en la base de datos
        """
        try:
            with self.__conexion_bd() as conexion:
                cursor = conexion.cursor()
                # Creación de tablas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Usuario(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre VARCHAR(50) NOT NULL,
                        apellido VARCHAR(50) NOT NULL,
                        nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
                        correo VARCHAR(100) NOT NULL UNIQUE,
                        contrasenia VARCHAR(256) NOT NULL
                    )
                    """)
                # Guardado de cambios en la conexión
                conexion.commit()

        except sqlite3.Error as e:
            conexion.rollback()  # Se recupera el último commit de la base de datos para eliminar errores.
            raise RuntimeError(f"Error al intentar crear las tablas en la base de datos. {e}")

    def iniciar_creacion(self) -> None:
        # Control de creación del archivo de la base de datos
        self.__crear_archivo_bd()

        # Creación tablas dentro de la base de datos
        self.__crear_tablas_bd()

    def obtener_usuario(self, id_usuario: int) -> Optional[UsuarioBD]:
        try:
            with self.__conexion_bd() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    SELECT * FROM Usuario WHERE id = ?
                    """, (id_usuario,)
                )
                usuarios = cursor.fetchall()

                # Eliminado commit innecesario para consultas SELECT
                if len(usuarios) == 0:
                    return None

                user = usuarios[0]
                return Usuario(id= user[0],
                                 nombre= user[1],
                                 apellido= user[2],
                                 nombre_usuario= user[3],
                                 correo= user[4])
                
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al obtener el usuario. {e}")

    def registrar_usuario(self, usuario: UsuarioBD) -> None:
        try:
            # Verificación de usuario no almacenado:
            if type(self.obtener_usuario(usuario.id)) == UsuarioBD:
                raise ValueError

            with self.__conexion_bd() as conexion:
                cursor = conexion.cursor()
                cursor.execute("""
                            INSERT INTO Usuario (nombre, apellido, nombre_usuario, correo, contrasenia) 
                            VALUES (?, ?, ?, ?, ?)
                            """, (usuario.nombre, usuario.apellido, usuario.nombre_usuario,
                                  usuario.correo, usuario.hashed_password))

                conexion.commit()  # Guardado de cambios en la conexión

        except sqlite3.Error as e:
            conexion.rollback()  # Se recupera el último commit de la base de datos para eliminar errores.
            raise RuntimeError(f"Error al registrar el usuario. {e}")

        except ValueError as e:
            raise RuntimeError(f"El id del usuario que intenta registrar ya está en uso. {e}")

    def modificar_usuario(self, id_usuario: int, usuario_modificado: UsuarioBD) -> None:
        try:
            usuario = self.obtener_usuario(id_usuario)
            if usuario is None:
                raise ValueError(f"No se encontro el usuario con id: {id_usuario}")

            with self.__conexion_bd() as conexion:
                cursor = conexion.cursor()
                cursor.execute("""
                        UPDATE Usuario
                        SET nombre = ?, apellido = ?, nombre_usuario = ?, correo = ?, contrasenia = ?
                        WHERE id = ?;
                    """, (usuario_modificado.nombre, usuario_modificado.apellido,
                          usuario_modificado.nombre_usuario, usuario_modificado.correo,
                          usuario_modificado.hashed_password, id_usuario))

                # Guardado de cambios en la conexión
                conexion.commit()

        except sqlite3.Error as e:
            conexion.rollback()  # Se recupera el último commit de la base de datos para eliminar errores.
            raise RuntimeError(f"Error al modificar el usuario. {e}")

        except ValueError as e:
            raise RuntimeError(f"El usuario que intenta actualizar no existe. {e}")

    def eliminar_usuario(self, id_usuario: int) -> None:
        try:
            usuario = self.obtener_usuario(id_usuario)
            if usuario is None:
                raise ValueError(f"No se encuentra el usuario con id: {id_usuario}")

            with self.__conexion_bd() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    DELETE FROM Usuario
                    WHERE id = ?
                    """, (id_usuario,)
                )
                conexion.commit()

        except sqlite3.Error as e:
            conexion.rollback()
            raise RuntimeError(f"Error al eliminar el usuario. {e}")
        except ValueError as e:
            raise RuntimeError(f"El usuario que intenta eliminar no existe. {e}")

    def cerrar_conexiones(self):
        """Cerrar conexiones abiertas explícitamente."""
        if self.__conexion:
            self.__conexion.close()
            self.__conexion = None
            print("Conexión cerrada explícitamente.")

    def _eliminar_bd(self, codigo_validacion: str) -> None:
        try:
            if HashContraseña().validar_contraseña(codigo_validacion, HASH_CODIGO_CONFIRMACION_ELIMINACION_BD):
                os.remove(RUTA_BD)
            else:
                raise CodigoIncorrecto("CODIGO INCORRECTO. No se llevo a cabo la eliminacion de la base de datos")
        except Exception as e:
            raise RuntimeError(f"Error al eliminar la base de datos: {e}")
