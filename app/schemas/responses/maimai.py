from pydantic import BaseModel

from app.enums.users import UserBindType


class CurrentMaimaiBindInfoResponseSingle(BaseModel):
    bind_type: UserBindType
    bind_content: str
    bind_name: str
    is_default: bool