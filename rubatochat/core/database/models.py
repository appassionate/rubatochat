from sqlmodel import Field, SQLModel, create_engine, Session
from sqlmodel import select

from typing import Union, List, Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str=Field(unique=True,)
    password: str
    # hint: the field should be DETEMRIED correcly, or it cant be serialized
    email:Optional[str] = Field(default=None)
    fullname:Optional[str] = Field(default=None)
    disabled:bool = Field(default=False)
    create_at:datetime=Field(default_factory=datetime.utcnow)
    
    #last_login:datetime=Field(default_factory=datetime.utcnow)

class OpenAIKEYS(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    content: str
    user_id: int = Field(foreign_key="user.id")
    create_at: datetime = Field(default_factory=datetime.utcnow)
    isvalid: bool = Field(default=True)

# model for a initialized chat
class ChatID(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default=None, unique=True)
    user_id: int = Field(foreign_key="user.id")
    create_at: datetime = Field(default_factory=datetime.utcnow)
    
    history_uuid: str = Field(default=None,)


#TODO: have to implement the chat history
class ChatHistory(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    history_id: int = Field(foreign_key="chatid.id")
    history_name: Optional[str] = Field(default=None)
    chat_id: int=Field(foreign_key="chatid.id")
    question: Optional[str] = Field(default=None)
    answer: Optional[str] = Field(default=None)



item_type_dict = {
    "user": User,
    "openaikeys": OpenAIKEYS,
}



#TODO: more elegant way to do this?
# method to add a user
def add_item(engine, item_type, **kwargs):
    
    try:
        item = item_type_dict[item_type](**kwargs)
    except:
        raise Exception(f"item_type: {item_type} not found")
    
    try:
        with Session(engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

            print(f"item: {item} has been added.")
    except:
        raise Exception("item failed to add")

        
    return item

def delete_item_by_id(engine, item_type, id):
    
    try:
        itemtype = item_type_dict[item_type]
    except:
        raise Exception(f"item_type: {item_type} not found")
    
    with Session(engine) as session:
        
        stmt = select(itemtype).where(itemtype.id == id)
        data = session.exec(stmt)

        #print(data.one())
        if data:
            try:
                session.delete(data.one())
                session.commit()
                #session.refresh(item)
                print(f"ID: {id} in {item_type} has been deleted.")
            except:
                raise Exception("items id not found")

    return data
