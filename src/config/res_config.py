# 该文件由 dev/tool/gen_res_code.py 自动生成, 勿手动修改
from config.path_config import PathConfig

_dir = PathConfig.res_dir


class res:
    """ 全部资源 """
    class locales:
        app_en = _dir / 'locales/app_en.qm'
        app_zh_c_n = _dir / 'locales/app_zh_CN.qm'
        qtbase_en = _dir / 'locales/qtbase_en.qm'
        qtbase_zh_c_n = _dir / 'locales/qtbase_zh_CN.qm'

