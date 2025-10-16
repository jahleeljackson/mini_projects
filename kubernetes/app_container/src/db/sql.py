import toml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy 


#import config 
with open("src/config.toml", "r") as f:
    config = toml.load(f)


#database setup
DATABASE_URL = f"sqlite:///./{config['db_name']}.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

#function for getting database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
