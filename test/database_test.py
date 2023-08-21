from rubatochat.core.database.models import User, OpenAIKEYS,ChatHistory, ChatID, add_item, delete_item_by_id
from rubatochat.api import DB_URL
from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine

engine = create_engine(DB_URL)
User.metadata.create_all(engine)
OpenAIKEYS.metadata.create_all(engine)

#then, check the username and password in the database


# add user item to database
add_item(engine, 
        "user", 
        id=3, 
        username="root", 
        password="root",
        fullname="root",
        email="1@1.com",
        disabled=False,
        created_at=datetime.utcnow())

_del = delete_item_by_id(engine, "user", id=3)
print(_del)