import time
import requests
import streamlit as st

from rubatochat.api import BACKEND_ADDRESS

from rubatochat.api.v1.apikeys import get_key_by_rank
from streamlit_extras.stylable_container import stylable_container

from rubatochat.api import db_engine
from rubatochat.api.v1.apikeys import get_key_by_rank

def chat_get_uuids():

    url = BACKEND_ADDRESS+"/chat/uuids"

    _params = {}
    _headers = {"Authorization": "Bearer "+ st.session_state.token}

    response = requests.get(url, params=_params,json={}, headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("查询失败",icon="❌")

    return response


def chat_ask(uuid, message):

    url = BACKEND_ADDRESS+"/chat/ask"

    _params = {
        "uuid": uuid,
        "message": message,
    }
    _headers = {"Authorization": "Bearer "+ st.session_state.token}
    
    response = requests.post(url, params=_params,json={}, headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("提问失败，请检查网络和APIKEY",icon="❌")

    return response

#检查是否登陆
if ("islogin" not in st.session_state) or (not st.session_state.islogin):
    st.write("您尚未登录, 请先登录。")
    st.stop()

USERNAME = "snow"

with st.sidebar:

    uuids = chat_get_uuids().json()["uuids"]
    uuid = st.selectbox("选择会话", uuids)

    with st.spinner(text='In progress'):

        # bond font
        _chat_intro = st.markdown("## 当前Chat会话信息: ", )
        st.text_area(label="UUID: ", value=uuid, height=6,)

        #_data = get_chat_info()
        #st输出一个表格数据
        #st.text_area(label="OPENAI_KEY: ", value=_df["openai_api_key"], height=10,)
        
        #st.text_area(label="OPENAI_KEY: ", value=_data["openai_api_key"], height=10,)
        #st.text_input(label="OPENAI_KEY: ", value=_data["openai_api_key"], type="password")
        #st.write(_df) #



st.title("💬 RubatoChat")


if not uuid:
    st.markdown("   请先新建会话")
    st.stop()

st.write("当前使用会话: " + uuid[-8:])

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you? 今天想问点什么？"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if _question := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    
    # openai.api_key = openai_api_key
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_message("user").write(prompt)
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)

    st.session_state.messages.append({"role": "user", "content": _question})
    st.chat_message("user").write(_question)
    response = chat_ask(uuid, _question)
    # st.write(type(msg))
    # st.write(msg.content)
    _answer = response.json()["answer"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": _answer})
    #st.write(answer)
    st.chat_message("assistant").write(_answer)

