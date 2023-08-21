import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to RubatoChat webserver! 👋")

st.markdown(
    """

# 你好！

这里是一个ChatGPT的交互式网页，基于FastAPI, LangChain, streamlit进行开发。

### 它将支持以下功能

- 用户登录
- 多用户保存私人OPENAI-API-KEYS
- 创建会话并进行交互式交流
"""
)


#option = st.sidebar.selectbox('选择一个选项', ('选项1', '选项2', '选项3'))




with st.sidebar:

    if st.session_state.get("islogin"):
        st.write(st.session_state.user["username"]+", 您好! 欢迎回来!")
        if st.button("退出登录"):

            st.session_state.islogin = False
            if st.session_state.get("token"):
                del st.session_state["token"]
            if st.session_state.get("user"):
                del st.session_state["user"]
            st.experimental_rerun()
