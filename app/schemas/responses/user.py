from pydantic import BaseModel

from app.enums.users import UserBindType


class UserResponseQQ(BaseModel):
    """通过QQ注册用户的信息响应模型"""
    uuid: str
    qq: str
    created_at: str

    model_config = {
        "from_attributes": True
    }

class UserBindResponse(BaseModel):
    """请求bind新账户的返回内容的请求体"""
    uuid: str
    bind_type: UserBindType
    bind_content: str
    bind_name: str
    is_default: bool

class GetUUIDResponse(BaseModel):
    """获取uuid的返回模型"""
    uuid: str
    bind_type: UserBindType
    bind_content: str
    bind_name: str | None = None


