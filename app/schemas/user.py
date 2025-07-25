from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserCreateQQ(BaseModel):
    """通过QQ创建用户的请求模型"""
    qq: str = Field(..., max_length=14, description="QQ号，最多14位")


class DivingFishBindCreate(BaseModel):
    """水鱼查分器绑定请求模型"""
    username: str = Field(..., min_length=1, max_length=50, description="水鱼查分器用户名")
    password: str = Field(..., min_length=1, max_length=100, description="水鱼查分器密码")
    bind_name: Optional[str] = Field(None, max_length=30, description="绑定名称，可选")
