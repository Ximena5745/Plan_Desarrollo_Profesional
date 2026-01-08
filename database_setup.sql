-- ================================================
-- PLAN DE DESARROLLO PROFESIONAL - DATABASE SETUP
-- ================================================
-- Ejecutar este script en Supabase SQL Editor
-- ================================================

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================
-- TABLA: PLANES MENSUALES
-- ================================================
CREATE TABLE IF NOT EXISTS monthly_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    mes DATE NOT NULL,
    
    -- Sección: Inicio de Mes
    competencias TEXT[],
    objetivos TEXT,
    fortalezas TEXT[],
    debilidades TEXT[],
    mejoras_hacer TEXT,
    herramientas_apoyo TEXT[],
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraint: Un plan por mes por usuario
    UNIQUE(user_id, mes)
);

CREATE INDEX idx_monthly_plans_user ON monthly_plans(user_id);
CREATE INDEX idx_monthly_plans_mes ON monthly_plans(mes);

-- ================================================
-- TABLA: EVALUACIÓN MENSUAL (FIN DE MES)
-- ================================================
CREATE TABLE IF NOT EXISTS monthly_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    monthly_plan_id UUID REFERENCES monthly_plans(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    
    -- Sección: Fin de Mes
    que_mejore TEXT,
    que_falta_mejorar TEXT,
    habilidades_desarrolladas TEXT[],
    propositos_proximo_mes TEXT[],
    momento_memorable TEXT,
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraint: Una evaluación por plan
    UNIQUE(monthly_plan_id)
);

CREATE INDEX idx_monthly_reviews_user ON monthly_reviews(user_id);
CREATE INDEX idx_monthly_reviews_plan ON monthly_reviews(monthly_plan_id);

-- ================================================
-- TABLA: BITÁCORAS SEMANALES
-- ================================================
CREATE TABLE IF NOT EXISTS weekly_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    semana_inicio DATE NOT NULL,
    semana_fin DATE NOT NULL,
    
    -- Contenido de la bitácora
    logros TEXT[],
    desafios TEXT[],
    aprendizajes TEXT,
    reflexiones TEXT,
    nivel_energia INT CHECK (nivel_energia BETWEEN 1 AND 5),
    nivel_satisfaccion INT CHECK (nivel_satisfaccion BETWEEN 1 AND 5),
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraint: Una bitácora por semana
    UNIQUE(user_id, semana_inicio)
);

CREATE INDEX idx_weekly_logs_user ON weekly_logs(user_id);
CREATE INDEX idx_weekly_logs_fecha ON weekly_logs(semana_inicio, semana_fin);

-- ================================================
-- TABLA: TAREAS DIARIAS
-- ================================================
CREATE TABLE IF NOT EXISTS daily_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    fecha DATE NOT NULL,
    
    -- Información de la tarea
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50), -- 'aprendizaje', 'compromiso', 'competencia', 'personal'
    
    -- Estado y flujo
    estado VARCHAR(20) DEFAULT 'pendiente', -- 'pendiente', 'en_progreso', 'completada', 'cancelada'
    prioridad VARCHAR(20) DEFAULT 'media', -- 'alta', 'media', 'baja'
    
    -- Tiempo
    tiempo_estimado INT, -- minutos
    tiempo_real INT, -- minutos
    
    -- Organización
    orden INT DEFAULT 0,
    tags TEXT[],
    notas TEXT,
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_daily_tasks_user ON daily_tasks(user_id);
CREATE INDEX idx_daily_tasks_fecha ON daily_tasks(fecha);
CREATE INDEX idx_daily_tasks_estado ON daily_tasks(estado);
CREATE INDEX idx_daily_tasks_categoria ON daily_tasks(categoria);

-- ================================================
-- TABLA: EVIDENCIAS (ARCHIVOS ADJUNTOS)
-- ================================================
CREATE TABLE IF NOT EXISTS evidencias (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES daily_tasks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    
    -- Información del archivo
    archivo_url TEXT NOT NULL,
    archivo_nombre VARCHAR(255) NOT NULL,
    tipo_archivo VARCHAR(50), -- 'imagen', 'pdf', 'documento', 'video', 'otro'
    mime_type VARCHAR(100),
    tamanio_kb INT,
    
    -- Descripción
    descripcion TEXT,
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_evidencias_task ON evidencias(task_id);
CREATE INDEX idx_evidencias_user ON evidencias(user_id);
CREATE INDEX idx_evidencias_tipo ON evidencias(tipo_archivo);

-- ================================================
-- TABLA: MÉTRICAS DIARIAS
-- ================================================
CREATE TABLE IF NOT EXISTS metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    fecha DATE NOT NULL,
    
    -- Métricas de tareas
    tareas_completadas INT DEFAULT 0,
    tareas_pendientes INT DEFAULT 0,
    tareas_en_progreso INT DEFAULT 0,
    
    -- Tiempo
    horas_dedicadas DECIMAL(5,2) DEFAULT 0,
    
    -- Evaluación personal
    nivel_satisfaccion INT CHECK (nivel_satisfaccion BETWEEN 1 AND 5),
    nivel_productividad INT CHECK (nivel_productividad BETWEEN 1 AND 5),
    notas_del_dia TEXT,
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraint: Una métrica por día por usuario
    UNIQUE(user_id, fecha)
);

CREATE INDEX idx_metrics_user ON metrics(user_id);
CREATE INDEX idx_metrics_fecha ON metrics(fecha);

-- ================================================
-- TABLA: COMPETENCIAS (CATÁLOGO)
-- ================================================
CREATE TABLE IF NOT EXISTS competencias (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    categoria VARCHAR(50), -- 'tecnica', 'blanda', 'liderazgo', 'comunicacion'
    icono VARCHAR(50), -- emoji o clase de icono
    color VARCHAR(20), -- color hex para UI
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insertar competencias predeterminadas
INSERT INTO competencias (nombre, descripcion, categoria, icono, color) VALUES
('Comunicación Efectiva', 'Habilidad para transmitir ideas claramente', 'blanda', '💬', '#3b82f6'),
('Liderazgo', 'Capacidad de guiar y motivar equipos', 'liderazgo', '👑', '#8b5cf6'),
('Pensamiento Crítico', 'Análisis profundo y toma de decisiones', 'blanda', '🧠', '#ec4899'),
('Programación Python', 'Desarrollo de software en Python', 'tecnica', '🐍', '#10b981'),
('Análisis de Datos', 'Interpretación y visualización de datos', 'tecnica', '📊', '#f59e0b'),
('Gestión del Tiempo', 'Organización y priorización efectiva', 'blanda', '⏰', '#6366f1'),
('Trabajo en Equipo', 'Colaboración y sinergia grupal', 'blanda', '🤝', '#14b8a6'),
('Adaptabilidad', 'Flexibilidad ante cambios', 'blanda', '🔄', '#a855f7'),
('Resolución de Problemas', 'Encontrar soluciones creativas', 'blanda', '🔍', '#ef4444'),
('Excel Avanzado', 'Dominio de fórmulas y análisis', 'tecnica', '📈', '#059669')
ON CONFLICT (nombre) DO NOTHING;

-- ================================================
-- TABLA: PERFILES DE USUARIO (EXTENSIÓN)
-- ================================================
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nombre_completo VARCHAR(255),
    avatar_url TEXT,
    cargo VARCHAR(100),
    departamento VARCHAR(100),
    fecha_ingreso DATE,
    bio TEXT,
    objetivos_generales TEXT,
    
    -- Configuración de notificaciones
    notif_tareas_pendientes BOOLEAN DEFAULT true,
    notif_fin_mes BOOLEAN DEFAULT true,
    notif_bitacora_semanal BOOLEAN DEFAULT true,
    
    -- Metadatos
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ================================================
-- FUNCIONES Y TRIGGERS
-- ================================================

-- Función: Actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_monthly_plans_updated_at BEFORE UPDATE ON monthly_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_monthly_reviews_updated_at BEFORE UPDATE ON monthly_reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_weekly_logs_updated_at BEFORE UPDATE ON weekly_logs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_daily_tasks_updated_at BEFORE UPDATE ON daily_tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función: Calcular métricas diarias automáticamente
CREATE OR REPLACE FUNCTION calculate_daily_metrics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO metrics (user_id, fecha, tareas_completadas, tareas_pendientes, tareas_en_progreso)
    SELECT 
        user_id,
        CURRENT_DATE,
        COUNT(*) FILTER (WHERE estado = 'completada'),
        COUNT(*) FILTER (WHERE estado = 'pendiente'),
        COUNT(*) FILTER (WHERE estado = 'en_progreso')
    FROM daily_tasks
    WHERE user_id = NEW.user_id AND fecha = NEW.fecha
    GROUP BY user_id
    ON CONFLICT (user_id, fecha) 
    DO UPDATE SET
        tareas_completadas = EXCLUDED.tareas_completadas,
        tareas_pendientes = EXCLUDED.tareas_pendientes,
        tareas_en_progreso = EXCLUDED.tareas_en_progreso;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger: Recalcular métricas al modificar tareas
CREATE TRIGGER recalculate_metrics AFTER INSERT OR UPDATE OR DELETE ON daily_tasks
    FOR EACH ROW EXECUTE FUNCTION calculate_daily_metrics();

-- ================================================
-- ROW LEVEL SECURITY (RLS)
-- ================================================

-- Habilitar RLS en todas las tablas
ALTER TABLE monthly_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE monthly_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidencias ENABLE ROW LEVEL SECURITY;
ALTER TABLE metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Políticas: Los usuarios solo ven sus propios datos
CREATE POLICY "Users can view own monthly_plans" ON monthly_plans
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own monthly_plans" ON monthly_plans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own monthly_plans" ON monthly_plans
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own monthly_plans" ON monthly_plans
    FOR DELETE USING (auth.uid() = user_id);

-- Repetir para otras tablas
CREATE POLICY "Users can view own monthly_reviews" ON monthly_reviews
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own monthly_reviews" ON monthly_reviews
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own monthly_reviews" ON monthly_reviews
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own monthly_reviews" ON monthly_reviews
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own weekly_logs" ON weekly_logs
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own weekly_logs" ON weekly_logs
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own weekly_logs" ON weekly_logs
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own weekly_logs" ON weekly_logs
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own daily_tasks" ON daily_tasks
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own daily_tasks" ON daily_tasks
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own daily_tasks" ON daily_tasks
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own daily_tasks" ON daily_tasks
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own evidencias" ON evidencias
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own evidencias" ON evidencias
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own evidencias" ON evidencias
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own metrics" ON metrics
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own metrics" ON metrics
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own metrics" ON metrics
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own user_profiles" ON user_profiles
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own user_profiles" ON user_profiles
    FOR UPDATE USING (auth.uid() = id);

-- Competencias: Todos pueden leer
CREATE POLICY "Anyone can view competencias" ON competencias
    FOR SELECT USING (true);

-- ================================================
-- VISTAS ÚTILES
-- ================================================

-- Vista: Resumen mensual por usuario
CREATE OR REPLACE VIEW monthly_summary AS
SELECT 
    mp.user_id,
    mp.mes,
    mp.objetivos,
    COALESCE(array_length(mp.competencias, 1), 0) as num_competencias,
    mr.que_mejore,
    COALESCE(array_length(mr.habilidades_desarrolladas, 1), 0) as num_habilidades,
    COUNT(dt.id) as total_tareas,
    COUNT(dt.id) FILTER (WHERE dt.estado = 'completada') as tareas_completadas,
    ROUND(COUNT(dt.id) FILTER (WHERE dt.estado = 'completada')::NUMERIC / NULLIF(COUNT(dt.id), 0) * 100, 2) as porcentaje_completado
FROM monthly_plans mp
LEFT JOIN monthly_reviews mr ON mp.id = mr.monthly_plan_id
LEFT JOIN daily_tasks dt ON dt.user_id = mp.user_id 
    AND DATE_TRUNC('month', dt.fecha) = DATE_TRUNC('month', mp.mes)
GROUP BY mp.user_id, mp.mes, mp.objetivos, mp.competencias, mr.que_mejore, mr.habilidades_desarrolladas;

-- Vista: Estadísticas de tareas por usuario
CREATE OR REPLACE VIEW task_statistics AS
SELECT 
    user_id,
    DATE_TRUNC('month', fecha) as mes,
    COUNT(*) as total_tareas,
    COUNT(*) FILTER (WHERE estado = 'completada') as completadas,
    COUNT(*) FILTER (WHERE estado = 'pendiente') as pendientes,
    COUNT(*) FILTER (WHERE estado = 'en_progreso') as en_progreso,
    AVG(tiempo_real) FILTER (WHERE tiempo_real IS NOT NULL) as tiempo_promedio,
    COUNT(DISTINCT fecha) as dias_activos
FROM daily_tasks
GROUP BY user_id, DATE_TRUNC('month', fecha);

-- ================================================
-- DATOS DE PRUEBA (OPCIONAL - COMENTAR EN PRODUCCIÓN)
-- ================================================

-- Puedes descomentar esto para tener datos de prueba
/*
INSERT INTO monthly_plans (user_id, mes, competencias, objetivos, fortalezas, debilidades)
VALUES (
    auth.uid(),
    CURRENT_DATE,
    ARRAY['Comunicación Efectiva', 'Programación Python'],
    'Mejorar mis habilidades de comunicación en reuniones',
    ARRAY['Proactivo', 'Organizado'],
    ARRAY['Timidez en presentaciones', 'Procrastinación']
);
*/

-- ================================================
-- FIN DEL SCRIPT
-- ================================================

-- Verificar que todo se creó correctamente
SELECT 'monthly_plans' as tabla, COUNT(*) as registros FROM monthly_plans
UNION ALL
SELECT 'daily_tasks', COUNT(*) FROM daily_tasks
UNION ALL
SELECT 'weekly_logs', COUNT(*) FROM weekly_logs
UNION ALL
SELECT 'competencias', COUNT(*) FROM competencias;
