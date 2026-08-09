from typing import Optional, Dict, Any, List

from pydantic import BaseModel

# --- 2. 数据模型 ---
class ChatRequest(BaseModel):
    message: Optional[str] = None
    image_url: Optional[str] = None
    thread_id: str
    interrupt_decision: Optional[Dict[str, Any]] = None