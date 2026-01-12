# 🚀 Despliegue en Render - Guía Paso a Paso

## ✅ Pre-requisitos Verificados

Los siguientes archivos están listos:
- ✅ `main.py` - Aplicación FastAPI
- ✅ `requirements.txt` - Dependencias
- ✅ `Procfile` - Comando de inicio
- ✅ `runtime.txt` - Python 3.11.7
- ✅ `.gitignore` - Archivos a ignorar
- ✅ `templates/` - Carpeta con HTML

---

## 📝 Paso 1: Preparar Git (si no lo has hecho)

Abre una terminal en tu proyecto y ejecuta:

```bash
# Verificar si ya tienes git inicializado
git status

# Si NO está inicializado, ejecuta:
git init
git add .
git commit -m "Preparar para despliegue en Render"
```

---

## 📤 Paso 2: Subir a GitHub

### Opción A: Si NO tienes repositorio en GitHub

1. Ve a [github.com](https://github.com) e inicia sesión
2. Clic en el botón "+" arriba a la derecha → "New repository"
3. Configura tu repositorio:
   - **Repository name**: `plan-desarrollo-profesional`
   - **Description**: Plan de Desarrollo Profesional con FastAPI
   - **Public** o **Private** (tu elección, ambos funcionan con Render)
   - ❌ NO marques "Initialize with README" (ya tienes archivos)
4. Clic en "Create repository"

5. En tu terminal, conecta y sube:
```bash
git remote add origin https://github.com/TU-USUARIO/plan-desarrollo-profesional.git
git branch -M main
git push -u origin main
```

### Opción B: Si YA tienes el repositorio

```bash
git add .
git commit -m "Preparar para despliegue en Render con runtime"
git push origin main
```

---

## 🌐 Paso 3: Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Clic en **"Get Started for Free"**
3. Opciones de registro:
   - **Recomendado:** "Sign up with GitHub" (más rápido)
   - O usa email/password
4. Completa el registro
5. ✅ **NO se requiere tarjeta de crédito**

---

## 🆕 Paso 4: Crear Web Service

1. En el dashboard de Render, clic en **"New +"** (botón azul arriba a la derecha)
2. Selecciona **"Web Service"**
3. Conectar GitHub:
   - Si es primera vez: Clic en "Connect GitHub" y autoriza Render
   - Busca tu repositorio: `plan-desarrollo-profesional`
   - Clic en **"Connect"**

---

## ⚙️ Paso 5: Configurar el Web Service

Completa el formulario con estos valores EXACTOS:

### Información Básica

| Campo | Valor |
|-------|-------|
| **Name** | `plan-desarrollo-profesional` |
| **Region** | Oregon (US West) o Frankfurt (EU Central) |
| **Branch** | `main` |
| **Root Directory** | (dejar vacío) |
| **Runtime** | Python 3 |

### Build & Deploy Settings

| Campo | Valor |
|-------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### Instance Type

| Campo | Valor |
|-------|-------|
| **Plan** | ⚡ **Free** |

---

## 🔐 Paso 6: Configurar Variables de Entorno

Antes de crear el servicio, baja hasta **"Environment Variables"**.

### Variables Requeridas

Clic en **"Add Environment Variable"** para cada una:

#### 1. SUPABASE_URL
```
Key: SUPABASE_URL
Value: https://xxxxxx.supabase.co
```
**Obtener:** Supabase Dashboard → Project Settings → API → URL

#### 2. SUPABASE_KEY
```
Key: SUPABASE_KEY
Value: eyJhbGc...
```
**Obtener:** Supabase Dashboard → Project Settings → API → anon public

#### 3. SUPABASE_SERVICE_KEY
```
Key: SUPABASE_SERVICE_KEY
Value: eyJhbGc...
```
**Obtener:** Supabase Dashboard → Project Settings → API → service_role
⚠️ **IMPORTANTE:** Esta es sensible, NO la compartas

#### 4. SECRET_KEY
```
Key: SECRET_KEY
Value: WAkOange0ksUtUqk1NHmnA-11-_Y4wFhoJvroOov5wQ
```
**Nota:** Usa el SECRET_KEY generado arriba o genera uno nuevo:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 5. ALGORITHM
```
Key: ALGORITHM
Value: HS256
```

#### 6. ENVIRONMENT
```
Key: ENVIRONMENT
Value: production
```

#### 7. ALLOWED_ORIGINS
```
Key: ALLOWED_ORIGINS
Value: https://plan-desarrollo-profesional.onrender.com
```
⚠️ **IMPORTANTE:** Reemplaza `plan-desarrollo-profesional` con el nombre que elegiste en el Paso 5

---

## 🚀 Paso 7: Desplegar

1. Revisa que todas las variables estén correctas
2. Clic en **"Create Web Service"** (botón azul al final)
3. Render comenzará a construir tu aplicación

### Proceso de Deploy (3-5 minutos)

Verás en la consola:

```
==> Cloning from https://github.com/tu-usuario/plan-desarrollo-profesional...
==> Checking out commit...
==> Building...
==> Installing dependencies from requirements.txt...
==> Starting service...
==> Your service is live 🎉
```

---

## ✅ Paso 8: Verificar Despliegue

1. Una vez que veas **"Live"** con un punto verde ✅
2. Arriba verás tu URL: `https://plan-desarrollo-profesional.onrender.com`
3. Clic en la URL para abrir tu aplicación
4. Deberías ver la página de login

### Primera Carga
- ⏰ Puede tardar **30-60 segundos** en cargar
- Esto es normal en el plan Free (la app se "despierta")
- Cargas posteriores serán rápidas

---

## 🔧 Paso 9: Actualizar ALLOWED_ORIGINS (si es necesario)

Si la URL final es diferente:

1. En Render, menú izquierdo → **"Environment"**
2. Busca la variable `ALLOWED_ORIGINS`
3. Clic en el lápiz para editar
4. Actualiza con la URL correcta: `https://tu-url-real.onrender.com`
5. Clic en **"Save Changes"**
6. Render redesplegará automáticamente (2-3 minutos)

---

## 🧪 Paso 10: Probar la Aplicación

### Test 1: Login
1. Ve a tu URL: `https://plan-desarrollo-profesional.onrender.com`
2. Debería aparecer la página de login
3. Intenta iniciar sesión con credenciales existentes

### Test 2: Registro
1. Clic en "Registrarse"
2. Ingresa un email y contraseña
3. Verifica que se cree el usuario

### Test 3: Dashboard
1. Después de login, deberías ver el dashboard
2. Verifica que muestre estadísticas
3. Navega entre las secciones (Tareas, Plan Mensual, Bitácora)

### Test 4: Crear Tarea
1. Ve a "Tareas"
2. Clic en "Nueva Tarea"
3. Crea una tarea de prueba
4. Verifica que se guarde correctamente

---

## 📊 Paso 11: Ver Logs (si hay problemas)

Si algo no funciona:

1. En Render, menú izquierdo → **"Logs"**
2. Verás la consola del servidor
3. Busca líneas rojas (errores)
4. Los errores comunes y soluciones están abajo

---

## ❌ Troubleshooting

### Error: "Application failed to respond"

**Causa:** El servidor no arrancó correctamente

**Solución:**
1. Verifica que el Start Command sea: `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Revisa los logs para ver el error específico

### Error: "502 Bad Gateway"

**Causa:** La aplicación no está escuchando en el puerto correcto

**Solución:**
1. Verifica que uses `--port $PORT` (con el símbolo `$`)
2. NO uses un puerto fijo como `--port 8000`

### Error: CORS al intentar login

**Causa:** `ALLOWED_ORIGINS` no coincide con la URL

**Solución:**
1. Ve a Environment Variables
2. Edita `ALLOWED_ORIGINS` con tu URL exacta de Render
3. NO incluyas `/` al final

### Error: "Database connection failed"

**Causa:** Credenciales de Supabase incorrectas

**Solución:**
1. Ve a Supabase Dashboard → Settings → API
2. Copia nuevamente las keys
3. Actualiza las variables en Render
4. Guarda y espera el redespliegue

### App muy lenta o se "duerme"

**Causa:** Plan Free se duerme después de 15 minutos

**Solución:**
1. Primera carga: Espera 30-60 segundos (normal)
2. Para mantenerla activa: Usa [UptimeRobot](https://uptimerobot.com) (gratis)
   - Configura ping cada 14 minutos
   - Tu app nunca se dormirá

---

## 🔄 Actualizar la Aplicación

Cuando hagas cambios al código:

```bash
# 1. Hacer cambios en tu código local
# 2. Commit y push
git add .
git commit -m "Descripción de cambios"
git push origin main

# 3. Render detectará el cambio y redesplegará automáticamente
```

---

## 📈 Monitoreo (Opcional pero Recomendado)

### Mantener la app siempre activa (GRATIS)

1. Ve a [uptimerobot.com](https://uptimerobot.com)
2. Crea cuenta gratis (NO requiere tarjeta)
3. Clic en **"Add New Monitor"**
4. Configuración:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Plan Desarrollo Profesional
   - **URL:** `https://plan-desarrollo-profesional.onrender.com`
   - **Monitoring Interval:** 14 minutes
5. Clic en **"Create Monitor"**

¡Listo! Tu app nunca se dormirá 🎉

---

## 🎉 ¡Despliegue Completado!

Tu aplicación está ahora en producción:
- 🌐 **URL:** `https://plan-desarrollo-profesional.onrender.com`
- 🔒 **SSL/HTTPS:** Activado automáticamente
- 💰 **Costo:** $0.00/mes
- 📊 **Límites:** 750 horas/mes (suficiente para uso personal)

### Próximos pasos:

1. **Comparte tu URL** con usuarios para que la prueben
2. **Configura UptimeRobot** para mantenerla siempre activa
3. **Monitorea los logs** en Render regularmente
4. **Haz backups** de tu base de datos en Supabase

---

## 📞 Soporte

Si tienes problemas:
1. Revisa la sección de Troubleshooting arriba
2. Consulta los logs en Render
3. Verifica la [Guía Completa](./GUIA_PRODUCCION.md) para más detalles

---

**¡Felicidades por tu despliegue exitoso! 🚀**
