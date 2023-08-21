#write a chat model based on langchain
import abc
import uuid
from langchain.llms import OpenAI
from typing import List, Optional, Union, Dict

from langchain.chat_models import ChatOpenAI

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


# has not using this class
class BaseChatClient(abc.ABC):
    
    uuid: str
    chat_type: str

    def question():
        
        pass
    
    async def _send_message(self, query):
        pass
    
    
    def close(self, ):
        return
    
    def is_valid(self):
        pass
    
    def reopen(self):
        pass
    
    def ping(self):
        pass
    

class ChatOpenAIChat():
    
    chat_type="chatopenai"
    topic_name: str
    model_name: str
    uuid: str
    openai_api_key: str
    #history: TODO: 加载保存的history
    
    @classmethod
    def from_dict(cls, _dict):
        
        return cls(**_dict)
    
    @classmethod
    def from_uuid(cls, uuid, manager):
        
        #TODO: 从数据库的uuid 取得client
        # if in running:
        # return (RUNNING_CHAT[uuid])

        return manager.get_chat(uuid)
    
    def _get_client_uuid(self, model_name):
        return self.chat_type+"_"+model_name+"_"+str(uuid.uuid4())

    def __init__(self, 
                 openai_api_key:str,
                 model_name="gpt-3.5-turbo", 
                 topic_name="unnamed",
                 temperature=0.2, #TODO
                 max_tokens=1024, #TODO
                 **kwargs):
        #TODO 这一块是直接用llm的比较好？
        self.topic_name = topic_name
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.uuid = self._get_client_uuid(model_name)
        self.llm = ChatOpenAI(model_name=model_name,
                              openai_api_key=self._get_openai_api_key(openai_api_key),
                              temperature=temperature,
                              max_tokens=max_tokens,
                              **kwargs
                              ) #TODO: AGENT?
            
    def _get_openai_api_key(self, key): #TODO:进行用户验证
        return key
    
    def question(self, message,):
        
        return self.llm([HumanMessage(content=message)])
        

class ChatManager():

    container: Dict[str,ChatOpenAIChat]
    max_volume: int=20 #TODO:how to implement MAX?


    def __init__(self, max_volume=20):
        self.container = {}
        self.max_volume = max_volume

    def get_chat(self, uuid):
        return self.container.get(uuid)

    def add_chat(self, chat:ChatOpenAIChat):

        self.container[chat.uuid] = chat
        return chat.uuid

    def close_chat(self, uuid):

        #self.container[uuid].close()
        self.container.pop(uuid)

    def get_chat_info(self, uuid):

        _chat = self.container.get(uuid)
        if not _chat:
            raise Exception("chat uuid not found in manager.")

        return {"uuid": _chat.uuid,
                "topic_name":_chat.topic_name,
                "chat_type":_chat.chat_type,
                "model_name":_chat.llm.model_name,
                "temperature":_chat.llm.temperature,
                "max_tokens":_chat.llm.max_tokens,
                #"openai_api_key":_chat.openai_api_key,
                }
