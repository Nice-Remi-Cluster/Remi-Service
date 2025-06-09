from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserCreateQQ(BaseModel):
    """通过QQ创建用户的请求模型"""
    qq: str = Field(..., max_length=14, description="QQ号，最多14位")


class UserBindMaimaiCN(BaseModel):
    """通过uuid绑定maimaidx"""
    uuid: str = Field(..., max_length=36, description="用户uuid")
    qr_code: str = Field(..., max_length=1000, description="maimaidx cn wechat qr_code content")