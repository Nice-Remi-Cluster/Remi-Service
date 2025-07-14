import tortoise
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import EmailStr
from tortoise.queryset import QuerySet

from app.enums.users import UserBindType
from app.models import MaimaiCNBind, MaimaiCurrent
from app.models.user import User, UserBind
from tortoise.exceptions import IntegrityError, DoesNotExist

from app.schemas.responses.maimai import CurrentMaimaiBindInfoResponseSingle
from app.schemas.responses.user import UserResponseQQ, UserBindResponse, GetUUIDResponse
from app.schemas.user import UserCreateQQ

r = APIRouter(
    prefix="/maimai",
    tags=["maimai"],
)


@r.get("/get-current-maimai-bind", response_model=list[CurrentMaimaiBindInfoResponseSingle])
async def get_current_maimai_bind(uuid: str):
    """获取当前maimai绑定信息

    Args:
        uuid: 用户唯一标识

    Returns:
        list[UserBindResponse]: 绑定信息列表
    """
    try:
        user = await User.get(uuid=uuid)
        maimai_current = await MaimaiCurrent.get_current_maimai_bind(user=user)

        return await maimai_current.json()

    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户maimai绑定不存在")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="发生了意料之外的错误")

@r.get("/update-current-maimai-bind", response_model=list[CurrentMaimaiBindInfoResponseSingle])
async def update_current_maimai_bind(
        uuid: str,
        divingfish_bind_name: str | None = None,
        luoxue_bind_name: str | None = None
):
    """更新用户当前maimai档案的信息

    Args:
        uuid: 用户唯一标识
        divingfish_bind_name:
        luoxue_bind_name:

    Returns:

    """
    user = await User.get_or_none(uuid=uuid)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    current_profile = await MaimaiCurrent.get_current_maimai_bind(user=user)

    divingfish_bind = None
    luoxue_bind = None

    if divingfish_bind_name:
        divingfish_binds = await UserBind.get_user_binds(
            user=user,
            bind_type=UserBindType.DivingFish,
        )
        for i in divingfish_binds:
            if i.bind_name == divingfish_bind_name:
                divingfish_bind = i
                break
        if not divingfish_bind:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="指定水鱼账号信息不存在")

    if luoxue_bind_name:
        luoxue_binds = await UserBind.get_user_binds(
            user=user,
            bind_type=UserBindType.Luoxue,
        )
        for i in luoxue_binds:
            if i.bind_name == luoxue_bind_name:
                luoxue_bind = i
                break
        if not luoxue_bind:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="指定落雪账号信息不存在")

    current_profile = await current_profile.update_binds(
        luoxue_bind=luoxue_bind,
        divingfish_bind=divingfish_bind
    )

    return await current_profile.json()

@r.get("/switch-current-maimai-bind", response_model=list[CurrentMaimaiBindInfoResponseSingle])
async def switch_current_maimai_bind(
        uuid: str,
        bind_name: str
):
    """
    切换当前maimai档案
    """
    user = await User.get_or_none(uuid=uuid)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    current_profile = await MaimaiCurrent.switch_current_maimai_bind(user, bind_name)
    if not current_profile:
        raise HTTPException(status_code=404, detail="用户没有此maimai档案")
    return await current_profile.json()