# SalesFlow - Sistema de Gestión de Ventas

Sistema basado en API REST para gestionar ventas, clientes y productos, implementando el patrón Builder para la construcción dinámica de reportes y facturas.

## 📋 Descripción

SalesFlow es una aplicación web desarrollada en Python (Flask) que permite:
- Registrar y gestionar ventas (CRUD completo)
- Consultar ventas por cliente
- Generar reportes filtrados dinámicamente
- Crear facturas detalladas
- Interfaz web básica para interacción

## 🏗️ Arquitectura

### Tecnologías Utilizadas
- **Backend**: Python 3.x + Flask
- **Base de Datos**: MySQL/MariaDB
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Patrón de Diseño**: Builder

### Estructura del Proyecto

```
SalesFlow/
│
├── app.py                 # Aplicación Flask principal con endpoints REST
├── models.py              # Modelos de datos (Cliente, Producto, Venta)
├── database.py            # Configuración y conexión a base de datos
├── builder.py             # Implementación del patrón Builder
├── requirements.txt       # Dependencias del proyecto
├── .env.example          # Ejemplo de configuración
│
├── templates/            # Plantillas HTML
│   ├── index.html        # Página principal
│   ├── ventas.html       # Gestión de ventas
│   └── reportes.html     # Reportes y facturas
│
└── static/               # Archivos estáticos
    ├── style.css         # Estilos CSS
    ├── ventas.js         # JavaScript para ventas
    └── reportes.js       # JavaScript para reportes
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- MySQL/MariaDB instalado y ejecutándose
- Base de datos `salesflow` creada (usar el archivo `salesflow.sql`)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**
   - Importar el archivo `salesflow.sql` en tu base de datos MySQL/MariaDB
   - Crear un archivo `.env` basado en `.env.example` y configurar las credenciales:
   ```
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=salesflow
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   ```

4. **Ejecutar la aplicación**
```bash
python app.py
```

5. **Acceder a la aplicación**
   - Interfaz web: http://localhost:5000
   - API REST: http://localhost:5000/api

## 📡 Endpoints de la API

### Ventas (CRUD)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/ventas` | Obtener todas las ventas |
| GET | `/api/ventas/<id>` | Obtener una venta por ID |
| POST | `/api/ventas` | Crear una nueva venta |
| PUT | `/api/ventas/<id>` | Actualizar una venta |
| DELETE | `/api/ventas/<id>` | Eliminar una venta |

### Consultas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/ventas/cliente/<id_cliente>` | Obtener ventas por cliente |

### Reportes y Facturas (Patrón Builder)

| Método | Endpoint | Descripción | Parámetros Query |
|--------|----------|-------------|------------------|
| GET | `/api/reportes/ventas` | Generar reporte de ventas | `id_cliente`, `id_producto`, `fecha_inicio`, `fecha_fin` |
| GET | `/api/facturas/<id_venta>` | Generar factura | - |

### Endpoints Auxiliares

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/clientes` | Obtener todos los clientes |
| GET | `/api/productos` | Obtener todos los productos |

## 🎯 Ejemplos de Uso

### Crear una Venta (POST)
```bash
curl -X POST http://localhost:5000/api/ventas \
  -H "Content-Type: application/json" \
  -d '{
    "id_cliente": 1,
    "id_producto": 1,
    "cantidad": 2
  }'
```

### Generar Reporte con Filtros (GET)
```bash
curl "http://localhost:5000/api/reportes/ventas?id_cliente=1&fecha_inicio=2025-11-01&fecha_fin=2025-11-30"
```

### Generar Factura (GET)
```bash
curl http://localhost:5000/api/facturas/1
```

## 🏛️ Patrón Builder - Justificación

El patrón Builder se implementa en dos contextos principales:

### 1. ReporteVentasBuilder
**Justificación**: Permite construir reportes de ventas de manera flexible, aplicando filtros opcionales (cliente, producto, rango de fechas) sin necesidad de crear múltiples métodos o constructores complejos. El builder permite:
- Construcción paso a paso del reporte
- Aplicación de filtros de forma incremental
- Cálculo automático de métricas
- Flexibilidad para agregar nuevos filtros en el futuro

**Uso en la arquitectura REST**:
- El endpoint `/api/reportes/ventas` recibe parámetros opcionales vía query string
- El builder construye dinámicamente el reporte según los filtros proporcionados
- La respuesta JSON incluye datos, métricas y filtros aplicados

### 2. FacturaBuilder
**Justificación**: Permite construir facturas detalladas agregando información de manera incremental:
- Establecer número de factura
- Agregar datos del cliente
- Agregar items de venta
- Calcular totales automáticamente

**Uso en la arquitectura REST**:
- El endpoint `/api/facturas/<id>` construye una factura completa
- El builder agrega información relacionada (cliente, productos)
- La respuesta incluye toda la información necesaria para mostrar la factura

## 📊 Diagramas UML

### Diagrama de Clases - Patrón Builder

```
┌─────────────────────┐
│   IReporteBuilder   │
│  (Interface)        │
├─────────────────────┤
│ + reset()           │
│ + set_titulo()      │
│ + set_tipo()        │
│ + aplicar_filtro_   │
│   cliente()         │
│ + aplicar_filtro_   │
│   fecha()           │
│ + aplicar_filtro_   │
│   producto()        │
│ + calcular_metricas │
│ + construir()       │
└─────────────────────┘
         ▲
         │ implements
         │
┌─────────────────────┐
│ ReporteVentasBuilder│
├─────────────────────┤
│ - reporte: Reporte  │
├─────────────────────┤
│ + reset()           │
│ + set_titulo()      │
│ + aplicar_filtro_   │
│   cliente()         │
│ + construir()       │
└─────────────────────┘
         │
         │ builds
         ▼
┌─────────────────────┐
│      Reporte        │
├─────────────────────┤
│ - titulo            │
│ - tipo              │
│ - filtros           │
│ - datos             │
│ - metricas          │
│ - fecha_generacion  │
├─────────────────────┤
│ + to_dict()         │
└─────────────────────┘
```

### Diagrama de Secuencia - Generación de Reporte

```
Cliente          Flask App        Builder         Models      Database
  │                 │                │              │            │
  │  GET /api/      │                │              │            │
  │  reportes/ventas│                │              │            │
  ├────────────────>│                │              │            │
  │                 │                │              │            │
  │                 │  new Builder() │              │            │
  │                 ├───────────────>│              │            │
  │                 │                │              │            │
  │                 │  reset()       │              │            │
  │                 ├───────────────>│              │            │
  │                 │  aplicar_filtro│              │            │
  │                 ├───────────────>│              │            │
  │                 │  construir()   │              │            │
  │                 ├───────────────>│              │            │
  │                 │                │  get_all()   │            │
  │                 │                ├─────────────>│            │
  │                 │                │              │  SELECT    │
  │                 │                │              ├───────────>│
  │                 │                │              │<───────────│
  │                 │                │<─────────────│            │
  │                 │<───────────────│              │            │
  │                 │  JSON Response │              │            │
  │<────────────────│                │              │            │
```

### Diagrama de Endpoints REST

```
┌─────────────────────────────────────────────────────────┐
│                    SalesFlow API                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Ventas (CRUD)                                          │
│  ├─ GET    /api/ventas                                 │
│  ├─ GET    /api/ventas/{id}                            │
│  ├─ POST   /api/ventas                                 │
│  ├─ PUT    /api/ventas/{id}                            │
│  └─ DELETE /api/ventas/{id}                            │
│                                                         │
│  Consultas                                              │
│  └─ GET    /api/ventas/cliente/{id_cliente}            │
│                                                         │
│  Reportes (Builder)                                     │
│  └─ GET    /api/reportes/ventas?filtros...             │
│                                                         │
│  Facturas (Builder)                                     │
│  └─ GET    /api/facturas/{id_venta}                    │
│                                                         │
│  Auxiliares                                             │
│  ├─ GET    /api/clientes                               │
│  └─ GET    /api/productos                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🧪 Pruebas con Postman

### Colección de Ejemplos

1. **Obtener todas las ventas**
   - Método: GET
   - URL: `http://localhost:5000/api/ventas`

2. **Crear una venta**
   - Método: POST
   - URL: `http://localhost:5000/api/ventas`
   - Body (JSON):
   ```json
   {
     "id_cliente": 1,
     "id_producto": 1,
     "cantidad": 2
   }
   ```

3. **Generar reporte con filtros**
   - Método: GET
   - URL: `http://localhost:5000/api/reportes/ventas?id_cliente=1&fecha_inicio=2025-11-01&fecha_fin=2025-11-30`

4. **Generar factura**
   - Método: GET
   - URL: `http://localhost:5000/api/facturas/1`

## 📝 Respuestas JSON

### Respuesta Exitosa
```json
{
  "success": true,
  "data": [...],
  "message": "Operación exitosa"
}
```

### Respuesta de Error
```json
{
  "success": false,
  "error": "Mensaje de error"
}
```

### Ejemplo de Reporte
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
      "total_ventas": 5,
      "total_monto": 12500.00,
      "promedio_venta": 2500.00,
      "cantidad_items": 5
    }
  }
}
```

## 🔧 Configuración Avanzada

### Variables de Entorno
- `DB_HOST`: Host de la base de datos (default: 127.0.0.1)
- `DB_PORT`: Puerto de la base de datos (default: 3306)
- `DB_NAME`: Nombre de la base de datos (default: salesflow)
- `DB_USER`: Usuario de la base de datos (default: root)
- `DB_PASSWORD`: Contraseña de la base de datos

## 📚 Documentación Técnica

### Validaciones Implementadas
- Validación de existencia de cliente al crear venta
- Validación de existencia de producto al crear venta
- Cálculo automático del total basado en precio y cantidad
- Validación de datos requeridos en todos los endpoints

### Manejo de Errores
- Códigos HTTP apropiados (200, 201, 400, 404, 500)
- Mensajes de error descriptivos en formato JSON
- Manejo de excepciones de base de datos

## 🎓 Justificación del Patrón Builder

### Ventajas en este Proyecto

1. **Flexibilidad**: Permite construir objetos complejos (reportes, facturas) paso a paso
2. **Reutilización**: El mismo builder puede crear diferentes variaciones de reportes
3. **Mantenibilidad**: Fácil agregar nuevos filtros o características sin modificar código existente
4. **Separación de responsabilidades**: La construcción del objeto está separada de su representación
5. **Legibilidad**: El código cliente es más claro y expresivo

### Comparación con Alternativas

- **Constructor con muchos parámetros**: Difícil de mantener y usar
- **Factory Method**: No permite construcción incremental
- **Strategy**: No aplica para construcción de objetos complejos

## 👥 Autor

Desarrollado como proyecto de Arquitectura de Software - Unidad II

## 📄 Licencia

Este proyecto es de uso educativo.

