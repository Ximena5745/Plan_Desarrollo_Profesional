-- ================================================
-- SCRIPT: Verificar y crear perfil de usuario
-- Usuario: lxisilva@poligran.edu.co
-- ================================================

-- 1. VERIFICAR SI EL USUARIO EXISTE EN AUTH
SELECT
    id as user_id,
    email,
    email_confirmed_at,
    created_at
FROM auth.users
WHERE email = 'lxisilva@poligran.edu.co';

-- 2. VERIFICAR SI TIENE PERFIL EN user_profiles
SELECT
    up.id,
    up.nombre_completo,
    up.cargo,
    up.departamento,
    up.created_at
FROM user_profiles up
INNER JOIN auth.users au ON au.id = up.id
WHERE au.email = 'lxisilva@poligran.edu.co';

-- 3. CREAR PERFIL SI NO EXISTE
-- (Ejecutar solo si el paso 2 no devuelve resultados)
INSERT INTO user_profiles (
    id,
    nombre_completo,
    cargo,
    departamento,
    bio,
    objetivos_generales,
    notif_tareas_pendientes,
    notif_fin_mes,
    notif_bitacora_semanal
)
SELECT
    au.id,
    'Usuario Poligran',  -- Cambiar por el nombre real si lo conoces
    'Estudiante',        -- Cambiar por el cargo real
    'Desarrollo',        -- Cambiar por el departamento real
    'Perfil creado automaticamente',
    'Desarrollo profesional continuo',
    true,
    true,
    true
FROM auth.users au
WHERE au.email = 'lxisilva@poligran.edu.co'
AND NOT EXISTS (
    SELECT 1 FROM user_profiles up WHERE up.id = au.id
);

-- 4. VERIFICAR QUE EL PERFIL FUE CREADO
SELECT
    au.email,
    au.email_confirmed_at,
    up.nombre_completo,
    up.cargo,
    up.departamento,
    up.created_at as perfil_creado_en
FROM auth.users au
LEFT JOIN user_profiles up ON up.id = au.id
WHERE au.email = 'lxisilva@poligran.edu.co';

-- 5. (OPCIONAL) ACTUALIZAR DATOS DEL PERFIL
-- Descomenta y modifica si necesitas actualizar los datos del perfil:
/*
UPDATE user_profiles
SET
    nombre_completo = 'Nombre Completo',
    cargo = 'Cargo Real',
    departamento = 'Departamento Real',
    fecha_ingreso = CURRENT_DATE,
    bio = 'Biografia del usuario'
WHERE id = (SELECT id FROM auth.users WHERE email = 'lxisilva@poligran.edu.co');
*/

-- 6. VERIFICAR ESTADÍSTICAS DEL USUARIO
-- Ver cuántas tareas, planes y bitácoras tiene el usuario
SELECT
    au.email,
    (SELECT COUNT(*) FROM daily_tasks WHERE user_id = au.id) as total_tareas,
    (SELECT COUNT(*) FROM monthly_plans WHERE user_id = au.id) as total_planes,
    (SELECT COUNT(*) FROM weekly_logs WHERE user_id = au.id) as total_bitacoras,
    (SELECT COUNT(*) FROM evidencias WHERE user_id = au.id) as total_evidencias
FROM auth.users au
WHERE au.email = 'lxisilva@poligran.edu.co';
