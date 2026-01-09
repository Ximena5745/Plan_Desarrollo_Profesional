# Paso a Paso: Crear Tablas en Supabase

## ✅ Estado Actual

- [x] Conexión a Supabase funcionando correctamente
- [ ] Tablas de la base de datos (0/7 creadas)
- [ ] Bucket de storage
- [ ] Perfil de usuario

---

## 📋 Instrucciones para Crear las Tablas

### Paso 1: Abrir el archivo database_setup.sql

1. En VSCode, abre el archivo: [database_setup.sql](database_setup.sql)
2. Presiona `Ctrl+A` para seleccionar todo
3. Presiona `Ctrl+C` para copiar

### Paso 2: Ir a Supabase

1. Abre tu navegador
2. Ve a: https://supabase.com/dashboard
3. Haz clic en tu proyecto: **Plan-Desarrollo-Profesional**
4. Espera a que cargue el dashboard

### Paso 3: Abrir SQL Editor

1. En el menú lateral izquierdo, busca el ícono `</>`
2. Haz clic en **SQL Editor**
3. Verás un editor de SQL vacío

### Paso 4: Pegar y Ejecutar el Script

1. Haz clic en el área del editor (debajo de "New query")
2. Presiona `Ctrl+V` para pegar el contenido de `database_setup.sql`
3. Verás un script SQL muy largo (aproximadamente 450 líneas)
4. **Haz clic en el botón "Run"** (esquina inferior derecha) o presiona `Ctrl+Enter`
5. Espera 5-10 segundos mientras se ejecuta

### Paso 5: Verificar Resultado

Deberías ver uno de estos mensajes:

**✅ Éxito:**
```
Success. No rows returned
```

**❌ Si hay error:**
- Lee el mensaje de error
- Verifica que copiaste TODO el contenido
- Intenta ejecutar de nuevo

### Paso 6: Verificar que las Tablas se Crearon

1. En el menú lateral, haz clic en **Table Editor** (ícono de tabla)
2. Deberías ver estas 7 tablas:
   - ✅ user_profiles
   - ✅ monthly_plans
   - ✅ monthly_reviews
   - ✅ weekly_logs
   - ✅ daily_tasks
   - ✅ evidencias
   - ✅ metrics

### Paso 7: Verificar desde la Terminal

Vuelve a VSCode y ejecuta:

```bash
python verificar_supabase.py
```

Ahora deberías ver:
```
[OK] Tabla 'user_profiles' existe
[OK] Tabla 'monthly_plans' existe
[OK] Tabla 'monthly_reviews' existe
[OK] Tabla 'weekly_logs' existe
[OK] Tabla 'daily_tasks' existe
[OK] Tabla 'evidencias' existe
[OK] Tabla 'metrics' existe

Tablas encontradas: 7/7
```

---

## 📦 Crear Bucket de Storage

Después de crear las tablas, necesitas crear el bucket para las evidencias:

### Paso 1: Ir a Storage

1. En Supabase, haz clic en **Storage** en el menú lateral (ícono de carpeta)
2. Verás una página con el título "Storage"

### Paso 2: Crear Bucket

1. Haz clic en el botón **"New bucket"** (botón verde)
2. Aparecerá un modal

### Paso 3: Configurar el Bucket

Completa los siguientes campos:

- **Name:** `evidencias`
- **Public bucket:** ✅ **MARCA ESTA CASILLA** (muy importante)
- **File size limit:** 10 MB (dejar por defecto)
- **Allowed MIME types:** Dejar vacío (permitir todos)

### Paso 4: Crear

1. Haz clic en **"Create bucket"**
2. El bucket aparecerá en la lista

### Paso 5: Verificar

Ejecuta nuevamente:

```bash
python verificar_supabase.py
```

Deberías ver:
```
[OK] Bucket 'evidencias' existe y es accesible
Archivos en el bucket: 0
```

---

## 👤 Crear Perfil de Usuario

### Paso 1: Volver al SQL Editor

1. Haz clic en **SQL Editor** en el menú lateral
2. Verás tu query anterior
3. Haz clic en **"New query"** o presiona `Ctrl+N`

### Paso 2: Abrir setup_user_profile.sql

1. En VSCode, abre el archivo: [setup_user_profile.sql](setup_user_profile.sql)
2. Presiona `Ctrl+A` para seleccionar todo
3. Presiona `Ctrl+C` para copiar

### Paso 3: Pegar y Ejecutar

1. En Supabase SQL Editor, presiona `Ctrl+V` para pegar
2. Haz clic en **"Run"** o presiona `Ctrl+Enter`
3. Verás varias tablas de resultados

### Paso 4: Verificar Resultados

Deberías ver:

**Query 1:** Información del usuario
```
| email                      | user_id                              |
|---------------------------|--------------------------------------|
| lxisilva@poligran.edu.co  | 2827ca83-222e-4ec1-85d2-f7ee67b53e61 |
```

**Query 2:** (Probablemente vacía la primera vez)

**Query 3:** Mensaje de INSERT
```
INSERT 0 1
```

**Query 4:** Perfil creado
```
| email                    | nombre_completo    | cargo      |
|--------------------------|-------------------|------------|
| lxisilva@poligran.edu.co | Usuario Poligran  | Estudiante |
```

**Query 6:** Estadísticas
```
| email                    | total_tareas | total_planes | total_bitacoras |
|--------------------------|-------------|--------------|-----------------|
| lxisilva@poligran.edu.co | 0           | 0            | 0               |
```

### Paso 5: Verificar desde Terminal

```bash
python verificar_supabase.py
```

Deberías ver:
```
[OK] Se encontraron 1 perfiles de usuario
   - ID: 2827ca83-222e-4ec1-85d2-f7ee67b53e61
     Nombre: Usuario Poligran
```

---

## ✅ Verificación Final

Ejecuta:

```bash
python verificar_supabase.py
```

**Resultado esperado:**

```
======================================================================
VERIFICACION DE SUPABASE
======================================================================

URL: https://srohzwfhockkzeszziko.supabase.co

[OK] Cliente de Supabase creado exitosamente

[1] Verificando tablas en la base de datos...
   [OK] Tabla 'user_profiles' existe
   [OK] Tabla 'monthly_plans' existe
   [OK] Tabla 'monthly_reviews' existe
   [OK] Tabla 'weekly_logs' existe
   [OK] Tabla 'daily_tasks' existe
   [OK] Tabla 'evidencias' existe
   [OK] Tabla 'metrics' existe

[2] Resumen:
   Tablas encontradas: 7/7
   [OK] Todas las tablas estan creadas correctamente!

[3] Verificando usuario: lxisilva@poligran.edu.co
   [OK] Se encontraron 1 perfiles de usuario
      - ID: 2827ca83-222e-4ec1-85d2-f7ee67b53e61
        Nombre: Usuario Poligran

[4] Verificando bucket 'evidencias'...
   [OK] Bucket 'evidencias' existe y es accesible
   Archivos en el bucket: 0

======================================================================
[OK] VERIFICACION COMPLETADA
======================================================================

Todo esta configurado correctamente!
Puedes probar el login con: python test_login.py
```

---

## 🚀 Siguiente Paso

Una vez que la verificación sea exitosa:

```bash
python test_login.py
```

Ingresa la contraseña cuando se solicite y deberías ver:

```
LOGIN EXITOSO!
```

---

## ❓ Problemas Comunes

### Error: "relation 'user_profiles' does not exist"

**Causa:** Las tablas no se crearon

**Solución:**
1. Ve a Supabase > SQL Editor
2. Ejecuta nuevamente el script `database_setup.sql`
3. Asegúrate de copiar TODO el contenido

### Error: "Bucket 'evidencias' not found"

**Causa:** El bucket no existe

**Solución:**
1. Ve a Supabase > Storage
2. Haz clic en "New bucket"
3. Nombre: `evidencias`
4. Marca "Public bucket"
5. Crear

### Error: "INSERT 0 0" en Query 3

**Causa:** El perfil ya existe

**Solución:**
- Esto es normal si ya ejecutaste el script antes
- El perfil ya está creado, puedes continuar

### No se encuentra ningún perfil de usuario

**Causa:** El usuario no existe en auth.users o el script no se ejecutó

**Solución:**
1. Verifica que el usuario exista en Authentication > Users
2. Ejecuta el script `setup_user_profile.sql` nuevamente
3. Verifica Query 4 para confirmar que se creó

---

## 📝 Checklist

- [ ] Abrir `database_setup.sql` en VSCode
- [ ] Copiar todo el contenido (Ctrl+A, Ctrl+C)
- [ ] Ir a Supabase > SQL Editor
- [ ] Pegar y ejecutar (Ctrl+V, luego Run)
- [ ] Verificar que aparezca "Success"
- [ ] Ir a Table Editor y ver las 7 tablas
- [ ] Ir a Storage y crear bucket "evidencias"
- [ ] Marcar bucket como "Public"
- [ ] Abrir `setup_user_profile.sql` en VSCode
- [ ] Copiar todo (Ctrl+A, Ctrl+C)
- [ ] Pegar en SQL Editor y ejecutar
- [ ] Verificar que se creó el perfil
- [ ] Ejecutar `python verificar_supabase.py`
- [ ] Verificar que todo esté en [OK]
- [ ] Ejecutar `python test_login.py`

---

**¡Sigue estos pasos y tu proyecto estará completamente configurado!** 🎉
