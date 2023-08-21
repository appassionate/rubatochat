import time
import requests
import streamlit as st

from rubatochat.api import BACKEND_ADDRESS

from rubatochat.api.v1.apikeys import get_key_by_rank
from streamlit_extras.stylable_container import stylable_container


st.title("💬当前会话")

#检查是否登陆
if ("islogin" not in st.session_state) or (not st.session_state.islogin):
    st.write("您尚未登录, 请先登录。")
    st.stop()

with st.sidebar:
    st.write(st.session_state.user["username"]+", 您好! 欢迎回来!")
    if st.button("退出登录"):

        st.session_state.islogin = False
        if st.session_state.get("token"):
            del st.session_state["token"]
        if st.session_state.get("user"):
            del st.session_state["user"]
        st.experimental_rerun()


def chat_create(api_key_rank:int=0,
                topic_name:str="unnamed",
                model_name="gpt-3.5-turbo", 
                temperature=0.2, #TODO
                max_tokens=1024, #TODO
                enable_stream:bool=False):

    url = BACKEND_ADDRESS+"/chat/create"

    _params = {
        "api_key_rank": api_key_rank,
        "topic_name": topic_name,
        "model_name": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "enable_stream": enable_stream,
    }
    _headers = {"Authorization": "Bearer "+ st.session_state.token}

    response = requests.post(url, params=_params,json={}, headers=_headers)
    if response.status_code == 200:
        _hint = st.success("添加成功",icon="✅")
    else:
        _hint = st.error("添加失败",icon="❌")
    time.sleep(1)
    _hint.empty()

    return response

def chat_get_uuids():

    url = BACKEND_ADDRESS+"/chat/uuids"

    _params = {}
    _headers = {"Authorization": "Bearer "+ st.session_state.token}

    response = requests.get(url, params=_params,headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("查询失败",icon="❌")

    return response

def chat_get(uuid):
    
        url = BACKEND_ADDRESS+"/chat/get"
    
        _params = {"uuid": uuid,}
        _headers = {"Authorization": "Bearer "+ st.session_state.token}
    
        response = requests.get(url, params=_params, headers=_headers)
        if not response.status_code == 200:
            _hint = st.error("查询失败",icon="❌")
    
        return response


def chat_close(uuid):
    
        url = BACKEND_ADDRESS+"/chat/close"
    
        _params = {"uuid": uuid,}
        _headers = {"Authorization": "Bearer "+ st.session_state.token}
    
        response = requests.delete(url, params=_params, headers=_headers)
        if not response.status_code == 200:
            _hint = st.error("关闭失败",icon="❌")
        else:
            _hint = st.success("关闭成功",icon="✅")
            time.sleep(1)
            _hint.empty()
    
        return response

#新建会话expander
with st.expander("新建Chat会话: "):

    _col0, _col1 = st.columns([3,1])
    _col2, _col3 = st.columns([1,1])
    with _col0:
        _topic_name = st.text_input(label="会话名称", )
    with _col1:
        _key_rank = st.text_input(label="OPENAI KEY RANK:")
    _model_name = st.text_input(label="模型类型",value="gpt-3.5-turbo" )
    with _col2:
        _model_temperature=st.text_input(label="模型温度", value=0.2)
    with _col3:
        _model_max_tokens=st.text_input(label="最大TOKEN数", value=1024)

    if st.button("新建"):
        chat_create(api_key_rank=_key_rank,
                    topic_name=_topic_name,
                    model_name=_model_name,
                    temperature=_model_temperature,
                    max_tokens=_model_max_tokens,
                    enable_stream=False,
                    )





def build_chat_unit(chat_id, stkey_prefix:str=""):


    _container = st.container()
    with _container:

        st.write(chat_id)

        if st.button("结束会话", key=stkey_prefix+"but_stop"+chat_id["uuid"]):
            chat_close(chat_id["uuid"])
            st.experimental_rerun()

    return 1



# 得到运行中的列表

#会话列表
st.markdown("#### 🏠会话列表: ")
uuids = chat_get_uuids().json()["uuids"]
st.markdown(f"##### 运行总数: {len(uuids)}")

chats_running = [chat_get(uuid).json()["chat_info"] for uuid in uuids]




for i, _chat in enumerate(chats_running):
    
    _rep = ""
    _rep = _rep + f"No. {i}    "
    _rep = _rep + "会话名称: "+ _chat["topic_name"] + "    "
    _rep = _rep + "SHORT_UUID: "+ _chat["uuid"][-8:] + "    "
    #_rep = _rep + "Status: "+ "running "

    with st.expander(_rep):
        build_chat_unit(_chat, )
        