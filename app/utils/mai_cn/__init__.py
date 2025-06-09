from wahlap_mai_ass_expander import MaiSimClient
from cfgs.config import MaimaiArcadeDXChipId


def mai_cn_client_constructor() -> MaiSimClient:
    """
    构造一个MaiSimClient
    TODO: 有待优化，其实这里可以复用httpx.AsyncClient实例或做其他优化
    """
    return MaiSimClient(chip_id=MaimaiArcadeDXChipId)