"""
配置文件
"""

md5_path = "./md5.txt"

# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# spliter
chunk_size = 25
chunk_overlap = 5
separators = [",", ".", "?", "!", " ", "\n","\n\n","","。","？","，","\r\n"]
max_spilt_char_number = 25    # 文本分割的阈值


#
similarity_threshold = 2            # 相似度阈值,检索返回匹配的文档数量


# 嵌入模型名称
embedding_model_name = "text-embedding-v4"

# 聊天模型
chat_model_name = "qwen3-max"

#
session_config = {
        "configurable":{
            "session_id": "001"
        }
    }