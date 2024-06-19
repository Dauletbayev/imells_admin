from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Подключение к базе данных
# SQLALCHEMY_DATABASE_URL1 = 'postgresql://postgres:daulet2005@localhost/imells'
SQLALCHEMY_DATABASE_URL = 'sqlite:///data.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=10)
SessionLocal = sessionmaker(bind=engine)

# Создание базового класса
Base = declarative_base()


# Создание сессий
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
