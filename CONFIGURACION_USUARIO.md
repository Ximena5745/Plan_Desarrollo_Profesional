# Configuración del Usuario: lxisilva@poligran.edu.co

## ✅ Tareas Completadas

He creado los siguientes archivos para configurar y probar el usuario:

1. **[setup_user_profile.sql](setup_user_profile.sql)** - Script SQL para verificar y crear el perfil
2. **[test_login.py](test_login.py)** - Script Python para probar el login

---

## 📋 PARTE 1: Verificar y Crear Perfil de Usuario

### Paso 1: Abrir Supabase

1. Ve a tu proyecto en Supabase: https://supabase.com
2. Navega a **SQL Editor** (icono de base de datos en el menú lateral)

### Paso 2: Ejecutar Script SQL

1. Abre el archivo [setup_user_profile.sql](setup_user_profile.sql)
2. Copia **TODO** el contenido del archivo
3. Pégalo en el SQL Editor de Supabase
4. Haz clic en **Run** (o presiona `Ctrl+Enter`)

### Paso 3: Verificar Resultados

El script ejecutará 6 consultas en secuencia:

**Query 1: Verificar usuario en auth.users**
- Debe devolver 1 fila con el email `lxisilva@poligran.edu.co`
- Verifica el `user_id` (lo necesitarás)

**Query 2: Verificar si tiene perfil**
- Si devuelve **0 filas** → El perfil NO existe, se creará en el paso 3
- Si devuelve **1 fila** → El perfil YA existe ✓

**Query 3: Crear perfil (solo si no existe)**
- Crea automáticamente el perfil con datos por defecto
- Debe mostrar: `INSERT 0 1` (1 fila insertada)

**Query 4: Verificación final**
- Debe mostrar todos los datos del usuario con su perfil
- Verifica que `nombre_completo`, `cargo`, `departamento` tengan valores

**Query 5: Actualizar datos (opcional)**
- **Descomenta** este bloque si quieres cambiar los datos del perfil
- Modifica los valores según corresponda:
  ```sql
  UPDATE user_profiles
  SET
      nombre_completo = 'Luis Ximena Silva',  -- Cambiar por nombre real
      cargo = 'Estudiante de Ingeniería',     -- Cambiar por cargo real
      departamento = 'Facultad de Ingeniería' -- Cambiar por departamento real
  WHERE id = (SELECT id FROM auth.users WHERE email = 'lxisilva@poligran.edu.co');
  ```

**Query 6: Estadísticas del usuario**
- Muestra cuántas tareas, planes y bitácoras tiene
- Si es usuario nuevo, todos los contadores estarán en 0

---

## 🔐 PARTE 2: Probar Login en la Aplicación

### Paso 1: Iniciar el Servidor

1. Abre una terminal en la carpeta del proyecto
2. Activa el entorno virtual:
   ```bash
   Scripts\activate   # Windows
   ```

3. Inicia el servidor:
   ```bash
   python main.py
   ```

4. Espera a ver este mensaje:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   ```

### Paso 2: Ejecutar Script de Prueba

1. **Abre OTRA terminal** (deja la primera corriendo el servidor)
2. Activa el entorno virtual:
   ```bash
   Scripts\activate   # Windows
   ```

3. Ejecuta el script de prueba:
   ```bash
   python test_login.py
   ```

4. Cuando te pida la contraseña, ingrésala

### Paso 3: Verificar Resultados

**Si el login es EXITOSO, verás:**
```
========================================================================
PRUEBA DE LOGIN - Plan de Desarrollo Profesional
========================================================================

Usuario: lxisilva@poligran.edu.co
URL: http://localhost:8000/api/auth/login

[1] Intentando login...

✓ LOGIN EXITOSO!

Token recibido: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Tipo de token: bearer

[2] Verificando datos del usuario...

✓ Datos del usuario obtenidos correctamente:
   Email: lxisilva@poligran.edu.co
   ID: 2827ca83-222e-4ec1-85d2-f7ee67b53e61
   Nombre: Usuario Poligran
   Cargo: Estudiante
   Departamento: Desarrollo

========================================================================
✓ PRUEBA COMPLETADA EXITOSAMENTE
========================================================================

Puedes iniciar sesion en: http://localhost:8000/login
Email: lxisilva@poligran.edu.co
========================================================================
```

**Si el login FALLA:**
- Verifica que la contraseña sea correcta
- Verifica que el email esté confirmado en Supabase
- Revisa los logs del servidor en la primera terminal

---

## 🌐 PARTE 3: Probar Login en el Navegador

### Opción A: Usar la Interfaz Web

1. Abre tu navegador
2. Ve a: http://localhost:8000/login
3. Ingresa las credenciales:
   - **Email:** lxisilva@poligran.edu.co
   - **Contraseña:** [tu contraseña]
4. Haz clic en **Iniciar Sesión**
5. Deberías ser redirigido al dashboard

### Opción B: Usar Herramientas de Desarrollo

Si quieres verificar manualmente con herramientas como Postman o curl:

**Endpoint:** `POST http://localhost:8000/api/auth/login`

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
```

**Body (x-www-form-urlencoded):**
```
username=lxisilva@poligran.edu.co
password=[tu_contraseña]
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## ❓ Solución de Problemas

### Error: "Invalid credentials"

**Causa:** La contraseña es incorrecta o el usuario no está confirmado

**Solución:**
1. En Supabase, ve a **Authentication** > **Users**
2. Encuentra el usuario `lxisilva@poligran.edu.co`
3. Verifica que `email_confirmed_at` tenga una fecha (no esté vacío)
4. Si está vacío, haz clic en los 3 puntos `...` > **Verify email**

O resetea la contraseña:
1. Haz clic en los 3 puntos `...` > **Send magic link**
2. O usa el botón **Reset password**

### Error: "User profile not found"

**Causa:** El perfil no se creó en la tabla `user_profiles`

**Solución:**
1. Ejecuta nuevamente el script [setup_user_profile.sql](setup_user_profile.sql)
2. Verifica que la Query 3 se ejecute correctamente
3. Revisa la Query 4 para confirmar que el perfil existe

### Error: "Connection refused" o "Server not found"

**Causa:** El servidor FastAPI no está corriendo

**Solución:**
1. Abre una terminal
2. Ejecuta: `python main.py`
3. Espera a que inicie completamente
4. Intenta el login nuevamente

### Error: "Invalid API key" al iniciar el servidor

**Causa:** Las credenciales de Supabase en `.env` no son correctas

**Solución:**
1. Verifica el archivo [.env](.env)
2. Asegúrate de que `SUPABASE_URL` y `SUPABASE_KEY` sean correctos
3. Cópialos desde: Supabase > Settings > API
4. Guarda el archivo `.env`
5. Reinicia el servidor

---

## 📊 Verificación Final

### Checklist de Verificación

- [ ] Usuario existe en `auth.users` en Supabase
- [ ] Email está confirmado (`email_confirmed_at` tiene fecha)
- [ ] Perfil existe en tabla `user_profiles`
- [ ] Servidor FastAPI está corriendo en http://localhost:8000
- [ ] Script `test_login.py` ejecuta exitosamente
- [ ] Puedo hacer login en http://localhost:8000/login
- [ ] Dashboard carga correctamente después del login

### Próximos Pasos

Una vez que el login funcione correctamente:

1. **Explora el dashboard** en http://localhost:8000/dashboard
2. **Crea tu primer plan mensual**
3. **Agrega tareas diarias**
4. **Registra tu primera bitácora semanal**
5. **Sube evidencias** de tus logros

---

## 📁 Archivos Creados

| Archivo | Propósito |
|---------|-----------|
| [setup_user_profile.sql](setup_user_profile.sql) | Script SQL para verificar/crear perfil de usuario |
| [test_login.py](test_login.py) | Script Python para probar el login |
| [CONFIGURACION_USUARIO.md](CONFIGURACION_USUARIO.md) | Este archivo (instrucciones) |

---

## 💡 Notas Importantes

1. **No compartas** tu contraseña con nadie
2. **No subas** el archivo `.env` a GitHub (ya está en `.gitignore`)
3. **Mantén actualizado** tu perfil en el dashboard
4. Si cambias el email del usuario, actualiza también el script de prueba

---

## 🎯 Resumen Rápido

**Para verificar y crear el perfil:**
```bash
# En Supabase SQL Editor
1. Abrir setup_user_profile.sql
2. Copiar todo el contenido
3. Pegar en SQL Editor
4. Ejecutar (Run)
```

**Para probar el login:**
```bash
# Terminal 1
python main.py

# Terminal 2
python test_login.py
# Ingresar contraseña cuando se solicite
```

**Para usar la aplicación:**
```
http://localhost:8000/login
Email: lxisilva@poligran.edu.co
Contraseña: [tu contraseña]
```

---

¡Listo! El usuario está configurado y listo para usar la aplicación. 🎉
