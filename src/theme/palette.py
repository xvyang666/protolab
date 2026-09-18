from PySide6.QtGui import QPalette, QColor

from config.setting import setting
from theme.color import _BaseColor, LightColor, DarkColor
from theme.themeMode import ThemeMode


class _BasePalette(QPalette):
    def __init__(self, color: _BaseColor):
        super().__init__()
        c = color
        is_light = c.mode == ThemeMode.light

        default_colors = {
            QPalette.ColorRole.WindowText: c.text.primary,
            QPalette.ColorRole.Button: c.grey.g100 if is_light else c.grey.g800,
            QPalette.ColorRole.Light: c.grey.g50,
            QPalette.ColorRole.Midlight: c.grey.g200,
            QPalette.ColorRole.Dark: c.grey.g700,
            QPalette.ColorRole.Mid: c.grey.g500,
            QPalette.ColorRole.Text: c.text.primary,
            QPalette.ColorRole.BrightText: c.common.white,
            QPalette.ColorRole.ButtonText: c.text.primary,
            QPalette.ColorRole.Base: c.background.paper,
            QPalette.ColorRole.Window: c.background.default,
            QPalette.ColorRole.Shadow: c.common.black,
            QPalette.ColorRole.Highlight: c.primary.main,
            QPalette.ColorRole.HighlightedText: c.primary.contrastText,
            QPalette.ColorRole.Link: c.info.main,
            QPalette.ColorRole.LinkVisited: c.secondary.main,
            QPalette.ColorRole.AlternateBase: c.grey.g100 if is_light else c.grey.g800,
            # QPalette.ColorRole.NoRole: c.common.trans,
            QPalette.ColorRole.ToolTipBase: c.grey.g800 if is_light else c.grey.g100,
            QPalette.ColorRole.ToolTipText: c.common.white if is_light else c.common.black,
            QPalette.ColorRole.PlaceholderText: c.text.disabled,
            QPalette.ColorRole.Accent: c.primary.main,
        }

        for role, color in default_colors.items():
            self.setColor(role, QColor(color))

        disabled_colors = {
            QPalette.ColorRole.WindowText: c.text.disabled,
            QPalette.ColorRole.Text: c.text.disabled,
            QPalette.ColorRole.ButtonText: c.text.disabled,
            QPalette.ColorRole.HighlightedText: c.text.disabled,
            QPalette.ColorRole.PlaceholderText: c.text.disabled,
            QPalette.ColorRole.BrightText: c.text.disabled,
            QPalette.ColorRole.Link: c.text.disabled,
            QPalette.ColorRole.LinkVisited: c.text.disabled,
            QPalette.ColorRole.Window: c.action.disabledBackground,
            QPalette.ColorRole.Base: c.action.disabledBackground,
            QPalette.ColorRole.AlternateBase: c.action.disabledBackground,
            QPalette.ColorRole.Button: c.action.disabledBackground,
            QPalette.ColorRole.Highlight: c.action.disabledBackground,
            QPalette.ColorRole.Light: c.action.disabledBackground,
            QPalette.ColorRole.Midlight: c.action.disabledBackground,
            QPalette.ColorRole.Dark: c.action.disabledBackground,
            QPalette.ColorRole.Mid: c.action.disabledBackground,
            QPalette.ColorRole.Shadow: c.action.disabledBackground,
            # QPalette.ColorRole.NoRole: c.common.trans,
            QPalette.ColorRole.ToolTipBase: c.action.disabledBackground,
            QPalette.ColorRole.ToolTipText: c.text.disabled,
            QPalette.ColorRole.Accent: c.text.disabled,
        }

        for role, color in disabled_colors.items():
            self.setColor(QPalette.ColorGroup.Disabled, role, QColor(color))


LightPalette: _BasePalette = _BasePalette(LightColor)
DarkPalette: _BasePalette = _BasePalette(DarkColor)
_map: dict[ThemeMode, _BasePalette] = {
    ThemeMode.light: LightPalette,
    ThemeMode.dark: DarkPalette,
}


def palette():
    return _map[setting.theme]
