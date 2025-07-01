from loguru import logger
from tortoise import fields, models
from tortoise.exceptions import OperationalError
from tortoise.models import Model
from tortoise.transactions import atomic, in_transaction
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
    is_default = fields.BooleanField(default=False)  # 是否为默认绑定
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:  # type: ignore
        # https://tortoise.github.io/models.html?h=meta#tortoise.models.Model.Meta.unique_together
        # 添加联合唯一约束，确保同一个用户不会重复绑定相同内容
        unique_together = (
            ("user", "bind_type", "bind_content"),
            ("user", "bind_type", "bind_name")
        )
    
    async def save(self, *args, **kwargs) -> None:
        """
        重写save方法，确保同一用户同一类型:
        1. 只有一个默认绑定
        2. 至少有一个默认绑定（如果存在绑定）
        """
        # 检查是否是唯一绑定
        existing_binds = await self.__class__.filter(
            user=self.user,
            bind_type=self.bind_type
        ).exclude(id=self.id).count()
        
        # 如果是唯一绑定，自动设为默认
        if existing_binds == 0:
            self.is_default = True
        
        if self.is_default:
            # 如果设置为默认绑定，先取消该用户该类型下的其他默认绑定
            await self.__class__.filter(
                user=self.user,
                bind_type=self.bind_type,
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        elif existing_binds > 0:
            # 检查是否还有默认绑定
            has_default = await self.__class__.filter(
                user=self.user,
                bind_type=self.bind_type,
                is_default=True
            ).exclude(id=self.id).exists()
            
            # 如果没有默认绑定，将第一个找到的绑定设为默认
            if not has_default:
                first_bind = await self.__class__.filter(
                    user=self.user,
                    bind_type=self.bind_type
                ).exclude(id=self.id).first()
                if first_bind:
                    first_bind.is_default = True
                    await first_bind.save(update_fields=['is_default'])
        
        await super().save(*args, **kwargs)

    @classmethod
    async def create_bind(cls, user: User, bind_type: UserBindType, bind_content: str,
                         bind_name: str | None = None, is_default: bool = False) -> "UserBind":
        """
        创建一个新的用户绑定
        :param is_default: 是否设置为默认绑定
        """
        bind = cls(user=user, bind_type=bind_type, bind_content=bind_content,
                  bind_name=bind_name, is_default=is_default)
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
    
    @classmethod
    async def get_default_bind(cls, user: User, bind_type: UserBindType) -> "UserBind | None":
        """
        获取用户指定类型的默认绑定
        """
        return await cls.filter(user=user, bind_type=bind_type, is_default=True).first()

    @classmethod
    async def set_default_bind_by_content(cls, user: User, bind_type: UserBindType, bind_content: str) -> bool:
        """
        通过绑定内容设置默认绑定
        :return: 是否设置成功
        """
        bind = await cls.filter(user=user, bind_type=bind_type, bind_content=bind_content).first()
        if not bind:
            return False
            
        # 使用事务确保操作原子性
        async with in_transaction() as connection:
            # 先取消该用户该类型下的其他默认绑定
            await cls.filter(
                user=user,
                bind_type=bind_type,
                is_default=True
            ).exclude(id=bind.id).using_db(connection).update(is_default=False)
            
            # 设置当前绑定为默认
            bind.is_default = True
            await bind.save(using_db=connection, update_fields=['is_default'])
        return True
