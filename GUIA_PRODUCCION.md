# Guía Paso a Paso: Despliegue a Producción

Esta guía te llevará desde tu desarrollo local hasta tener la aplicación corriendo en producción.

---

## 📋 Tabla de Contenidos
1. [Preparación del Código](#1-preparación-del-código)
2. [Configuración de Variables de Entorno](#2-configuración-de-variables-de-entorno)
3. [Opciones de Hosting](#3-opciones-de-hosting)
4. [Despliegue en Railway (Recomendado)](#4-despliegue-en-railway-recomendado)
5. [Despliegue en Render](#5-despliegue-en-render-alternativa)
6. [Configuración de Supabase](#6-configuración-de-supabase)
7. [Verificación Post-Despliegue](#7-verificación-post-despliegue)
8. [Seguridad y Mejores Prácticas](#8-seguridad-y-mejores-prácticas)

---

## 1. Preparación del Código

### 1.1 Crear archivo requirements.txt
```bash
pip freeze > requirements.txt
```

Verifica que contenga (mínimo):
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
supabase==2.3.0
pydantic==2.5.2
```

### 1.2 Crear archivo runtime.txt (opcional)
```txt
python-3.11.7
```

### 1.3 Crear Procfile para el servidor
Crea un archivo llamado `Procfile` (sin extensión):
```
web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### 1.4 Actualizar main.py para producción
Agrega esta configuración al inicio de `main.py`:

```python
import os

# Configuración de producción
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",")

app = FastAPI(
    title="Plan de Desarrollo Profesional",
    docs_url=None if IS_PRODUCTION else "/docs",  # Desactivar docs en producción
    redoc_url=None if IS_PRODUCTION else "/redoc"
)

# CORS actualizado
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 1.5 Crear archivo .gitignore
```txt
__pycache__/
*.py[cod]
*$py.class
.env
.env.local
venv/
ENV/
.DS_Store
*.log
.claude/
```

### 1.6 Verificar estructura del proyecto
```
Plan_Desarrollo_Profesional/
├── main.py
├── templates/
│   ├── dashboard.html
│   └── login.html
├── requirements.txt
├── Procfile
├── runtime.txt (opcional)
├── .gitignore
└── README.md
```

---

## 2. Configuración de Variables de Entorno

### 2.1 Variables requeridas
Necesitarás configurar estas variables en tu servicio de hosting:

```env
# Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_anon_key_aqui
SUPABASE_SERVICE_KEY=tu_service_role_key_aqui

# JWT
SECRET_KEY=genera_una_clave_secreta_super_segura_aqui
ALGORITHM=HS256

# Entorno
ENVIRONMENT=production
ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### 2.2 Generar SECRET_KEY seguro
Ejecuta en Python:
```python
import secrets
print(secrets.token_urlsafe(32))
```
Usa la salida como tu `SECRET_KEY`.

---

## 3. Opciones de Hosting 100% GRATIS

### Comparación de Plataformas Gratuitas

| Plataforma | Limitaciones | Facilidad | Recomendación |
|------------|-------------|-----------|---------------|
| **Render (Free)** | Se duerme después de 15 min de inactividad, 750 hrs/mes | ⭐⭐⭐⭐⭐ | **MEJOR OPCIÓN** |
| **Fly.io (Free)** | 3 VMs compartidas, 160GB tráfico/mes | ⭐⭐⭐⭐ | Muy buena alternativa |
| **PythonAnywhere (Free)** | 100MB almacenamiento, solo HTTP (no HTTPS) | ⭐⭐⭐ | Buena opción |
| **Railway (Free)** | $5 crédito gratis/mes (~500 hrs), luego requiere pago | ⭐⭐⭐⭐⭐ | Solo 1 mes gratis |
| **Koyeb (Free)** | Se duerme, limitado a 1 app | ⭐⭐⭐⭐ | Alternativa viable |

**Recomendación:** Render Free Tier (fácil + confiable + SSL gratis)

### 🎯 Mejor Opción: Render Free Tier

**Ventajas:**
- ✅ Completamente gratis para siempre
- ✅ SSL/HTTPS automático
- ✅ Deploy automático desde GitHub
- ✅ Fácil de configurar
- ✅ No requiere tarjeta de crédito

**Limitaciones:**
- ⏸️ La app se "duerme" después de 15 minutos de inactividad
- 🐌 Tarda 30-60 segundos en "despertar" al primer acceso
- 📊 750 horas gratis por mes (suficiente para uso personal/educativo)

**Ideal para:** Proyectos educativos, portfolios, demos, uso personal

---

## 4. Despliegue en Render (100% GRATIS - Recomendado)

### Paso 1: Preparar repositorio Git
```bash
# Inicializar Git (si no lo has hecho)
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Preparar para producción"
```

### Paso 2: Subir a GitHub
1. Crear repositorio en GitHub (público o privado, no importa)
2. Conectar y hacer push:
```bash
git remote add origin https://github.com/tu-usuario/tu-repo.git
git branch -M main
git push -u origin main
```

### Paso 3: Crear cuenta en Render (GRATIS)
1. Ve a [render.com](https://render.com)
2. Clic en "Get Started for Free"
3. Registrarte con tu cuenta de GitHub (recomendado)
4. **NO se requiere tarjeta de crédito** ✅

### Paso 4: Crear Web Service
1. Clic en "New +" (botón azul arriba a la derecha)
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub:
   - Si es la primera vez, autoriza Render a acceder a GitHub
   - Busca y selecciona tu repositorio

### Paso 5: Configurar el Servicio
Completa el formulario con estos valores:

**Información básica:**
- **Name**: `plan-desarrollo-profesional` (o el nombre que prefieras)
- **Region**: Selecciona el más cercano (ej: Oregon, Frankfurt)
- **Branch**: `main`
- **Runtime**: Python 3

**Build & Deploy:**
- **Build Command**:
  ```
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Plan:**
- ⚡ Selecciona **"Free"** (¡importante!)

### Paso 6: Configurar Variables de Entorno
Antes de hacer clic en "Create Web Service":

1. Baja hasta la sección **"Environment Variables"**
2. Clic en "Add Environment Variable"
3. Agrega cada una de estas variables:

```
SUPABASE_URL=https://xxxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc...
SECRET_KEY=tu_secret_key_generado
ALGORITHM=HS256
ENVIRONMENT=production
ALLOWED_ORIGINS=https://tu-app.onrender.com
```

**⚠️ Importante:** Reemplaza `tu-app` en `ALLOWED_ORIGINS` con el nombre que elegiste en el paso 5.

### Paso 7: Desplegar
1. Clic en **"Create Web Service"** (botón azul al final)
2. Render comenzará a construir tu aplicación
3. Espera 3-5 minutos mientras:
   - ⬇️ Descarga tu código
   - 📦 Instala dependencias
   - 🚀 Inicia el servidor

### Paso 8: Verificar Despliegue
1. Una vez que veas **"Live"** con un punto verde ✅
2. Clic en la URL (algo como `https://plan-desarrollo-profesional.onrender.com`)
3. Deberías ver tu aplicación de login

### Paso 9: Actualizar ALLOWED_ORIGINS (si es necesario)
Si la URL final es diferente a la que pusiste:
1. Ve a "Environment" en el menú izquierdo
2. Edita `ALLOWED_ORIGINS` con la URL correcta
3. Guarda los cambios (Render redesplegará automáticamente)

---

## 5. Alternativas 100% Gratuitas

### Opción A: Fly.io (Siempre Activo - Muy Bueno)

**Ventajas:**
- ✅ NO se duerme (siempre activo 24/7)
- ✅ 3 VMs compartidas gratis
- ✅ 160GB de tráfico/mes
- ✅ SSL gratis

**Limitaciones:**
- 🔧 Configuración un poco más técnica
- 💳 Requiere tarjeta de crédito (pero NO cobra)

**Pasos rápidos:**
```bash
# 1. Instalar Fly CLI
# Windows (PowerShell):
iwr https://fly.io/install.ps1 -useb | iex

# 2. Login
fly auth login

# 3. Lanzar la app
fly launch

# 4. Configurar variables de entorno
fly secrets set SUPABASE_URL="https://xxx.supabase.co"
fly secrets set SUPABASE_KEY="eyJhbGc..."
fly secrets set SUPABASE_SERVICE_KEY="eyJhbGc..."
fly secrets set SECRET_KEY="tu_secret_key"
fly secrets set ENVIRONMENT="production"
fly secrets set ALLOWED_ORIGINS="https://tu-app.fly.dev"

# 5. Desplegar
fly deploy
```

**Guía completa:** [https://fly.io/docs/languages-and-frameworks/python/](https://fly.io/docs/languages-and-frameworks/python/)

---

### Opción B: PythonAnywhere (Siempre Activo - Básico)

**Ventajas:**
- ✅ NO se duerme (siempre activo 24/7)
- ✅ Super fácil de configurar
- ✅ No requiere tarjeta de crédito

**Limitaciones:**
- ❌ Solo HTTP (no HTTPS en plan gratis)
- 💾 100MB de almacenamiento
- 🐌 CPU limitado
- 🌐 Dominio: `username.pythonanywhere.com`

**NO recomendado** para esta app por la falta de HTTPS (Supabase requiere HTTPS).

---

### Opción C: Koyeb (Se Duerme - Similar a Render)

**Ventajas:**
- ✅ SSL gratis
- ✅ Deploy desde GitHub
- ✅ Interfaz amigable

**Limitaciones:**
- ⏸️ Se duerme como Render
- 📱 Solo 1 app en plan gratis

**Pasos:** Muy similares a Render, visita [koyeb.com](https://www.koyeb.com/)

---

## 🎯 Recomendación Final

### Para uso educativo/personal (acceso ocasional):
✅ **Render Free Tier** - Más fácil, no requiere tarjeta

### Para que esté siempre disponible (24/7):
✅ **Fly.io Free Tier** - Requiere tarjeta pero no cobra

### Ambas opciones incluyen:
- SSL/HTTPS gratis
- Deploy automático desde GitHub
- Suficiente para proyectos personales/educativos

---

## 6. Configuración de Supabase

### 6.1 Verificar Políticas RLS
1. Ve a Supabase Dashboard → Table Editor
2. Para cada tabla (`users`, `daily_tasks`, `monthly_plans`, etc.):
   - Verifica que RLS esté HABILITADO
   - Verifica las políticas de SELECT, INSERT, UPDATE, DELETE

### 6.2 Verificar Índices
```sql
-- Índice para mejorar rendimiento en daily_tasks
CREATE INDEX IF NOT EXISTS idx_daily_tasks_user_id ON daily_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_daily_tasks_fecha_inicio ON daily_tasks(fecha_inicio);
CREATE INDEX IF NOT EXISTS idx_daily_tasks_parent_task_id ON daily_tasks(parent_task_id);

-- Índice para monthly_plans
CREATE INDEX IF NOT EXISTS idx_monthly_plans_user_id ON monthly_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_monthly_plans_mes ON monthly_plans(mes);

-- Índice para weekly_logs
CREATE INDEX IF NOT EXISTS idx_weekly_logs_user_id ON weekly_logs(user_id);
```

### 6.3 Configurar Backups
1. Supabase hace backups automáticos diarios
2. Para backups adicionales: Database → Backups
3. Configura snapshots semanales (plan Pro)

### 6.4 Obtener las Keys
En Supabase Dashboard:
1. Project Settings → API
2. Copia:
   - **URL**: `https://xxxxxx.supabase.co`
   - **anon public**: Para `SUPABASE_KEY`
   - **service_role**: Para `SUPABASE_SERVICE_KEY` (¡NUNCA expongas esta key!)

---

## 7. Verificación Post-Despliegue

### 7.1 Checklist de Verificación
- [ ] La URL de producción carga correctamente
- [ ] Puedes hacer login con usuario existente
- [ ] Puedes registrar un nuevo usuario
- [ ] Puedes crear una tarea
- [ ] Las tareas se visualizan en Lista y Kanban
- [ ] Puedes editar y eliminar tareas
- [ ] El dashboard muestra estadísticas correctas
- [ ] Puedes crear un Plan Mensual
- [ ] Puedes agregar competencias
- [ ] Los gráficos se renderizan correctamente
- [ ] Puedes crear una Bitácora Semanal

### 7.2 Testing de Endpoints
Usa la consola del navegador o Postman:

```javascript
// Test de health check
fetch('https://tu-app.railway.app/')
  .then(r => r.json())
  .then(console.log)

// Test de login
fetch('https://tu-app.railway.app/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'username=test@test.com&password=test123'
})
  .then(r => r.json())
  .then(console.log)
```

### 7.3 Revisar Logs
En Railway/Render:
1. Ve a la pestaña "Deployments" o "Logs"
2. Busca errores (líneas rojas)
3. Verifica que no haya warnings críticos

---

## 8. Seguridad y Mejores Prácticas

### 8.1 Seguridad de Secrets
- ✅ NUNCA subas el archivo `.env` a Git
- ✅ Usa variables de entorno en la plataforma de hosting
- ✅ Rota el `SECRET_KEY` cada 3-6 meses
- ✅ Usa diferentes keys para dev y producción

### 8.2 CORS y Dominios
```python
# Solo permite tu dominio de producción
ALLOWED_ORIGINS = [
    "https://tu-app.railway.app",
    "https://tu-dominio-personalizado.com"
]
```

### 8.3 Rate Limiting (Opcional pero recomendado)
Instala:
```bash
pip install slowapi
```

Agrega a `main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/login")
@limiter.limit("5/minute")  # 5 intentos por minuto
async def login(request: Request, ...):
    ...
```

### 8.4 HTTPS
- Railway y Render proveen SSL gratis
- Verifica que tu app use `https://` y no `http://`
- Redirige HTTP a HTTPS

### 8.5 Monitoreo
Opciones gratuitas:
1. **UptimeRobot** (monitoreo de disponibilidad)
   - Configura ping cada 5 minutos a tu URL
   - Alerta por email si cae

2. **Sentry** (monitoreo de errores)
   ```bash
   pip install sentry-sdk[fastapi]
   ```

   ```python
   import sentry_sdk

   sentry_sdk.init(
       dsn="tu_sentry_dsn",
       environment="production"
   )
   ```

3. **Logs de Supabase**
   - Dashboard → Logs
   - Revisa queries lentas, errores de autenticación

---

## 9. Dominio Personalizado (Opcional)

### 9.1 Comprar Dominio
Opciones: Namecheap, GoDaddy, Google Domains, Cloudflare

### 9.2 Configurar DNS en Railway
1. Project Settings → Domains
2. Clic en "Add Custom Domain"
3. Ingresa `tudominio.com`
4. Copia los registros CNAME/A
5. Agrégalos en tu proveedor de DNS

### 9.3 Configurar DNS en Render
Similar a Railway:
1. Settings → Custom Domain
2. Sigue las instrucciones para agregar registros DNS

---

## 10. Mantenimiento Continuo

### 10.1 Actualizaciones
```bash
# Actualizar dependencias
pip install --upgrade fastapi uvicorn supabase

# Actualizar requirements.txt
pip freeze > requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Actualizar dependencias"
git push
```

### 10.2 Backups de Base de Datos
1. Supabase hace backups automáticos
2. Exporta manual cada mes:
   - Dashboard → Database → Backups → Export

### 10.3 Monitorear Uso (100% Gratis)
- **Render Free**: 750 horas/mes (suficiente para proyectos personales)
- **Fly.io Free**: 3 VMs compartidas, 160GB tráfico/mes
- **Supabase Free**: 500MB base de datos, 2GB transferencia, 1GB almacenamiento archivos
- **GitHub**: Repositorios ilimitados públicos/privados (gratis)

**Nota:** Si necesitas más recursos en el futuro:
- Render: $7/mes (siempre activo, más RAM/CPU)
- Supabase Pro: $25/mes (backups, más espacio)
- Fly.io: Pay-as-you-go después del free tier

---

## 11. Troubleshooting Común

### Error: "Application Error"
- Revisa logs en Railway/Render
- Verifica variables de entorno
- Asegúrate que `requirements.txt` esté completo

### Error: "502 Bad Gateway"
- El servidor no arrancó correctamente
- Revisa el `Procfile`
- Verifica el puerto: `--port ${PORT:-8000}`

### Error: "CORS policy"
- Actualiza `ALLOWED_ORIGINS` con tu dominio de producción
- No uses `*` en producción

### Error: "Database connection failed"
- Verifica `SUPABASE_URL` y `SUPABASE_KEY`
- Checa que las variables no tengan espacios extra
- Prueba la conexión desde el código local primero

### App lenta o se duerme en Render
- **Primera carga lenta (30-60s)**: Normal en Render Free, la app se despierta
- **Solución**: Usa Fly.io Free (siempre activo) o upgrade a Render $7/mes
- **Mejorar rendimiento**: Agrega índices a la base de datos, optimiza queries SQL
- **Mantener despierta**: Configura un ping cada 14 minutos con [UptimeRobot](https://uptimerobot.com) (gratis)

---

## 12. Checklist Final de Despliegue

Antes de lanzar:
- [ ] Código subido a GitHub
- [ ] `.gitignore` configurado (no subir `.env`)
- [ ] `requirements.txt` actualizado
- [ ] `Procfile` creado
- [ ] Variables de entorno configuradas en hosting
- [ ] Supabase RLS habilitado en todas las tablas
- [ ] Índices de base de datos creados
- [ ] CORS configurado con dominio de producción
- [ ] SECRET_KEY generado y configurado
- [ ] App desplegada y accesible
- [ ] Login funcional
- [ ] CRUD de tareas funcional
- [ ] Plan Mensual funcional
- [ ] Gráficos renderizando
- [ ] Bitácora Semanal funcional
- [ ] Monitoreo configurado (UptimeRobot/Sentry)
- [ ] SSL/HTTPS activo

---

## 13. Comandos Útiles

```bash
# Ver logs en Railway (CLI)
railway logs

# Ver logs en Render (CLI)
render logs

# Redeploy manual
git commit --allow-empty -m "Trigger redeploy"
git push

# Rollback en Railway
railway rollback

# Test local de producción
ENVIRONMENT=production uvicorn main:app --reload
```

---

## 🎉 ¡Listo!

Tu aplicación ahora está en producción. Comparte la URL con usuarios y empieza a recibir feedback.

**URL de ejemplo:**
- Railway: `https://plan-desarrollo.up.railway.app`
- Render: `https://plan-desarrollo.onrender.com`

**Próximos pasos:**
1. Configura dominio personalizado
2. Agrega analytics (Google Analytics, Plausible)
3. Implementa backups automáticos adicionales
4. Considera agregar autenticación con Google/GitHub
5. Mejora el SEO con meta tags

¿Necesitas ayuda con algún paso específico? ¡Pregunta!
