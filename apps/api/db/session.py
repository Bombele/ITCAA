from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de la base de datos
# Para empezar usamos SQLite local, luego puedes cambiar a PostgreSQL o MySQL
DATABASE_URL = "sqlite:///./itcaa.db"

# Crear el motor de conexión
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Necesario solo para SQLite
)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
