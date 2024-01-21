import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
parent_dir = os.path.dirname(current_directory)

if not os.path.exists(f"{parent_dir}/var"):
    os.makedirs(f"{parent_dir}/var")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{parent_dir}/var/app.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    return db
