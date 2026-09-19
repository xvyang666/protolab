from PySide6.QtGui import QPalette, QColor

from theme.color import BaseColor, LightColor, DarkColor
from theme.themeMode import ThemeMode


class Palette(QPalette):
    def __init__(self, color: BaseColor):
        super().__init__()
        c = color
        is_light = c.mode == ThemeMode.light

        default_colors = {
            # Window
            QPalette.ColorRole.Window: c.background.default,
            QPalette.ColorRole.WindowText: c.text.primary,

            # Button
            QPalette.ColorRole.Button: c.grey.g200 if is_light else c.grey.g900,
            QPalette.ColorRole.ButtonText: c.text.primary,

            # Base / Input / View
            QPalette.ColorRole.Base: c.background.paper,
            QPalette.ColorRole.Text: c.text.primary,
            QPalette.ColorRole.AlternateBase: c.grey.g100 if is_light else c.grey.g800,
            QPalette.ColorRole.PlaceholderText: c.text.disabled,

            # Highlight & Selection
            QPalette.ColorRole.Highlight: c.primary.main,
            QPalette.ColorRole.HighlightedText: c.primary.contrastText,
            QPalette.ColorRole.Accent: c.primary.main,
            QPalette.ColorRole.BrightText: c.common.white,

            # ToolTip
            QPalette.ColorRole.ToolTipBase: c.grey.g800 if is_light else c.grey.g100,
            QPalette.ColorRole.ToolTipText: c.common.white if is_light else c.common.black,

            # Hyperlink
            QPalette.ColorRole.Link: c.info.main,
            QPalette.ColorRole.LinkVisited: c.secondary.main,

            # 3D Border & Shadow
            QPalette.ColorRole.Light: c.grey.g100 if is_light else c.grey.g600,
            QPalette.ColorRole.Midlight: c.grey.g200 if is_light else c.grey.g700,
            QPalette.ColorRole.Mid: c.grey.g300 if is_light else c.grey.g800,
            QPalette.ColorRole.Dark: c.grey.g400 if is_light else c.grey.g900,
            QPalette.ColorRole.Shadow: c.common.black if is_light else c.common.white,
        }

        for role, color in default_colors.items():
            self.setColor(role, QColor(color))

        disabled_colors = {
            # Window
            QPalette.ColorRole.Window: c.action.disabledBackground,
            QPalette.ColorRole.WindowText: c.text.disabled,

            # Button
            QPalette.ColorRole.Button: c.action.disabledBackground,
            QPalette.ColorRole.ButtonText: c.text.disabled,

            # Base / Input / View
            QPalette.ColorRole.Base: c.action.disabledBackground,
            QPalette.ColorRole.Text: c.text.disabled,
            QPalette.ColorRole.AlternateBase: c.action.disabledBackground,
            QPalette.ColorRole.PlaceholderText: c.text.disabled,

            # Highlight & Selection
            QPalette.ColorRole.Highlight: c.action.disabledBackground,
            QPalette.ColorRole.HighlightedText: c.text.disabled,
            QPalette.ColorRole.Accent: c.text.disabled,
            QPalette.ColorRole.BrightText: c.text.disabled,

            # ToolTip
            QPalette.ColorRole.ToolTipBase: c.action.disabledBackground,
            QPalette.ColorRole.ToolTipText: c.text.disabled,

            # Hyperlink
            QPalette.ColorRole.Link: c.text.disabled,
            QPalette.ColorRole.LinkVisited: c.text.disabled,

            # 3D Border & Shadow
            QPalette.ColorRole.Light: c.action.disabledBackground,
            QPalette.ColorRole.Midlight: c.action.disabledBackground,
            QPalette.ColorRole.Mid: c.action.disabledBackground,
            QPalette.ColorRole.Dark: c.action.disabledBackground,
            QPalette.ColorRole.Shadow: c.action.disabledBackground,
        }

        for role, color in disabled_colors.items():
            self.setColor(QPalette.ColorGroup.Disabled, role, QColor(color))


LightPalette: Palette = Palette(LightColor)
DarkPalette: Palette = Palette(DarkColor)


