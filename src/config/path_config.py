from pathlib import Path

_file = Path(__file__)


class PathConfig:
    version = '0.0.1'

    root_dir = _file.parent.parent.parent
    src_dir = root_dir / "src"
    res_dir = root_dir / "res"
    data_dir = root_dir / "data" / version

    setting_json_file = data_dir / "settings.json"

    @staticmethod
    def init():
        for i in [
            PathConfig.data_dir
        ]:
            i.mkdir(parents=True, exist_ok=True)
