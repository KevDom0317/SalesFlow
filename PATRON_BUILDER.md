# Documentación del Patrón Builder en SalesFlow

## 📖 Introducción

El patrón Builder se implementa en SalesFlow para construir objetos complejos (reportes y facturas) de manera flexible y escalable. Este documento explica su implementación y justificación técnica.

## 🎯 Implementación

### 1. ReporteVentasBuilder

**Ubicación**: `builder.py`

**Propósito**: Construir reportes de ventas con filtros opcionales y métricas calculadas.

**Flujo de Construcción**:
```python
builder = ReporteVentasBuilder()
reporte = (builder
    .reset()
    .set_titulo("Reporte de Ventas")
    .set_tipo("reporte_ventas")
    .aplicar_filtro_cliente(1)
    .aplicar_filtro_fecha("2025-11-01", "2025-11-30")
    .calcular_metricas()
    .construir())
```

**Características**:
- Construcción paso a paso
- Filtros opcionales (cliente, producto, fechas)
- Cálculo automático de métricas
- Conversión a formato JSON

### 2. FacturaBuilder

**Ubicación**: `builder.py`

**Propósito**: Construir facturas detalladas con información completa.

**Flujo de Construcción**:
```python
builder = FacturaBuilder()
factura = (builder
    .reset()
    .set_numero_factura(1)
    .set_cliente(1)
    .agregar_item(1)
    .calcular_total()
    .construir())
```

**Características**:
- Agregación incremental de items
- Cálculo automático de totales
- Información completa del cliente
- Estructura lista para presentación

## 🔍 Justificación Técnica

### Problema que Resuelve

Sin el patrón Builder, tendríamos que:
1. Crear múltiples métodos para cada combinación de filtros
2. Usar constructores con muchos parámetros opcionales
3. Duplicar lógica de construcción en diferentes lugares

### Solución con Builder

1. **Un solo punto de construcción**: Un builder centraliza la lógica
2. **API fluida**: Métodos encadenables para mejor legibilidad
3. **Extensibilidad**: Fácil agregar nuevos filtros sin romper código existente
4. **Validación incremental**: Validar en cada paso de construcción

## 📊 Ventajas en la Arquitectura REST

### Flexibilidad en Endpoints

El endpoint `/api/reportes/ventas` puede recibir cualquier combinación de parámetros:
- Sin filtros: reporte general
- Con filtro de cliente: reporte por cliente
- Con múltiples filtros: reporte complejo

Todo esto sin necesidad de múltiples endpoints o parámetros complejos.

### Separación de Responsabilidades

- **Controller (app.py)**: Maneja HTTP y validaciones básicas
- **Builder (builder.py)**: Construye el objeto complejo
- **Models (models.py)**: Accede a los datos

## 🎨 Ejemplo de Uso en la API

### Request
```http
GET /api/reportes/ventas?id_cliente=1&fecha_inicio=2025-11-01&fecha_fin=2025-11-30
```

### Procesamiento Interno
```python
# En app.py
builder = ReporteVentasBuilder()
builder.reset()
builder.set_titulo("Reporte de Ventas")

if id_cliente:
    builder.aplicar_filtro_cliente(id_cliente)
if fecha_inicio and fecha_fin:
    builder.aplicar_filtro_fecha(fecha_inicio, fecha_fin)

reporte = builder.calcular_metricas().construir()
```

### Response
```json
{
  "success": true,
  "reporte": {
    "titulo": "Reporte de Ventas",
    "filtros_aplicados": {
      "id_cliente": 1,
      "fecha_inicio": "2025-11-01",
      "fecha_fin": "2025-11-30"
    },
    "metricas": {
      "total_ventas": 5,
      "total_monto": 12500.00
    },
    "datos": [...]
  }
}
```

## 🔄 Comparación con Alternativas

### Alternativa 1: Constructor con Parámetros Opcionales
```python
# ❌ No recomendado
reporte = Reporte(
    titulo="Reporte",
    id_cliente=1,
    id_producto=None,
    fecha_inicio="2025-11-01",
    fecha_fin="2025-11-30",
    # ... muchos más parámetros
)
```
**Problemas**: Difícil de leer, mantener y extender.

### Alternativa 2: Múltiples Métodos Estáticos
```python
# ❌ No recomendado
reporte = Reporte.por_cliente(1)
reporte = Reporte.por_cliente_y_fecha(1, "2025-11-01", "2025-11-30")
# ... muchos métodos
```
**Problemas**: Explosión combinatoria de métodos.

### Solución con Builder ✅
```python
# ✅ Recomendado
builder = ReporteVentasBuilder()
builder.reset().set_titulo("Reporte")
if id_cliente:
    builder.aplicar_filtro_cliente(id_cliente)
if fecha_inicio:
    builder.aplicar_filtro_fecha(fecha_inicio, fecha_fin)
reporte = builder.construir()
```
**Ventajas**: Flexible, legible, extensible.

## 📈 Escalabilidad

### Agregar Nuevo Filtro

Para agregar un filtro por rango de montos:

1. **Agregar método al Builder**:
```python
def aplicar_filtro_monto(self, monto_min: float, monto_max: float):
    self.reporte.filtros['monto_min'] = monto_min
    self.reporte.filtros['monto_max'] = monto_max
    return self
```

2. **Actualizar método construir()**:
```python
if 'monto_min' in self.reporte.filtros:
    ventas = [v for v in ventas 
              if monto_min <= float(v['total']) <= monto_max]
```

3. **Usar en el endpoint**:
```python
if monto_min and monto_max:
    builder.aplicar_filtro_monto(monto_min, monto_max)
```

**Sin modificar**: Código existente, otros endpoints, estructura base.

## 🎓 Conclusión

El patrón Builder en SalesFlow proporciona:
- ✅ Flexibilidad en la construcción de objetos complejos
- ✅ Código limpio y mantenible
- ✅ Fácil extensión sin romper funcionalidad existente
- ✅ Integración perfecta con arquitectura REST
- ✅ Separación clara de responsabilidades

Este patrón es especialmente adecuado para sistemas que necesitan construir objetos con múltiples variaciones y configuraciones opcionales.

