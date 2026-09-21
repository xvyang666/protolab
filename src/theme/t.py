from pathlib import Path

from PySide6.QtGui import QIcon

from config.path_config import PathConfig
from config.setting import setting
from theme.color import LightColor, DarkColor, BaseColor
from theme.icon import IconEnum
from theme.theme_mode import ThemeMode


class Theme:

    __theme_color_map: dict[ThemeMode, BaseColor] = {
        ThemeMode.light: LightColor,
        ThemeMode.dark: DarkColor,
    }

    @property
    def color(self):
        return self.__theme_color_map[setting.theme_mode]

    __theme_icon_dir_map: dict[ThemeMode, Path] = {
        ThemeMode.light: PathConfig.res_dir / 'icon/light',
        ThemeMode.dark: PathConfig.res_dir / 'icon/dark',
    }
    __icon_cache: dict[ThemeMode, dict[IconEnum, QIcon]] = {
        ThemeMode.light: {},
        ThemeMode.dark: {},
    }

    def get_icon(self, i: IconEnum) -> QIcon:
        """
        找当前主题下的图标, 如果找不到将使用 light 主题下的图标, 实在没有返回个空的Icon
        """
        if icon := self.__icon_cache[setting.theme_mode].get(i, None):
            return icon

        icon = QIcon(str(self.__theme_icon_dir_map[setting.theme_mode] / i.value))
        if icon.isNull():
            from bus.obj import logger
            logger.default.warning(f'null icon: {setting.theme_mode} {i}')

            # 由于枚举是以 light 目录为基准生成的, 所以当前主题如果是 light 那图标正常肯定存在
            # 如果 light 也不存在, 那也不用再试一次了
            if setting.theme_mode != ThemeMode.light:
                icon = QIcon(str(self.__theme_icon_dir_map[ThemeMode.light] / i.value))

        self.__icon_cache[setting.theme_mode][i] = icon
        return icon
