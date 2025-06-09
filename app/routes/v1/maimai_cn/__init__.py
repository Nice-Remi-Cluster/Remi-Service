from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import EmailStr
from wahlap_mai_ass_expander.exceptions import QrCodeExpired

from app.enums.users import UserBindType
from app.models.user import User, UserBind
from tortoise.exceptions import IntegrityError, DoesNotExist

from app.schemas.responses.mai_cn import MaiCNGetUidResponse
from app.schemas.user import UserCreateQQ
from app.utils.secure.pwd import check_password
from app.utils.mai_cn import mai_cn_client_constructor
from httpx import HTTPError

r = APIRouter(
    prefix="/maimaicn",
    tags=["maimai_cn"],
)


@r.get("/get-uid", response_model=MaiCNGetUidResponse)
async def get_maimai_cn_uid(qr_code_content: str):
    try:
        client = mai_cn_client_constructor()
        response = await client.qr_scan(qr_code_content)
        return {"errorID": response["errorID"], "uid": response["userID"]}
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    except QrCodeExpired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="二维码已过期"
        )
    except HTTPError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"由于网络原因，获取用户uuid失败，重试可能会解决问题"
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户uuid失败: {str(e)}"
        )
