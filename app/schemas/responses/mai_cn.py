from pydantic import BaseModel



class MaiCNGetUidResponse(BaseModel):
    """通过QQ注册用户的信息响应模型"""
    errorID: int
    uid: int

    model_config = {
        "from_attributes": True
    }
