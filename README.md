🤖 基于通义千问 + Chroma+Streamlit 的 RAG 智能知识库问答系统

一套本地私有化部署、开箱即用的检索增强生成（RAG）智能问答系统，支持 TXT 文档上传入库、MD5 去重、流式问答输出、会话历史持久化，严格依据私有知识库精准作答，无外部数据依赖，适合个人 / 团队搭建私有知识助手。

✨ 项目核心功能

- 私有知识库管理：支持 TXT 文件在线上传，自动文本分片、MD5 去重、向量入库，避免重复存储
- 本地向量存储：基于 Chroma 轻量级向量库，数据全本地持久化，无云端泄露风险
- 流式问答输出：Streamlit 前端实现打字机式流式回复，交互更流畅
- 多轮对话记忆：会话历史本地 JSON 持久化，支持上下文连贯问答
- 极简可视化界面：双页面分离设计（知识库上传 + 智能问答），零前端成本
- 精准检索生成：基于通义千问大模型 + DashScope 向量模型，拒绝回答幻觉

🛠️ 技术栈

表格

  技术 / 框架            	用途                 
  Python 3.8+        	开发语言               
  LangChain          	RAG 流程编排、大模型调用、向量检索
  通义千问 (ChatTongyi)  	对话生成大模型            
  DashScopeEmbeddings	文本向量化模型            
  Chroma             	本地轻量级向量数据库         
  Streamlit          	快速搭建 Web 交互前端      
  JSON / 本地文件        	会话历史、MD5 去重记录持久化   

📁 完整项目结构

plaintext

    AI-RAG-Knowledge-Base/
    ├── app_file_upload.py    # 知识库文件上传前端页面
    ├── app_qa.py             # 智能问答前端页面（流式输出+对话记忆）
    ├── rag.py                # RAG核心问答链（检索+提示词+大模型+会话历史）
    ├── vector_store.py       # 向量库服务封装（Chroma检索器）
    ├── knowlendge_base.py    # 知识库核心服务（文件处理、分片、MD5去重、入库）
    ├── file_history_store.py # 会话历史本地持久化管理
    ├── config_data.py        # 全局配置文件（模型、路径、分片参数）
    ├── md5.txt               # 已上传文件MD5记录（自动生成）
    ├── chroma_db/            # Chroma向量数据库存储目录（自动生成）
    ├── chat_history/         # 会话历史本地存储目录（自动生成）
    └── requirements.txt      # 项目依赖清单

🚀 快速部署

1. 环境准备

- 安装 Python 3.8 及以上版本
- 前往阿里云 DashScope 平台申请 API Key（通义千问 / 向量模型调用）

2. 安装依赖

bash

运行

    pip install -r requirements.txt

3. 配置环境变量

bash

运行

    # Windows
    set DASHSCOPE_API_KEY=你的DashScope_API_Key
    
    # macOS/Linux
    export DASHSCOPE_API_KEY=你的DashScope_API_Key

4. 启动项目

启动知识库上传页面

bash

运行

    streamlit run app_file_upload.py

启动智能问答页面

bash

运行

    streamlit run app_qa.py

📖 使用流程

1. 上传知识库文档
   
   打开文件上传页面 → 上传 TXT 格式文档 → 系统自动完成分片、去重、向量入库
2. 发起智能问答
   
   打开问答页面 → 输入问题 → 系统流式输出回答，自动关联知识库内容
3. 多轮对话
   
   支持上下文连续提问，会话历史本地保存，刷新页面不丢失

⚙️ 核心配置（config_data.py）

python

运行

    # 向量库配置
    collection_name = "rag"
    persist_directory = "./chroma_db"
    
    # 文本分片配置
    chunk_size = 25
    chunk_overlap = 5
    max_spilt_char_number = 25
    
    # 模型配置
    embedding_model_name = "text-embedding-v4"
    chat_model_name = "qwen3-max"
    
    # 检索配置
    similarity_threshold = 2
    
    # 会话配置
    session_config = {"configurable": {"session_id": "001"}}

🧩 核心模块说明

1. 知识库模块（knowlendge_base.py）

- 实现 TXT 文本读取、MD5 文件去重、递归文本分片
- 对接 Chroma 完成向量入库，支持批量文档处理

2. 向量库模块（vector_store.py）

- 封装 Chroma 向量库，提供标准化检索器接口
- 支持配置相似度检索数量，适配 RAG 检索流程

3. RAG 问答模块（rag.py）

- 构建完整检索增强问答链，集成上下文记忆
- 支持流式输出，对接通义千问大模型生成回答

4. 会话历史模块（file_history_store.py）

- 基于本地 JSON 文件实现会话历史持久化
- 支持多会话 ID 管理，上下文不混乱

5. 前端界面

- app_file_upload.py：文件上传、进度提示、入库结果展示
- app_qa.py：聊天界面、流式输出、对话历史缓存

❗ 常见问题

1. 流式输出历史记录丢失

已修复：通过迭代器拼接完整字符串后存入会话状态，确保历史记录稳定存储

2. 无法打开 chroma.sqlite3

该文件为 Chroma 数据库文件，需用 DB Browser for SQLite 或 PyCharm Database 工具打开

3. 模型调用报错

检查 DashScope API Key 是否正确配置，账号是否有对应模型调用权限

4. 文件上传重复

系统已做 MD5 去重，重复文件会提示 “已经处理过该数据”

📌 项目亮点

1. 全本地私有化：无第三方云服务依赖，数据安全可控
2. 开箱即用：配置简单，两行命令启动完整服务
3. 流式交互：打字机式输出，提升用户体验
4. 模块化设计：代码解耦，易扩展、易维护
5. 生产级功能：文件去重、会话记忆、异常处理齐全

📝 免责声明

本项目仅供学习与内部使用，调用通义千问 / DashScope 模型产生的费用由使用者自行承担，请勿用于商业用途。

---

配套 requirements.txt 文件

plaintext

    streamlit>=1.30.0
    langchain>=0.1.0
    langchain-community>=0.0.10
    langchain-core>=0.1.10
    langchain-chroma>=0.1.0
    chromadb>=0.4.22
    dashscope>=1.14.0
