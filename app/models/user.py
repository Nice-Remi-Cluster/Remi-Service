from tortoise import fields, models
import uuid
from app.utils.secure import pwd
import secrets


class User(models.Model):
    """
    The User model
    """

    id = fields.IntField(primary_key=True, generated=True)
    #: This is a username
    uuid = fields.CharField(max_length=36, unique=True)
    email = fields.CharField(max_length=255, unique=True, null=True)
    username = fields.CharField(max_length=20)
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    @classmethod
    async def create_user(cls, username: str, email: str) -> "User":
        """
        创建一个新的用户实例
        """
        user = cls(username=username, uuid=str(uuid.uuid4()), email=email)
        await user.save()
        await user.set_password(secrets.token_hex(12))  # 设置随机默认密码
        return user

    async def set_password(self, password: str) -> None:
        """
        设置用户密码（自动哈希）
        """
        self.password_hash = pwd.get_password_hash(password)
        await self.save(update_fields=['password_hash'])

    class PydanticMeta:
        exclude = ["password_hash"]
