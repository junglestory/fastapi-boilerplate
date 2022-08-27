from tkinter import E
from fastapi import FastAPI, status
from fastapi.params import Depends 
from sqlalchemy.orm import Session
from db.connection import get_db
from models import News
from pydantic import BaseModel, ValidationError
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    seq: int
    journal_id: str
    title:  str
    publish_date:  str
    link_url: str
    writer:  str
    content: str
    class Config:
        orm_mode = True


def Response(status, message, data):
    return {
        "status": status,
        "message": message,
        "data": data
    }


app = FastAPI()

@app.get("/")
def hello(db: Session = Depends(get_db)):
    # logging.debug("hello world")
    return {"Hello": "World"}


@app.get("/news")
def get_news_all(db: Session = Depends(get_db)):
    datas = db.query(News).all()

    status = True
    message = "News retrieved successfully"

    if len(datas) <= 0:
        status = False
        message = "News not found"

    return Response(status, message, datas)


@app.get("/news/{journal_id}")
def get_news_journal(journal_id: str, db: Session = Depends(get_db)):    
    datas = db.query(News).filter(News.journal_id == journal_id).all()

    status = True
    message = "News retrieved successfully"

    if len(datas) <= 0:
        status = False
        message = "News not found"

    return Response(status, message, datas)


@app.post("/news")
def create_news(item: Item, db: Session = Depends(get_db)):
    try:
        new_news = News()
        new_news.journal_id = item.journal_id
        new_news.title =  item.title
        new_news.publish_date =  item.publish_date
        new_news.link_url =  item.link_url
        new_news.writer =  item.writer
        new_news.content =  item.content
        
        db.add(new_news)
        db.flush()

        db.refresh(new_news, attribute_names=['seq'])
        data = {"seq": new_news.seq}
        db.commit()

        status = True
        message = "News added successfully."
    except ValidationError as e:
        status = False
        data = None
        message = e
    
    return Response(status, message, data)


@app.put("/news")
def update_news(item: Item, db: Session = Depends(get_db)):
    try:
        is_updated = db.query(News).filter(News.seq == item.seq).update({
            News.journal_id: item.journal_id,
            News.title: item.title,
            News.publish_date: item.publish_date,
            News.link_url: item.link_url,
            News.writer: item.writer,
            News.content: item.content
        }, synchronize_session=False)
        
        db.flush()
        db.commit()

        status = True
        message = "News updated successfully"        

        if is_updated == 1:
            data = db.query(News).filter(
                News.seq == item.seq).one()
        elif is_updated == 0:
            message = "News not updated. No product found with this seq :" + \
                str(item.seq)
            status = False
            data = None
    except Exception as e:
        status = False
        data = None
        message = e
        print("Error : ", e)

    return Response(status, message, data)


@app.delete("/news/{seq}")
def delete_news(seq: int, db: Session = Depends(get_db)):
    data = None

    try:
        status = True
        
        is_deleted = db.query(News).filter(News.seq == seq).delete()
        db.commit()

        if is_deleted == 1:
            message = "News deleted successfully"
        else:
            message = "News not updated. No product found with this seq :" + \
                str(seq)    
    except Exception as e:
        status = False
        message = e

    return Response(status, message, data)

