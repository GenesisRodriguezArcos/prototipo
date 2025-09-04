import os

# Credenciales y parámetros
DB_USER = os.getenv("DB_USER", "system")
DB_PASS = os.getenv("DB_PASS", "Admin12345")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE", "XEPDB1")  # nombre del servicio en Oracle XE

# Formato para python-oracledb en modo THIN (service_name, no SID)
dsn = f"{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

# Cadena para SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"oracle+oracledb://{DB_USER}:{DB_PASS}@{dsn}"

SQLALCHEMY_TRACK_MODIFICATIONS = False
