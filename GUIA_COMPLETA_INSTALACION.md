# Guía Completa de Instalación y Configuración
## Plan de Desarrollo Profesional

Esta guía te llevará paso a paso desde cero hasta tener la aplicación funcionando y subida a GitHub.

---

## 📋 Índice

1. [Configuración de Supabase](#1-configuración-de-supabase)
2. [Configuración del Proyecto Local](#2-configuración-del-proyecto-local)
3. [Verificación del Usuario](#3-verificación-del-usuario)
4. [Subir a GitHub](#4-subir-a-github)
5. [Verificación Final](#5-verificación-final)

---

## 1. Configuración de Supabase

### Paso 1.1: Crear Cuenta y Proyecto

1. **Crear cuenta en Supabase**
   - Ve a: https://supabase.com
   - Haz clic en **Start your project**
   - Regístrate con tu email o cuenta de GitHub
   - Confirma tu email

2. **Crear nuevo proyecto**
   - Haz clic en **New Project**
   - Selecciona tu organización (o crea una nueva)
   - Completa los datos:
     - **Name:** `Plan-Desarrollo-Profesional`
     - **Database Password:** Crea una contraseña segura (guárdala!)
     - **Region:** Selecciona la más cercana (ej: South America - São Paulo)
     - **Pricing Plan:** Free (0$ al mes)
   - Haz clic en **Create new project**
   - ⏱️ Espera 2-3 minutos mientras se crea el proyecto

3. **Verificar que el proyecto esté listo**
   - Verás un dashboard con estadísticas
   - En la parte superior verás el estado: **Project is ready**

### Paso 1.2: Obtener Credenciales de la API

1. En el menú lateral, ve a **Settings** (⚙️ ícono de engranaje)
2. Haz clic en **API**
3. En la sección **Project API keys**, encontrarás:
   - **Project URL:** `https://xxxxxxxxxxxxx.supabase.co`
   - **anon/public key:** Una clave larga que empieza con `eyJ...`
   - **service_role key:** Otra clave larga (haz clic en el ícono del ojo para revelarla)

4. **Copia estas 3 credenciales** (las usaremos en el paso 2.2):
   ```
   URL: https://xxxxxxxxxxxxx.supabase.co
   ANON KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SERVICE KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Paso 1.3: Configurar la Base de Datos

1. **Abrir SQL Editor**
   - En el menú lateral, haz clic en **SQL Editor** (ícono <>)
   - Verás un editor de SQL vacío

2. **Ejecutar el script de creación de tablas**
   - Abre el archivo `database_setup.sql` de este proyecto
   - **Copia TODO el contenido** (Ctrl+A, Ctrl+C)
   - **Pégalo** en el SQL Editor de Supabase
   - Haz clic en **Run** (o presiona Ctrl+Enter)
   - ⏱️ Espera unos segundos
   - Deberías ver: **Success. No rows returned**

3. **Verificar que las tablas se crearon**
   - En el menú lateral, ve a **Table Editor**
   - Deberías ver las siguientes tablas:
     - ✅ `user_profiles`
     - ✅ `monthly_plans`
     - ✅ `monthly_reviews`
     - ✅ `weekly_logs`
     - ✅ `daily_tasks`
     - ✅ `evidencias`
     - ✅ `metrics`

### Paso 1.4: Crear Bucket de Storage (para evidencias)

1. **Ir a Storage**
   - En el menú lateral, haz clic en **Storage** (ícono de carpeta)
   - Verás una página vacía

2. **Crear nuevo bucket**
   - Haz clic en **New bucket**
   - Completa los datos:
     - **Name:** `evidencias`
     - **Public bucket:** ✅ Marcado (para que las imágenes sean accesibles)
   - Haz clic en **Create bucket**

3. **Configurar políticas del bucket**
   - Haz clic en el bucket `evidencias` que acabas de crear
   - Ve a **Policies**
   - Haz clic en **New policy**
   - Selecciona **For full customization**

   **Política 1: Permitir lectura pública**
   - Policy name: `Public Access`
   - Allowed operation: `SELECT`
   - Target roles: `public`
   - USING expression: `true`
   - Haz clic en **Save policy**

   **Política 2: Permitir subida de archivos autenticados**
   - Haz clic en **New policy** nuevamente
   - Policy name: `Authenticated users can upload`
   - Allowed operation: `INSERT`
   - Target roles: `authenticated`
   - USING expression: `(bucket_id = 'evidencias'::text)`
   - Haz clic en **Save policy**

4. **Verificar que el bucket funcione**
   - Ve a la pestaña **Explore**
   - Intenta subir un archivo de prueba (cualquier imagen)
   - Si funciona, ¡perfecto! Ya puedes eliminar el archivo de prueba

### Paso 1.5: Verificar Configuración del Usuario

1. **Ver usuarios registrados**
   - En el menú lateral, ve a **Authentication** (ícono de usuario)
   - Haz clic en **Users**
   - Deberías ver al usuario: `lxisilva@poligran.edu.co`

2. **Verificar que el email esté confirmado**
   - Busca la columna **Email Confirmed At**
   - Si tiene una fecha → ✅ Confirmado
   - Si está vacío → Haz clic en los 3 puntos `...` → **Verify email**

3. **Crear perfil del usuario**
   - Ve a **SQL Editor**
   - Abre el archivo `setup_user_profile.sql` de este proyecto
   - Copia TODO el contenido
   - Pégalo en el SQL Editor
   - Haz clic en **Run**
   - Verás varias tablas de resultados
   - La última debe mostrar el perfil del usuario creado

---

## 2. Configuración del Proyecto Local

### Paso 2.1: Verificar Entorno Virtual

1. **Abrir terminal en la carpeta del proyecto**
   - En VSCode: Terminal → New Terminal
   - O abre PowerShell/CMD en la carpeta

2. **Verificar si el entorno virtual está activo**
   ```bash
   # En Windows verás algo como:
   (Plan_Desarrollo_Profesional) C:\Users\...
   ```

3. **Si NO está activo, actívalo:**
   ```bash
   # Windows
   Scripts\activate

   # Mac/Linux
   source bin/activate
   ```

4. **Verificar que las dependencias estén instaladas:**
   ```bash
   pip list
   ```
   - Deberías ver: fastapi, uvicorn, supabase, etc.
   - Si no están instaladas:
     ```bash
     pip install -r requirements.txt
     ```

### Paso 2.2: Configurar Variables de Entorno

1. **Abrir el archivo `.env`**
   - Está en la raíz del proyecto
   - Si no existe, copia `.env.example` como `.env`:
     ```bash
     copy .env.example .env
     ```

2. **Editar el archivo `.env`**
   - Abre `.env` con un editor de texto
   - Reemplaza estos valores con tus credenciales de Supabase (del Paso 1.2):

   ```env
   # =======================================
   # CONFIGURACIÓN DE SUPABASE
   # =======================================
   SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

   # =======================================
   # CONFIGURACIÓN JWT
   # =======================================
   SECRET_KEY=tu-clave-super-secreta-cambiala-por-algo-aleatorio-largo
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440

   # =======================================
   # CONFIGURACIÓN DE LA APLICACIÓN
   # =======================================
   APP_NAME=Plan de Desarrollo Profesional
   DEBUG=True
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

   # =======================================
   # CONFIGURACIÓN DE ARCHIVOS
   # =======================================
   MAX_FILE_SIZE_MB=10
   ALLOWED_FILE_TYPES=image/jpeg,image/png,image/gif,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document
   UPLOAD_DIR=uploads
   SUPABASE_BUCKET_NAME=evidencias
   ```

3. **Generar una clave secreta segura (opcional pero recomendado)**
   ```bash
   # Windows (PowerShell)
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})

   # Mac/Linux
   openssl rand -hex 32
   ```
   - Copia el resultado y reemplaza `SECRET_KEY` en `.env`

4. **Guardar el archivo `.env`**

### Paso 2.3: Probar que el Servidor Inicie

1. **Iniciar el servidor:**
   ```bash
   python main.py
   ```

2. **Verificar mensajes:**
   ```
   OK - Conexion a Supabase establecida correctamente
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process [12345] using WatchFiles
   INFO:     Started server process [67890]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

3. **Si ves estos mensajes → ✅ ¡Perfecto!**

4. **Abrir en el navegador:**
   - Ve a: http://localhost:8000
   - Deberías ver la página de login

5. **Detener el servidor:**
   - Presiona `Ctrl+C` en la terminal

---

## 3. Verificación del Usuario

### Paso 3.1: Probar Login con Script

1. **Abrir una NUEVA terminal** (mantén la del servidor abierta)

2. **Activar entorno virtual:**
   ```bash
   Scripts\activate
   ```

3. **Ejecutar script de prueba:**
   ```bash
   python test_login.py
   ```

4. **Ingresar contraseña cuando se solicite**

5. **Verificar resultado:**
   - ✅ Debe mostrar: "LOGIN EXITOSO!"
   - ✅ Debe mostrar los datos del usuario
   - ❌ Si falla, revisa el Paso 1.5

### Paso 3.2: Probar Login en el Navegador

1. **Asegúrate de que el servidor esté corriendo**
   ```bash
   python main.py
   ```

2. **Abrir el navegador:**
   - Ve a: http://localhost:8000/login

3. **Ingresar credenciales:**
   - Email: `lxisilva@poligran.edu.co`
   - Contraseña: [tu contraseña]

4. **Hacer clic en "Iniciar Sesión"**

5. **Verificar:**
   - ✅ Deberías ser redirigido al dashboard
   - ✅ Verás tu nombre en la esquina superior derecha
   - ✅ Verás las estadísticas en 0 (usuario nuevo)

---

## 4. Subir a GitHub

### Paso 4.1: Verificar Archivo .gitignore

1. **Abrir `.gitignore`**
   - Debería existir en la raíz del proyecto

2. **Verificar que contenga esto:**
   ```gitignore
   # Entorno virtual
   Scripts/
   Lib/
   Include/
   pyvenv.cfg

   # Variables de entorno (IMPORTANTE!)
   .env

   # Archivos de Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python

   # Archivos subidos por usuarios
   uploads/
   *.log

   # IDEs
   .vscode/
   .idea/
   *.swp
   *.swo
   *~

   # Sistema operativo
   .DS_Store
   Thumbs.db
   ```

3. **Si no existe o está incompleto, créalo/actualízalo**

### Paso 4.2: Inicializar Repositorio Git

1. **Verificar estado actual:**
   ```bash
   git status
   ```
   - Si dice "not a git repository" → Continúa al paso 2
   - Si muestra archivos → Salta al paso 4.3

2. **Inicializar git:**
   ```bash
   git init
   ```

3. **Configurar tu usuario (si es la primera vez):**
   ```bash
   git config --global user.name "Ximena5745"
   git config --global user.email "lxisilva@poligran.edu.co"
   ```

### Paso 4.3: Agregar Archivos al Repositorio

1. **Ver qué archivos se agregarán:**
   ```bash
   git status
   ```
   - ⚠️ **IMPORTANTE:** NO debe aparecer `.env` (debe estar en rojo o no aparecer)
   - Si aparece `.env`, verifica tu `.gitignore`

2. **Agregar todos los archivos:**
   ```bash
   git add .
   ```

3. **Verificar archivos agregados:**
   ```bash
   git status
   ```
   - Deberías ver archivos en verde
   - Verifica que `.env` NO esté en la lista

4. **Crear el primer commit:**
   ```bash
   git commit -m "Initial commit: Plan de Desarrollo Profesional

   - Configuracion completa de FastAPI
   - Templates HTML con dashboard interactivo
   - Integracion con Supabase
   - Sistema de autenticacion JWT
   - Gestion de tareas, planes mensuales y bitacoras
   - Scripts de configuracion y pruebas"
   ```

### Paso 4.4: Conectar con GitHub

1. **Verificar si ya tiene remote:**
   ```bash
   git remote -v
   ```

2. **Si NO tiene remote, agregarlo:**
   ```bash
   git remote add origin https://github.com/Ximena5745/Plan_Desarrollo_Profesional.git
   ```

3. **Verificar que se agregó:**
   ```bash
   git remote -v
   ```
   - Deberías ver:
     ```
     origin  https://github.com/Ximena5745/Plan_Desarrollo_Profesional.git (fetch)
     origin  https://github.com/Ximena5745/Plan_Desarrollo_Profesional.git (push)
     ```

### Paso 4.5: Subir a GitHub

1. **Obtener la rama principal:**
   ```bash
   git branch -M main
   ```

2. **Subir los archivos:**
   ```bash
   git push -u origin main
   ```

3. **Si te pide autenticación:**
   - **Usuario:** `Ximena5745`
   - **Contraseña:** Usa un **Personal Access Token** (no tu contraseña)

   **Si no tienes un token:**
   - Ve a: https://github.com/settings/tokens
   - Click en **Generate new token (classic)**
   - Marca: `repo` (acceso completo a repositorios)
   - Click en **Generate token**
   - **Copia el token** (¡no podrás verlo de nuevo!)
   - Usa ese token como contraseña

4. **Esperar a que termine:**
   ```
   Enumerating objects: 45, done.
   Counting objects: 100% (45/45), done.
   Delta compression using up to 8 threads
   Compressing objects: 100% (40/40), done.
   Writing objects: 100% (45/45), 125.45 KiB | 15.68 MiB/s, done.
   Total 45 (delta 12), reused 0 (delta 0), pack-reused 0
   To https://github.com/Ximena5745/Plan_Desarrollo_Profesional.git
    * [new branch]      main -> main
   Branch 'main' set up to track remote branch 'main' from 'origin'.
   ```

5. **Verificar en GitHub:**
   - Ve a: https://github.com/Ximena5745/Plan_Desarrollo_Profesional
   - Deberías ver todos tus archivos
   - ⚠️ **VERIFICA** que NO esté el archivo `.env`

---

## 5. Verificación Final

### Checklist Completo

**Supabase:**
- [ ] Proyecto creado y activo
- [ ] Todas las tablas creadas (7 tablas)
- [ ] Bucket `evidencias` creado y público
- [ ] Usuario `lxisilva@poligran.edu.co` confirmado
- [ ] Perfil de usuario creado en `user_profiles`

**Proyecto Local:**
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado con credenciales reales
- [ ] Servidor inicia sin errores
- [ ] Conexión a Supabase establecida

**Funcionalidad:**
- [ ] Login funciona en http://localhost:8000/login
- [ ] Script `test_login.py` ejecuta exitosamente
- [ ] Dashboard carga correctamente
- [ ] Puedo crear una tarea de prueba

**GitHub:**
- [ ] Repositorio inicializado
- [ ] Archivo `.gitignore` configurado
- [ ] Primer commit creado
- [ ] Archivos subidos a GitHub
- [ ] Archivo `.env` NO está en GitHub

---

## 🎉 ¡Felicitaciones!

Has completado la instalación y configuración completa del proyecto.

### Próximos Pasos:

1. **Explorar la aplicación:**
   - Crea tu primer plan mensual
   - Agrega algunas tareas
   - Registra una bitácora semanal

2. **Personalizar:**
   - Actualiza tu perfil en el dashboard
   - Ajusta los colores y temas según tu preferencia

3. **Desarrollar:**
   - Haz cambios en el código
   - Crea commits frecuentes:
     ```bash
     git add .
     git commit -m "Descripcion del cambio"
     git push
     ```

4. **Compartir:**
   - Tu repositorio está público en: https://github.com/Ximena5745/Plan_Desarrollo_Profesional
   - Puedes compartirlo con otros usuarios

---

## 📞 Ayuda y Soporte

Si encuentras problemas:

1. **Revisa la sección específica** de esta guía
2. **Consulta los archivos de documentación:**
   - [README.md](README.md) - Información general
   - [INSTRUCCIONES_DE_USO.md](INSTRUCCIONES_DE_USO.md) - Uso de la aplicación
   - [CONFIGURACION_USUARIO.md](CONFIGURACION_USUARIO.md) - Configuración del usuario
3. **Revisa los logs:**
   - Terminal del servidor (errores de backend)
   - Consola del navegador F12 (errores de frontend)
4. **Verifica configuración:**
   - Archivo `.env`
   - Credenciales de Supabase
   - Estado del servidor

---

## 📊 Comandos Útiles

```bash
# Iniciar servidor
python main.py

# Probar login
python test_login.py

# Ver estado de git
git status

# Hacer commit
git add .
git commit -m "Mensaje del commit"
git push

# Actualizar dependencias
pip install -r requirements.txt

# Ver logs en tiempo real
# (ejecutar mientras el servidor está corriendo en otra terminal)
tail -f logs/app.log
```

---

**Versión:** 1.0
**Última actualización:** 2026-01-08
**Autor:** Plan de Desarrollo Profesional
