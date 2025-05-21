from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    生成密码的哈希值
    """
    return pwd_context.hash(password)

def check_password(password: str, password_hash: str) -> bool:
    """
    检查提供的密码是否与存储的密码哈希匹配
    """
    return pwd_context.verify(password, password_hash)
