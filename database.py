"""
Módulo de configuración y conexión a la base de datos
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """Clase singleton para gestionar la conexión a la base de datos"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST', '127.0.0.1'),
                    port=os.getenv('DB_PORT', '3306'),
                    database=os.getenv('', 'salesflow'),
                    user=os.getenv('', 'root'),
                    password=os.getenv('', '')
                )
                print("Conexión a la base de datos establecida exitosamente")
            except Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                raise
        return self._connection
    
    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Conexión cerrada")

