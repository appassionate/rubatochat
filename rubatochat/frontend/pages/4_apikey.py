# 写一个streamlit 的页面用于输出 用户所属的apikeys
import time
import requests

import streamlit as st
from urllib3.exceptions import ConnectTimeoutError

import streamlit as st
from rubatochat.api import db_engine, BACKEND_ADDRESS
from rubatochat.api.v1.apikeys import get_key_by_rank, is_open_ai_key_valid

from streamlit_extras.stylable_container import stylable_container

st.title("🔑OPENAI API KEYS 管理")

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

#这些函数都带状态，不需要传入user信息

# 需要的request实现
def apikey_create(newkey):

    _headers = {"Authorization": "Bearer "+ st.session_state.token}
    _params = {}
    url = BACKEND_ADDRESS+"/openaikeys/add"

    response = requests.post(url, params=_params, json=[newkey], headers=_headers)
    if response.status_code == 200:
        _hint = st.success("添加成功",icon="✅")
    else:
        _hint = st.error("添加失败",icon="❌")
    time.sleep(1)
    _hint.empty()

    return response

def apikey_count():

    _params = {}
    _headers = {"Authorization": "Bearer "+ st.session_state.token}

    url = BACKEND_ADDRESS+"/openaikeys/count"
    response = requests.get(url, params=_params,headers=_headers)
    st.write(response)
    if not response.status_code == 200:
        _hint = st.error("数量查询失败",icon="❌")
        raise Exception("数量查询失败")

    return response

def apikey_check(rank):

    _params = {"rank": rank,}
    _headers = {"Authorization": "Bearer "+ st.session_state.token}

    url = BACKEND_ADDRESS+"/openaikeys/check"

    response = requests.get(url, params=_params,headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("查询失败",icon="❌")
        #_hint.empty()
    
    return response


def apikey_valid(key_id):

    _params = {"key_id": key_id,}
    _headers = {"Authorization": "Bearer "+ st.session_state.token}

    url = BACKEND_ADDRESS+"/openaikeys/isvalid"
    response = requests.get(url, params=_params, headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("查询失败",icon="❌")
        #_hint.empty()
    else:
        _hint = st.success("查询成功",icon="✅")
        time.sleep(1)
        _hint.empty()
    
    return response


def apikey_delete(key_id):
    
    _params = {"key_id": key_id,}
    _headers = {"Authorization": "Bearer "+ st.session_state.token}

    url = BACKEND_ADDRESS+"/openaikeys/delete"

    response = requests.delete(url, params=_params, headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("删除失败",icon="❌")
        #_hint.empty()
    else:
        _hint = st.success("删除成功",icon="✅")
        time.sleep(1)
        _hint.empty()
    
    return response

def apikey_update(key_id, new_key):

    _params = {
        "key_id":key_id,
        "new_key": new_key,
    }
    _headers = {"Authorization": "Bearer "+ st.session_state.token}


    url = BACKEND_ADDRESS+"/openaikeys/update"

    response = requests.post(url, params=_params, json={},headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("更新失败",icon="❌")
        #_hint.empty()
    else:
        _hint = st.success("更新成功",icon="✅")
        time.sleep(1)
        _hint.empty()
    
    return response


with st.expander("添加新的OPENAI API KEY:"):
    
    _newkey = st.text_input(label="OPENAI KEY:", type="password")
    #st.text_input(label="备注", )
    if st.button("新建"):
        try:
            _res = apikey_create(newkey=_newkey)
            st.experimental_rerun()
        except ConnectTimeoutError:
            st.error("连接超时，请检查网络连接")

st.markdown("### OPENAI API KEYS当前列表: ", )

def build_key_unit(key_rank: int, key_id:int, key_content: str, stkey_prefix:str=""):


    _container = st.container()

    with _container:

        i = key_rank
        _stpre = stkey_prefix

        current_key = st.text_input(label=f"KEY RANK: {i}", value=key_content, type="password",key=f"key_{i}")
        _col_create, _col_valid, _col_edit, _col_del = st.columns([1,1,1,1],gap="small")

        with _col_create:
            if st.button("创建会话",key=_stpre+f"but_create_{i}",):
                st.write("fake create")
        with _col_edit:
            if st.button("保存更改",key=_stpre+f"but_edit_{i}",):
                apikey_update(key_id=key_id, new_key=current_key)
                
        with _col_valid:
            if st.button("检查",key=_stpre+f"but_check_{i}",):
                _valid=apikey_valid(key_id=key_id).json()["is_valid"]
                if _valid:
                    st.success("当前KEY有效")
                else:
                    st.error("当前KEY无效")
        with _col_del:
            if st.button("删除", key=_stpre+f"but_del_{i}"):
                _res = apikey_delete(key_id=key_id) #根据key的主键id删除
                if _res.status_code == 200:
                    return 0
                st.experimental_rerun()

    return 1



with st.expander("管理秘钥"):


    _count = apikey_count().json()["count"]
    st.markdown(f"##### 当前秘钥数量: {_count}")
    if not _count:
        st.write("当前没有保存的秘钥，请进行添加")

    # st.write("Hello world")
    for i in range(_count):
        _key = apikey_check(rank=i).json()["key"]
        _key_id = apikey_check(rank=i).json()["key_id"]
        build_key_unit(key_rank=i, key_id=_key_id, key_content=_key)
        # _key, _ = st.columns([5,1])
        # with _key:

    # cols = st.columns(4,)
    # with cols[0:2]:
    #     st.button("edit")
    # with cols[3]:
    #     st.button("delete")

    #st.button("刷新", on_click=get_key_by_rank(username=username, rank=0))
