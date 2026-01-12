-- ================================================
-- FINANCIAL CONTROL MODULE - Migration 002
-- Date: 2026-01-12
-- Purpose: Add financial tracking tables and categories
-- ================================================

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================
-- TABLE: FINANCIAL CATEGORIES
-- ================================================
CREATE TABLE IF NOT EXISTS financial_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) CHECK (tipo IN ('ingreso', 'gasto', 'deuda')) NOT NULL,
    color VARCHAR(7) DEFAULT '#6366f1',
    icono VARCHAR(50),
    descripcion TEXT,
    es_predeterminada BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(user_id, nombre, tipo)
);

CREATE INDEX IF NOT EXISTS idx_financial_categories_user ON financial_categories(user_id);
CREATE INDEX IF NOT EXISTS idx_financial_categories_tipo ON financial_categories(tipo);

-- ================================================
-- TABLE: FINANCIAL RECORDS
-- ================================================
CREATE TABLE IF NOT EXISTS financial_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    category_id UUID REFERENCES financial_categories(id) ON DELETE SET NULL,

    mes DATE NOT NULL,
    fecha_transaccion DATE NOT NULL,
    tipo VARCHAR(20) CHECK (tipo IN ('ingreso', 'gasto', 'deuda', 'pago_recurrente')) NOT NULL,
    monto DECIMAL(12,2) NOT NULL CHECK (monto >= 0),
    descripcion TEXT,
    categoria_nombre VARCHAR(100),

    es_recurrente BOOLEAN DEFAULT false,
    recurrencia_tipo VARCHAR(20),
    deuda_saldo_pendiente DECIMAL(12,2),
    deuda_pagada BOOLEAN DEFAULT false,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_financial_records_user ON financial_records(user_id);
CREATE INDEX IF NOT EXISTS idx_financial_records_mes ON financial_records(mes);
CREATE INDEX IF NOT EXISTS idx_financial_records_fecha ON financial_records(fecha_transaccion);
CREATE INDEX IF NOT EXISTS idx_financial_records_tipo ON financial_records(tipo);
CREATE INDEX IF NOT EXISTS idx_financial_records_category ON financial_records(category_id);

-- ================================================
-- TABLE: FINANCIAL MONTHLY SUMMARY
-- ================================================
CREATE TABLE IF NOT EXISTS financial_monthly_summary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    mes DATE NOT NULL,

    total_ingresos DECIMAL(12,2) DEFAULT 0,
    total_gastos DECIMAL(12,2) DEFAULT 0,
    total_deudas DECIMAL(12,2) DEFAULT 0,
    balance DECIMAL(12,2) DEFAULT 0,
    tasa_ahorro DECIMAL(5,2) DEFAULT 0,

    gastos_por_categoria JSONB DEFAULT '[]'::jsonb,
    ingresos_por_categoria JSONB DEFAULT '[]'::jsonb,

    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(user_id, mes)
);

CREATE INDEX IF NOT EXISTS idx_financial_summary_user ON financial_monthly_summary(user_id);
CREATE INDEX IF NOT EXISTS idx_financial_summary_mes ON financial_monthly_summary(mes);

-- ================================================
-- FUNCTION: CREATE DEFAULT CATEGORIES
-- ================================================
CREATE OR REPLACE FUNCTION create_default_financial_categories(p_user_id UUID)
RETURNS void AS $$
BEGIN
    -- Ingresos
    INSERT INTO financial_categories (user_id, nombre, tipo, color, icono, es_predeterminada)
    VALUES
        (p_user_id, 'Salario', 'ingreso', '#22c55e', '💰', true),
        (p_user_id, 'Freelance', 'ingreso', '#10b981', '💻', true),
        (p_user_id, 'Inversiones', 'ingreso', '#14b8a6', '📈', true),
        (p_user_id, 'Otros Ingresos', 'ingreso', '#06b6d4', '💵', true)
    ON CONFLICT (user_id, nombre, tipo) DO NOTHING;

    -- Gastos
    INSERT INTO financial_categories (user_id, nombre, tipo, color, icono, es_predeterminada)
    VALUES
        (p_user_id, 'Alimentación', 'gasto', '#ef4444', '🍔', true),
        (p_user_id, 'Transporte', 'gasto', '#f97316', '🚗', true),
        (p_user_id, 'Vivienda', 'gasto', '#f59e0b', '🏠', true),
        (p_user_id, 'Servicios', 'gasto', '#eab308', '💡', true),
        (p_user_id, 'Entretenimiento', 'gasto', '#a855f7', '🎬', true),
        (p_user_id, 'Salud', 'gasto', '#ec4899', '⚕️', true),
        (p_user_id, 'Educación', 'gasto', '#3b82f6', '📚', true),
        (p_user_id, 'Compras', 'gasto', '#8b5cf6', '🛍️', true),
        (p_user_id, 'Otros Gastos', 'gasto', '#6366f1', '📦', true)
    ON CONFLICT (user_id, nombre, tipo) DO NOTHING;

    -- Deudas
    INSERT INTO financial_categories (user_id, nombre, tipo, color, icono, es_predeterminada)
    VALUES
        (p_user_id, 'Tarjeta de Crédito', 'deuda', '#dc2626', '💳', true),
        (p_user_id, 'Préstamo Personal', 'deuda', '#b91c1c', '🏦', true),
        (p_user_id, 'Préstamo Hipotecario', 'deuda', '#991b1b', '🏡', true)
    ON CONFLICT (user_id, nombre, tipo) DO NOTHING;
END;
$$ LANGUAGE plpgsql;

-- ================================================
-- TRIGGER: AUTO-CALCULATE MONTHLY SUMMARY
-- ================================================
CREATE OR REPLACE FUNCTION recalculate_financial_summary()
RETURNS TRIGGER AS $$
DECLARE
    v_user_id UUID;
    v_mes DATE;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_user_id := OLD.user_id;
        v_mes := OLD.mes;
    ELSE
        v_user_id := NEW.user_id;
        v_mes := NEW.mes;
    END IF;

    INSERT INTO financial_monthly_summary (user_id, mes, total_ingresos, total_gastos, total_deudas, balance, tasa_ahorro)
    SELECT
        v_user_id,
        v_mes,
        COALESCE(SUM(monto) FILTER (WHERE tipo = 'ingreso'), 0) as total_ingresos,
        COALESCE(SUM(monto) FILTER (WHERE tipo = 'gasto'), 0) as total_gastos,
        COALESCE(SUM(monto) FILTER (WHERE tipo = 'deuda'), 0) as total_deudas,
        COALESCE(SUM(monto) FILTER (WHERE tipo = 'ingreso'), 0) -
            COALESCE(SUM(monto) FILTER (WHERE tipo = 'gasto'), 0) as balance,
        CASE
            WHEN SUM(monto) FILTER (WHERE tipo = 'ingreso') > 0 THEN
                ((SUM(monto) FILTER (WHERE tipo = 'ingreso') - SUM(monto) FILTER (WHERE tipo = 'gasto')) /
                 SUM(monto) FILTER (WHERE tipo = 'ingreso') * 100)::DECIMAL(5,2)
            ELSE 0
        END as tasa_ahorro
    FROM financial_records
    WHERE user_id = v_user_id AND mes = v_mes
    GROUP BY user_id, mes
    ON CONFLICT (user_id, mes) DO UPDATE SET
        total_ingresos = EXCLUDED.total_ingresos,
        total_gastos = EXCLUDED.total_gastos,
        total_deudas = EXCLUDED.total_deudas,
        balance = EXCLUDED.balance,
        tasa_ahorro = EXCLUDED.tasa_ahorro,
        updated_at = NOW();

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS recalculate_summary_on_record_change ON financial_records;
CREATE TRIGGER recalculate_summary_on_record_change
    AFTER INSERT OR UPDATE OR DELETE ON financial_records
    FOR EACH ROW EXECUTE FUNCTION recalculate_financial_summary();

-- ================================================
-- TRIGGER: UPDATE TIMESTAMP
-- ================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_financial_categories_updated_at ON financial_categories;
CREATE TRIGGER update_financial_categories_updated_at
    BEFORE UPDATE ON financial_categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_financial_records_updated_at ON financial_records;
CREATE TRIGGER update_financial_records_updated_at
    BEFORE UPDATE ON financial_records
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- ROW LEVEL SECURITY
-- ================================================
ALTER TABLE financial_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_monthly_summary ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can manage own financial_categories" ON financial_categories;
DROP POLICY IF EXISTS "Users can manage own financial_records" ON financial_records;
DROP POLICY IF EXISTS "Users can view own financial_monthly_summary" ON financial_monthly_summary;

-- Policies for financial_categories
CREATE POLICY "Users can manage own financial_categories" ON financial_categories
    FOR ALL USING (auth.uid() = user_id);

-- Policies for financial_records
CREATE POLICY "Users can manage own financial_records" ON financial_records
    FOR ALL USING (auth.uid() = user_id);

-- Policies for financial_monthly_summary
CREATE POLICY "Users can view own financial_monthly_summary" ON financial_monthly_summary
    FOR SELECT USING (auth.uid() = user_id);

-- ================================================
-- VERIFICATION
-- ================================================
SELECT 'Migración 002_financial_control completada exitosamente' AS status;

SELECT 'financial_categories' as tabla, COUNT(*) as registros FROM financial_categories
UNION ALL
SELECT 'financial_records', COUNT(*) FROM financial_records
UNION ALL
SELECT 'financial_monthly_summary', COUNT(*) FROM financial_monthly_summary;
