from pydantic import BaseModel,Field,ConfigDict
from typing import Optional

class UserRequest(BaseModel):
    username: str
    password: str

# user_info 对应的类：基础类 + Info 类（id、用户名）
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id:int
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )

class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse=Field(...,alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class UserUpdateRequest(BaseModel):
    nickname: str=None
    avatar: str=None
    gender: str=None
    bio: str=None
    phone : str=None

class UserChangerPasswordRequest(BaseModel):
    old_password: str=Field(...,alias="oldPassword")
    new_password: str=Field(...,min_length=6,alias="newPassword")