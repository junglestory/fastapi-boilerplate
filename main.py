from fastapi import FastAPI, status
from fastapi.params import Depends 
from sqlalchemy.orm import Session
from db.connection import get_db
from models import News
from pydantic import BaseModel, ValidationError
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    # seq: int
    journal_id: str
    title:  str
    publish_date:  str
    link_url: str
    writer:  str
    content: str
    class Config:
        orm_mode = True


def Response(data, code, message, error):
    return {
        "data": data,
        "code": code,
        "message": message,
        "error": error
    }


app = FastAPI()

@app.get("/")
def hello(db: Session = Depends(get_db)):
    # logging.debug("hello world")
    return {"Hello": "World"}


@app.get("/news")
def get_news_all(db: Session = Depends(get_db)):
    datas = db.query(News).all()

    return datas


@app.get("/news/{journal_id}")
def get_news_journal(journal_id: str, db: Session = Depends(get_db)):    
    datas = db.query(News).filter(News.journal_id == journal_id).all()

    return datas


@app.post("/news")
def create_news(item: Item, db: Session = Depends(get_db)):
    print(item)
    data = ""
    
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

        # get id of the inserted product
        db.refresh(new_news, attribute_names=['seq'])
        data = {"seq": new_news.seq}
        db.commit()
    except ValidationError as e:
        print(e)
    
    return Response(data, 200, "Product added successfully.", False)


@app.put("/news", status_code=status.HTTP_201_CREATED)
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

        response_msg = "Product updated successfully"
        response_code = 200
        error = False

        if is_updated == 1:
            data = db.query(News).filter(
                News.seq == item.seq).one()
        elif is_updated == 0:
            response_msg = "Product not updated. No product found with this id :" + \
                str(item.seq)
            error = True
            data = None

        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@app.delete("/news/{seq}")
def delete_news(seq: int, db: Session = Depends(get_db)):
    db.query(News).filter(News.seq == seq).delete()
    db.commit()