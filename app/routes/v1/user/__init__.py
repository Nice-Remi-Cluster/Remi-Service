from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.models import User
from app.schemas import UserCreate, UserResponse
from tortoise.exceptions import IntegrityError, DoesNotExist

from app.utils.secure.pwd import check_password

r = APIRouter(
    prefix="/user",
    tags=["user"],
)


@r.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """
    创建新用户
    """
    try:
        # 创建用户
        user = await User.create_user(username=user_data.username, email=user_data.email)
        # 设置密码
        await user.set_password(user_data.password)

        # 返回用户信息
        return {
            "username": user.username,
            "created_at": user.created_at.isoformat()
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建用户失败: {str(e)}"
        )

@r.post("/validate_password", status_code=status.HTTP_200_OK)
async def validate_password(user_email: EmailStr, password: str):
    """
    密码验证
    仅作为调试使用，任何时候都不要在外部直接请求密码验证，可能会被网络抓包篡改

    :param user_email:
    :param password:
    :return:
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
