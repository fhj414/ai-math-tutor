import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def get_database_url():
    configured_url = os.getenv("DATABASE_URL")
    if configured_url:
        return configured_url

    sqlite_path = "./math_tutor.db"
    if os.getenv("VERCEL") or os.getenv("VERCEL_ENV"):
        sqlite_path = "/tmp/math_tutor.db"

    return f"sqlite:///{sqlite_path}"


DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
