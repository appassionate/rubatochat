_key = "sk-xxxxxxxxxxxx"


import numpy as np
import matplotlib.pyplot as plt

from langchain.agents import tool
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI


class CalcData(BaseModel):
    numA: int
    numB: int 
    
    
@tool
def get_multi_output(cdata:CalcData):
    """return cdata calculation output: numA*numB"""
    return cdata.numA * cdata.numB
@tool
def get_square_output(number):
    "return number^2, the square result"
    return number**2
    
    
llm = ChatOpenAI(
                 model="gpt-3.5-turbo", 
                 temperature=0, 
                 base_url="https://api.moonshot.cn/v1",
                 openai_api_key=_key)
                 
tools = [get_plus_output, get_square_output]
llm_with_tools = llm.bind_tools(tools)


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            # "You are very powerful assistant, but don't know current events.",
            "You are very powerful mathmatical processors, for each query validate the quesition and return the result, otherwise cancel",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


lst = list(agent_executor.stream({"input": "numA:7, numB:3 multi them, and sqaure the answer,then run the numA*ans, and ans^2" , }))  # Yeah this worked !!



