from pathlib import Path

from PySide6.QtGui import QIcon

from bus.obj import logger
from config.path_config import PathConfig
from config.setting import setting
from theme.icon import Icon
from theme.palette import Palette, LightPalette, DarkPalette
from theme.themeMode import ThemeMode

__theme_palette_map: dict[ThemeMode, Palette] = {
    ThemeMode.light: LightPalette,
    ThemeMode.dark: DarkPalette,
}


def get_theme_palette():
    """ 获取当前 theme 的 palette """
    return __theme_palette_map[setting.theme]


__theme_icon_dir_map: dict[ThemeMode, Path] = {
    ThemeMode.light: PathConfig.res_dir / 'icon/light',
    ThemeMode.dark: PathConfig.res_dir / 'icon/dark',
}
__icon_cache: dict[ThemeMode, dict[Icon, QIcon]] = {
    ThemeMode.light: {},
    ThemeMode.dark: {},
}


def get_theme_icon(i: Icon) -> QIcon:
    """
    找当前主题下的图标, 如果找不到将使用 light 主题下的图标, 实在没有返回个空的Icon
    """
    if icon := __icon_cache[setting.theme].get(i, None):
        return icon

    icon = QIcon(str(__theme_icon_dir_map[setting.theme] / i.value))
    if icon.isNull():
        logger.default.warning(f'null icon: {setting.theme} {i}')

        # 由于枚举是以 light 目录为基准生成的, 所以当前主题如果是 light 那图标正常肯定存在
        # 如果 light 也不存在, 那也不用再试一次了
        if setting.theme != ThemeMode.light:
            icon = QIcon(str(__theme_icon_dir_map[ThemeMode.light] / i.value))

    __icon_cache[setting.theme][i] = icon
    return icon
