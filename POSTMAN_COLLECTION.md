# Colección Postman - SalesFlow API

## 📬 Importar en Postman

Crea una nueva colección en Postman llamada "SalesFlow API" y agrega los siguientes requests:

## 🔵 Ventas

### 1. Obtener Todas las Ventas
- **Método**: GET
- **URL**: `http://localhost:5000/api/ventas`
- **Headers**: Ninguno

### 2. Obtener Venta por ID
- **Método**: GET
- **URL**: `http://localhost:5000/api/ventas/1`
- **Headers**: Ninguno

### 3. Crear Nueva Venta
- **Método**: POST
- **URL**: `http://localhost:5000/api/ventas`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "id_cliente": 1,
  "id_producto": 1,
  "cantidad": 2
}
```

### 4. Actualizar Venta
- **Método**: PUT
- **URL**: `http://localhost:5000/api/ventas/1`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "id_cliente": 1,
  "id_producto": 2,
  "cantidad": 3
}
```

### 5. Eliminar Venta
- **Método**: DELETE
- **URL**: `http://localhost:5000/api/ventas/1`
- **Headers**: Ninguno

## 🔍 Consultas

### 6. Ventas por Cliente
- **Método**: GET
- **URL**: `http://localhost:5000/api/ventas/cliente/1`
- **Headers**: Ninguno

## 📊 Reportes (Patrón Builder)

### 7. Reporte General (Sin Filtros)
- **Método**: GET
- **URL**: `http://localhost:5000/api/reportes/ventas`
- **Headers**: Ninguno

### 8. Reporte por Cliente
- **Método**: GET
- **URL**: `http://localhost:5000/api/reportes/ventas?id_cliente=1`
- **Headers**: Ninguno

### 9. Reporte por Rango de Fechas
- **Método**: GET
- **URL**: `http://localhost:5000/api/reportes/ventas?fecha_inicio=2025-11-01&fecha_fin=2025-11-30`
- **Headers**: Ninguno

### 10. Reporte con Múltiples Filtros
- **Método**: GET
- **URL**: `http://localhost:5000/api/reportes/ventas?id_cliente=1&id_producto=1&fecha_inicio=2025-11-01&fecha_fin=2025-11-30`
- **Headers**: Ninguno

## 🧾 Facturas (Patrón Builder)

### 11. Generar Factura
- **Método**: GET
- **URL**: `http://localhost:5000/api/facturas/1`
- **Headers**: Ninguno

## 📋 Endpoints Auxiliares

### 12. Obtener Todos los Clientes
- **Método**: GET
- **URL**: `http://localhost:5000/api/clientes`
- **Headers**: Ninguno

### 13. Obtener Todos los Productos
- **Método**: GET
- **URL**: `http://localhost:5000/api/productos`
- **Headers**: Ninguno

## 📸 Ejemplos de Respuestas

### Respuesta Exitosa (GET /api/ventas)
```json
{
  "success": true,
  "data": [
    {
      "id_venta": 1,
      "id_cliente": 1,
      "id_producto": 1,
      "fecha": "2025-11-04T19:50:19",
      "cantidad": 1,
      "total": 12500.00,
      "cliente_nombre": "Carlos Pérez",
      "cliente_correo": "carlosp@example.com",
      "producto_nombre": "Laptop HP",
      "producto_precio": 12500.00
    }
  ],
  "total": 1
}
```

### Respuesta de Reporte
```json
{
  "success": true,
  "reporte": {
    "titulo": "Reporte de Ventas",
    "tipo": "reporte_ventas",
    "filtros_aplicados": {
      "id_cliente": 1
    },
    "fecha_generacion": "2025-11-05T10:30:00",
    "formato": "JSON",
    "datos": [...],
    "metricas": {
      "total_ventas": 2,
      "total_monto": 13200.00,
      "promedio_venta": 6600.00,
      "cantidad_items": 3
    }
  }
}
```

### Respuesta de Factura
```json
{
  "success": true,
  "factura": {
    "numero_factura": 1,
    "cliente": {
      "id": 1,
      "nombre": "Carlos Pérez",
      "correo": "carlosp@example.com",
      "telefono": "555-1234",
      "direccion": "Av. Central 123"
    },
    "items": [
      {
        "id_venta": 1,
        "producto": "Laptop HP",
        "descripcion": "Laptop 15 pulgadas, Ryzen 5, 8GB RAM",
        "cantidad": 1,
        "precio_unitario": 12500.00,
        "subtotal": 12500.00
      }
    ],
    "subtotal": 12500.00,
    "total": 12500.00,
    "fecha": "2025-11-04T19:50:19",
    "estado": "generada"
  }
}
```

### Respuesta de Error
```json
{
  "success": false,
  "error": "Cliente no encontrado"
}
```

## 🎯 Variables de Entorno en Postman

Crea una variable de entorno en Postman:
- `base_url`: `http://localhost:5000`

Luego puedes usar `{{base_url}}/api/ventas` en las URLs.

## ✅ Checklist de Pruebas

- [ ] Obtener todas las ventas
- [ ] Crear una nueva venta
- [ ] Obtener venta por ID
- [ ] Actualizar una venta existente
- [ ] Eliminar una venta
- [ ] Obtener ventas por cliente
- [ ] Generar reporte sin filtros
- [ ] Generar reporte con filtro de cliente
- [ ] Generar reporte con filtro de fechas
- [ ] Generar reporte con múltiples filtros
- [ ] Generar factura de una venta
- [ ] Verificar manejo de errores (IDs inválidos)

