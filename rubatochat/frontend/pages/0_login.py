import streamlit as st
import time
from rubatochat.api import BACKEND_ADDRESS

import requests


#登录设置

def access_token(username, password):

    url = BACKEND_ADDRESS+"/token"

    _data = {
        "username": username,
        "password": password,
    }

    response = requests.post(url, data=_data)
    if response.status_code == 200:
        _hint = st.success("登录成功",icon="✅")
    else:
        _hint = st.error("登录失败，请检查账号密码",icon="❌")
    time.sleep(1)
    _hint.empty()
    
    return response

def access_user():

    url = BACKEND_ADDRESS+"/users/me"
    _headers = {"Authorization": "Bearer "+ token}
    
    response = requests.get(url, data={}, headers=_headers)
    if not response.status_code == 200:
        _hint = st.error("登录信息失效，请重新登录。",icon="❌")
    time.sleep(1)
    return response

#name, authentication_status, username = authenticator.login('Login', 'main')

_islogin = False #写成state 不然每次刷新都会重置

if "islogin" not in st.session_state:
    st.session_state["islogin"] = False


if not st.session_state.islogin:

    st.error("您尚未登录。")
    with st.container():
        usnm = st.text_input("用户名：", value="", key="username")
        pswd = st.text_input("密码：", value="", key="password", type="password")

        if st.button("登录"):
            token = access_token(usnm, pswd)
            if token.status_code == 200:
                token = token.json()["access_token"]
                st.session_state["token"] = token
                user = access_user()
                st.session_state["user"] = user.json()
                st.session_state.islogin = True
                
                st.experimental_rerun()

else:
    # 输出当前用户基本信息
    st.write(st.session_state.user["username"]+", 您好! 欢迎回来!")

    if st.button("退出登录"):

        st.session_state.islogin = False
        if st.session_state.get("token"):
            del st.session_state["token"]
        if st.session_state.get("user"):
            del st.session_state["user"]
        st.experimental_rerun()


#登录基本配置

# 登录保存token到state

# 登录对接后端数据库和api