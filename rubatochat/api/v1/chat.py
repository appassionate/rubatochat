import asyncio
from typing import AsyncIterable, Awaitable, Callable, List, Optional, Union
from typing import Union
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

from rubatochat.api import db_engine
from .auth import get_current_active_user
from rubatochat.api.v1.apikeys import get_key_by_rank

from rubatochat.core.database.models import User, OpenAIKEYS, Session, add_item, delete_item_by_id, select
from rubatochat.utils.logger import logger
from rubatochat.core.chat.base import ChatOpenAIChat, ChatManager

from langchain.schema import HumanMessage, SystemMessage

# async def wait_done(fn: Awaitable, event: asyncio.Event):
#     try:
#         await fn
#     except Exception as e:
#         print(e)
#         event.set()
#     finally:
#         event.set()

app = APIRouter()

MANAGERS = {} #TODO: use database to store chat manager?

def get_manager(user: User=Depends(get_current_active_user)) -> ChatManager:

    username = user.username

    if MANAGERS.get(username) == None: # cache running chat
        MANAGERS[username] = ChatManager()
    manager = MANAGERS[username]
    return manager

@app.post("/chat/create", tags=["chat"])
async def create_chatopenaichat(
                 api_key_rank:int=0,
                 topic_name:str="unnamed",
                 model_name="gpt-3.5-turbo", 
                 temperature=0.2, #TODO
                 max_tokens=1024, #TODO
                 enable_stream:bool=False,
                 user:User=Depends(get_current_active_user)
                 ):
    
    #这里需要获取用户的名称，再获取得到对应的openaikeys
    #TODO:根据登录信息
    _key = get_key_by_rank(api_key_rank, user=user)
    api_key = _key.content

    # 流式文本生成
    # https://github.com/elevenching/learning-large-model/blob/main/learning_langchain/streaming_chat/server.py
    
    handlers = [AsyncIteratorCallbackHandler()] if enable_stream else []

    chat =  ChatOpenAIChat(openai_api_key=api_key,
                           topic_name=topic_name,
                           model_name=model_name, 
                           temperature=temperature, #TODO
                           max_tokens=max_tokens, #TODO
                           streaming=True,
                           callbacks=handlers,) #打开异步stream
    
    _uuid = chat.uuid
    _responce = chat.question("hello")
    _responce = str(_responce)
    
    logger.info("successfully created an openai chat model.")
    logger.info("chat uuid: "+_uuid)

    manager = get_manager(user)
    if manager.container.get(_uuid):
        #新建的chat不应该在manager中
        raise Exception("chat uuid already exists in manager")
    manager.container[_uuid] = chat

    return {"uuid":_uuid,
            "responce_hello":_responce,
            "chat": manager.container[_uuid],
            }

@app.get("/chat/get", tags=["chat"])
async def get_chat(uuid:str, user:User=Depends(get_current_active_user)):

    _manager = get_manager(user)
    return {"chat_info":_manager.get_chat_info(uuid)}
    #return _get_chat(uuid, username)

@app.get("/chat/uuids", tags=["chat"])
async def list_uuids(user:User=Depends(get_current_active_user)):

    _manager = get_manager(user)
    _res = {"uuids":list(_manager.container.keys())}

    return _res

def _get_chat(uuid:str, user:User=Depends(get_current_active_user)):

    manager = get_manager(user)
    chat = manager.container.get(uuid)
    if chat == None:
        raise Exception("chat uuid not found in manager")
    
    return chat

@app.post("/chat/ask", tags=["chat"])
async def ask2chat(uuid:str, message:str, user:User=Depends(get_current_active_user)):

    #1. 后端如何生成含有uuid的实例
    #2. 如何根据uuid找到对应的chat

    chat = _get_chat(uuid, user)
    hcallbacks = chat.llm.callbacks #todo:流式文本生成句柄？
    answer = chat.question(message)

    return {"uuid":uuid,
            "question":message,
            "answer":answer,
            }

@app.delete("/chat/close", tags=["chat"])
async def close_chat(uuid:str, user:User=Depends(get_current_active_user)):
        
        manager = get_manager(user)
        manager.close_chat(uuid)
    
        return {"uuid":uuid,
                "status":"success",
                }


#TRYTO use streaming response

    #response = chat.question(message)
    # coroutine = wait_done(chat.llm.agenerate(messages=[[HumanMessage(content=mesage)]]), handler.done)
    # task = asyncio.create_task(coroutine)

    # async for token in handler.aiter():
    #     yield f"{token}"
    
    # await task
    #return StreamingResponse(task, media_type="text/event-stream")

# @app.get("/chat/conversation")
# def talk2chat(uuid:str, message:str):
#     return StreamingResponse(ask2chat(uuid, message), media_type="text/event-stream")
