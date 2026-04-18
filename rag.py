"""

"""
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
from vector_store import VectorStoreService
from file_history_store import get_history
import config_data as config


def print_prompt(prompt):
    """
    打印prompt
    :param prompt:
    :return:
    """
    print('=='*13)
    print(prompt.to_string())
    print('=='*13)

    return prompt


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding_model=DashScopeEmbeddings(
                model=config.embedding_model_name)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主"
                           "简洁专业的回答用户的问题,参考资料为:\n{context}"),
                ("system","我提供的用户历史会话记录如下:"),

                MessagesPlaceholder("history"),
                ("human", "{input}")
            ]
        )
        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()


    def __get_chain(self):
        """
        获取最终执行链
        :param self:
        :return:
        """
        retriever = self.vector_service.get_retriever()

        def format_document(documents: list[Document]):
            """
            格式化文档
            :param documents:
            :return:
            """
            if documents is None or len(documents) == 0:
                return "无相关参考资料"
            formatted_str = ""
            for doc in documents:
                formatted_str += f"文档片段:{doc.page_content}\n文档原数据:{doc.metadata}\n\n"

            return formatted_str

        def format_for_retriever(value):
            return value["input"]

        def format_for_prompt_template(value):
            new_value={}
            new_value["input"] = value["input"]["input"]
            new_value["history"] = value["input"]["history"]
            new_value["context"] = value["context"]
            return new_value

        chain=(
            {
                "input": RunnablePassthrough(),
                "context" : RunnableLambda(format_for_retriever) | retriever | format_document
             } | RunnableLambda(format_for_prompt_template)| self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
             chain,
             get_history,
             input_messages_key="input",
             history_messages_key="history"
        )


        return conversation_chain


if __name__ == '__main__':
    # session_id配置

    rag_service = RagService()
    res = rag_service.chain.invoke({"input": "IO"}, session_config)
    print(res)