from typing import Optional

from tortoise import models, fields

from app.enums.users import UserBindType
from app.models import UserBind, User
from app.schemas.responses.maimai import CurrentMaimaiBindInfoResponseSingle


class MaimaiCNBind(models.Model):
    """
     MaiMai绑定模型
     一个maimaicn对应水鱼和落雪各一个查分器
    """

    id = fields.IntField(primary_key=True, generated=True)

    mai_bind = fields.ForeignKeyField(
        "models.UserBind",
        related_name="maimaicn_binds",
        on_delete=fields.CASCADE,
    )
    luoxue_bind = fields.ForeignKeyField(
        "models.UserBind",
        related_name="luoxue_binds",
        on_delete=fields.CASCADE,
        null=True
    )
    divingfish_bind = fields.ForeignKeyField(
        "models.UserBind",
        related_name="divingfish_binds",
        on_delete=fields.CASCADE,
        null=True
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = (
            ("mai_bind", "luoxue_bind", "divingfish_bind"),
        )

    @classmethod
    async def get_binds(cls, mai_bind: UserBind) -> "MaimaiCNBind":
        if not isinstance(mai_bind, UserBind):
            return None

        return (await cls.get_or_create(mai_bind=mai_bind))[0]

    async def update_binds(
            self,
            luoxue_bind: UserBind | None = None,
            divingfish_bind: UserBind | None = None
    ) -> "MaimaiCNBind":
        """
        更新绑定
        """
        if luoxue_bind:
            self.luoxue_bind = luoxue_bind

        if divingfish_bind:
            self.divingfish_bind = divingfish_bind
        await self.save()
        return self

    async def json(self) -> list[CurrentMaimaiBindInfoResponseSingle]:
        """
        转换为JSON
        """
        fetched_bind: list[UserBind] = [
            await i
            for i in [
                self.mai_bind,
                self.luoxue_bind,
                self.divingfish_bind
            ]
            if await i is not None
        ]
        return [
            CurrentMaimaiBindInfoResponseSingle(
                bind_type=i.bind_type,
                bind_content=i.bind_content,
                bind_name=i.bind_name,
                is_default=i.is_default
            )
            for i in fetched_bind
        ]


class MaimaiCurrent(models.Model):
    """
    maimai当前使用的maimai账号
    """

    id = fields.IntField(primary_key=True, generated=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="maimai_current_user",
        on_delete=fields.CASCADE,
    )
    mai_bind = fields.ForeignKeyField(
        "models.MaimaiCNBind",
        related_name="maimai_current_bind",
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = (
            ("user", "mai_bind"),
        )

    @classmethod
    async def get_current_maimai_bind(cls, user: User) -> Optional["MaimaiCNBind"]:
        """
        获取当前使用的maimai账号，如果没有，寻找已有的mai bind并添加一个，没有则返回None

        :param user:
        :return:
        """

        result = await cls.filter(user=user).count()

        if result == 0:
            user_bind_maimai = await UserBind.get_user_binds(user, UserBindType.MaimaiCN)
            if len(user_bind_maimai) == 0:
                return None

            maimai_bind = await MaimaiCNBind.get_binds(user_bind_maimai[0])

            new_current = await cls.create(user=user, mai_bind=maimai_bind)
            await new_current.save()
            return maimai_bind

        return (await cls.filter(user=user).prefetch_related("mai_bind").first()).mai_bind  # noqa

    @classmethod
    async def switch_current_maimai_bind(cls, user: User, maimai_bind_name: str) -> Optional["MaimaiCNBind"]:
        """
        切换maimai档案
        """
        maimai_current_instance = await MaimaiCurrent.filter(user=user).first()
        maimai_binds = await UserBind.get_user_binds(user, UserBindType.MaimaiCN)
        maimai_bind = None
        for b in maimai_binds:
            if b.bind_name == maimai_bind_name:
                maimai_bind = b
                break
        if not maimai_bind:
            return None

        maimai_cn_bind = await MaimaiCNBind.get_binds(maimai_bind)
        maimai_current_instance.mai_bind = maimai_cn_bind
        await maimai_current_instance.save()
        return await cls.get_current_maimai_bind(user)
