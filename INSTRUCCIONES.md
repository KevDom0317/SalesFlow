# Instrucciones Rápidas - SalesFlow

## 🚀 Inicio Rápido

### 1. Configurar Base de Datos

```bash
# Importar el esquema de base de datos
mysql -u root -p salesflow < salesflow.sql
```

O usar phpMyAdmin/MySQL Workbench para importar `salesflow.sql`

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=salesflow
DB_USER=root
DB_PASSWORD=tu_contraseña
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

```bash
python app.py
```

### 5. Acceder a la Aplicación

- **Interfaz Web**: http://localhost:5000
- **API REST**: http://localhost:5000/api

## 📝 Pruebas Rápidas

### Crear una Venta
```bash
curl -X POST http://localhost:5000/api/ventas \
  -H "Content-Type: application/json" \
  -d '{"id_cliente": 1, "id_producto": 1, "cantidad": 2}'
```

### Obtener Todas las Ventas
```bash
curl http://localhost:5000/api/ventas
```

### Generar Reporte
```bash
curl "http://localhost:5000/api/reportes/ventas?id_cliente=1"
```

### Generar Factura
```bash
curl http://localhost:5000/api/facturas/1
```

## 🎯 Endpoints Principales

- `GET /api/ventas` - Listar todas las ventas
- `POST /api/ventas` - Crear venta
- `GET /api/ventas/{id}` - Obtener venta por ID
- `PUT /api/ventas/{id}` - Actualizar venta
- `DELETE /api/ventas/{id}` - Eliminar venta
- `GET /api/ventas/cliente/{id}` - Ventas por cliente
- `GET /api/reportes/ventas` - Generar reporte (con filtros opcionales)
- `GET /api/facturas/{id}` - Generar factura

## 📚 Documentación Completa

Ver `README.md` para documentación completa y `PATRON_BUILDER.md` para detalles del patrón Builder.

