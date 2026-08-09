from fastapi import APIRouter
from fastapi.sse import ServerSentEvent

from app.models.schemas import ChatRequest
from fastapi.responses import StreamingResponse
from app.agents.personal_chief import search_recipes, get_messages, clear_messages
from sse_starlette.sse import EventSourceResponse
from app.agents.email_agent import email_agent


router = APIRouter()


@router.post("/chat/stream")
async def chat_endpoint(request: ChatRequest):
    """流式对话"""
    return StreamingResponse(
        search_recipes(request.message, request.image_url, request.thread_id),
        media_type="text/event-stream"
    )


@router.get("/chat/messages")
async def get_chat_messages(thread_id: str):
    """获取历史消息"""
    messages = get_messages(thread_id)
    return {"messages": messages}


@router.delete("/chat/messages")
async def clear_chat_messages(thread_id: str):
    """清空历史消息"""
    clear_messages(thread_id)
    return {"success": True}

@router.post("/chat/send", tags=["聊天"])
async def send_chat(request: ChatRequest):
    """发送聊天消息，使用 SSE 流式返回 Agent 响应。同时处理 HITL 中断决策。"""
    return EventSourceResponse(email_agent.generate_sse(request.thread_id, request.message or "", request.interrupt_decision))