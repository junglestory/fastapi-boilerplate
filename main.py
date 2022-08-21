import string
from typing import Union
from fastapi import FastAPI
from fastapi.params import Depends 
from sqlalchemy.orm import Session
from db.connection import get_db
from models import News

app = FastAPI()

@app.get("/")
def hello(db: Session = Depends(get_db)):
    # logging.debug("hello world")
    return {"Hello": "World"}


@app.get("/news")
def news_list(db: Session = Depends(get_db)):
    datas = db.query(News).all()
    
    return datas


@app.get("/news/{journal_id}")
def news_journal(journal_id: str, db: Session = Depends(get_db)):    
    datas = db.query(News).filter(News.journal_id == journal_id).all()

    return datas