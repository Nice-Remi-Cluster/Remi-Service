import casbin
from casbin.util import builtin_operators as op

from cfgs.config import CasbinPolicyPath, CasbinModelPath

casbin_e = casbin.Enforcer(
    CasbinModelPath,
    CasbinPolicyPath
)

# 添加内置函数
casbin_e.add_function("key_match2", op.key_match2)

def init():
    casbin_e.add_policy('admin', 'luoxue', 'write', 'allow')
    casbin_e.add_grouping_policy('user1', 'admin')
    casbin_e.save_policy()

if __name__ == '__main__':
    init()
    print(casbin_e.enforce('user1', 'luoxue', 'write'))