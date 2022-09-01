from fastapi import FastAPI
from fastapi.params import Depends 
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import ValidationError
from models import News
import schemas
import logging


def Response(status, message, data):
    return {
        "status": status,
        "message": message,
        "data": data
    }


app = FastAPI()

@app.get("/")
def hello(db: Session = Depends(get_db)):
    logging.debug("hello world")
    return {"Hello": "World"}


@app.get("/news")
def get_news_all(db: Session = Depends(get_db)):
    datas = db.query(News).all()

    status = True
    message = "News retrieved successfully"

    if len(datas) <= 0:
        status = False
        message = "News not found"

    logging.info(message)
    
    return Response(status, message, datas)


@app.get("/news/{journal_id}")
def get_news_by_journal_id(journal_id: str, db: Session = Depends(get_db)):    
    logging.info("journal id : {}".format(journal_id))

    datas = db.query(News).filter(News.journal_id == journal_id).all()

    status = True
    message = "News retrieved successfully"

    if len(datas) <= 0:
        status = False
        message = "News not found"

    logging.info(message)

    return Response(status, message, datas)


@app.post("/news")
def create_news(item: schemas.Item, db: Session = Depends(get_db)):
    try:
        logging.info(item)

        news = News()
        news.journal_id = item.journal_id
        news.title =  item.title
        news.publish_date =  item.publish_date
        news.link_url =  item.link_url
        news.writer =  item.writer
        news.content =  item.content
        
        db.add(news)
        db.flush()

        db.refresh(news, attribute_names=['seq'])
        data = {"seq": news.seq}
        db.commit()

        status = True
        message = "News added successfully."

        logging.info(message)
    except ValidationError as e:
        logging.error(e)
        status = False
        data = None
        message = e
    
    return Response(status, message, data)


@app.put("/news")
def update_news(item: schemas.Item, db: Session = Depends(get_db)):
    try:
        logging.info(item)

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
        
        logging.info(message)
    except Exception as e:
        logging.error(e)
        status = False
        data = None
        message = e

    return Response(status, message, data)


@app.delete("/news/{seq}")
def delete_news(seq: int, db: Session = Depends(get_db)):
    data = None

    try:
        logging.info("seq : {}".format(str(seq)))

        status = True
        
        is_deleted = db.query(News).filter(News.seq == seq).delete()
        db.commit()

        if is_deleted == 1:
            message = "News deleted successfully"
        else:
            message = "News not updated. No product found with this seq :" + \
                str(seq)    
        
        logging.info(message)
    except Exception as e:
        logging.error(e)
        status = False
        message = e

    return Response(status, message, data)

