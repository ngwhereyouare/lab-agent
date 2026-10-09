import bcrypt


def hash_password(password: str) -> str:
    """对密码加密"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码的有效性"""
    """  "123" -> "xxsdasdasdasfa"  """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except (ValueError, TypeError):
        # 历史数据可能不是合法的 bcrypt 哈希，按密码错误处理。
        return False
