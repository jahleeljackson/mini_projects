import toml
from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session 
from src.db.schema import Item, ItemCreate, ItemResponse
from src.db.sql import get_db


#fastapi instance 
app = FastAPI() 

#import config 
with open("src/config.toml", "r") as f:
    config = toml.load(f)


@app.get("/")
async def home():
    return {"Jahleel": "Jackson"}


#api endpoint to create a user 
@app.post("/items", response_model=ItemResponse)
async def create_item(db_name: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**db_name.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#api endpoint to read a user
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=ItemResponse)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


if __name__ == "__main__":
    import uvicorn 

    uvicorn.run(app, host=f"{config['host']}", port=config['port'])

