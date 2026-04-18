import time
from rag import RagService
import streamlit as st
import config_data as config


# 标题
st.title("AI智能客服")

st.divider()        # 分割线


# 记录缓存
if "message" not in st.session_state:
    st.session_state.message = [{"role": "assistant", "content": "您好,请问有什么可以帮助你的?"}]
# 加载缓存
for message in st.session_state.message:
    st.chat_message(message["role"]).write(message["content"])

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()


# 用户输入框
prompt = st.chat_input("请输入您要问的问题")
if prompt:
    # 显示用户输入
    st.chat_message("user").write(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})

    ai_list=[]
    with st.spinner("思考中..."):
        # 模拟处理用户输入
        res_stream = st.session_state["rag"].chain.stream({"input": prompt},config.session_config)

        def capture(generator, ai_list):
            for chunk in generator:
                ai_list.append(chunk)
                yield chunk


        # 显示处理结果
        st.chat_message("assistant").write(capture(res_stream,ai_list))
        st.session_state.message.append({"role": "assistant", "content": "".join(ai_list)})


