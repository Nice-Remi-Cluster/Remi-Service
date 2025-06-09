import casbin
from casbin.util import builtin_operators as op

from cfgs.config import CasbinPolicyPath, CasbinModelPath

casbin_e = casbin.Enforcer(
    CasbinModelPath,
    CasbinPolicyPath
)

casbin_e.add_function("key_match2", op.key_match2)


def validate_casbin(user: str, path: str, method: str):
    return casbin_e.enforce(user, path, method)

