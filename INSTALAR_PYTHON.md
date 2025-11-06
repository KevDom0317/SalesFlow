# 🐍 Cómo Instalar Python para SalesFlow

## Problema Detectado

Python no está instalado o no está en el PATH del sistema. Necesitas instalarlo para ejecutar el proyecto.

## Solución: Instalar Python

### Opción 1: Instalador Oficial (Recomendado)

1. **Descargar Python**
   - Ve a: https://www.python.org/downloads/
   - Descarga la versión más reciente de Python 3.x (3.8 o superior)
   - O descarga directo: https://www.python.org/downloads/windows/

2. **Instalar Python**
   - Ejecuta el instalador descargado
   - **IMPORTANTE**: ✅ Marca la casilla **"Add Python to PATH"** o **"Add Python 3.x to PATH"**
   - Haz clic en "Install Now"
   - Espera a que termine la instalación

3. **Verificar Instalación**
   - Abre PowerShell o CMD
   - Ejecuta: `python --version`
   - Deberías ver algo como: `Python 3.11.x`

4. **Ejecutar el Proyecto**
   - Vuelve a ejecutar `iniciar.bat`
   - O ejecuta manualmente:
     ```bash
     pip install -r requirements.txt
     python app.py
     ```

### Opción 2: Microsoft Store (Alternativa)

1. Abre Microsoft Store
2. Busca "Python"
3. Instala "Python 3.11" o superior
4. Se agregará automáticamente al PATH

### Opción 3: Si Python ya está Instalado

Si Python ya está instalado pero no funciona, necesita agregarse al PATH:

1. **Encontrar dónde está Python**
   - Busca en: `C:\Users\TuUsuario\AppData\Local\Programs\Python\`
   - O en: `C:\Python3x\`

2. **Agregar al PATH**
   - Presiona `Win + X` y selecciona "Sistema"
   - Haz clic en "Configuración avanzada del sistema"
   - Haz clic en "Variables de entorno"
   - En "Variables del sistema", busca "Path" y haz clic en "Editar"
   - Haz clic en "Nuevo" y agrega la ruta donde está Python (ej: `C:\Python311\`)
   - También agrega la carpeta Scripts (ej: `C:\Python311\Scripts\`)
   - Haz clic en "Aceptar" en todas las ventanas
   - **Reinicia PowerShell/CMD** para que los cambios surtan efecto

3. **Verificar**
   ```bash
   python --version
   ```

## Ejecutar el Proyecto Manualmente

Si prefieres no usar el script `.bat`, puedes ejecutar manualmente:

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python app.py
```

## Verificar que Todo Funciona

Después de instalar Python:

1. Abre PowerShell en la carpeta del proyecto
2. Ejecuta: `python --version` (debe mostrar la versión)
3. Ejecuta: `pip --version` (debe mostrar la versión de pip)
4. Ejecuta: `python app.py`
5. Abre el navegador en: http://localhost:5000

## Solución de Problemas

### Error: "pip no se reconoce"
**Solución**: Python se instaló sin pip. Reinstala Python marcando todas las opciones.

### Error: "python no se reconoce"
**Solución**: Python no está en el PATH. Reinstala Python marcando "Add to PATH" o agrégalo manualmente como se explica arriba.

### Error: "La ejecución de scripts está deshabilitada"
**Solución**: Ejecuta PowerShell como Administrador y ejecuta:
```powershell
Set-ExecutionPolicy RemoteSigned
```

## ¿Necesitas Más Ayuda?

- Documentación oficial de Python: https://docs.python.org/3/
- Guía de instalación: https://realpython.com/installing-python/

