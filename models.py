"""
Modelos de datos para SalesFlow
"""
from database import Database
from datetime import datetime
from typing import Optional, Dict, List

class Cliente:
    """Modelo para la entidad Cliente"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los clientes"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes ORDER BY id_cliente")
        clientes = cursor.fetchall()
        cursor.close()
        return clientes
    
    @staticmethod
    def get_by_id(id_cliente: int):
        """Obtiene un cliente por ID"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        return cliente

class Producto:
    """Modelo para la entidad Producto"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los productos"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos ORDER BY id_producto")
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    @staticmethod
    def get_by_id(id_producto: int):
        """Obtiene un producto por ID"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        return producto

class Venta:
    """Modelo para la entidad Venta"""
    
    @staticmethod
    def create(id_cliente: int, id_producto: int, cantidad: int, total: float):
        """Crea una nueva venta"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO ventas (id_cliente, id_producto, cantidad, total, fecha) VALUES (%s, %s, %s, %s, NOW())",
                (id_cliente, id_producto, cantidad, total)
            )
            conn.commit()
            venta_id = cursor.lastrowid
            cursor.close()
            return venta_id
        except Error as e:
            conn.rollback()
            cursor.close()
            raise e
    
    @staticmethod
    def get_all():
        """Obtiene todas las ventas con información de cliente y producto"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.id_venta, v.id_cliente, v.id_producto, v.fecha, v.cantidad, v.total,
                   c.nombre as cliente_nombre, c.correo as cliente_correo,
                   p.nombre as producto_nombre, p.precio as producto_precio
            FROM ventas v
            INNER JOIN clientes c ON v.id_cliente = c.id_cliente
            INNER JOIN productos p ON v.id_producto = p.id_producto
            ORDER BY v.fecha DESC
        """)
        ventas = cursor.fetchall()
        cursor.close()
        return ventas
    
    @staticmethod
    def get_by_id(id_venta: int):
        """Obtiene una venta por ID con información relacionada"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.id_venta, v.id_cliente, v.id_producto, v.fecha, v.cantidad, v.total,
                   c.nombre as cliente_nombre, c.correo as cliente_correo, c.telefono as cliente_telefono,
                   c.direccion as cliente_direccion,
                   p.nombre as producto_nombre, p.descripcion as producto_descripcion, 
                   p.precio as producto_precio
            FROM ventas v
            INNER JOIN clientes c ON v.id_cliente = c.id_cliente
            INNER JOIN productos p ON v.id_producto = p.id_producto
            WHERE v.id_venta = %s
        """, (id_venta,))
        venta = cursor.fetchone()
        cursor.close()
        return venta
    
    @staticmethod
    def get_by_cliente(id_cliente: int):
        """Obtiene todas las ventas de un cliente"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.id_venta, v.id_cliente, v.id_producto, v.fecha, v.cantidad, v.total,
                   c.nombre as cliente_nombre, c.correo as cliente_correo,
                   p.nombre as producto_nombre, p.precio as producto_precio
            FROM ventas v
            INNER JOIN clientes c ON v.id_cliente = c.id_cliente
            INNER JOIN productos p ON v.id_producto = p.id_producto
            WHERE v.id_cliente = %s
            ORDER BY v.fecha DESC
        """, (id_cliente,))
        ventas = cursor.fetchall()
        cursor.close()
        return ventas
    
    @staticmethod
    def update(id_venta: int, id_cliente: int, id_producto: int, cantidad: int, total: float):
        """Actualiza una venta existente"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE ventas SET id_cliente = %s, id_producto = %s, cantidad = %s, total = %s WHERE id_venta = %s",
                (id_cliente, id_producto, cantidad, total, id_venta)
            )
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            conn.rollback()
            cursor.close()
            raise e
    
    @staticmethod
    def delete(id_venta: int):
        """Elimina una venta"""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            conn.rollback()
            cursor.close()
            raise e

