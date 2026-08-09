import json
from langchain.agents import AgentState, create_agent
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from langchain.agents.middleware import wrap_model_call, dynamic_prompt, HumanInTheLoopMiddleware
from langchain.agents.middleware import ModelRequest, ModelResponse
from typing import Callable
from app.common.logger import logger
import aiosqlite
import os
from langchain_deepseek import ChatDeepSeek

AUTHENTICATED_KEY = "authenticated"

# state信息，记录用户是否授权邮箱操作
class AuthenticatedState(AgentState):
    authenticated: bool

# ==================== 1. 定义工具 ====================
# 定义工具，用于用户邮箱鉴权
@tool
def authenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
    """Authenticate the user with the given email and password"""

    # 定义变量，记录校验结果
    authenticated = False
    message = "Authentication failed"

    # 校验邮箱和密码
    if email == "huge@itcast.cn" and password == "123":
        authenticated = True
        message = "Successfully authenticated"

    # 返回校验结果
    return Command(
            update={
                "authenticated": authenticated,
                "messages": [
                    ToolMessage(message, tool_call_id=runtime.tool_call_id)
                ],
            }
        )
# 定义工具，用于操作邮箱
@tool
def check_inbox() -> list[dict]:
    """Read an email from the given address."""
    # 模拟收件箱邮件
    return [
        {
            "subject": "周末见个面？",
            "content": """
                嗨 虎哥，
                我下周会去城里，不知道我们有没有机会一起喝杯咖啡？

                祝好，简
            """,
            "from": "jane@itcast.cn",
            "status": "unread"
        },
        {
            "subject": "周五会议",
            "content": """
                嗨 虎哥，
                非常抱歉，我周五的会议无法准时参加了，能不能重新安排个时间？

                祝好，小李
            """,
            "from": "lixiaolong@itcast.cn",
            "status": "checked"
        }
    ]

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an response email"""
    return f"邮件已发送至 {to} , 主题： {subject} , 内容： {body}"


# 定义中间件，实现动态工具
@wrap_model_call
async def dynamic_tool_call(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Allow read inbox and send email tools only if user provides correct email and password"""

    authenticated = request.state.get(AUTHENTICATED_KEY)

    if authenticated:
        tools = [check_inbox, send_email]
    else:
        tools = [authenticate]

    request = request.override(tools=tools)
    return await handler(request)


# 定义提示词
authenticated_prompt = "You are a helpful assistant that can check the inbox and send emails."
unauthenticated_prompt = """You are a helpful email assistant.
    For system security protocols, you must authenticate user before any other interaction.
    """
# 定义动态提示词中间件
@dynamic_prompt
def dynamic_prompt_func(request: ModelRequest) -> str:
    """Generate system prompt based on authentication status"""
    authenticated = request.state.get(AUTHENTICATED_KEY)
    final_prompt = authenticated_prompt if authenticated else unauthenticated_prompt
    return final_prompt

# ==================== 辅助函数 ====================
def _serialize(obj):
    """递归转换对象为可 JSON 序列化的格式"""
    if hasattr(obj, 'value'):
        return _serialize(obj.value)
    elif hasattr(obj, 'model_dump'):
        return obj.model_dump()
    elif isinstance(obj, (list, tuple)):
        return [_serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


class EmailAgent:

    def __init__(self):
        self.conn: aiosqlite.Connection = None
        self.checkpointer: BaseCheckpointSaver = None
        self.agent = None

    async def init(self):
        await self.init_checkpointer()
        logger.info("checkpointer 初始化完成 ....")
        await self.init_agent()
        logger.info("email agent 初始化完成 ....")

    async def init_checkpointer(self):
        # 建立连接
        os.makedirs("./db", exist_ok=True)
        self.conn = await aiosqlite.connect("./db/mail_fiend.db")
        logger.info("sqlite connection 完成 ....")
        # 初始化checkpointer
        self.checkpointer = AsyncSqliteSaver(conn = self.conn)
        # 自动建表
        await self.checkpointer.setup()

    async def close(self):
        await self.conn.close()
        logger.info("sqlite connection 关闭 ....")

    async def init_agent(self):
        llm = ChatDeepSeek(
            model="deepseek-chat",
            api_key="",  # 填你的真实key
            temperature=0.1
        )
        self.agent = create_agent(
            llm,
            tools=[authenticate, check_inbox, send_email],
            state_schema=AuthenticatedState,
            checkpointer=self.checkpointer,
            middleware=[
                dynamic_tool_call,
                dynamic_prompt_func,
                HumanInTheLoopMiddleware(
                    interrupt_on={
                        "authenticate": False,
                        "check_inbox": False,
                        "send_email": True,
                    }
                )
            ],
        )


    # ==================== SSE 流式响应 ====================
    async def generate_sse(self, thread_id: str, message: str, interrupt_decision: dict):
        """生成 SSE 事件流"""
        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        # 使用 HumanMessage 封装用户消息
        messages = {"messages": [HumanMessage(content=message)]}
        # 判断是消息还是 command
        _input = messages
        if interrupt_decision:
            _input = Command(resume={
                "decisions": [interrupt_decision]
            })

        logger.info(f"调用agent，Input：{_input}")
        try:
            # 使用 astream_events 流式获取事件
            async for chunk in self.agent.astream(
                _input,
                config=config,
                stream_mode=["messages", "updates"],
                version="v2"
            ):
                event_type = chunk["type"]
                data = chunk["data"]

                # 1. messages - LLM 流式输出（token 级别）
                if event_type == "messages":
                    token, metadata = data
                    content = None
                    if isinstance(token, AIMessage) and hasattr(token, "content"):
                        content = token.content

                    if content:
                        yield {
                            "event": "message",
                            "data": json.dumps(
                                {"type": "message", "content": content},
                                ensure_ascii=False
                            )
                        }

                # 2. updates - 节点完成的 state 更新
                elif event_type == "updates":
                    # 2a. 中断事件
                    if "__interrupt__" in data:
                        interrupt_data = data['__interrupt__']
                        details = _serialize(interrupt_data)
                        yield {
                            "event": "interrupt",
                            "data": json.dumps(
                                {
                                    "type": "interrupt",
                                    "interrupt": {
                                        "reason": "需要人工确认",
                                        "details": details
                                    }
                                },
                                ensure_ascii=False, default=str
                            )
                        }

            # 无中断 → 流正常结束
            yield {
                "event": "done",
                "data": json.dumps({"type": "done", "content": "处理完成"}, ensure_ascii=False)
            }

        except Exception as e:
            logger.error(f"SSE 流中断: {e}", exc_info=True)
            yield {
                "event": "error",
                "data": json.dumps({"type": "error", "error": str(e)}, ensure_ascii=False)
            }

    async def get_messages(self, thread_id: str) -> dict:
        """获取会话历史，如果存在中断则返回中断信息"""
        logger.info(f"获取历史消息，thread_id: {thread_id}")

        config = {"configurable": {"thread_id": thread_id}}
        state = await self.agent.aget_state(config)
        if state is None or not state.values:
            return {"messages": []}

        messages = state.values.get("messages", [])

        # 转换消息格式
        result = []
        for msg in messages:
            if not msg.content:
                continue
            if isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})

        response = {"messages": result}

        # 检查是否存在中断
        interrupts = None
        if hasattr(state, 'interrupts') and state.interrupts:
            interrupts = state.interrupts
        elif hasattr(state, 'tasks') and state.tasks:
            for task in state.tasks:
                if hasattr(task, 'interrupts') and task.interrupts:
                    interrupts = task.interrupts
                    break

        if interrupts:
            response["has_interrupt"] = True
            response["interrupt"] = {
                "reason": "需要人工确认",
                "details": _serialize(interrupts)
            }

        return response

email_agent = EmailAgent()

__all__ = ["email_agent"]