"""
Script de prueba para verificar el login del usuario
Usuario: lxisilva@poligran.edu.co
"""

import requests
import json
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración
BASE_URL = "http://localhost:8000"
EMAIL = "lxisilva@poligran.edu.co"

def test_login(email, password):
    """Prueba el login con las credenciales proporcionadas"""

    print("=" * 70)
    print("PRUEBA DE LOGIN - Plan de Desarrollo Profesional")
    print("=" * 70)
    print(f"\nUsuario: {email}")
    print(f"URL: {BASE_URL}/api/auth/login")

    # Datos del login
    login_data = {
        "username": email,  # FastAPI OAuth2 usa "username" como nombre del campo
        "password": password
    }

    try:
        print("\n[1] Intentando login...")
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=login_data,  # OAuth2PasswordRequestForm espera form data, no JSON
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            data = response.json()
            print("\n✓ LOGIN EXITOSO!")
            print(f"\nToken recibido: {data.get('access_token', 'N/A')[:50]}...")
            print(f"Tipo de token: {data.get('token_type', 'N/A')}")

            # Probar acceso al endpoint /me
            token = data.get('access_token')
            if token:
                print("\n[2] Verificando datos del usuario...")
                me_response = requests.get(
                    f"{BASE_URL}/api/auth/me",
                    headers={"Authorization": f"Bearer {token}"}
                )

                if me_response.status_code == 200:
                    user_data = me_response.json()
                    print("\n✓ Datos del usuario obtenidos correctamente:")
                    print(f"   Email: {user_data.get('email', 'N/A')}")
                    print(f"   ID: {user_data.get('id', 'N/A')}")
                    print(f"   Nombre: {user_data.get('nombre_completo', 'No configurado')}")
                    print(f"   Cargo: {user_data.get('cargo', 'No configurado')}")
                    print(f"   Departamento: {user_data.get('departamento', 'No configurado')}")
                else:
                    print(f"\n✗ Error al obtener datos del usuario: {me_response.status_code}")
                    print(f"   Respuesta: {me_response.text}")

            print("\n" + "=" * 70)
            print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
            print("=" * 70)
            print("\nPuedes iniciar sesion en: http://localhost:8000/login")
            print(f"Email: {email}")
            print("=" * 70)
            return True

        elif response.status_code == 401:
            print("\n✗ LOGIN FALLIDO: Credenciales incorrectas")
            print(f"   Mensaje: {response.json().get('detail', 'Sin detalles')}")
            return False

        elif response.status_code == 404:
            print("\n✗ ERROR: Endpoint no encontrado")
            print("   Verifica que el servidor este ejecutandose en http://localhost:8000")
            return False

        else:
            print(f"\n✗ ERROR INESPERADO: Status {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR DE CONEXION")
        print("   El servidor no esta ejecutandose.")
        print("\n   Para iniciar el servidor:")
        print("   1. Abre una terminal en la carpeta del proyecto")
        print("   2. Ejecuta: python main.py")
        print("   3. Espera a ver: 'Uvicorn running on http://0.0.0.0:8000'")
        print("   4. Ejecuta este script nuevamente")
        return False

    except Exception as e:
        print(f"\n✗ ERROR INESPERADO: {str(e)}")
        return False

def main():
    """Función principal"""
    print("\n")
    print("INSTRUCCIONES:")
    print("1. Asegurate de que el servidor este ejecutandose (python main.py)")
    print("2. Ingresa la contrasena del usuario cuando se solicite")
    print()

    # Solicitar contraseña
    password = input(f"Ingresa la contrasena para {EMAIL}: ")

    if not password:
        print("\n✗ Error: Debes ingresar una contrasena")
        return

    # Ejecutar prueba de login
    test_login(EMAIL, password)

if __name__ == "__main__":
    main()
