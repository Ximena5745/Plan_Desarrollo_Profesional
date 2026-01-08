# 🚀 Plan de Desarrollo Profesional - Aplicación Web

## 📋 Descripción
Aplicación web completa para gestionar tu plan de desarrollo profesional con:
- ✅ Planes mensuales (inicio y fin de mes)
- ✅ Bitácoras semanales
- ✅ Tareas diarias (vista lista y Kanban)
- ✅ Carga de evidencias (imágenes, PDFs, documentos)
- ✅ Dashboard con métricas y gráficos
- ✅ Exportar reportes a Excel
- ✅ Sistema multiusuario (10-15 usuarios)

## 🎨 Características de la Interfaz
- **Diseño moderno** con Tailwind CSS + DaisyUI
- **Tema oscuro/claro** automático
- **Responsive** (móvil, tablet, desktop)
- **Drag & Drop** para Kanban
- **Notificaciones** visuales
- **Animaciones suaves**

## 🛠️ Stack Tecnológico
- **Backend**: FastAPI (Python)
- **Frontend**: HTML5 + Tailwind CSS + Alpine.js
- **Base de Datos**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage (evidencias)
- **Gráficos**: Chart.js
- **Hosting**: Render.com (backend) + Netlify (frontend)

## 📦 Instalación Rápida

### 1. Requisitos Previos
```bash
# Python 3.10 o superior
python --version

# pip actualizado
pip install --upgrade pip
```

### 2. Clonar y Configurar

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Supabase

1. Ve a [supabase.com](https://supabase.com) y crea cuenta gratis
2. Crea un nuevo proyecto
3. Ve a Settings > API y copia:
   - Project URL
   - anon/public key
   - service_role key (solo backend)

4. Ve a SQL Editor y ejecuta el script `database_setup.sql`

5. Ve a Storage y crea un bucket llamado `evidencias` con acceso público

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales de Supabase
nano .env
```

### 5. Ejecutar Aplicación

```bash
# Desarrollo (con recarga automática)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Abre tu navegador en: `http://localhost:8000`

## 📁 Estructura del Proyecto

```
plan-desarrollo-api/
├── app/
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── config.py               # Configuración y variables
│   ├── database.py             # Conexión Supabase
│   ├── models.py               # Modelos Pydantic
│   ├── auth.py                 # Autenticación JWT
│   ├── routers/
│   │   ├── tasks.py           # Rutas de tareas
│   │   ├── monthly.py         # Planes mensuales
│   │   ├── weekly.py          # Bitácoras semanales
│   │   ├── files.py           # Upload evidencias
│   │   └── dashboard.py       # Métricas y reportes
│   └── templates/
│       ├── index.html         # Página principal
│       ├── login.html         # Login
│       ├── dashboard.html     # Dashboard
│       ├── tasks.html         # Gestión de tareas
│       ├── monthly.html       # Planes mensuales
│       └── weekly.html        # Bitácoras semanales
├── static/
│   ├── css/
│   │   └── custom.css         # Estilos personalizados
│   └── js/
│       ├── app.js             # JavaScript principal
│       ├── kanban.js          # Funcionalidad Kanban
│       └── charts.js          # Gráficos y métricas
├── uploads/                    # Evidencias temporales
├── database_setup.sql          # Script SQL para Supabase
├── requirements.txt            # Dependencias Python
├── .env.example               # Ejemplo de variables
└── README.md                  # Este archivo
```

## 🚀 Despliegue en Producción

### Opción 1: Render.com (Backend) + Netlify (Frontend)

**Backend en Render:**
1. Crea cuenta en [render.com](https://render.com)
2. New Web Service > Connect tu repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Agrega variables de entorno desde .env

**Frontend estático en Netlify:**
1. Sube carpeta `static/` y `templates/` a Netlify
2. Configura CORS en FastAPI para permitir dominio de Netlify

### Opción 2: Railway.app (Todo en uno)
1. Crea cuenta en [railway.app](https://railway.app)
2. New Project > Deploy from GitHub
3. Agrega variables de entorno
4. Railway detecta FastAPI automáticamente

### Opción 3: PythonAnywhere (Gratis)
1. Crea cuenta free en [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sube archivos vía FTP o Git
3. Configura WSGI para FastAPI
4. Límite: 512MB RAM, suficiente para 10-15 usuarios

## 📊 Uso de la Aplicación

### 1. Registro e Inicio de Sesión
- Primera vez: Registra tu cuenta
- Usuarios adicionales: El admin puede crear cuentas

### 2. Dashboard Principal
- Vista general de progreso
- Tareas pendientes/completadas
- Gráficos de evolución
- Métricas mensuales

### 3. Plan Mensual
- **Inicio de mes**: Define competencias, objetivos, fortalezas
- **Fin de mes**: Evalúa logros, habilidades desarrolladas

### 4. Bitácora Semanal
- Registra logros de la semana
- Documenta desafíos
- Reflexiones y aprendizajes

### 5. Tareas Diarias
- **Vista Lista**: Todas las tareas ordenadas
- **Vista Kanban**: Arrastra entre Pendiente → En Progreso → Completada
- **Carga evidencias**: Adjunta imágenes, PDFs, documentos

### 6. Reportes
- Exporta a Excel tus planes mensuales
- Descarga evidencias en ZIP
- Integración con Power BI (API REST)

## 🔧 Personalización

### Cambiar Colores del Tema
Edita `static/css/custom.css`:
```css
:root {
  --primary: #6366f1;    /* Color principal */
  --secondary: #8b5cf6;  /* Color secundario */
  --accent: #ec4899;     /* Color de acento */
}
```

### Agregar Más Competencias
Edita `app/config.py` en la lista `COMPETENCIAS_DEFAULT`

### Modificar Categorías de Tareas
Edita `app/models.py` en el enum `TaskCategory`

## 🔐 Seguridad

- Autenticación JWT con tokens de 30 minutos
- Contraseñas hasheadas con bcrypt
- CORS configurado solo para dominios autorizados
- Rate limiting en rutas sensibles
- Validación de archivos subidos (tipo y tamaño)

## 📈 Integración con Power BI

La aplicación expone API REST para conectar con Power BI:

```
GET /api/tasks/all          # Todas las tareas
GET /api/monthly/all        # Planes mensuales
GET /api/weekly/all         # Bitácoras semanales
GET /api/metrics/summary    # Métricas agregadas
```

**En Power BI:**
1. Obtener datos > Web
2. URL: `http://tu-dominio/api/tasks/all`
3. Agregar header: `Authorization: Bearer TU_TOKEN`

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Supabase connection failed"
- Verifica que SUPABASE_URL y SUPABASE_KEY estén correctos en .env
- Verifica que el proyecto Supabase esté activo

### Error: "File upload failed"
- Verifica que el bucket 'evidencias' exista en Supabase Storage
- Verifica permisos del bucket (debe ser público para lectura)

### Las tareas no se guardan
- Ejecuta el script `database_setup.sql` en Supabase
- Verifica que las tablas se hayan creado correctamente

## 📞 Soporte

Para problemas o mejoras, crea un issue en el repositorio.

## 📄 Licencia

MIT License - Libre para uso personal y comercial.

---

**¡Listo para usar! 🎉**

Cualquier duda, revisa la documentación o contacta al equipo de desarrollo.
