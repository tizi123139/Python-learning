

# Langchain

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/python-learning/20260716110215983.png)

| 组件                            | 作用                   | 核心功能                                                | 常见用途                         |
| :------------------------------ | :--------------------- | :------------------------------------------------------ | :------------------------------- |
| **Models（模型）**              | 连接大语言模型         | 统一模型接口支持多模型切换调用 GPT / Claude / Gemini 等 | 聊天机器人文本生成AI 问答        |
| **Prompts（提示词模板）**       | 管理 Prompt 模板       | Prompt 参数化动态变量替换模板复用                       | AI 对话内容生成结构化输出        |
| **Document Loader（文档加载）** | 读取外部文档数据       | 加载 PDF / TXT / DOCX读取网页与数据库统一文档格式       | 知识库RAG 系统文档问答           |
| **Text Splitter（文本切分）**   | 拆分长文本             | 文本 Chunk 切分控制 Token 长度优化向量检索              | RAG向量数据库长文本处理          |
| **Memory（记忆）**              | 实现上下文记忆         | 保存聊天历史长期记忆对话状态管理                        | 聊天机器人AI 助手Agent           |
| **Retriever（检索器）**         | 检索相关知识内容       | 向量搜索语义检索RAG 数据召回                            | 企业知识库AI 搜索文档问答        |
| **Tools（工具）**               | 调用外部工具与 API     | 搜索互联网数据库查询执行代码                            | AI Agent自动化任务数据分析       |
| **Output Parser（输出解析器）** | 解析模型输出结果       | 结构化输出JSON 解析格式校验                             | API 返回自动化系统数据处理       |
| **Chains（链）**                | 组合多个组件形成工作流 | 多步骤执行流程编排组件串联                              | 复杂 AI 应用RAG 工作流Agent 系统 |

## RAG

RAG（Retrieval-Augmented Generation）即检索增强生成，为大模型提供了从特定数据源检索到的信息，以此来修正和补充生成的答案。可以总结为一个公式：RAG = 检索技术 + LLM 提示

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/python-learning/20260716103850930.png)

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/python-learning/20260716125514140.png)

## 文档加载与切分

### Document Loader——加载文档

| Loader                     | 来源          | 安装包                               |
| :------------------------- | :------------ | :----------------------------------- |
| TextLoader                 | .txt 文件     | langchain（内置）                    |
| PyPDFLoader                | PDF 文件      | langchain-community + pypdf          |
| WebBaseLoader              | 网页 URL      | langchain-community + beautifulsoup4 |
| CSVLoader                  | CSV 文件      | langchain-community                  |
| UnstructuredMarkdownLoader | Markdown 文件 | langchain-community + unstructured   |

```
# 加载文本文件（内置，无需额外安装）
from langchain_community.document_loaders import TextLoader

loader = TextLoader("knowledge.txt", encoding="utf-8")
docs = loader.load()

print(f"加载了 {len(docs)} 个文档")
print(f"内容预览: {docs[0].page_content[:150]}...")
```

### Text Splitter——文档切分

```
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 创建切分器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,         # 每块最多 500 个字符
    chunk_overlap=50,       # 块之间重叠 50 个字符
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    # 优先按段落分割，然后是句子，最后是字符
)

# 示例文档
long_text = """菜鸟教程（RUNOOB）是一个免费的编程学习平台。

平台提供了丰富的编程语言教程，包括但不限于：
- Python 教程：从基础语法到数据分析
- Java 教程：面向对象编程到 Spring 框架
- 前端教程：HTML、CSS、JavaScript 及其框架

所有教程都配有详细的代码示例和在线运行环境。
学习者可以通过边学边练的方式快速掌握编程技能。"""

# 切分文档
chunks = text_splitter.split_text(long_text)
```



## Agent

Agent 的核心是一个简单的循环：**调用模型 → 检查是否需要工具 → 执行工具 → 重复**。直到模型不再请求工具调用，Agent 停止并返回最终结果。

```
模型判断需要调用某个工具 → 执行工具并拿到结果 → 模型根据结果继续思考 → 可能再调用工具 → 直到得出最终答案。
```



![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/python-learning/20260716110404017.png)

## 消息类型



| 类型          | 角色    | 说明                               | 典型内容                 |
| :------------ | :------ | :--------------------------------- | :----------------------- |
| HumanMessage  | 用户    | 用户发送的消息                     | "今天天气怎么样？"       |
| AIMessage     | AI 助手 | 模型的回复，可能包含 tool_calls    | "今天杭州晴天，25°C"     |
| SystemMessage | 系统    | 系统指令，定义 AI 的角色和行为规则 | "你是一个专业的天气助手" |
| ToolMessage   | 工具    | 工具执行后的返回结果               | "晴，25°C，湿度 60%"     |



## 中间件

| 钩子            | 执行频率     | 执行位置     | 主要用途                     |
| :-------------- | :----------- | :----------- | :--------------------------- |
| before_agent    | 一次         | Agent 开始前 | 初始化、权限检查、输入预处理 |
| before_model    | 每次循环     | 模型调用前   | 消息预处理、动态上下文注入   |
| wrap_model_call | 每次循环     | 包裹模型调用 | 重试、降级、缓存、请求改写   |
| after_model     | 每次循环     | 模型调用后   | 内容审核、响应过滤、日志     |
| wrap_tool_call  | 每次工具调用 | 包裹工具执行 | 工具重试、结果缓存、参数改写 |
| after_agent     | 一次         | Agent 结束后 | 格式化输出、统计、清理资源   |

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/python-learning/20260716130524891.png)

```cmd
streamlit run app_qa.py
```

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/java-learning/20260715181158338.png)

# 智扫通机器人智能客服

## 项目结构

```
├── app.py                      # Streamlit 入口（Web UI）
├── agent/
│   ├── react_agent.py          # ReAct 智能体核心
│   └── tools/
│       ├── agent_tools.py      # 七种工具定义
│       └── middleware.py       # 中间件（监控/日志/提示词切换）
├── rag/
│   ├── rag_service.py          # RAG 检索增强生成服务
│   └── vector_store.py         # ChromaDB 向量库管理
├── model/
│   └── factory.py              # 模型工厂（通义千问 + 嵌入模型）
├── config/
│   ├── agent.yml               # 智能体配置
│   ├── chroma.yml              # 向量库配置（分块/检索参数）
│   ├── prompts.yml             # 提示词路径管理
│   └── rag.yml                 # 模型选择
├── prompts/
│   ├── main_prompt.txt         # 主对话提示词
│   ├── rag_summarize_prompt.txt # RAG 摘要提示词
│   └── report_prompt.txt       # 报告生成提示词
├── data/
│   ├── external/records.csv    # 用户使用记录数据
│   ├── 扫地机器人 100 问.txt    # 知识库 - FAQ
│   ├── 故障排除.txt             # 知识库 - 故障处理
│   ├── 维护保养.txt             # 知识库 - 维护保养
│   └── 选购指南.txt             # 知识库 - 选购建议
└── utils/
    ├── config_handler.py       # YAML 配置加载
    ├── file_handler.py         # 文件处理
    ├── logger_handler.py       # 日志管理
    ├── path_tool.py            # 路径工具
    └── prompt_loader.py        # 提示词加载器
```

## 技术栈

| 组件           | 技术选型                          |
| -------------- | --------------------------------- |
| **LLM**        | 通义千问 `qwen3-max`（DashScope） |
| **Embedding**  | `text-embedding-v4`（DashScope）  |
| **向量数据库** | ChromaDB                          |
| **智能体框架** | LangChain ReAct Agent             |
| **Web UI**     | Streamlit                         |
| **编程语言**   | Python 3.10+                      |

## 工具

| 工具                      | 功能                               |
| ------------------------- | ---------------------------------- |
| `rag_summarize`           | 从向量知识库检索扫地机器人专业知识 |
| `get_weather`             | 查询指定城市实时天气（湿度/降雨）  |
| `get_user_location`       | 获取用户所在城市                   |
| `get_user_id`             | 获取当前用户唯一标识               |
| `get_current_month`       | 获取当前月份                       |
| `fetch_external_data`     | 检索用户指定月份的使用记录         |
| `fill_context_for_report` | 为报告生成注入上下文               |

![](https://cdn.jsdelivr.net/gh/tizi123139/image-bed/python-learning/20260716103543529.png)





[LangChain 中文教程 | LangChain 中文文档](https://langchain-doc.cn/)

[LangChain 教程 | 菜鸟教程](https://www.runoob.com/langchain/langchain-tutorial.html)