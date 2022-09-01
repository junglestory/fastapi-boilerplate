from sqlalchemy import Column, String, Integer, TEXT, DATETIME
from db.database import Base
from sqlalchemy.sql import func

class News(Base):
    __tablename__ = "news"

    seq = Column(Integer, primary_key=True, index=True)  
    journal_id = Column(String(10))  
    title = Column(String(200))  
    publish_date = Column(String(20))  
    link_url = Column(String(200))  
    writer = Column(String(50))  
    content = Column(TEXT)  
    reg_date = Column(DATETIME(timezone=True), default=func.now()) 