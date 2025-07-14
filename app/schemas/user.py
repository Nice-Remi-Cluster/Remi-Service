from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserCreateQQ(BaseModel):
    """通过QQ创建用户的请求模型"""
    qq: str = Field(..., max_length=14, description="QQ号，最多14位")
