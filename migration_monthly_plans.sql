-- Migration: Add missing columns to monthly_plans table
-- Date: 2026-01-12
-- Purpose: Add new Plan Mensual fields for competencias tracking

-- Step 1: Delete any problematic records (optional, uncomment if needed)
-- DELETE FROM monthly_plans
-- WHERE user_id = '2827ca83-222e-4ec1-86d2-f7ee67b53e61'
-- AND mes = '2026-01-10';

-- Step 2: Add missing columns to monthly_plans table
ALTER TABLE monthly_plans
ADD COLUMN IF NOT EXISTS competencias_trabajar TEXT,
ADD COLUMN IF NOT EXISTS que_quiero_lograr TEXT,
ADD COLUMN IF NOT EXISTS mis_fortalezas TEXT,
ADD COLUMN IF NOT EXISTS mis_debilidades TEXT,
ADD COLUMN IF NOT EXISTS que_mejore TEXT,
ADD COLUMN IF NOT EXISTS que_falta_mejorar TEXT,
ADD COLUMN IF NOT EXISTS habilidades_desarrolladas TEXT,
ADD COLUMN IF NOT EXISTS momento_memorable TEXT,
ADD COLUMN IF NOT EXISTS competencias JSONB DEFAULT '[]'::jsonb;

-- Step 3: Refresh PostgREST schema cache (Supabase will do this automatically)
-- You may need to wait 30-60 seconds or manually refresh in Supabase Dashboard

-- Step 4: Verify the columns were added
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'monthly_plans'
ORDER BY ordinal_position;
