# 🔧 Configurar Conexión a la Base de Datos

## 📌 Importante: Cómo Funciona la Conexión

La aplicación **NO se conecta a phpMyAdmin**. Se conecta **directamente a MySQL/MariaDB**.

- **phpMyAdmin**: Es solo una herramienta web para ver y gestionar la base de datos
- **MySQL/MariaDB**: Es el servidor de base de datos real (corre en el puerto 3306)
- **La aplicación Python**: Se conecta directamente a MySQL usando el puerto 3306

## ✅ Verificar que la Base de Datos Existe

Si puedes ver `salesflow` en phpMyAdmin (http://localhost/phpmyadmin), significa que:
- ✅ MySQL está corriendo
- ✅ La base de datos `salesflow` existe
- ✅ Solo necesitas configurar las credenciales

## 🔐 Configurar Credenciales

### Paso 1: Identificar tus Credenciales de MySQL

En phpMyAdmin, las credenciales que usas son:
- **Usuario**: Generalmente `root`
- **Contraseña**: La que configuraste cuando instalaste MySQL/XAMPP/WAMP

### Paso 2: Editar el archivo .env

Abre el archivo `.env` en la raíz del proyecto y configura:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=salesflow
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
```

**Si usas XAMPP o WAMP sin contraseña**, deja `DB_PASSWORD=` vacío.

### Paso 3: Verificar las Tablas

En phpMyAdmin, verifica que la base de datos `salesflow` tenga estas tablas:
- `clientes`
- `productos`
- `ventas`

Si no las tienes, importa el archivo `salesflow.sql` desde phpMyAdmin.

## 🧪 Probar la Conexión

### Opción 1: Ejecutar la Aplicación

```bash
python app.py
```

Si ves este mensaje, la conexión es exitosa:
```
Conexión a la base de datos establecida exitosamente
 * Running on http://127.0.0.1:5000
```

### Opción 2: Probar desde Python

Crea un archivo `test_db.py`:

```python
from database import Database

try:
    db = Database()
    conn = db.get_connection()
    print("✅ Conexión exitosa!")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"Tablas encontradas: {tables}")
    cursor.close()
except Exception as e:
    print(f"❌ Error: {e}")
```

Ejecuta: `python test_db.py`

## 🔍 Solución de Problemas

### Error: "Access denied for user 'root'@'localhost'"

**Solución**: 
1. Verifica la contraseña en el archivo `.env`
2. Si usas XAMPP, la contraseña por defecto puede estar vacía
3. Prueba con diferentes credenciales

### Error: "Unknown database 'salesflow'"

**Solución**:
1. Crea la base de datos desde phpMyAdmin o desde MySQL:
   ```sql
   CREATE DATABASE salesflow;
   ```
2. Importa el archivo `salesflow.sql` desde phpMyAdmin

### Error: "Can't connect to MySQL server"

**Solución**:
1. Verifica que MySQL esté corriendo
2. En XAMPP/WAMP: Inicia el servicio MySQL desde el panel de control
3. Verifica el puerto 3306 (puede ser diferente en algunos sistemas)

### Error: "Table doesn't exist"

**Solución**:
1. Importa el archivo SQL desde phpMyAdmin:
   - Ve a phpMyAdmin
   - Selecciona la base de datos `salesflow`
   - Haz clic en "Importar"
   - Selecciona el archivo `salesflow.sql`
   - Haz clic en "Continuar"

## 📝 Configuración por Defecto

Si no tienes archivo `.env`, la aplicación usará estos valores por defecto:

```python
host='127.0.0.1'
port='3306'
database='salesflow'
user='root'
password=''  # Sin contraseña
```

## 🎯 Resumen

1. **phpMyAdmin** = Herramienta web para ver la base de datos
2. **MySQL** = Servidor de base de datos (puerto 3306)
3. **La aplicación** = Se conecta directamente a MySQL
4. **Archivo .env** = Configura las credenciales de conexión

Si puedes ver la base de datos en phpMyAdmin, solo necesitas configurar las credenciales correctas en el archivo `.env`.

