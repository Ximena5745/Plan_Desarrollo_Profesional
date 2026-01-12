-- Agregar columna actividades_lograr a monthly_plans
ALTER TABLE monthly_plans
ADD COLUMN IF NOT EXISTS actividades_lograr JSONB DEFAULT '[]'::jsonb;

-- Verificar que se agregó correctamente
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'monthly_plans'
  AND column_name = 'actividades_lograr';
