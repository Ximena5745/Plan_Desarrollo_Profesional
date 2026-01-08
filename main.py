"""
Plan de Desarrollo Profesional - Aplicación FastAPI
Versión: 1.0.0
"""

from fastapi import FastAPI, Request, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import aiofiles
from jose import JWTError, jwt
from passlib.context import CryptContext

# ============================================
# CONFIGURACIÓN
# ============================================

load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", SUPABASE_KEY)

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "tu-secret-key-super-segura")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Configuración de archivos
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME", "evidencias")

# Crear directorio de uploads
UPLOAD_DIR.mkdir(exist_ok=True)

# Cliente Supabase
try:
    if not SUPABASE_URL or not SUPABASE_KEY or "tuproyecto" in SUPABASE_URL:
        print("\n" + "="*70)
        print("ADVERTENCIA: Configuracion de Supabase no encontrada")
        print("="*70)
        print("Por favor, configura las credenciales de Supabase en el archivo .env")
        print("\n1. Visita: https://supabase.com")
        print("2. Crea un proyecto (es gratis)")
        print("3. Ve a Settings > API y copia tus credenciales")
        print("4. Actualiza el archivo .env con tus credenciales")
        print("5. Ejecuta el script database_setup.sql en el SQL Editor")
        print("="*70 + "\n")
        # Crear clientes dummy para que la app no crashee
        supabase = None
        supabase_admin = None
    else:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("OK - Conexion a Supabase establecida correctamente")
except Exception as e:
    print(f"\nERROR al conectar con Supabase: {str(e)}")
    print("La aplicacion se iniciara pero las funcionalidades de base de datos no estaran disponibles.\n")
    supabase = None
    supabase_admin = None

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# ============================================
# APLICACIÓN FASTAPI
# ============================================

app = FastAPI(
    title="Plan de Desarrollo Profesional",
    description="API para gestión de planes de desarrollo profesional",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ============================================
# MODELOS PYDANTIC
# ============================================

class UserCreate(BaseModel):
    email: str
    password: str
    nombre_completo: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str

class MonthlyPlan(BaseModel):
    mes: date
    competencias: Optional[List[str]] = []
    objetivos: Optional[str] = None
    fortalezas: Optional[List[str]] = []
    debilidades: Optional[List[str]] = []
    mejoras_hacer: Optional[str] = None
    herramientas_apoyo: Optional[List[str]] = []

class MonthlyReview(BaseModel):
    monthly_plan_id: str
    que_mejore: Optional[str] = None
    que_falta_mejorar: Optional[str] = None
    habilidades_desarrolladas: Optional[List[str]] = []
    propositos_proximo_mes: Optional[List[str]] = []
    momento_memorable: Optional[str] = None

class WeeklyLog(BaseModel):
    semana_inicio: date
    semana_fin: date
    logros: Optional[List[str]] = []
    desafios: Optional[List[str]] = []
    aprendizajes: Optional[str] = None
    reflexiones: Optional[str] = None
    nivel_energia: Optional[int] = Field(None, ge=1, le=5)
    nivel_satisfaccion: Optional[int] = Field(None, ge=1, le=5)

class DailyTask(BaseModel):
    fecha: date
    titulo: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = "personal"
    estado: Optional[str] = "pendiente"
    prioridad: Optional[str] = "media"
    tiempo_estimado: Optional[int] = None
    tiempo_real: Optional[int] = None
    orden: Optional[int] = 0
    tags: Optional[List[str]] = []
    notas: Optional[str] = None

class TaskUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    tiempo_real: Optional[int] = None
    orden: Optional[int] = None
    notas: Optional[str] = None

# ============================================
# AUTENTICACIÓN
# ============================================

def create_access_token(data: dict):
    """Crear token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificar token JWT"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# ============================================
# RUTAS - AUTENTICACIÓN
# ============================================

@app.post("/api/auth/register", response_model=Token)
async def register(user: UserCreate):
    """Registrar nuevo usuario"""
    try:
        # Crear usuario en Supabase Auth
        response = supabase_admin.auth.admin.create_user({
            "email": user.email,
            "password": user.password,
            "email_confirm": True
        })
        
        user_id = response.user.id
        
        # Crear perfil
        if user.nombre_completo:
            supabase_admin.table("user_profiles").insert({
                "id": user_id,
                "nombre_completo": user.nombre_completo
            }).execute()
        
        # Generar token
        access_token = create_access_token({"sub": user_id, "email": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_id,
            "email": user.email
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar usuario: {str(e)}")

@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin):
    """Iniciar sesión"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        access_token = create_access_token({
            "sub": response.user.id,
            "email": response.user.email
        })
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": response.user.id,
            "email": response.user.email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.get("/api/auth/me")
async def get_current_user(user_id: str = Depends(verify_token)):
    """Obtener información del usuario actual"""
    try:
        profile = supabase.table("user_profiles").select("*").eq("id", user_id).single().execute()
        return profile.data
    except:
        return {"id": user_id, "nombre_completo": None}

# ============================================
# RUTAS - PLANES MENSUALES
# ============================================

@app.post("/api/monthly/plans")
async def create_monthly_plan(plan: MonthlyPlan, user_id: str = Depends(verify_token)):
    """Crear plan mensual"""
    data = plan.dict()
    data["user_id"] = user_id
    
    response = supabase.table("monthly_plans").insert(data).execute()
    return response.data[0]

@app.get("/api/monthly/plans")
async def get_monthly_plans(user_id: str = Depends(verify_token), limit: int = 12):
    """Obtener planes mensuales del usuario"""
    response = supabase.table("monthly_plans") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("mes", desc=True) \
        .limit(limit) \
        .execute()
    return response.data

@app.get("/api/monthly/plans/{plan_id}")
async def get_monthly_plan(plan_id: str, user_id: str = Depends(verify_token)):
    """Obtener plan mensual específico"""
    response = supabase.table("monthly_plans") \
        .select("*") \
        .eq("id", plan_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

@app.put("/api/monthly/plans/{plan_id}")
async def update_monthly_plan(plan_id: str, plan: MonthlyPlan, user_id: str = Depends(verify_token)):
    """Actualizar plan mensual"""
    response = supabase.table("monthly_plans") \
        .update(plan.dict(exclude_unset=True)) \
        .eq("id", plan_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0]

@app.post("/api/monthly/reviews")
async def create_monthly_review(review: MonthlyReview, user_id: str = Depends(verify_token)):
    """Crear evaluación mensual"""
    data = review.dict()
    data["user_id"] = user_id
    
    response = supabase.table("monthly_reviews").insert(data).execute()
    return response.data[0]

@app.get("/api/monthly/reviews/{plan_id}")
async def get_monthly_review(plan_id: str, user_id: str = Depends(verify_token)):
    """Obtener evaluación mensual"""
    response = supabase.table("monthly_reviews") \
        .select("*") \
        .eq("monthly_plan_id", plan_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

# ============================================
# RUTAS - BITÁCORAS SEMANALES
# ============================================

@app.post("/api/weekly/logs")
async def create_weekly_log(log: WeeklyLog, user_id: str = Depends(verify_token)):
    """Crear bitácora semanal"""
    data = log.dict()
    data["user_id"] = user_id
    
    response = supabase.table("weekly_logs").insert(data).execute()
    return response.data[0]

@app.get("/api/weekly/logs")
async def get_weekly_logs(user_id: str = Depends(verify_token), limit: int = 20):
    """Obtener bitácoras semanales"""
    response = supabase.table("weekly_logs") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("semana_inicio", desc=True) \
        .limit(limit) \
        .execute()
    return response.data

@app.get("/api/weekly/logs/{log_id}")
async def get_weekly_log(log_id: str, user_id: str = Depends(verify_token)):
    """Obtener bitácora semanal específica"""
    response = supabase.table("weekly_logs") \
        .select("*") \
        .eq("id", log_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

# ============================================
# RUTAS - TAREAS DIARIAS
# ============================================

@app.post("/api/tasks")
async def create_task(task: DailyTask, user_id: str = Depends(verify_token)):
    """Crear tarea"""
    data = task.dict()
    data["user_id"] = user_id
    
    response = supabase.table("daily_tasks").insert(data).execute()
    return response.data[0]

@app.get("/api/tasks")
async def get_tasks(
    user_id: str = Depends(verify_token),
    fecha: Optional[date] = None,
    estado: Optional[str] = None,
    categoria: Optional[str] = None
):
    """Obtener tareas con filtros"""
    query = supabase.table("daily_tasks").select("*").eq("user_id", user_id)
    
    if fecha:
        query = query.eq("fecha", fecha.isoformat())
    if estado:
        query = query.eq("estado", estado)
    if categoria:
        query = query.eq("categoria", categoria)
    
    response = query.order("orden").order("created_at").execute()
    return response.data

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str, user_id: str = Depends(verify_token)):
    """Obtener tarea específica"""
    response = supabase.table("daily_tasks") \
        .select("*") \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: str, task: TaskUpdate, user_id: str = Depends(verify_token)):
    """Actualizar tarea"""
    data = task.dict(exclude_unset=True)
    
    # Si se marca como completada, agregar timestamp
    if data.get("estado") == "completada":
        data["completed_at"] = datetime.utcnow().isoformat()
    
    response = supabase.table("daily_tasks") \
        .update(data) \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0]

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str, user_id: str = Depends(verify_token)):
    """Eliminar tarea"""
    supabase.table("daily_tasks") \
        .delete() \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .execute()
    return {"message": "Tarea eliminada"}

# ============================================
# RUTAS - EVIDENCIAS (ARCHIVOS)
# ============================================

@app.post("/api/evidencias/upload")
async def upload_evidencia(
    file: UploadFile = File(...),
    task_id: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    user_id: str = Depends(verify_token)
):
    """Subir evidencia (archivo)"""
    try:
        # Validar tamaño
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(400, f"Archivo muy grande. Máximo {MAX_FILE_SIZE_MB}MB")
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{timestamp}_{file.filename}"
        
        # Guardar localmente (temporal)
        file_path = UPLOAD_DIR / filename
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(contents)
        
        # Subir a Supabase Storage
        try:
            storage_response = supabase.storage.from_(SUPABASE_BUCKET_NAME).upload(
                filename,
                contents,
                {"content-type": file.content_type}
            )
            
            # Obtener URL pública
            public_url = supabase.storage.from_(SUPABASE_BUCKET_NAME).get_public_url(filename)
            archivo_url = public_url
        except:
            # Si falla Supabase, usar archivo local
            archivo_url = f"/uploads/{filename}"
        
        # Determinar tipo de archivo
        tipo_archivo = "otro"
        if file.content_type.startswith("image/"):
            tipo_archivo = "imagen"
        elif file.content_type == "application/pdf":
            tipo_archivo = "pdf"
        elif "document" in file.content_type or "word" in file.content_type:
            tipo_archivo = "documento"
        
        # Guardar en BD
        evidencia_data = {
            "user_id": user_id,
            "task_id": task_id,
            "archivo_url": archivo_url,
            "archivo_nombre": file.filename,
            "tipo_archivo": tipo_archivo,
            "mime_type": file.content_type,
            "tamanio_kb": len(contents) // 1024,
            "descripcion": descripcion
        }
        
        response = supabase.table("evidencias").insert(evidencia_data).execute()
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(500, f"Error al subir archivo: {str(e)}")

@app.get("/api/evidencias")
async def get_evidencias(
    user_id: str = Depends(verify_token),
    task_id: Optional[str] = None
):
    """Obtener evidencias"""
    query = supabase.table("evidencias").select("*").eq("user_id", user_id)
    
    if task_id:
        query = query.eq("task_id", task_id)
    
    response = query.order("created_at", desc=True).execute()
    return response.data

@app.delete("/api/evidencias/{evidencia_id}")
async def delete_evidencia(evidencia_id: str, user_id: str = Depends(verify_token)):
    """Eliminar evidencia"""
    # Obtener evidencia
    evidencia = supabase.table("evidencias") \
        .select("*") \
        .eq("id", evidencia_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    
    # Intentar eliminar de Supabase Storage
    try:
        filename = evidencia.data["archivo_url"].split("/")[-1]
        supabase.storage.from_(SUPABASE_BUCKET_NAME).remove([filename])
    except:
        pass
    
    # Eliminar de BD
    supabase.table("evidencias").delete().eq("id", evidencia_id).execute()
    
    return {"message": "Evidencia eliminada"}

# ============================================
# RUTAS - DASHBOARD Y MÉTRICAS
# ============================================

@app.get("/api/dashboard/summary")
async def get_dashboard_summary(user_id: str = Depends(verify_token)):
    """Obtener resumen del dashboard"""
    today = date.today()
    first_day_month = today.replace(day=1)
    
    # Tareas del mes
    tasks_month = supabase.table("daily_tasks") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("fecha", first_day_month.isoformat()) \
        .execute()
    
    tasks_data = tasks_month.data
    total_tasks = len(tasks_data)
    completed_tasks = len([t for t in tasks_data if t["estado"] == "completada"])
    pending_tasks = len([t for t in tasks_data if t["estado"] == "pendiente"])
    
    # Plan mensual actual
    current_plan = supabase.table("monthly_plans") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("mes", first_day_month.isoformat()) \
        .limit(1) \
        .execute()
    
    # Bitácoras del mes
    weekly_logs = supabase.table("weekly_logs") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("semana_inicio", first_day_month.isoformat()) \
        .execute()
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_rate": round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0,
        "current_month_plan": current_plan.data[0] if current_plan.data else None,
        "weekly_logs_count": len(weekly_logs.data),
        "today": today.isoformat()
    }

@app.get("/api/dashboard/tasks-by-day")
async def get_tasks_by_day(user_id: str = Depends(verify_token), days: int = 7):
    """Obtener tareas agrupadas por día (últimos N días)"""
    start_date = date.today() - timedelta(days=days)
    
    tasks = supabase.table("daily_tasks") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("fecha", start_date.isoformat()) \
        .execute()
    
    # Agrupar por fecha
    tasks_by_day = {}
    for task in tasks.data:
        task_date = task["fecha"]
        if task_date not in tasks_by_day:
            tasks_by_day[task_date] = {"total": 0, "completadas": 0, "pendientes": 0}
        
        tasks_by_day[task_date]["total"] += 1
        if task["estado"] == "completada":
            tasks_by_day[task_date]["completadas"] += 1
        elif task["estado"] == "pendiente":
            tasks_by_day[task_date]["pendientes"] += 1
    
    return tasks_by_day

@app.get("/api/competencias")
async def get_competencias():
    """Obtener catálogo de competencias"""
    response = supabase.table("competencias").select("*").execute()
    return response.data

# ============================================
# RUTAS - PÁGINAS HTML
# ============================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Página principal - redireccionar a login o dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Página del dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    """Página de tareas"""
    return templates.TemplateResponse("tasks.html", {"request": request})

@app.get("/monthly", response_class=HTMLResponse)
async def monthly_page(request: Request):
    """Página de planes mensuales"""
    return templates.TemplateResponse("monthly.html", {"request": request})

@app.get("/weekly", response_class=HTMLResponse)
async def weekly_page(request: Request):
    """Página de bitácoras semanales"""
    return templates.TemplateResponse("weekly.html", {"request": request})

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check():
    """Verificar estado de la aplicación"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
