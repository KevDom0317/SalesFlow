"""
Aplicación Flask principal - API REST para SalesFlow
"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import Venta, Cliente, Producto
from builder import ReporteVentasBuilder, FacturaBuilder
from datetime import datetime
import mysql.connector

app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen

# ==================== ENDPOINTS DE VENTAS (CRUD) ====================

@app.route('/api/ventas', methods=['GET'])
def get_ventas():
    """Obtiene todas las ventas"""
    try:
        ventas = Venta.get_all()
        # Convertir fechas datetime a string
        for venta in ventas:
            if isinstance(venta['fecha'], datetime):
                venta['fecha'] = venta['fecha'].isoformat()
        return jsonify({
            "success": True,
            "data": ventas,
            "total": len(ventas)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ventas/<int:id_venta>', methods=['GET'])
def get_venta(id_venta):
    """Obtiene una venta por ID"""
    try:
        venta = Venta.get_by_id(id_venta)
        if venta:
            if isinstance(venta['fecha'], datetime):
                venta['fecha'] = venta['fecha'].isoformat()
            return jsonify({
                "success": True,
                "data": venta
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Venta no encontrada"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ventas', methods=['POST'])
def create_venta():
    """Crea una nueva venta"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({
                "success": False,
                "error": "No se proporcionaron datos"
            }), 400
        
        id_cliente = data.get('id_cliente')
        id_producto = data.get('id_producto')
        cantidad = data.get('cantidad', 1)
        
        if not id_cliente or not id_producto:
            return jsonify({
                "success": False,
                "error": "id_cliente e id_producto son requeridos"
            }), 400
        
        # Validar que cliente y producto existan
        cliente = Cliente.get_by_id(id_cliente)
        if not cliente:
            return jsonify({
                "success": False,
                "error": "Cliente no encontrado"
            }), 404
        
        producto = Producto.get_by_id(id_producto)
        if not producto:
            return jsonify({
                "success": False,
                "error": "Producto no encontrado"
            }), 404
        
        # Calcular total
        precio_unitario = float(producto['precio'])
        total = precio_unitario * cantidad
        
        # Crear venta
        venta_id = Venta.create(id_cliente, id_producto, cantidad, total)
        
        # Obtener la venta creada
        venta = Venta.get_by_id(venta_id)
        if isinstance(venta['fecha'], datetime):
            venta['fecha'] = venta['fecha'].isoformat()
        
        return jsonify({
            "success": True,
            "message": "Venta creada exitosamente",
            "data": venta
        }), 201
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ventas/<int:id_venta>', methods=['PUT'])
def update_venta(id_venta):
    """Actualiza una venta existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No se proporcionaron datos"
            }), 400
        
        # Verificar que la venta existe
        venta_existente = Venta.get_by_id(id_venta)
        if not venta_existente:
            return jsonify({
                "success": False,
                "error": "Venta no encontrada"
            }), 404
        
        id_cliente = data.get('id_cliente', venta_existente['id_cliente'])
        id_producto = data.get('id_producto', venta_existente['id_producto'])
        cantidad = data.get('cantidad', venta_existente['cantidad'])
        
        # Validar cliente y producto
        if id_cliente and not Cliente.get_by_id(id_cliente):
            return jsonify({
                "success": False,
                "error": "Cliente no encontrado"
            }), 404
        
        if id_producto and not Producto.get_by_id(id_producto):
            return jsonify({
                "success": False,
                "error": "Producto no encontrado"
            }), 404
        
        # Calcular nuevo total
        producto = Producto.get_by_id(id_producto)
        precio_unitario = float(producto['precio'])
        total = precio_unitario * cantidad
        
        # Actualizar venta
        Venta.update(id_venta, id_cliente, id_producto, cantidad, total)
        
        # Obtener venta actualizada
        venta = Venta.get_by_id(id_venta)
        if isinstance(venta['fecha'], datetime):
            venta['fecha'] = venta['fecha'].isoformat()
        
        return jsonify({
            "success": True,
            "message": "Venta actualizada exitosamente",
            "data": venta
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ventas/<int:id_venta>', methods=['DELETE'])
def delete_venta(id_venta):
    """Elimina una venta"""
    try:
        # Verificar que la venta existe
        venta = Venta.get_by_id(id_venta)
        if not venta:
            return jsonify({
                "success": False,
                "error": "Venta no encontrada"
            }), 404
        
        # Eliminar venta
        Venta.delete(id_venta)
        
        return jsonify({
            "success": True,
            "message": "Venta eliminada exitosamente"
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== ENDPOINTS DE CONSULTAS ====================

@app.route('/api/ventas/cliente/<int:id_cliente>', methods=['GET'])
def get_ventas_by_cliente(id_cliente):
    """Obtiene todas las ventas de un cliente específico"""
    try:
        # Verificar que el cliente existe
        cliente = Cliente.get_by_id(id_cliente)
        if not cliente:
            return jsonify({
                "success": False,
                "error": "Cliente no encontrado"
            }), 404
        
        ventas = Venta.get_by_cliente(id_cliente)
        
        # Convertir fechas
        for venta in ventas:
            if isinstance(venta['fecha'], datetime):
                venta['fecha'] = venta['fecha'].isoformat()
        
        return jsonify({
            "success": True,
            "cliente": {
                "id": cliente['id_cliente'],
                "nombre": cliente['nombre'],
                "correo": cliente['correo']
            },
            "data": ventas,
            "total": len(ventas)
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== ENDPOINTS DE REPORTES (PATRÓN BUILDER) ====================

@app.route('/api/reportes/ventas', methods=['GET'])
def generar_reporte_ventas():
    """Genera un reporte de ventas con filtros opcionales usando el patrón Builder"""
    try:
        # Obtener parámetros de filtro de la query string
        id_cliente = request.args.get('id_cliente', type=int)
        id_producto = request.args.get('id_producto', type=int)
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        # Construir reporte usando Builder
        builder = ReporteVentasBuilder()
        builder.reset()
        builder.set_titulo("Reporte de Ventas")
        builder.set_tipo("reporte_ventas")
        
        # Aplicar filtros si están presentes
        if id_cliente:
            builder.aplicar_filtro_cliente(id_cliente)
        
        if id_producto:
            builder.aplicar_filtro_producto(id_producto)
        
        if fecha_inicio and fecha_fin:
            builder.aplicar_filtro_fecha(fecha_inicio, fecha_fin)
        
        # Construir y obtener el reporte
        reporte = builder.calcular_metricas().construir()
        
        return jsonify({
            "success": True,
            "reporte": reporte.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/facturas/<int:id_venta>', methods=['GET'])
def generar_factura(id_venta):
    """Genera una factura detallada usando el patrón Builder"""
    try:
        venta = Venta.get_by_id(id_venta)
        if not venta:
            return jsonify({
                "success": False,
                "error": "Venta no encontrada"
            }), 404
        
        # Construir factura usando Builder
        factura_builder = FacturaBuilder()
        factura_builder.reset()
        factura_builder.set_numero_factura(id_venta)
        factura_builder.set_cliente(venta['id_cliente'])
        factura_builder.agregar_item(id_venta)
        
        if isinstance(venta['fecha'], datetime):
            factura_builder.set_fecha(venta['fecha'].isoformat())
        else:
            factura_builder.set_fecha(venta['fecha'])
        
        factura = factura_builder.construir()
        
        return jsonify({
            "success": True,
            "factura": factura
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== ENDPOINTS AUXILIARES ====================

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    """Obtiene todos los clientes"""
    try:
        clientes = Cliente.get_all()
        return jsonify({
            "success": True,
            "data": clientes,
            "total": len(clientes)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/productos', methods=['GET'])
def get_productos():
    """Obtiene todos los productos"""
    try:
        productos = Producto.get_all()
        return jsonify({
            "success": True,
            "data": productos,
            "total": len(productos)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== INTERFAZ WEB ====================

@app.route('/')
def index():
    """Página principal de la interfaz web"""
    return render_template('index.html')

@app.route('/ventas')
def ventas_page():
    """Página de gestión de ventas"""
    return render_template('ventas.html')

@app.route('/reportes')
def reportes_page():
    """Página de reportes"""
    return render_template('reportes.html')

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint no encontrado"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Error interno del servidor"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

