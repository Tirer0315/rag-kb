"""
离线流程主要开发
"""


# 知识库
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
import os
import config_data as config
import hashlib
# hashlib可以计算字符串的md5值


def check_md5(md5_str: str):
    """
    检查传入的 md5 字符串是否存在于知识库中
    :return:
    false 表示这个md5 没有被处理
    true  表示这个md5 已经被处理
    """
    if not os.path.exists(config.md5_path):
        # 文件不存在,这个md5没有被处理
        open(config.md5_path, "w" ,encoding="utf-8").close()    # 创建一个空文件
        return False
    else:
        for line in open(config.md5_path, "r" ,encoding="utf-8").readlines():
            line = line.strip()         # 去掉换行符,去掉空格
            if line == md5_str:         # 判断传入的 md5 是否存在于文件中
                return True
        return False




def save_md5(md5_str: str):
    """
    将传入的 md5 添加到知识库中
    :return:
    """
    with open(config.md5_path, "a" ,encoding="utf-8") as f:     # a 追加模式
        f.write(md5_str + "\n")




def get_string_md5(input_str: str, encoding="utf-8"):
    """
    将传入的字符串转化为 md5 字符串(16进制)
    :return:
    """
    # 将字符串还原为 bytes 字节数组
    str_bytes = input_str.encode(encoding)

    # 计算 md5
    md5_obj = hashlib.md5(str_bytes)        # 创建 md5 对象 | 将字节数组传入 md5 对象
    md5_hex = md5_obj.hexdigest()           # 得到 md5 的 16 进制字符串
    return md5_hex




class KnowledgeBaseService(object):
    """
    知识库服务
    """
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)        # 如果文件夹不存在,则创建;存在则跳过
        self.chroma=Chroma(
            collection_name=config.collection_name,         # 数据库的表名,存放在配置文件中
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory=config.persist_directory      # 数据库的存放目录,存放在配置文件中
        )
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,                   # 分割后文本段的最大长度

            chunk_overlap=config.chunk_overlap,             # 分割后文本段之间的重叠长度
            separators=config.separators,                    # 自然段落的划分符号
            length_function=len
        )


    def upload_by_str(self,data: str,filename):
        """
        将传入的字符串转换为md5字符串
        :param data:
        :param filename:
        :return:
        """
        # 获取字符串的 md5
        md5_str = get_string_md5(data)

        # 检查 md5 是否已经处理过
        if check_md5(md5_str):
            return "已经处理过该数据"

        # 判断数据长度是否超过阈值,超过则进行分段处理
        if len(data)>config.max_spilt_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]


        # 标明数据源
        metadata ={
                "source":filename
                , "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                , "operator":"小杭"
            }

        self.chroma.add_texts(                  # 将内容加载到向量库中
            texts=knowledge_chunks,
            metadatas= [metadata for _ in knowledge_chunks]
        )

        save_md5(md5_str)               # 保存 md5
        return "上传成功,内容已经存放到向量库"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str("小杭是一个好学生", "小杭.txt")
    print(r)