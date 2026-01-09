"""
Script para verificar la conexion y configuracion de Supabase
"""

from supabase import create_client
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuracion
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def verificar_conexion():
    """Verifica la conexion basica a Supabase"""
    print("=" * 70)
    print("VERIFICACION DE SUPABASE")
    print("=" * 70)
    print(f"\nURL: {SUPABASE_URL}")
    print(f"ANON KEY: {SUPABASE_KEY[:50]}...")

    try:
        # Crear cliente
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("\n[OK] Cliente de Supabase creado exitosamente")

        # Verificar tablas
        print("\n[1] Verificando tablas en la base de datos...")
        tablas_esperadas = [
            "user_profiles",
            "monthly_plans",
            "monthly_reviews",
            "weekly_logs",
            "daily_tasks",
            "evidencias",
            "metrics"
        ]

        tablas_encontradas = []
        tablas_faltantes = []

        for tabla in tablas_esperadas:
            try:
                # Intentar hacer una consulta simple
                response = supabase.table(tabla).select("*").limit(0).execute()
                tablas_encontradas.append(tabla)
                print(f"   [OK] Tabla '{tabla}' existe")
            except Exception as e:
                tablas_faltantes.append(tabla)
                print(f"   [X] Tabla '{tabla}' NO existe - {str(e)[:50]}")

        # Resumen de tablas
        print(f"\n[2] Resumen:")
        print(f"   Tablas encontradas: {len(tablas_encontradas)}/{len(tablas_esperadas)}")

        if len(tablas_faltantes) > 0:
            print(f"\n   [!] FALTAN {len(tablas_faltantes)} TABLAS:")
            for tabla in tablas_faltantes:
                print(f"      - {tabla}")
            print("\n   ACCION REQUERIDA:")
            print("   1. Ve a Supabase > SQL Editor")
            print("   2. Abre el archivo: database_setup.sql")
            print("   3. Copia TODO el contenido")
            print("   4. Pegalo en el SQL Editor")
            print("   5. Ejecuta el script (RUN)")
            return False
        else:
            print("   [OK] Todas las tablas estan creadas correctamente!")

        # Verificar usuario
        print(f"\n[3] Verificando usuario: lxisilva@poligran.edu.co")
        try:
            # Intentar obtener el perfil del usuario
            response = supabase.table("user_profiles").select("*").execute()

            if len(response.data) > 0:
                print(f"   [OK] Se encontraron {len(response.data)} perfiles de usuario")
                for perfil in response.data:
                    print(f"      - ID: {perfil.get('id')}")
                    print(f"        Nombre: {perfil.get('nombre_completo', 'No configurado')}")
            else:
                print("   [!] No se encontraron perfiles de usuario")
                print("\n   ACCION REQUERIDA:")
                print("   1. Ve a Supabase > SQL Editor")
                print("   2. Abre el archivo: setup_user_profile.sql")
                print("   3. Copia TODO el contenido")
                print("   4. Pegalo en el SQL Editor")
                print("   5. Ejecuta el script (RUN)")
        except Exception as e:
            print(f"   [X] Error al verificar usuario: {str(e)[:100]}")

        # Verificar bucket de storage
        print(f"\n[4] Verificando bucket 'evidencias'...")
        try:
            # Listar archivos en el bucket (puede estar vacio)
            response = supabase.storage.from_("evidencias").list()
            print(f"   [OK] Bucket 'evidencias' existe y es accesible")
            print(f"   Archivos en el bucket: {len(response) if response else 0}")
        except Exception as e:
            print(f"   [X] Bucket 'evidencias' NO existe o no es accesible")
            print(f"   Error: {str(e)[:100]}")
            print("\n   ACCION REQUERIDA:")
            print("   1. Ve a Supabase > Storage")
            print("   2. Haz clic en 'New bucket'")
            print("   3. Nombre: evidencias")
            print("   4. Marca 'Public bucket'")
            print("   5. Haz clic en 'Create bucket'")

        print("\n" + "=" * 70)
        print("[OK] VERIFICACION COMPLETADA")
        print("=" * 70)

        if len(tablas_faltantes) == 0:
            print("\nTodo esta configurado correctamente!")
            print("Puedes probar el login con: python test_login.py")
        else:
            print("\n[!] Se requiere accion (ver arriba)")

        return True

    except Exception as e:
        print(f"\n[X] ERROR AL CONECTAR CON SUPABASE:")
        print(f"   {str(e)}")
        print("\n   Verifica que las credenciales en .env sean correctas")
        return False

if __name__ == "__main__":
    verificar_conexion()
