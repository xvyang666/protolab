from pathlib import Path

from config.__meta__ import Meta


class PathConfig:
    _file = Path(__file__)
    proj_dir = _file.parent.parent.parent
    src_dir = proj_dir / "src"
    res_dir = proj_dir / "res"
    data_dir = proj_dir / "data" / Meta.version

    setting_json_file = data_dir / "settings.json"

    @staticmethod
    def init():
        for i in [
            PathConfig.data_dir
        ]:
            i.mkdir(parents=True, exist_ok=True)
