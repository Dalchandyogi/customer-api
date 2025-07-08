from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


password = 'Debug%402006'
user = 'u604935531_dalchandyogi'
host = 'srv1872.hstgr.io'  
port = 3306
db_name = 'u604935531_customers'

URL_DATABASE = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
