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

# Configuración de entorno
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"
ALLOWED_ORIGINS_LIST = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",")

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

# Advertencia de seguridad en producción
if IS_PRODUCTION and SECRET_KEY == "tu-secret-key-super-segura":
    print("\n" + "="*70)
    print("⚠️  ADVERTENCIA DE SEGURIDAD")
    print("="*70)
    print("Estás usando el SECRET_KEY por defecto en producción.")
    print("Por favor, genera un SECRET_KEY seguro y configúralo en las")
    print("variables de entorno de tu plataforma de hosting.")
    print("="*70 + "\n")

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
    version="1.0.0",
    docs_url=None if IS_PRODUCTION else "/docs",  # Desactivar docs en producción
    redoc_url=None if IS_PRODUCTION else "/redoc",  # Desactivar redoc en producción
    openapi_url=None if IS_PRODUCTION else "/openapi.json"  # Desactivar OpenAPI en producción
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS_LIST,
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

class CompetenciaProgress(BaseModel):
    nombre: str
    progreso_inicio: int = 0  # 0-100
    progreso_actual: int = 0  # 0-100
    progreso_fin: Optional[int] = None  # 0-100
    evidencias: Optional[List[str]] = []
    notas: Optional[str] = None

class MonthlyPlan(BaseModel):
    mes: date
    competencias_trabajar: Optional[str] = None  # Texto libre
    competencias: Optional[List[dict]] = []  # Lista de competencias con progreso
    que_quiero_lograr: Optional[str] = None
    actividades_lograr: Optional[List[dict]] = []  # Lista de actividades para lograr objetivos
    mis_fortalezas: Optional[str] = None
    mis_debilidades: Optional[str] = None
    objetivos: Optional[str] = None
    fortalezas: Optional[List[str]] = []
    debilidades: Optional[List[str]] = []
    mejoras_hacer: Optional[str] = None
    herramientas_apoyo: Optional[List[str]] = []

class MonthlyReview(BaseModel):
    monthly_plan_id: str
    que_mejore: Optional[str] = None
    que_falta_mejorar: Optional[str] = None
    habilidades_desarrolladas: Optional[str] = None
    momento_memorable: Optional[str] = None
    propositos_proximo_mes: Optional[List[str]] = []

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
    titulo: str
    descripcion: Optional[str] = None

    # Fechas (solo inicio y fin)
    fecha_inicio: date  # Obligatorio
    fecha_fin: date  # Obligatorio

    # Clasificación y categorización
    clasificacion: Optional[str] = None  # desarrollo, investigacion, documentacion, etc.
    categoria: Optional[str] = "personal"  # aprendizaje, compromiso, competencia, personal

    # Estado y prioridad
    estado: Optional[str] = "pendiente"  # pendiente, en_progreso, completada, cancelada
    prioridad: Optional[str] = "media"  # baja, media, alta

    # Progreso y tiempo
    progreso: Optional[int] = 0  # 0-100
    tiempo_estimado: Optional[int] = None
    tiempo_real: Optional[int] = None

    # Jerarquía
    parent_task_id: Optional[str] = None  # UUID de la tarea padre
    es_macrotarea: Optional[bool] = False

    # Otros
    orden: Optional[int] = 0
    tags: Optional[List[str]] = []
    notas: Optional[str] = None
    observaciones: Optional[str] = None

class TaskUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None

    # Fechas
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    # Clasificación y categorización
    clasificacion: Optional[str] = None
    categoria: Optional[str] = None

    # Estado y prioridad
    estado: Optional[str] = None
    prioridad: Optional[str] = None

    # Progreso y tiempo
    progreso: Optional[int] = None
    tiempo_estimado: Optional[int] = None
    tiempo_real: Optional[int] = None

    # Jerarquía
    parent_task_id: Optional[str] = None
    es_macrotarea: Optional[bool] = None

    # Otros
    orden: Optional[int] = None
    notas: Optional[str] = None
    observaciones: Optional[str] = None

class Actividad(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_fin: date
    clasificacion: Optional[str] = None  # proyecto, curso, certificacion, objetivo
    estado: Optional[str] = "en_progreso"  # en_progreso, completada, pausada, cancelada
    prioridad: Optional[str] = "media"  # baja, media, alta
    grupo: Optional[str] = None  # Para agrupar actividades relacionadas
    color: Optional[str] = None  # Color para identificar visualmente
    progreso: Optional[int] = 0  # Porcentaje 0-100
    tags: Optional[List[str]] = []
    notas: Optional[str] = None

class ActividadUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    clasificacion: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    grupo: Optional[str] = None
    color: Optional[str] = None
    progreso: Optional[int] = None
    notas: Optional[str] = None

class UserConfig(BaseModel):
    clasificaciones: Optional[List[str]] = [
        'desarrollo', 'investigacion', 'documentacion', 'reunion',
        'estudio', 'revision', 'planificacion', 'testing'
    ]
    categorias: Optional[List[str]] = [
        'aprendizaje', 'compromiso', 'competencia', 'personal'
    ]

class UserConfigUpdate(BaseModel):
    clasificaciones: Optional[List[str]] = None
    categorias: Optional[List[str]] = None

# ============================================
# FINANCIAL MODELS
# ============================================

class FinancialCategory(BaseModel):
    nombre: str
    tipo: str  # 'ingreso', 'gasto', 'deuda'
    color: Optional[str] = '#6366f1'
    icono: Optional[str] = None
    descripcion: Optional[str] = None

class FinancialRecord(BaseModel):
    mes: date
    fecha_transaccion: date
    tipo: str  # 'ingreso', 'gasto', 'deuda', 'pago_recurrente'
    monto: float
    descripcion: Optional[str] = None
    category_id: Optional[str] = None
    categoria_nombre: Optional[str] = None
    es_recurrente: Optional[bool] = False
    recurrencia_tipo: Optional[str] = None
    deuda_saldo_pendiente: Optional[float] = None
    deuda_pagada: Optional[bool] = False

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

    # Verificar si ya existe un plan para este mes
    mes_str = plan.mes.isoformat() if isinstance(plan.mes, date) else plan.mes
    existing = supabase_admin.table("monthly_plans") \
        .select("id") \
        .eq("user_id", user_id) \
        .eq("mes", mes_str) \
        .execute()

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un plan para el mes {plan.mes}"
        )

    data = plan.dict()
    data["user_id"] = user_id

    # Convertir fecha a string para JSON
    if isinstance(data.get("mes"), date):
        data["mes"] = data["mes"].isoformat()

    response = supabase_admin.table("monthly_plans").insert(data).execute()
    return response.data[0]

@app.get("/api/monthly/plans")
async def get_monthly_plans(user_id: str = Depends(verify_token), limit: int = 12):
    """Obtener planes mensuales del usuario"""
    response = supabase_admin.table("monthly_plans") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("mes", desc=True) \
        .limit(limit) \
        .execute()
    return response.data

@app.get("/api/monthly/plans/{plan_id}")
async def get_monthly_plan(plan_id: str, user_id: str = Depends(verify_token)):
    """Obtener plan mensual específico"""
    response = supabase_admin.table("monthly_plans") \
        .select("*") \
        .eq("id", plan_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

@app.put("/api/monthly/plans/{plan_id}")
async def update_monthly_plan(plan_id: str, plan: MonthlyPlan, user_id: str = Depends(verify_token)):
    """Actualizar plan mensual"""
    data = plan.dict(exclude_unset=True)

    # Convertir fecha a string para JSON
    if isinstance(data.get("mes"), date):
        data["mes"] = data["mes"].isoformat()

    response = supabase_admin.table("monthly_plans") \
        .update(data) \
        .eq("id", plan_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0]

@app.post("/api/monthly/reviews")
async def create_monthly_review(review: MonthlyReview, user_id: str = Depends(verify_token)):
    """Crear evaluación mensual"""
    data = review.dict()
    data["user_id"] = user_id
    
    response = supabase_admin.table("monthly_reviews").insert(data).execute()
    return response.data[0]

@app.get("/api/monthly/reviews/{plan_id}")
async def get_monthly_review(plan_id: str, user_id: str = Depends(verify_token)):
    """Obtener evaluación mensual"""
    response = supabase_admin.table("monthly_reviews") \
        .select("*") \
        .eq("monthly_plan_id", plan_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

@app.put("/api/monthly/plans/{plan_id}/competencias")
async def update_competencias_progress(
    plan_id: str,
    competencias: List[dict],
    user_id: str = Depends(verify_token)
):
    """Actualizar progreso de competencias de un plan mensual"""
    response = supabase_admin.table("monthly_plans") \
        .update({"competencias": competencias}) \
        .eq("id", plan_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0]

@app.get("/api/monthly/evolution")
async def get_competencias_evolution(user_id: str = Depends(verify_token), months: int = 6):
    """Obtener evolución de competencias en los últimos N meses"""
    # Obtener planes de los últimos N meses
    response = supabase_admin.table("monthly_plans") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("mes", desc=True) \
        .limit(months) \
        .execute()

    plans = response.data

    # Compilar evolución de competencias
    evolution = {}
    for plan in plans:
        if plan.get("competencias"):
            mes = plan["mes"]
            for comp in plan["competencias"]:
                nombre = comp.get("nombre")
                if nombre:
                    if nombre not in evolution:
                        evolution[nombre] = []
                    evolution[nombre].append({
                        "mes": mes,
                        "progreso_inicio": comp.get("progreso_inicio", 0),
                        "progreso_actual": comp.get("progreso_actual", 0),
                        "progreso_fin": comp.get("progreso_fin")
                    })

    return {
        "evolution": evolution,
        "plans": plans
    }

@app.get("/api/monthly/comparison/{plan_id}")
async def get_plan_comparison(plan_id: str, user_id: str = Depends(verify_token)):
    """Obtener comparación inicio vs fin de mes para un plan específico"""
    # Obtener el plan
    plan_response = supabase_admin.table("monthly_plans") \
        .select("*") \
        .eq("id", plan_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()

    plan = plan_response.data

    # Obtener la review
    review_response = supabase_admin.table("monthly_reviews") \
        .select("*") \
        .eq("monthly_plan_id", plan_id) \
        .eq("user_id", user_id) \
        .execute()

    review = review_response.data[0] if review_response.data else None

    # Calcular métricas de comparación
    competencias = plan.get("competencias", [])
    comparison = {
        "plan": plan,
        "review": review,
        "competencias_stats": {
            "total": len(competencias),
            "con_progreso": len([c for c in competencias if c.get("progreso_fin") is not None]),
            "promedio_progreso_inicio": sum([c.get("progreso_inicio", 0) for c in competencias]) / len(competencias) if competencias else 0,
            "promedio_progreso_fin": sum([c.get("progreso_fin", 0) for c in competencias if c.get("progreso_fin") is not None]) / len([c for c in competencias if c.get("progreso_fin") is not None]) if [c for c in competencias if c.get("progreso_fin") is not None] else 0,
            "competencias": competencias
        }
    }

    return comparison

# ============================================
# RUTAS - BITÁCORAS SEMANALES
# ============================================

@app.post("/api/weekly/logs")
async def create_weekly_log(log: WeeklyLog, user_id: str = Depends(verify_token)):
    """Crear bitácora semanal"""
    data = log.dict()
    data["user_id"] = user_id

    # Convertir fechas a string para JSON
    if isinstance(data.get("semana_inicio"), date):
        data["semana_inicio"] = data["semana_inicio"].isoformat()
    if isinstance(data.get("semana_fin"), date):
        data["semana_fin"] = data["semana_fin"].isoformat()

    response = supabase_admin.table("weekly_logs").insert(data).execute()
    return response.data[0]

@app.get("/api/weekly/logs")
async def get_weekly_logs(user_id: str = Depends(verify_token), limit: int = 20):
    """Obtener bitácoras semanales"""
    response = supabase_admin.table("weekly_logs") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("semana_inicio", desc=True) \
        .limit(limit) \
        .execute()
    return response.data

@app.get("/api/weekly/logs/{log_id}")
async def get_weekly_log(log_id: str, user_id: str = Depends(verify_token)):
    """Obtener bitácora semanal específica"""
    response = supabase_admin.table("weekly_logs") \
        .select("*") \
        .eq("id", log_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

@app.put("/api/weekly/logs/{log_id}")
async def update_weekly_log(log_id: str, log: WeeklyLog, user_id: str = Depends(verify_token)):
    """Actualizar bitácora semanal"""
    data = log.dict(exclude_unset=True)

    # Convertir fechas a string para JSON
    if isinstance(data.get("semana_inicio"), date):
        data["semana_inicio"] = data["semana_inicio"].isoformat()
    if isinstance(data.get("semana_fin"), date):
        data["semana_fin"] = data["semana_fin"].isoformat()

    response = supabase_admin.table("weekly_logs") \
        .update(data) \
        .eq("id", log_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0]

# ============================================
# RUTAS - TAREAS DIARIAS
# ============================================

@app.post("/api/tasks")
async def create_task(task: DailyTask, user_id: str = Depends(verify_token)):
    """Crear tarea"""
    data = task.dict()
    data["user_id"] = user_id

    # Convertir fechas a string para JSON
    if isinstance(data.get("fecha_inicio"), date):
        data["fecha_inicio"] = data["fecha_inicio"].isoformat()
    if isinstance(data.get("fecha_fin"), date):
        data["fecha_fin"] = data["fecha_fin"].isoformat()

    # Limpiar valores vacíos para campos UUID (evitar error de PostgreSQL)
    if data.get("parent_task_id") == "" or data.get("parent_task_id") is None:
        data["parent_task_id"] = None

    # Limpiar otros campos opcionales vacíos
    if data.get("clasificacion") == "":
        data["clasificacion"] = None

    response = supabase_admin.table("daily_tasks").insert(data).execute()
    return response.data[0]

@app.get("/api/tasks")
async def get_tasks(
    user_id: str = Depends(verify_token),
    estado: Optional[str] = None,
    categoria: Optional[str] = None,
    clasificacion: Optional[str] = None
):
    """Obtener tareas con filtros"""
    query = supabase_admin.table("daily_tasks").select("*").eq("user_id", user_id)

    if estado:
        query = query.eq("estado", estado)
    if categoria:
        query = query.eq("categoria", categoria)
    if clasificacion:
        query = query.eq("clasificacion", clasificacion)

    response = query.order("orden").order("created_at").execute()
    return response.data

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str, user_id: str = Depends(verify_token)):
    """Obtener tarea específica"""
    response = supabase_admin.table("daily_tasks") \
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

    # Convertir fechas a string para JSON
    if isinstance(data.get("fecha_inicio"), date):
        data["fecha_inicio"] = data["fecha_inicio"].isoformat()
    if isinstance(data.get("fecha_fin"), date):
        data["fecha_fin"] = data["fecha_fin"].isoformat()

    # Si se marca como completada, agregar timestamp y progreso 100%
    if data.get("estado") == "completada":
        data["completed_at"] = datetime.utcnow().isoformat()
        data["progreso"] = 100

    response = supabase_admin.table("daily_tasks") \
        .update(data) \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0]

@app.get("/api/tasks/{task_id}/subtareas")
async def get_subtareas(task_id: str, user_id: str = Depends(verify_token)):
    """Obtener todas las subtareas de una macrotarea"""
    # Primero verificar que la tarea pertenece al usuario
    parent_task = supabase_admin.table("daily_tasks") \
        .select("*") \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()

    if not parent_task.data:
        raise HTTPException(404, "Tarea no encontrada")

    # Obtener subtareas
    subtareas = supabase_admin.table("daily_tasks") \
        .select("*") \
        .eq("parent_task_id", task_id) \
        .order("orden") \
        .order("created_at") \
        .execute()

    return subtareas.data

@app.put("/api/tasks/{task_id}/recalcular-progreso")
async def recalcular_progreso(task_id: str, user_id: str = Depends(verify_token)):
    """Recalcular progreso de una macrotarea basándose en sus subtareas"""
    # Verificar que la tarea existe y pertenece al usuario
    task = supabase_admin.table("daily_tasks") \
        .select("*") \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()

    if not task.data:
        raise HTTPException(404, "Tarea no encontrada")

    if not task.data.get("es_macrotarea"):
        raise HTTPException(400, "La tarea no es una macrotarea")

    # Obtener subtareas
    subtareas = supabase_admin.table("daily_tasks") \
        .select("progreso") \
        .eq("parent_task_id", task_id) \
        .execute()

    if not subtareas.data:
        return {"message": "No hay subtareas", "progreso": 0}

    # Calcular promedio
    total = sum(st.get("progreso", 0) for st in subtareas.data)
    promedio = total // len(subtareas.data)

    # Actualizar macrotarea
    updated = supabase_admin.table("daily_tasks") \
        .update({"progreso": promedio}) \
        .eq("id", task_id) \
        .execute()

    return {"message": "Progreso recalculado", "progreso": promedio}

@app.put("/api/tasks/{task_id}/recalcular-fechas")
async def recalcular_fechas(task_id: str, user_id: str = Depends(verify_token)):
    """Recalcular fechas de una macrotarea basándose en sus subtareas"""
    # Verificar que la tarea existe y pertenece al usuario
    task = supabase_admin.table("daily_tasks") \
        .select("*") \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()

    if not task.data:
        raise HTTPException(404, "Tarea no encontrada")

    if not task.data.get("es_macrotarea"):
        raise HTTPException(400, "La tarea no es una macrotarea")

    # Obtener subtareas
    subtareas = supabase_admin.table("daily_tasks") \
        .select("fecha_inicio, fecha_fin") \
        .eq("parent_task_id", task_id) \
        .execute()

    if not subtareas.data or len(subtareas.data) == 0:
        return {"message": "No hay subtareas", "fecha_inicio": None, "fecha_fin": None}

    # Filtrar subtareas que tengan fechas válidas
    fechas_inicio = [st["fecha_inicio"] for st in subtareas.data if st.get("fecha_inicio")]
    fechas_fin = [st["fecha_fin"] for st in subtareas.data if st.get("fecha_fin")]

    if not fechas_inicio or not fechas_fin:
        return {"message": "Las subtareas no tienen fechas definidas", "fecha_inicio": None, "fecha_fin": None}

    # Calcular MIN(fecha_inicio) y MAX(fecha_fin)
    fecha_inicio_min = min(fechas_inicio)
    fecha_fin_max = max(fechas_fin)

    # Actualizar macrotarea
    updated = supabase_admin.table("daily_tasks") \
        .update({
            "fecha_inicio": fecha_inicio_min,
            "fecha_fin": fecha_fin_max
        }) \
        .eq("id", task_id) \
        .execute()

    return {
        "message": "Fechas recalculadas",
        "fecha_inicio": fecha_inicio_min,
        "fecha_fin": fecha_fin_max
    }

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str, user_id: str = Depends(verify_token)):
    """Eliminar tarea"""
    supabase_admin.table("daily_tasks") \
        .delete() \
        .eq("id", task_id) \
        .eq("user_id", user_id) \
        .execute()
    return {"message": "Tarea eliminada"}

# ============================================
# RUTAS - ACTIVIDADES
# ============================================

@app.post("/api/actividades")
async def create_actividad(actividad: Actividad, user_id: str = Depends(verify_token)):
    """Crear actividad"""
    data = actividad.dict()
    data["user_id"] = user_id

    # Convertir fechas a string para JSON
    if isinstance(data.get("fecha_inicio"), date):
        data["fecha_inicio"] = data["fecha_inicio"].isoformat()
    if isinstance(data.get("fecha_fin"), date):
        data["fecha_fin"] = data["fecha_fin"].isoformat()

    response = supabase_admin.table("actividades").insert(data).execute()
    return response.data[0]

@app.get("/api/actividades")
async def get_actividades(
    user_id: str = Depends(verify_token),
    estado: Optional[str] = None,
    clasificacion: Optional[str] = None,
    grupo: Optional[str] = None
):
    """Obtener actividades con filtros opcionales"""
    query = supabase_admin.table("actividades").select("*").eq("user_id", user_id)

    if estado:
        query = query.eq("estado", estado)
    if clasificacion:
        query = query.eq("clasificacion", clasificacion)
    if grupo:
        query = query.eq("grupo", grupo)

    response = query.order("fecha_inicio", desc=True).execute()
    return response.data

@app.get("/api/actividades/{actividad_id}")
async def get_actividad(actividad_id: str, user_id: str = Depends(verify_token)):
    """Obtener actividad específica"""
    response = supabase_admin.table("actividades") \
        .select("*") \
        .eq("id", actividad_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data

@app.put("/api/actividades/{actividad_id}")
async def update_actividad(
    actividad_id: str,
    actividad: ActividadUpdate,
    user_id: str = Depends(verify_token)
):
    """Actualizar actividad"""
    data = actividad.dict(exclude_unset=True)

    # Convertir fechas a string para JSON
    if isinstance(data.get("fecha_inicio"), date):
        data["fecha_inicio"] = data["fecha_inicio"].isoformat()
    if isinstance(data.get("fecha_fin"), date):
        data["fecha_fin"] = data["fecha_fin"].isoformat()

    response = supabase_admin.table("actividades") \
        .update(data) \
        .eq("id", actividad_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0]

@app.delete("/api/actividades/{actividad_id}")
async def delete_actividad(actividad_id: str, user_id: str = Depends(verify_token)):
    """Eliminar actividad"""
    supabase_admin.table("actividades") \
        .delete() \
        .eq("id", actividad_id) \
        .eq("user_id", user_id) \
        .execute()
    return {"message": "Actividad eliminada"}

@app.get("/api/actividades/grupos/list")
async def get_grupos_actividades(user_id: str = Depends(verify_token)):
    """Obtener lista de grupos únicos de actividades del usuario"""
    response = supabase_admin.table("actividades") \
        .select("grupo") \
        .eq("user_id", user_id) \
        .execute()

    # Extraer grupos únicos (sin None/null)
    grupos = set()
    for item in response.data:
        if item.get("grupo"):
            grupos.add(item["grupo"])

    return {"grupos": sorted(list(grupos))}

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
        
        response = supabase_admin.table("evidencias").insert(evidencia_data).execute()
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(500, f"Error al subir archivo: {str(e)}")

@app.get("/api/evidencias")
async def get_evidencias(
    user_id: str = Depends(verify_token),
    task_id: Optional[str] = None
):
    """Obtener evidencias"""
    query = supabase_admin.table("evidencias").select("*").eq("user_id", user_id)
    
    if task_id:
        query = query.eq("task_id", task_id)
    
    response = query.order("created_at", desc=True).execute()
    return response.data

@app.delete("/api/evidencias/{evidencia_id}")
async def delete_evidencia(evidencia_id: str, user_id: str = Depends(verify_token)):
    """Eliminar evidencia"""
    # Obtener evidencia
    evidencia = supabase_admin.table("evidencias") \
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
    supabase_admin.table("evidencias").delete().eq("id", evidencia_id).execute()
    
    return {"message": "Evidencia eliminada"}

# ============================================
# RUTAS - CONFIGURACIÓN DE USUARIO
# ============================================

@app.get("/api/config")
async def get_user_config(user_id: str = Depends(verify_token)):
    """Obtener configuración del usuario (clasificaciones y categorías personalizadas)"""
    try:
        # Intentar obtener configuración existente
        response = supabase_admin.table("user_config") \
            .select("*") \
            .eq("user_id", user_id) \
            .single() \
            .execute()

        return response.data
    except Exception as e:
        # Si no existe, crear con valores por defecto
        default_config = {
            "user_id": user_id,
            "clasificaciones": [
                'desarrollo', 'investigacion', 'documentacion', 'reunion',
                'estudio', 'revision', 'planificacion', 'testing'
            ],
            "categorias": [
                'aprendizaje', 'compromiso', 'competencia', 'personal'
            ]
        }

        response = supabase_admin.table("user_config").insert(default_config).execute()
        return response.data[0]

@app.put("/api/config")
async def update_user_config(config: UserConfigUpdate, user_id: str = Depends(verify_token)):
    """Actualizar configuración del usuario"""
    data = config.dict(exclude_unset=True)

    # Intentar actualizar
    try:
        response = supabase_admin.table("user_config") \
            .update(data) \
            .eq("user_id", user_id) \
            .execute()

        if response.data:
            return response.data[0]
        else:
            # Si no existe, crear
            data["user_id"] = user_id
            response = supabase_admin.table("user_config").insert(data).execute()
            return response.data[0]
    except Exception as e:
        raise HTTPException(500, f"Error al actualizar configuración: {str(e)}")

@app.post("/api/config/clasificaciones")
async def add_clasificacion(clasificacion: dict, user_id: str = Depends(verify_token)):
    """Agregar una nueva clasificación personalizada"""
    nueva_clasificacion = clasificacion.get("nombre")

    if not nueva_clasificacion:
        raise HTTPException(400, "Nombre de clasificación requerido")

    # Obtener configuración actual
    config = await get_user_config(user_id)
    clasificaciones_actuales = config.get("clasificaciones", [])

    # Agregar si no existe
    if nueva_clasificacion not in clasificaciones_actuales:
        clasificaciones_actuales.append(nueva_clasificacion)

        response = supabase_admin.table("user_config") \
            .update({"clasificaciones": clasificaciones_actuales}) \
            .eq("user_id", user_id) \
            .execute()

        return {"message": "Clasificación agregada", "clasificaciones": clasificaciones_actuales}

    return {"message": "Clasificación ya existe", "clasificaciones": clasificaciones_actuales}

@app.post("/api/config/categorias")
async def add_categoria(categoria: dict, user_id: str = Depends(verify_token)):
    """Agregar una nueva categoría personalizada"""
    nueva_categoria = categoria.get("nombre")

    if not nueva_categoria:
        raise HTTPException(400, "Nombre de categoría requerido")

    # Obtener configuración actual
    config = await get_user_config(user_id)
    categorias_actuales = config.get("categorias", [])

    # Agregar si no existe
    if nueva_categoria not in categorias_actuales:
        categorias_actuales.append(nueva_categoria)

        response = supabase_admin.table("user_config") \
            .update({"categorias": categorias_actuales}) \
            .eq("user_id", user_id) \
            .execute()

        return {"message": "Categoría agregada", "categorias": categorias_actuales}

    return {"message": "Categoría ya existe", "categorias": categorias_actuales}

# ============================================
# RUTAS - DASHBOARD Y MÉTRICAS
# ============================================

@app.get("/api/dashboard/summary")
async def get_dashboard_summary(user_id: str = Depends(verify_token)):
    """Obtener resumen del dashboard"""
    today = date.today()
    first_day_month = today.replace(day=1)
    
    # Tareas del mes (filtra por fecha_inicio >= primer día del mes)
    tasks_month = supabase_admin.table("daily_tasks") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("fecha_inicio", first_day_month.isoformat()) \
        .execute()

    tasks_data = tasks_month.data
    total_tasks = len(tasks_data)
    completed_tasks = len([t for t in tasks_data if t["estado"] == "completada"])
    pending_tasks = len([t for t in tasks_data if t["estado"] == "pendiente"])
    
    # Plan mensual actual
    current_plan = supabase_admin.table("monthly_plans") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("mes", first_day_month.isoformat()) \
        .limit(1) \
        .execute()
    
    # Bitácoras del mes
    weekly_logs = supabase_admin.table("weekly_logs") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("semana_inicio", first_day_month.isoformat()) \
        .execute()
    
    return {
        "totalTasks": total_tasks,
        "completedTasks": completed_tasks,
        "pendingTasks": pending_tasks,
        "completionRate": round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0,
        "currentMonthPlan": current_plan.data[0] if current_plan.data else None,
        "weeklyLogsCount": len(weekly_logs.data),
        "today": today.isoformat()
    }

@app.get("/api/dashboard/tasks-by-day")
async def get_tasks_by_day(user_id: str = Depends(verify_token), days: int = 7):
    """Obtener tareas agrupadas por día de inicio (últimos N días)"""
    start_date = date.today() - timedelta(days=days)

    tasks = supabase_admin.table("daily_tasks") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("fecha_inicio", start_date.isoformat()) \
        .execute()

    # Agrupar por fecha_inicio
    tasks_by_day = {}
    for task in tasks.data:
        task_date = task.get("fecha_inicio")
        if not task_date:
            continue

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
    response = supabase_admin.table("competencias").select("*").execute()
    return response.data

# ============================================
# RUTAS - CONTROL FINANCIERO
# ============================================

@app.post("/api/financial/categories")
async def create_financial_category(category: FinancialCategory, user_id: str = Depends(verify_token)):
    """Crear categoría financiera"""
    data = category.dict()
    data["user_id"] = user_id
    response = supabase_admin.table("financial_categories").insert(data).execute()
    return response.data[0]

@app.get("/api/financial/categories")
async def get_financial_categories(user_id: str = Depends(verify_token), tipo: Optional[str] = None):
    """Obtener categorías financieras"""
    query = supabase_admin.table("financial_categories").select("*").eq("user_id", user_id)
    if tipo:
        query = query.eq("tipo", tipo)
    response = query.order("nombre").execute()
    return response.data

@app.post("/api/financial/records")
async def create_financial_record(record: FinancialRecord, user_id: str = Depends(verify_token)):
    """Crear registro financiero"""
    data = record.dict()
    data["user_id"] = user_id

    if isinstance(data.get("mes"), date):
        data["mes"] = data["mes"].isoformat()
    if isinstance(data.get("fecha_transaccion"), date):
        data["fecha_transaccion"] = data["fecha_transaccion"].isoformat()

    # Obtener nombre de categoría
    if data.get("category_id"):
        try:
            cat = supabase_admin.table("financial_categories") \
                .select("nombre").eq("id", data["category_id"]).single().execute()
            data["categoria_nombre"] = cat.data["nombre"]
        except:
            pass

    response = supabase_admin.table("financial_records").insert(data).execute()
    return response.data[0]

@app.get("/api/financial/records")
async def get_financial_records(
    user_id: str = Depends(verify_token),
    mes: Optional[str] = None,
    tipo: Optional[str] = None,
    limit: int = 100
):
    """Obtener registros financieros"""
    query = supabase_admin.table("financial_records").select("*").eq("user_id", user_id)
    if mes:
        query = query.eq("mes", mes)
    if tipo:
        query = query.eq("tipo", tipo)
    response = query.order("fecha_transaccion", desc=True).limit(limit).execute()
    return response.data

@app.delete("/api/financial/records/{record_id}")
async def delete_financial_record(record_id: str, user_id: str = Depends(verify_token)):
    """Eliminar registro financiero"""
    supabase_admin.table("financial_records").delete().eq("id", record_id).eq("user_id", user_id).execute()
    return {"message": "Registro eliminado"}

@app.get("/api/financial/summary")
async def get_financial_summary(user_id: str = Depends(verify_token), mes: Optional[str] = None):
    """Obtener resumen financiero del mes"""
    if not mes:
        mes = date.today().replace(day=1).isoformat()

    try:
        summary = supabase_admin.table("financial_monthly_summary") \
            .select("*").eq("user_id", user_id).eq("mes", mes).single().execute()
        summary_data = summary.data
    except:
        summary_data = {
            "user_id": user_id,
            "mes": mes,
            "total_ingresos": 0,
            "total_gastos": 0,
            "total_deudas": 0,
            "balance": 0,
            "tasa_ahorro": 0
        }

    # Obtener desglose por categoría
    records = supabase_admin.table("financial_records") \
        .select("*").eq("user_id", user_id).eq("mes", mes).execute()

    gastos_por_categoria = {}
    ingresos_por_categoria = {}
    deudas_por_categoria = {}

    for record in records.data:
        cat_name = record.get("categoria_nombre") or "Sin categoría"
        monto = float(record.get("monto", 0))

        if record["tipo"] == "gasto":
            gastos_por_categoria[cat_name] = gastos_por_categoria.get(cat_name, 0) + monto
        elif record["tipo"] == "ingreso":
            ingresos_por_categoria[cat_name] = ingresos_por_categoria.get(cat_name, 0) + monto
        elif record["tipo"] == "deuda":
            deudas_por_categoria[cat_name] = deudas_por_categoria.get(cat_name, 0) + monto

    summary_data["gastos_por_categoria"] = [{"categoria": k, "monto": v} for k, v in gastos_por_categoria.items()]
    summary_data["ingresos_por_categoria"] = [{"categoria": k, "monto": v} for k, v in ingresos_por_categoria.items()]
    summary_data["deudas_por_categoria"] = [{"categoria": k, "monto": v} for k, v in deudas_por_categoria.items()]

    return summary_data

@app.post("/api/financial/initialize")
async def initialize_financial_categories(user_id: str = Depends(verify_token)):
    """Inicializar categorías predeterminadas"""
    supabase_admin.rpc("create_default_financial_categories", {"p_user_id": user_id}).execute()
    return {"message": "Categorías inicializadas"}

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
