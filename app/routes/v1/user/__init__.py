import tortoise
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import EmailStr
from tortoise.queryset import QuerySet

from app.enums.users import UserBindType
from app.models.user import User, UserBind
from tortoise.exceptions import IntegrityError, DoesNotExist

from app.schemas.responses.user import UserResponseQQ, UserBindResponse, GetUUIDResponse
from app.schemas.user import UserCreateQQ
from app.utils.secure.pwd import check_password

r = APIRouter(
    prefix="/user",
    tags=["user"],
)


@r.post("/create-by-qq", response_model=UserResponseQQ, status_code=status.HTTP_201_CREATED)
async def create_user_by_qq(user_data: UserCreateQQ):
    """
    创建新用户
    """
    try:
        if await UserBind.get_user_by_bind(UserBindType.QQ, user_data.qq):
            raise IntegrityError()
        
        # 创建用户
        user = await User.create_user()
        
        await user.add_bind(UserBindType.QQ, user_data.qq)

        # 返回用户信息
        return {
            "uuid": user.uuid,
            "qq": user_data.qq,
            "created_at": user.created_at.isoformat()
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该qq已创建对应用户"
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建用户失败: {str(e)}"
        )

@r.get("/get-uuid", response_model=GetUUIDResponse)
async def get_uuid(bind_type: UserBindType, bind_content: str):
    try:
        user = await UserBind.get_user_by_bind(bind_type, bind_content)
        if user:
            return {
                "uuid": user.uuid,
                "bind_type": bind_type,
                "bind_content": bind_content,
            }
        else:
            raise DoesNotExist(User)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户uuid失败: {str(e)}"
        )

@r.get("/bind", response_model=UserBindResponse)
async def bind(uuid: str, bind_type: UserBindType, bind_content: str, bind_name: str | None = None):
    try:
        if await UserBind.get_user_by_bind(bind_type, bind_content):
            raise IntegrityError()
        user = await User.get(uuid=uuid)
        await user.add_bind(bind_type, bind_content, bind_name)
        return {
            "success": True,
            "data": {
                "uuid": uuid,
                "bind_type": bind_type,
                "bind_content": bind_content,
                "bind_name": bind_name or ""
            }
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="需绑定的内容已与相应用户绑定"
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"绑定失败: {str(e)}"
        )



@r.post("/validate_password", status_code=status.HTTP_200_OK)
async def validate_password(user_email: EmailStr, password: str):
    """
    密码验证
    仅作为调试使用，任何时候都不要在外部直接请求密码验证，可能会被网络抓包篡改
    """
    try:
        user = await User.get(email=user_email)
        if check_password(password, user.password_hash):
            return {"valid": True}
        else:
            return {"valid": False}
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
