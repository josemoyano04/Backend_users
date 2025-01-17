import bcrypt

class HashContraseña:
    """
    Clase singleton encargada de hashear contraseñas y validar las mismas.

    Esta clase proporciona métodos para generar un hash de una contraseña
    utilizando el algoritmo bcrypt y para verificar si una contraseña
    coincide con un hash previamente generado. Se implementa como un
    singleton para asegurar que solo haya una instancia de la clase
    en toda la aplicación.

    Métodos:
        hashear_contraseña(contraseña: str) -> str:
            Genera un hash de la contraseña proporcionada.

        validar_contraseña(contraseña: str, hashed: str) -> bool:
            Verifica si la contraseña proporcionada coincide con el hash.
    """
    # Singleton
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = super(HashContraseña, cls).__new__(cls)
        return cls.__instancia

    def __init__(self):
        if not hasattr(self, "__inicializado"):
            self.__inicializado = True
            
    # Métodos
    def hashear_contraseña(self, contraseña: str) -> str:
        """
        Genera un hash de la contraseña proporcionada.

        Args:
            contraseña (str): La contraseña que se desea hashear.

        Returns:
            str: El hash de la contraseña generado.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password=contraseña.encode("utf-8"), 
                               salt=salt)
        
        return hashed.decode("utf-8")
    
    def validar_contraseña(self, contraseña: str, hashed: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con el hash.

        Args:
            contraseña (str): La contraseña que se desea validar.
            hashed (str): El hash contra el cual se va a validar la contraseña.

        Returns:
            bool: True si la contraseña coincide con el hash, False en caso contrario.
        """
        
        return bcrypt.checkpw(password= contraseña.encode("utf-8"), 
                              hashed_password= hashed.encode("utf-8"))
        