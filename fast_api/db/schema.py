import toml
from sqlalchemy import Column, Integer, String
import sqlalchemy 
from db.sql import engine
from pydantic import BaseModel

#import config 
with open("config.toml", "r") as f:
    config = toml.load(f)

Base = sqlalchemy.orm.declarative_base()

#database model
class Book(Base):
    __tablename__ = config['table_name']
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String)

#defining data model for item creation
class BookCreate(BaseModel):
    title: str 
    author: str
    description: str 

#data model for item retrieval
class BookResponse(BaseModel):
    id: int 
    title: str
    author: str 
    description: str 

#create table 
Base.metadata.create_all(bind=engine)
