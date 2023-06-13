from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# check_same_thread es necesario solo para SQLite
engine = create_engine("sqlite:///blog.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()
