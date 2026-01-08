# Plan de Desarrollo Profesional - Instrucciones de Uso

## ✅ Correcciones Realizadas

Se han realizado los siguientes ajustes al proyecto para que funcione correctamente:

### 1. Estructura de Carpetas
- ✅ Creadas las carpetas `templates/` y `static/`
- ✅ Creadas subcarpetas `static/css/` y `static/js/`
- ✅ Movidos archivos HTML a la carpeta `templates/`

### 2. Archivos HTML Creados
- ✅ [templates/index.html](templates/index.html) - Página de inicio con redirección automática
- ✅ [templates/login.html](templates/login.html) - Página de login y registro
- ✅ [templates/dashboard.html](templates/dashboard.html) - Dashboard principal (SPA completa)
- ✅ [templates/tasks.html](templates/tasks.html) - Página de tareas (redirige al dashboard)
- ✅ [templates/monthly.html](templates/monthly.html) - Plan mensual (redirige al dashboard)
- ✅ [templates/weekly.html](templates/weekly.html) - Bitácora semanal (redirige al dashboard)

### 3. Configuración
- ✅ Creado archivo [.env](.env) con plantilla de configuración
- ✅ Mejorado manejo de errores para credenciales de Supabase no configuradas
- ✅ Instaladas todas las dependencias de [requirements.txt](requirements.txt)

### 4. Verificación
- ✅ El servidor FastAPI inicia correctamente en `http://localhost:8000`

---

## 🚀 Cómo Iniciar la Aplicación

### Paso 1: Activar el Entorno Virtual (si no está activado)

**Windows:**
```bash
Scripts\activate
```

**Mac/Linux:**
```bash
source bin/activate
```

### Paso 2: Iniciar el Servidor

```bash
python main.py
```

El servidor se iniciará en: **http://localhost:8000**

---

## ⚙️ Configuración de Supabase (Importante)

Actualmente el archivo [.env](.env) tiene credenciales de ejemplo. Para que la aplicación funcione completamente, necesitas configurar Supabase:

### 1. Crear Proyecto en Supabase

1. Ve a [https://supabase.com](https://supabase.com)
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto
4. Espera a que el proyecto se inicialice (2-3 minutos)

### 2. Obtener Credenciales

1. Ve a **Settings** > **API**
2. Copia los siguientes valores:
   - **Project URL** (ejemplo: `https://tuproyecto.supabase.co`)
   - **anon/public key** (clave pública)
   - **service_role key** (clave de servicio, mantener secreta)

### 3. Actualizar el Archivo .env

Abre el archivo [.env](.env) y reemplaza:

```env
SUPABASE_URL=https://tuproyecto.supabase.co
SUPABASE_KEY=tu-anon-key-aqui
SUPABASE_SERVICE_KEY=tu-service-role-key-aqui
```

Con tus credenciales reales.

### 4. Configurar la Base de Datos

1. En Supabase, ve a **SQL Editor**
2. Abre el archivo [database_setup.sql](database_setup.sql) de este proyecto
3. Copia todo el contenido y pégalo en el SQL Editor
4. Haz clic en **RUN** para ejecutar el script
5. Verifica que se crearon las tablas: `user_profiles`, `monthly_plans`, `weekly_logs`, `daily_tasks`, `evidencias`, etc.

### 5. Crear Bucket de Storage (para evidencias)

1. En Supabase, ve a **Storage**
2. Crea un nuevo bucket llamado `evidencias`
3. Configúralo como **público** (para que las imágenes sean accesibles)

---

## 🌐 Acceder a la Aplicación

Una vez iniciado el servidor, abre tu navegador en:

- **Página Principal:** http://localhost:8000
- **Login:** http://localhost:8000/login
- **Dashboard:** http://localhost:8000/dashboard

**Nota:** La primera vez te redirigirá automáticamente a `/login`

---

## 📂 Estructura del Proyecto

```
Plan_Desarrollo_Profesional/
├── templates/              # Plantillas HTML
│   ├── index.html         # Página de inicio
│   ├── login.html         # Login y registro
│   ├── dashboard.html     # Dashboard principal (SPA)
│   ├── tasks.html         # Gestión de tareas
│   ├── monthly.html       # Planes mensuales
│   └── weekly.html        # Bitácoras semanales
├── static/                # Archivos estáticos
│   ├── css/              # Estilos personalizados
│   └── js/               # JavaScript personalizado
├── uploads/              # Evidencias subidas (local)
├── main.py               # Aplicación FastAPI
├── requirements.txt      # Dependencias Python
├── .env                  # Variables de entorno
├── .env.example          # Ejemplo de variables
├── database_setup.sql    # Script SQL para Supabase
└── README.md             # Documentación completa
```

---

## 🔧 Solución de Problemas

### Error: "Unresolved import" en VSCode

Estos son errores del IDE. Para solucionarlos:

1. Presiona `Ctrl + Shift + P` (Windows) o `Cmd + Shift + P` (Mac)
2. Busca: **Python: Select Interpreter**
3. Selecciona el intérprete que está en la carpeta del proyecto (el que tiene `Scripts` o `bin`)

### Error: "Module not found"

Si aparece este error al iniciar el servidor:

```bash
pip install -r requirements.txt
```

### El servidor no inicia

Verifica que el puerto 8000 no esté en uso:

**Windows:**
```bash
netstat -ano | findstr :8000
```

**Mac/Linux:**
```bash
lsof -i :8000
```

Si está en uso, cierra el proceso o cambia el puerto en [main.py](main.py:668) (última línea).

### Las páginas no se ven correctamente

- Verifica que las carpetas `templates/` y `static/` existan
- Verifica que todos los archivos HTML estén en `templates/`
- Limpia la caché del navegador: `Ctrl + Shift + R` (Windows) o `Cmd + Shift + R` (Mac)

---

## 📝 Funcionalidades de la Aplicación

### 1. Sistema de Autenticación
- Registro de usuarios
- Login con email y contraseña
- JWT tokens para sesiones seguras
- Logout

### 2. Dashboard
- Resumen de tareas del mes
- Gráficos de progreso
- Estadísticas de completitud
- Vista rápida del plan mensual

### 3. Gestión de Tareas Diarias
- Crear, editar y eliminar tareas
- Categorías: personal, trabajo, estudio, etc.
- Estados: pendiente, en progreso, completada
- Prioridades: baja, media, alta
- Adjuntar evidencias (imágenes, PDFs, documentos)

### 4. Plan Mensual
- Definir competencias a desarrollar
- Establecer objetivos del mes
- Identificar fortalezas y debilidades
- Plan de mejoras
- Evaluación al final del mes

### 5. Bitácora Semanal
- Registrar logros de la semana
- Documentar desafíos enfrentados
- Reflexiones y aprendizajes
- Niveles de energía y satisfacción

### 6. Gestión de Evidencias
- Subir imágenes (JPG, PNG, GIF)
- Subir documentos (PDF, Word)
- Asociar evidencias a tareas específicas
- Almacenamiento en Supabase Storage

---

## 🔐 Seguridad

- ✅ Autenticación JWT con tokens que expiran en 24 horas
- ✅ Contraseñas hasheadas con bcrypt
- ✅ CORS configurado para dominios autorizados
- ✅ Validación de tamaño y tipo de archivos subidos (máx 10MB)
- ✅ Autenticación requerida en todas las rutas protegidas

---

## 📊 API Endpoints

La aplicación expone los siguientes endpoints REST:

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Tareas
- `POST /api/tasks` - Crear tarea
- `GET /api/tasks` - Listar tareas (con filtros)
- `GET /api/tasks/{id}` - Obtener tarea específica
- `PUT /api/tasks/{id}` - Actualizar tarea
- `DELETE /api/tasks/{id}` - Eliminar tarea

### Planes Mensuales
- `POST /api/monthly/plans` - Crear plan mensual
- `GET /api/monthly/plans` - Listar planes mensuales
- `GET /api/monthly/plans/{id}` - Obtener plan específico
- `PUT /api/monthly/plans/{id}` - Actualizar plan

### Bitácoras Semanales
- `POST /api/weekly/logs` - Crear bitácora semanal
- `GET /api/weekly/logs` - Listar bitácoras
- `GET /api/weekly/logs/{id}` - Obtener bitácora específica

### Evidencias
- `POST /api/evidencias/upload` - Subir archivo
- `GET /api/evidencias` - Listar evidencias
- `DELETE /api/evidencias/{id}` - Eliminar evidencia

### Dashboard
- `GET /api/dashboard/summary` - Resumen del dashboard
- `GET /api/dashboard/tasks-by-day` - Tareas por día

---

## 🎨 Personalización

### Cambiar el Puerto

Edita [main.py](main.py) línea 668:

```python
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

Cambia `port=8000` por el puerto deseado.

### Cambiar Tamaño Máximo de Archivos

Edita [.env](.env):

```env
MAX_FILE_SIZE_MB=10
```

Cambia el valor a tu preferencia.

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la sección de **Solución de Problemas** arriba
2. Verifica que la configuración de Supabase sea correcta
3. Revisa los logs del servidor en la consola
4. Verifica la consola del navegador (F12) para errores de JavaScript

---

## ✨ Próximos Pasos

1. **Configurar Supabase** (si aún no lo has hecho)
2. **Crear tu primer usuario** en `/login`
3. **Explorar el dashboard** y familiarizarte con la interfaz
4. **Crear tu primer plan mensual** para este mes
5. **Agregar tareas diarias** y comenzar a trackear tu progreso

---

## 🎉 ¡Listo para Usar!

Tu aplicación está configurada y lista para funcionar. Una vez que configures Supabase, tendrás acceso completo a todas las funcionalidades.

**¡Mucho éxito en tu desarrollo profesional! 🚀**
