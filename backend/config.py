import oracledb  
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de conexión
DB_USER = os.getenv("DB_USER", "SYSTEM")
DB_PASS = os.getenv("DB_PASS", "Admin12345")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE", "XEPDB1")

# URI para SQLAlchemy con Oracle
SQLALCHEMY_DATABASE_URI = f'oracle+oracledb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}'

# Construir DSN dinámicamente (para test de conexión)
dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"

def test_oracle_connection():
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASS,
            dsn=dsn
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM PRODUCTOS")
            rows = cursor.fetchall()
            print("📦 Productos encontrados:" if rows else "⚠️ No hay registros en PRODUCTOS.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"❌ Error: {error.message}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
