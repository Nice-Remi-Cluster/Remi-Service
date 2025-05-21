from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """创建用户的请求模型"""
    email: str = EmailStr()
    username: str = Field(..., min_length=3, max_length=20, description="用户名，长度在3-20之间")
    password: str = Field(..., min_length=6, description="密码，最小长度为6个字符")


class UserResponse(BaseModel):
    """用户信息响应模型"""
    username: str
    created_at: str

    model_config = {
        "from_attributes": True
    }
