import toml
from sqlalchemy import Column, Integer, String
import sqlalchemy 
from src.db.sql import engine
from pydantic import BaseModel

#import config 
with open("src/config.toml", "r") as f:
    config = toml.load(f)

Base = sqlalchemy.orm.declarative_base()

#database model
class Item(Base):
    __tablename__ = config['table_name']
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

#defining data model for item creation
class ItemCreate(BaseModel):
    name: str 
    description: str 

#data model for item retrieval
class ItemResponse(BaseModel):
    id: int 
    name: str
    description: str 

#create table 
Base.metadata.create_all(bind=engine)
