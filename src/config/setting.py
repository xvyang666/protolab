from pydantic import BaseModel

from config.path_config import PathConfig
from theme.theme_mode import ThemeMode


class _MainWindowLoc(BaseModel):
    x: int = 560
    y: int = 240
    w: int = 800
    h: int = 600


class _Setting(BaseModel):
    style: str = 'fusion'
    theme_mode: ThemeMode = ThemeMode.light
    main_window_loc: _MainWindowLoc = _MainWindowLoc()

    def load(self):
        try:
            with open(PathConfig.setting_json_file, mode="r", encoding="utf-8") as f:
                content = f.read()
                updated = _Setting.model_validate_json(content)
                self.__dict__.update(updated.__dict__)

        except Exception:
            pass

    def save(self):
        with open(PathConfig.setting_json_file, mode="w", encoding="utf-8") as f:
            f.write(self.model_dump_json())


setting: _Setting = _Setting()
