import toml
from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session 
from db.schema import Book, BookCreate, BookResponse
from db.sql import get_db


#fastapi instance 
app = FastAPI() 

#import config 
with open("config.toml", "r") as f:
    config = toml.load(f)


#api endpoint to create a user 
@app.post("/books", response_model=BookResponse)
async def create_book(db_name: BookCreate, db: Session = Depends(get_db)):
    db_item = Book(**db_name.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/")
async def home():
    return {"jahleel": "jackson"}

#api endpoint to read a user
@app.get("/books/{book_id}", response_model=BookResponse)
async def read_book(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Book).filter(Book.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/books/{book_id}", response_model=BookResponse)
async def delete_book(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Book).filter(Book.id == item_id).first()
    db.delete(db_item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


if __name__ == "__main__":
    import uvicorn 

    uvicorn.run(app, host=f"{config['host']}", port=config['port'])

