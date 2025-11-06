"""
Implementación del patrón Builder para la construcción de reportes y facturas
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
from models import Venta, Cliente, Producto

class Reporte:
    """Clase que representa un reporte construido"""
    
    def __init__(self):
        self.titulo = ""
        self.tipo = ""
        self.filtros = {}
        self.datos = []
        self.metricas = {}
        self.fecha_generacion = None
        self.formato = "JSON"
    
    def to_dict(self) -> Dict:
        """Convierte el reporte a diccionario para respuesta JSON"""
        return {
            "titulo": self.titulo,
            "tipo": self.tipo,
            "filtros_aplicados": self.filtros,
            "fecha_generacion": self.fecha_generacion.isoformat() if self.fecha_generacion else None,
            "formato": self.formato,
            "datos": self.datos,
            "metricas": self.metricas
        }

class IReporteBuilder(ABC):
    """Interfaz Builder para construir reportes"""
    
    @abstractmethod
    def reset(self) -> 'IReporteBuilder':
        """Reinicia el builder para construir un nuevo reporte"""
        pass
    
    @abstractmethod
    def set_titulo(self, titulo: str) -> 'IReporteBuilder':
        """Establece el título del reporte"""
        pass
    
    @abstractmethod
    def set_tipo(self, tipo: str) -> 'IReporteBuilder':
        """Establece el tipo de reporte"""
        pass
    
    @abstractmethod
    def aplicar_filtro_cliente(self, id_cliente: int) -> 'IReporteBuilder':
        """Aplica filtro por cliente"""
        pass
    
    @abstractmethod
    def aplicar_filtro_fecha(self, fecha_inicio: str, fecha_fin: str) -> 'IReporteBuilder':
        """Aplica filtro por rango de fechas"""
        pass
    
    @abstractmethod
    def aplicar_filtro_producto(self, id_producto: int) -> 'IReporteBuilder':
        """Aplica filtro por producto"""
        pass
    
    @abstractmethod
    def calcular_metricas(self) -> 'IReporteBuilder':
        """Calcula métricas del reporte (total, promedio, etc.)"""
        pass
    
    @abstractmethod
    def construir(self) -> Reporte:
        """Construye y retorna el reporte final"""
        pass

class ReporteVentasBuilder(IReporteBuilder):
    """Builder concreto para construir reportes de ventas"""
    
    def __init__(self):
        self.reporte = Reporte()
    
    def reset(self) -> 'IReporteBuilder':
        """Reinicia el builder"""
        self.reporte = Reporte()
        return self
    
    def set_titulo(self, titulo: str) -> 'IReporteBuilder':
        """Establece el título del reporte"""
        self.reporte.titulo = titulo
        return self
    
    def set_tipo(self, tipo: str) -> 'IReporteBuilder':
        """Establece el tipo de reporte"""
        self.reporte.tipo = tipo
        return self
    
    def aplicar_filtro_cliente(self, id_cliente: int) -> 'IReporteBuilder':
        """Aplica filtro por cliente"""
        self.reporte.filtros['id_cliente'] = id_cliente
        return self
    
    def aplicar_filtro_fecha(self, fecha_inicio: str, fecha_fin: str) -> 'IReporteBuilder':
        """Aplica filtro por rango de fechas"""
        self.reporte.filtros['fecha_inicio'] = fecha_inicio
        self.reporte.filtros['fecha_fin'] = fecha_fin
        return self
    
    def aplicar_filtro_producto(self, id_producto: int) -> 'IReporteBuilder':
        """Aplica filtro por producto"""
        self.reporte.filtros['id_producto'] = id_producto
        return self
    
    def calcular_metricas(self) -> 'IReporteBuilder':
        """Calcula métricas del reporte"""
        if not self.reporte.datos:
            self.reporte.metricas = {
                "total_ventas": 0,
                "total_monto": 0.0,
                "promedio_venta": 0.0,
                "cantidad_items": 0
            }
        else:
            total_monto = sum(float(venta['total']) for venta in self.reporte.datos)
            cantidad_items = sum(int(venta['cantidad']) for venta in self.reporte.datos)
            self.reporte.metricas = {
                "total_ventas": len(self.reporte.datos),
                "total_monto": round(total_monto, 2),
                "promedio_venta": round(total_monto / len(self.reporte.datos), 2) if self.reporte.datos else 0.0,
                "cantidad_items": cantidad_items
            }
        return self
    
    def construir(self) -> Reporte:
        """Construye el reporte aplicando los filtros y obteniendo datos"""
        # Obtener datos según los filtros aplicados
        ventas = []
        
        if 'id_cliente' in self.reporte.filtros:
            ventas = Venta.get_by_cliente(self.reporte.filtros['id_cliente'])
        else:
            ventas = Venta.get_all()
        
        # Aplicar filtro de producto si existe
        if 'id_producto' in self.reporte.filtros:
            ventas = [v for v in ventas if v['id_producto'] == self.reporte.filtros['id_producto']]
        
        # Aplicar filtro de fecha si existe
        if 'fecha_inicio' in self.reporte.filtros and 'fecha_fin' in self.reporte.filtros:
            fecha_inicio = datetime.fromisoformat(self.reporte.filtros['fecha_inicio'])
            fecha_fin = datetime.fromisoformat(self.reporte.filtros['fecha_fin'])
            ventas_filtradas = []
            for v in ventas:
                fecha_venta = v['fecha']
                if isinstance(fecha_venta, str):
                    fecha_venta = datetime.fromisoformat(fecha_venta.replace(' ', 'T'))
                elif isinstance(fecha_venta, datetime):
                    fecha_venta = fecha_venta
                else:
                    continue
                
                if fecha_inicio <= fecha_venta <= fecha_fin:
                    ventas_filtradas.append(v)
            ventas = ventas_filtradas
        
        # Convertir fechas a formato string para JSON
        for venta in ventas:
            if isinstance(venta['fecha'], datetime):
                venta['fecha'] = venta['fecha'].isoformat()
            elif isinstance(venta['fecha'], str):
                # Ya está en formato string
                pass
        
        self.reporte.datos = ventas
        self.reporte.fecha_generacion = datetime.now()
        
        # Calcular métricas si no se han calculado
        if not self.reporte.metricas:
            self.calcular_metricas()
        
        return self.reporte

class FacturaBuilder:
    """Builder para construir facturas detalladas"""
    
    def __init__(self):
        self.factura = {
            "numero_factura": None,
            "cliente": {},
            "items": [],
            "subtotal": 0.0,
            "total": 0.0,
            "fecha": None,
            "estado": "generada"
        }
    
    def reset(self):
        """Reinicia el builder"""
        self.factura = {
            "numero_factura": None,
            "cliente": {},
            "items": [],
            "subtotal": 0.0,
            "total": 0.0,
            "fecha": None,
            "estado": "generada"
        }
        return self
    
    def set_numero_factura(self, numero: int):
        """Establece el número de factura"""
        self.factura["numero_factura"] = numero
        return self
    
    def set_cliente(self, id_cliente: int):
        """Establece el cliente de la factura"""
        cliente = Cliente.get_by_id(id_cliente)
        if cliente:
            self.factura["cliente"] = {
                "id": cliente['id_cliente'],
                "nombre": cliente['nombre'],
                "correo": cliente['correo'],
                "telefono": cliente.get('telefono', ''),
                "direccion": cliente.get('direccion', '')
            }
        return self
    
    def agregar_item(self, id_venta: int):
        """Agrega un item de venta a la factura"""
        venta = Venta.get_by_id(id_venta)
        if venta:
            item = {
                "id_venta": venta['id_venta'],
                "producto": venta['producto_nombre'],
                "descripcion": venta.get('producto_descripcion', ''),
                "cantidad": venta['cantidad'],
                "precio_unitario": float(venta['producto_precio']),
                "subtotal": float(venta['total'])
            }
            self.factura["items"].append(item)
            self.factura["subtotal"] += float(venta['total'])
        return self
    
    def calcular_total(self):
        """Calcula el total de la factura"""
        # En este caso el subtotal es igual al total (sin impuestos)
        self.factura["total"] = round(self.factura["subtotal"], 2)
        return self
    
    def set_fecha(self, fecha: str):
        """Establece la fecha de la factura"""
        self.factura["fecha"] = fecha
        return self
    
    def construir(self):
        """Construye la factura final"""
        if not self.factura["fecha"]:
            self.factura["fecha"] = datetime.now().isoformat()
        self.calcular_total()
        return self.factura

