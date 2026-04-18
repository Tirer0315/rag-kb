"""
基于streamlit 的前端页面交互代码
"""


import time
import streamlit as st
from knowlendge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# 文件上传框
upload_file = st.file_uploader(
    "请上传TXT文件",
    type="txt",
    accept_multiple_files=False
)

# session_state 是一个字典,不会随着页面的刷新重置
if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()


# 在文件不为空的情况下,处理文件信息
if upload_file is not None:
    file_name=upload_file.name
    file_type=upload_file.type
    file_size=upload_file.size / 1024  # KB

    st.subheader(f"文件名:{file_name}")
    st.write(f"文件类型:{file_type} | 文件大小:{file_size:.2f}KB")

    # getvalue() 获取上传文件的内容(bytes) decode("utf-8") 转换为字符串
    text = upload_file.getvalue().decode("utf-8")

    with st.spinner("文件上传中..."):
        time.sleep(1)
        # 与后端交互
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.text(result)