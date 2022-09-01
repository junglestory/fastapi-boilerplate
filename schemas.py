from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    seq: Union[int, None] = None
    journal_id: str
    title:  str
    publish_date: Union[str, None] = None
    link_url: Union[str, None] = None
    writer: Union[str, None] = None
    content: Union[str, None] = None

    class Config:
        orm_mode = True