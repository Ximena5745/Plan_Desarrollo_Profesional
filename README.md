# 🚀 Plan de Desarrollo Profesional - Aplicación Web

## 📋 Descripción
Aplicación web completa para gestionar tu plan de desarrollo profesional con:
- ✅ Planes mensuales (inicio y evaluación de fin de mes)
- ✅ Bitácoras semanales con reflexiones
- ✅ Gestión de tareas con jerarquía (Macrotareas → Subtareas)
- ✅ Vista Lista y Kanban (drag & drop)
- ✅ Dashboard con métricas y estadísticas
- ✅ Sistema multiusuario con autenticación JWT
- ✅ Clasificaciones y categorías personalizables por usuario

## 🎨 Características de la Interfaz
- **Diseño moderno** con Tailwind CSS + DaisyUI
- **Tema oscuro/claro** automático
- **Responsive** (móvil, tablet, desktop)
- **Drag & Drop** para Kanban
- **Notificaciones** visuales
- **Animaciones suaves**
- **Jerarquía visual** de tareas

## 🛠️ Stack Tecnológico
- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: HTML5 + Tailwind CSS + Alpine.js
- **Base de Datos**: Supabase (PostgreSQL)
- **Autenticación**: JWT custom
- **Gráficos**: Chart.js
- **Iconos**: Font Awesome

## 📦 Instalación y Configuración

### 1. Requisitos Previos
```bash
# Python 3.10 o superior
python --version

# pip actualizado
pip install --upgrade pip
```

### 2. Clonar y Configurar
```bash
# Activar entorno virtual (si ya existe)
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crea o edita el archivo `.env` con tus credenciales de Supabase:

```env
# Supabase Configuration
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-service-role-key

# JWT Configuration
JWT_SECRET_KEY=tu-secret-key-muy-segura
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

### 4. Configurar Base de Datos en Supabase

1. Ve a [supabase.com](https://supabase.com) y accede a tu proyecto
2. Ve a **SQL Editor** y ejecuta el script `database_setup.sql`
3. Verifica que se crearon las siguientes tablas:
   - `daily_tasks` - Tareas diarias
   - `monthly_plans` - Planes mensuales
   - `monthly_reviews` - Evaluaciones mensuales
   - `weekly_logs` - Bitácoras semanales
   - `user_config` - Configuración personalizada por usuario
   - `metrics` - Métricas calculadas automáticamente

### 5. Ejecutar Aplicación

```bash
# Iniciar servidor (Windows)
iniciar.bat

# O manualmente:
python main.py

# O con uvicorn directamente:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Abre tu navegador en: `http://localhost:8000`

**Usuario de prueba:**
- Email: lxisilva@poligran.edu.co
- Contraseña: (configura en primera ejecución)

## 📁 Estructura del Proyecto

```
Plan_Desarrollo_Profesional/
├── main.py                     # Aplicación FastAPI principal
├── templates/
│   ├── login.html             # Página de login
│   └── dashboard.html         # Dashboard principal (SPA)
├── static/
│   └── style.css              # Estilos personalizados
├── uploads/                    # Archivos subidos (temporal)
├── database_setup.sql          # Script inicial de base de datos
├── requirements.txt            # Dependencias Python
├── .env                       # Variables de entorno (no subir a Git)
├── .env.example               # Ejemplo de configuración
├── iniciar.bat                # Script de inicio rápido (Windows)
└── README.md                  # Este archivo
```

## 📊 Funcionalidades Principales

### 1. Dashboard
- **Estadísticas del mes**: Total de tareas, completadas, pendientes, tasa de completitud
- **Gráficos**: Progreso semanal, tareas por categoría
- **Actividad reciente**: Últimas tareas y bitácoras

### 2. Gestión de Tareas

#### Características:
- **Jerarquía**: Macrotareas que agrupan subtareas
- **Progreso automático**: Las macrotareas calculan su progreso del promedio de sus subtareas
- **Estado automático según progreso**:
  - Progreso 0% → Estado: Pendiente
  - Progreso 1-99% → Estado: En Progreso
  - Progreso 100% → Estado: Completada
- **Validación**: Progreso >90% requiere evidencias
- **Clasificaciones y categorías personalizables** por usuario
- **Campos de fecha**: Fecha inicio y fecha fin (rango)

#### Vistas disponibles:
- **Lista**: Tabla jerárquica con indentación visual
- **Kanban**: Drag & drop entre Pendiente, En Progreso y Completada

#### Campos de cada tarea:
- Título y descripción
- Clasificación (personalizable)
- Categoría (personalizable)
- Estado (pendiente, en_progreso, completada, cancelada)
- Prioridad (baja, media, alta)
- Progreso (0-100%)
- Fecha inicio y fecha fin
- Es macrotarea (checkbox)
- Tarea padre (para subtareas)
- Observaciones

### 3. Plan Mensual

#### Inicio de Mes:
- Competencias a trabajar
- ¿Qué quiero lograr?
- Mis fortalezas
- Mis debilidades

#### Fin de Mes - Evaluación:
- ¿Qué mejoré?
- ¿Qué me faltó mejorar?
- Habilidades desarrolladas
- Momento memorable

### 4. Bitácora Semanal

Registra semanalmente:
- Período (fecha inicio - fecha fin)
- Logros de la semana
- Desafíos enfrentados
- Aprendizajes
- Reflexiones
- Nivel de energía (1-5)
- Satisfacción (1-5)

### 5. Configuración Personalizable

Cada usuario puede agregar sus propias:
- **Clasificaciones**: desarrollo, investigación, documentación, etc.
- **Categorías**: aprendizaje, compromiso, competencia, personal, etc.

## 🔧 Características Técnicas

### Autenticación
- Sistema JWT custom (no usa Supabase Auth)
- Tokens con expiración de 30 minutos
- Protección de rutas con dependencia `verify_token`

### Base de Datos
- **Row Level Security (RLS)** habilitado en todas las tablas
- **Políticas RLS** configuradas por usuario
- **Triggers automáticos**:
  - Cálculo de progreso de macrotareas
  - Actualización de métricas diarias
- **Service Role Key** usado en backend para bypassear RLS

### API Endpoints

#### Autenticación:
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Inicio de sesión

#### Tareas:
- `GET /api/tasks` - Listar tareas (con filtros)
- `POST /api/tasks` - Crear tarea
- `PUT /api/tasks/{id}` - Actualizar tarea
- `DELETE /api/tasks/{id}` - Eliminar tarea

#### Configuración:
- `GET /api/config` - Obtener clasificaciones y categorías del usuario
- `POST /api/config/clasificaciones` - Agregar clasificación
- `POST /api/config/categorias` - Agregar categoría

#### Plan Mensual:
- `POST /api/monthly/plans` - Crear plan mensual
- `GET /api/monthly/plans` - Listar planes
- `POST /api/monthly/reviews` - Crear evaluación mensual

#### Bitácora Semanal:
- `POST /api/weekly/logs` - Crear bitácora
- `GET /api/weekly/logs` - Listar bitácoras

#### Dashboard:
- `GET /api/dashboard/summary` - Resumen de estadísticas
- `GET /api/dashboard/tasks-by-day` - Tareas agrupadas por día

## 🎯 Uso de la Aplicación

### Primer Uso
1. Accede a `http://localhost:8000`
2. Regístrate con tu email institucional
3. El sistema creará automáticamente tu perfil y configuración inicial

### Crear una Tarea
1. Ve a **Tareas** en el menú
2. Clic en **+ Nueva Tarea**
3. Llena los campos requeridos:
   - Título (obligatorio)
   - Fecha inicio y fin (obligatorio)
   - Categoría (obligatorio)
   - Clasificación, estado, prioridad (opcionales)
4. Marca "Es una Macrotarea" si quieres agrupar subtareas
5. Clic en **Crear Tarea**

### Crear una Subtarea
1. Crea o edita una tarea
2. En el campo "Tarea Padre" selecciona la macrotarea
3. El progreso de la macrotarea se calculará automáticamente

### Editar y Eliminar
- **Vista Lista**: Botones de lápiz (editar) y papelera (eliminar) en cada fila
- **Vista Kanban**: Menú de 3 puntos (⋮) en cada tarjeta

### Cambiar Estado con Drag & Drop
1. Ve a vista **Kanban**
2. Arrastra las tarjetas entre columnas
3. El estado se actualizará automáticamente

## 🐛 Solución de Problemas

### Error: "API Call failed"
- Verifica que el servidor esté ejecutándose (`python main.py`)
- Verifica que las variables de entorno en `.env` sean correctas
- Revisa la consola del servidor para ver el error específico

### Error: "401 Unauthorized"
- Tu token JWT expiró (30 minutos)
- Vuelve a iniciar sesión desde `/login`

### Las tareas no se muestran en la Lista
- Verifica en la consola del navegador (F12) si hay errores JavaScript
- Revisa que las tareas se estén cargando (aparece el contador verde arriba de la tabla)

### El dashboard muestra "undefined% completado"
- Verifica que el backend esté enviando datos en camelCase
- Revisa la respuesta del endpoint `/api/dashboard/summary`

### Error al guardar Plan Mensual o Bitácora
- Verifica que todos los campos obligatorios estén llenos
- Revisa la consola del navegador para ver el error específico
- Verifica que las tablas existan en Supabase

## 🔐 Seguridad

- Autenticación JWT con secret key
- Contraseñas no implementadas en esta versión (solo email)
- RLS habilitado en Supabase
- CORS configurado para localhost en desarrollo

## 📈 Próximas Mejoras

- [ ] Sistema de evidencias (upload de archivos)
- [ ] Exportar reportes a Excel
- [ ] Gráficos más avanzados
- [ ] Notificaciones de tareas pendientes
- [ ] Filtros avanzados en vista de tareas
- [ ] Búsqueda global

## 🚀 Despliegue a Producción (100% GRATIS)

### ✨ Opciones Gratuitas Disponibles

| Plataforma | Costo | Limitación | Ideal Para |
|------------|-------|------------|------------|
| **Render** | GRATIS | Se duerme tras 15 min | Uso educativo/personal |
| **Fly.io** | GRATIS | Requiere tarjeta (no cobra) | Siempre activo 24/7 |

### Verificación Pre-Despliegue
Ejecuta el script de verificación antes de desplegar:
```bash
python check_production.py
```

Este script verificará:
- ✅ Archivos necesarios (Procfile, requirements.txt, etc.)
- ✅ Variables de entorno configuradas correctamente
- ✅ .gitignore incluyendo archivos sensibles
- ✅ Configuración de seguridad
- ✅ Dependencias completas

### Guía Completa de Despliegue

Para instrucciones detalladas paso a paso sobre cómo desplegar la aplicación GRATIS:

📖 **[Ver Guía Completa de Producción GRATIS](./GUIA_PRODUCCION.md)**

La guía incluye:
- ✅ Despliegue en Render (100% gratis, recomendado)
- ✅ Alternativas gratuitas (Fly.io, Koyeb)
- ✅ Configuración de Supabase (gratis hasta 500MB)
- ✅ Variables de entorno
- ✅ Seguridad y mejores prácticas
- ✅ Monitoreo gratuito con UptimeRobot
- ✅ Troubleshooting común

### Despliegue Rápido en Render (GRATIS)

1. **Verificar configuración**:
   ```bash
   python check_production.py
   ```

2. **Subir a GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Preparar para producción"
   git push origin main
   ```

3. **Configurar en Render** (NO requiere tarjeta de crédito):
   - Ve a [render.com](https://render.com)
   - Clic en "Get Started for Free"
   - Conecta tu repositorio de GitHub
   - Selecciona plan **"Free"**
   - Agrega variables de entorno
   - ¡Despliega!

4. **Variables de entorno requeridas**:
   ```
   SUPABASE_URL=https://xxxxxx.supabase.co
   SUPABASE_KEY=eyJhbGc...
   SUPABASE_SERVICE_KEY=eyJhbGc...
   SECRET_KEY=tu_clave_generada_segura
   ALGORITHM=HS256
   ENVIRONMENT=production
   ALLOWED_ORIGINS=https://tu-app.onrender.com
   ```

### Generar SECRET_KEY
```python
import secrets
print(secrets.token_urlsafe(32))
```

Copia la salida y úsala como `SECRET_KEY` en las variables de entorno.

---

### 💡 Notas sobre Render Free

**Limitación:** La app se "duerme" después de 15 minutos sin actividad.
- Primera carga: 30-60 segundos (mientras despierta)
- Cargas subsecuentes: Rápidas (mientras esté activa)

**Solución:** Para mantenerla siempre activa, usa [UptimeRobot](https://uptimerobot.com) (gratis) para hacer ping cada 14 minutos.

**Alternativa:** Usa Fly.io (gratis, siempre activo, pero requiere tarjeta de crédito)

## 📄 Licencia

Proyecto de desarrollo profesional - Uso educativo

---

**¡Listo para usar! 🎉**

Para cualquier problema, revisa la sección de "Solución de Problemas" o contacta al equipo de desarrollo.
