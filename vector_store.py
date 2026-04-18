

from langchain_chroma import Chroma
import config_data as config
from config_data import persist_directory


class VectorStoreService(object):
    def __init__(self,embedding_model):
        """

        :param embedding_model: 嵌入向量模型传入

        """
        self.embedding = embedding_model
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory = persist_directory
        )

    def get_retriever(self):
        """
        返回向量检索器,方便加入chain
        :return:
        """
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStoreService(DashScopeEmbeddings(model=config.embedding_model_name)).get_retriever()
    res = retriever.invoke("陀螺仪--MPU6050模块")
    print(res)


