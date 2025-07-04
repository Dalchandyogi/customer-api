from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# password = 'debug%40123' 
# URL_DATABASE = f'mysql+pymysql://root:{password}@localhost:3306/customer'
# URL_DATABASE = 'mysql://root:duJTWqqqYbceDpETwCufcxirGEGHBHmg@yamabiko.proxy.rlwy.net:16263/railway'
URL_DATABASE = 'mysql+pymysql://root:duJTWqqqYbceDpETwCufcxirGEGHBHmg@yamabiko.proxy.rlwy.net:16263/railway'


engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
