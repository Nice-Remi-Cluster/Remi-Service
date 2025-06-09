from loguru import logger
from tortoise import fields, models
import uuid
from app.enums.users import UserBindType
from app.utils.secure import pwd
import secrets


class User(models.Model):
    """
    The User model
    """

    id = fields.IntField(primary_key=True, generated=True)
    uuid = fields.CharField(max_length=36, unique=True)
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    @classmethod
    async def create_user(cls) -> "User":
        """
        创建一个新的用户实例
        """
        user = cls(uuid=str(uuid.uuid4()))
        await user.save()
        await user.set_password(secrets.token_hex(12))
        return user

    async def set_password(self, password: str) -> None:
        """
        设置用户密码（自动哈希）
        """
        self.password_hash = pwd.get_password_hash(password)
        await self.save(update_fields=['password_hash'])
    
    async def add_bind(self, bind_type: UserBindType, bind_content: str, bind_name: str | None = None) -> "UserBind":
        """
        为用户添加一个指定类型绑定
        """
        return await UserBind.create_bind(self, bind_type, bind_content, bind_name)
    
    async def get_binds(self, bind_type: UserBindType) -> list["UserBind"]:
        """
        获取用户的所有指定类型绑定
        """
        return await UserBind.filter(user=self, bind_type=bind_type)

    class PydanticMeta:
        exclude = ["password_hash"]


class UserBind(models.Model):
    """
    用户绑定模型
    """
    id = fields.IntField(primary_key=True, generated=True)
    user = fields.ForeignKeyField("models.User", related_name="binds", on_delete=fields.CASCADE)
    bind_type = fields.CharEnumField(UserBindType)
    bind_name = fields.CharField(max_length=30, null=True)  # 可选的绑定名称, 比如主账号就叫 主
    bind_content = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:  # type: ignore
        # https://tortoise.github.io/models.html?h=meta#tortoise.models.Model.Meta.unique_together
        # 添加联合唯一约束，确保同一个用户不会重复绑定相同内容
        unique_together = (("user", "bind_type", "bind_content"),)
    
    @classmethod
    async def create_bind(cls, user: User, bind_type: UserBindType, bind_content: str, bind_name: str | None = None) -> "UserBind":
        """
        创建一个新的用户绑定
        """
        bind = cls(user=user, bind_type=bind_type, bind_content=bind_content, bind_name=bind_name)
        await bind.save()
        return bind
    
    @classmethod
    async def get_user_by_bind(cls, bind_type: UserBindType, bind_content: str) -> User | None:
        """
        通过Bind内容查找用户
        """
        bind = await cls.filter(bind_type=bind_type, bind_content=bind_content).prefetch_related("user").first()
        if bind:
            return bind.user
        return None