# 🚀 Guía para Ejecutar el Proyecto SalesFlow

## Paso 1: Verificar Prerequisitos

### 1.1 Python instalado
Abre PowerShell o CMD y verifica:
```bash
python --version
```
Debe ser Python 3.8 o superior.

### 1.2 MySQL/MariaDB instalado y ejecutándose
- Verifica que MySQL esté corriendo en tu sistema
- Debe estar en el puerto 3306 (por defecto)

## Paso 2: Configurar la Base de Datos

### 2.1 Crear la base de datos
```bash
mysql -u root -p
```

Dentro de MySQL:
```sql
CREATE DATABASE salesflow;
EXIT;
```

### 2.2 Importar el esquema
```bash
mysql -u root -p salesflow < C:\Users\Kevin\Downloads\salesflow.sql
```

**O usando phpMyAdmin:**
1. Abre phpMyAdmin en tu navegador
2. Selecciona "Importar"
3. Elige el archivo `salesflow.sql` desde `C:\Users\Kevin\Downloads\`
4. Haz clic en "Continuar"

## Paso 3: Configurar Variables de Entorno

### 3.1 Editar el archivo .env
El archivo `.env` ya está creado en el proyecto. Ábrelo y ajusta según tu configuración:

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=salesflow
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
```

**Si no tienes contraseña en MySQL**, deja `DB_PASSWORD=` vacío.

## Paso 4: Instalar Dependencias

Abre PowerShell en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Si tienes problemas, prueba:
```bash
python -m pip install -r requirements.txt
```

## Paso 5: Ejecutar la Aplicación

En la misma terminal, ejecuta:

```bash
python app.py
```

Deberías ver algo como:
```
Conexión a la base de datos establecida exitosamente
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## Paso 6: Abrir en el Navegador

1. Abre tu navegador web (Chrome, Firefox, Edge, etc.)
2. Ve a: **http://localhost:5000**
3. ¡Listo! Deberías ver la interfaz de SalesFlow

## 📱 Páginas Disponibles

- **Inicio**: http://localhost:5000
- **Ventas**: http://localhost:5000/ventas
- **Reportes**: http://localhost:5000/reportes

## 🔧 Solución de Problemas

### Error: "No module named 'flask'"
**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL server"
**Solución**: 
1. Verifica que MySQL esté ejecutándose
2. Revisa las credenciales en el archivo `.env`
3. Verifica que la base de datos `salesflow` exista

### Error: "Access denied for user"
**Solución**: 
1. Verifica el usuario y contraseña en `.env`
2. Asegúrate de que el usuario tenga permisos en la base de datos

### Error: "Table doesn't exist"
**Solución**: Importa el archivo SQL:
```bash
mysql -u root -p salesflow < C:\Users\Kevin\Downloads\salesflow.sql
```

### Puerto 5000 ya en uso
**Solución**: 
1. Cierra la aplicación que usa el puerto 5000
2. O modifica el puerto en `app.py` línea final:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia 5000 por 5001
```

## 🧪 Probar la API

### Con el navegador:
- Ve a: http://localhost:5000/api/ventas
- Deberías ver un JSON con las ventas

### Con PowerShell (curl):
```powershell
curl http://localhost:5000/api/ventas
```

### Con Postman:
- Importa la colección desde `POSTMAN_COLLECTION.md`
- O crea un request GET a: http://localhost:5000/api/ventas

## ✅ Verificar que Todo Funciona

1. **Interfaz Web**: http://localhost:5000 - Debe mostrar la página principal
2. **API Ventas**: http://localhost:5000/api/ventas - Debe retornar JSON
3. **API Clientes**: http://localhost:5000/api/clientes - Debe retornar JSON
4. **API Productos**: http://localhost:5000/api/productos - Debe retornar JSON

## 🎯 Próximos Pasos

Una vez que el proyecto esté ejecutándose:
1. Explora la interfaz web en http://localhost:5000
2. Prueba crear una venta desde la página de Ventas
3. Genera un reporte desde la página de Reportes
4. Prueba los endpoints de la API con Postman

## 📞 Si Necesitas Ayuda

Revisa los archivos de documentación:
- `README.md` - Documentación completa
- `INSTRUCCIONES.md` - Instrucciones rápidas
- `POSTMAN_COLLECTION.md` - Ejemplos de API

