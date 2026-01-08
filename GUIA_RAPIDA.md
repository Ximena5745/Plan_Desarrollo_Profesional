# 🚀 GUÍA RÁPIDA DE INSTALACIÓN

## ⚡ Instalación en 5 Minutos

### 1. Instalar Python (si no lo tienes)
Descarga Python 3.10+ de [python.org](https://python.org)

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Supabase
1. Crea cuenta gratis en [supabase.com](https://supabase.com)
2. Crea nuevo proyecto
3. Ve a SQL Editor y pega TODO el contenido de `database_setup.sql`
4. Ejecuta el script
5. Ve a Storage → Create bucket → nombre: `evidencias` → público

### 4. Configurar variables
```bash
# Copia .env.example a .env
cp .env.example .env

# Edita .env con tus credenciales de Supabase
# (las encuentras en Settings → API)
```

### 5. Ejecutar aplicación
```bash
python main.py
```

Abre: http://localhost:8000

## 📦 Estructura de Archivos

```
plan-desarrollo-api/
├── main.py                    ← Backend FastAPI completo
├── requirements.txt           ← Dependencias Python
├── .env.example              ← Plantilla de configuración
├── database_setup.sql        ← Script SQL para Supabase
├── README.md                 ← Documentación completa
├── GUIA_RAPIDA.md           ← Este archivo
└── templates/               ← Archivos HTML (crear carpeta)
    ├── base.html            ← Template base
    ├── index.html           ← Página inicial
    ├── login.html           ← Login
    ├── dashboard.html       ← Dashboard principal
    ├── tasks.html           ← Gestión de tareas
    ├── monthly.html         ← Planes mensuales
    └── weekly.html          ← Bitácoras semanales
```

## 🎨 Próximos Pasos

Los archivos HTML con la interfaz moderna se encuentran separados.
Crea una carpeta `templates/` y coloca allí los archivos HTML.

Los archivos CSS/JS van en carpeta `static/`:
```
static/
├── css/
│   └── custom.css
└── js/
    ├── app.js
    ├── kanban.js
    └── charts.js
```

## ⚠️ Solución de Problemas Comunes

**Error: ModuleNotFoundError**
→ `pip install -r requirements.txt`

**Error: Connection refused**
→ Verifica las credenciales de Supabase en .env

**Error: 404 en templates**
→ Crea la carpeta `templates/` en el mismo nivel que main.py

**Error al subir archivos**
→ Verifica que el bucket `evidencias` exista en Supabase Storage

## 📞 Necesitas Ayuda?

1. Revisa README.md para documentación completa
2. Verifica que todos los archivos estén en su lugar
3. Asegúrate de ejecutar el script SQL en Supabase

¡Listo para usar! 🎉
