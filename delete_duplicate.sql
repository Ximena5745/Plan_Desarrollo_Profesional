-- Eliminar el registro duplicado que está causando problemas
-- Este registro se creó con un error pero quedó guardado en la base de datos

DELETE FROM monthly_plans
WHERE user_id = '2827ca83-222e-4ec1-86d2-f7ee67b53e61'
AND mes = '2026-01-10';

-- Verificar que se eliminó correctamente
SELECT * FROM monthly_plans
WHERE user_id = '2827ca83-222e-4ec1-86d2-f7ee67b53e61'
ORDER BY mes DESC;
