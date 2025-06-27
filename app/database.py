import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
# print("DATABASE_URL:", DATABASE_URL)
DATABASE_URL = "postgresql://postgres.dpraafklueiiaogxdqdt:Wewe10989299!!@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()