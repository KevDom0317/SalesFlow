# 🔗 URLs para Pruebas en Postman - SalesFlow

## 🚀 URL Base
```
http://localhost:5000
```

---

## 📊 VENTAS (CRUD)

### 1. Obtener Todas las Ventas
```
GET http://localhost:5000/api/ventas
```

### 2. Obtener Venta por ID
```
GET http://localhost:5000/api/ventas/1
```
*Cambia `1` por el ID de la venta que quieras consultar*

### 3. Crear Nueva Venta
```
POST http://localhost:5000/api/ventas
```
**Headers:**
- `Content-Type: application/json`

**Body (raw JSON):**
```json
{
  "id_cliente": 1,
  "id_producto": 1,
  "cantidad": 2
}
```

### 4. Actualizar Venta
```
PUT http://localhost:5000/api/ventas/1
```
*Cambia `1` por el ID de la venta que quieras actualizar*

**Headers:**
- `Content-Type: application/json`

**Body (raw JSON):**
```json
{
  "id_cliente": 1,
  "id_producto": 2,
  "cantidad": 3
}
```

### 5. Eliminar Venta
```
DELETE http://localhost:5000/api/ventas/1
```
*Cambia `1` por el ID de la venta que quieras eliminar*

---

## 🔍 CONSULTAS

### 6. Ventas por Cliente
```
GET http://localhost:5000/api/ventas/cliente/1
```
*Cambia `1` por el ID del cliente*

---

## 📈 REPORTES (Patrón Builder)

### 7. Reporte General (Sin Filtros)
```
GET http://localhost:5000/api/reportes/ventas
```

### 8. Reporte por Cliente
```
GET http://localhost:5000/api/reportes/ventas?id_cliente=1
```

### 9. Reporte por Producto
```
GET http://localhost:5000/api/reportes/ventas?id_producto=1
```

### 10. Reporte por Rango de Fechas
```
GET http://localhost:5000/api/reportes/ventas?fecha_inicio=2025-11-01&fecha_fin=2025-11-30
```

### 11. Reporte con Múltiples Filtros
```
GET http://localhost:5000/api/reportes/ventas?id_cliente=1&id_producto=1&fecha_inicio=2025-11-01&fecha_fin=2025-11-30
```

---

## 🧾 FACTURAS (Patrón Builder)

### 12. Generar Factura
```
GET http://localhost:5000/api/facturas/1
```
*Cambia `1` por el ID de la venta*

---

## 📋 ENDPOINTS AUXILIARES

### 13. Obtener Todos los Clientes
```
GET http://localhost:5000/api/clientes
```

### 14. Obtener Todos los Productos
```
GET http://localhost:5000/api/productos
```

---

## 📝 Ejemplos de Body para POST/PUT

### Crear Venta (POST)
```json
{
  "id_cliente": 1,
  "id_producto": 1,
  "cantidad": 2
}
```

### Actualizar Venta (PUT)
```json
{
  "id_cliente": 1,
  "id_producto": 2,
  "cantidad": 5
}
```

---

## 🎯 Configurar Variable en Postman

Para facilitar las pruebas, crea una variable de entorno en Postman:

1. Ve a **Environments** → **Create Environment**
2. Nombre: `SalesFlow Local`
3. Agrega variable:
   - **Variable**: `base_url`
   - **Initial Value**: `http://localhost:5000`
4. Selecciona este environment

Luego puedes usar en las URLs: `{{base_url}}/api/ventas`

---

## ✅ Checklist de Pruebas Recomendadas

### Básicas
- [ ] `GET /api/ventas` - Ver todas las ventas
- [ ] `GET /api/clientes` - Ver clientes disponibles
- [ ] `GET /api/productos` - Ver productos disponibles

### CRUD Ventas
- [ ] `POST /api/ventas` - Crear una venta nueva
- [ ] `GET /api/ventas/{id}` - Ver venta específica
- [ ] `PUT /api/ventas/{id}` - Actualizar venta
- [ ] `DELETE /api/ventas/{id}` - Eliminar venta

### Consultas
- [ ] `GET /api/ventas/cliente/1` - Ventas de un cliente

### Reportes (Builder)
- [ ] `GET /api/reportes/ventas` - Reporte general
- [ ] `GET /api/reportes/ventas?id_cliente=1` - Con filtro cliente
- [ ] `GET /api/reportes/ventas?fecha_inicio=2025-11-01&fecha_fin=2025-11-30` - Con filtro fechas
- [ ] `GET /api/reportes/ventas?id_cliente=1&id_producto=1` - Múltiples filtros

### Facturas (Builder)
- [ ] `GET /api/facturas/1` - Generar factura

### Validaciones
- [ ] Crear venta con cliente inexistente (debe dar error)
- [ ] Crear venta con producto inexistente (debe dar error)
- [ ] Obtener venta con ID inexistente (debe dar 404)

---

## 📸 Respuestas Esperadas

### Éxito (200/201)
```json
{
  "success": true,
  "data": [...],
  "message": "Operación exitosa"
}
```

### Error (400/404/500)
```json
{
  "success": false,
  "error": "Mensaje de error"
}
```

---

## 🚨 Notas Importantes

1. **Asegúrate de que la aplicación esté corriendo** antes de hacer las pruebas
2. **Ejecuta primero** `GET /api/clientes` y `GET /api/productos` para conocer los IDs disponibles
3. **Usa IDs válidos** que existan en tu base de datos
4. **Para fechas**, usa formato `YYYY-MM-DD` (ejemplo: `2025-11-01`)
5. **Todos los endpoints retornan JSON**

