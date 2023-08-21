
#some abstraction already implemented in api/v1/chat.py

# get a chat python file implement from langchain
def get_chat_implement(filename):
    
    #file name is a python script for creating a langchain to  construct a chat manager
    #the file should be in the same directory as this file
    chains = someaction(filename)
    
    
    return chains


def get_chat_manager(chains):
    #chains is a langchain object
    #create a chat manager based on the langchain
    #return the chat manager
    return chat_manager


