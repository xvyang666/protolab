"""
注意: 这里定义颜色时统一使用 '#' 格式, 不能用 'rgb()' 或 'rgba()'
后者虽然在 qss 中生效, 但 QColor 直接实例化不支持

支持:
QColor('name')  # 'red', 'transparent' ...
QColor('#rgb')
QColor('#rrggbb')
QColor('#aarrggbb')  # alpha 通道在最前面

不支持
QColor('rgb(r, g, b)')
QColor('rgba(r, g, b, a)')
"""
from pydantic import BaseModel


class _CommonColor(BaseModel):
    black: str = "#000000"
    white: str = "#ffffff"
    trans: str = '#00000000'


class _GreyScale(BaseModel):
    g50: str = "#fafafa"
    g100: str = "#f5f5f5"
    g200: str = "#eeeeee"
    g300: str = "#e0e0e0"
    g400: str = "#bdbdbd"
    g500: str = "#9e9e9e"
    g600: str = "#757575"
    g700: str = "#616161"
    g800: str = "#424242"
    g900: str = "#212121"
    a100: str = "#f5f5f5"
    a200: str = "#eeeeee"
    a400: str = "#bdbdbd"
    a700: str = "#616161"


class _ColorVariant(BaseModel):
    main: str
    light: str
    dark: str
    contrastText: str


class _TextColor(BaseModel):
    primary: str
    secondary: str
    disabled: str


class _BackgroundColor(BaseModel):
    paper: str
    default: str


class _ActionColor(BaseModel):
    active: str
    hover: str
    hoverOpacity: float
    selected: str
    selectedOpacity: float
    disabled: str
    disabledBackground: str
    disabledOpacity: float
    focus: str
    focusOpacity: float
    activatedOpacity: float


class BaseColor(BaseModel):
    common: _CommonColor = _CommonColor()
    grey: _GreyScale = _GreyScale()

    primary: _ColorVariant
    secondary: _ColorVariant
    error: _ColorVariant
    warning: _ColorVariant
    info: _ColorVariant
    success: _ColorVariant
    divider: str
    background: _BackgroundColor
    text: _TextColor
    action: _ActionColor


class _LightColor(BaseColor):
    primary: _ColorVariant = _ColorVariant(main="#1976d2", light="#42a5f5", dark="#1565c0", contrastText="#ffffff")
    secondary: _ColorVariant = _ColorVariant(main="#9c27b0", light="#ba68c8", dark="#7b1fa2", contrastText="#ffffff")
    error: _ColorVariant = _ColorVariant(main="#d32f2f", light="#ef5350", dark="#c62828", contrastText="#ffffff")
    warning: _ColorVariant = _ColorVariant(main="#ed6c02", light="#ff9800", dark="#e65100", contrastText="#ffffff")
    info: _ColorVariant = _ColorVariant(main="#0288d1", light="#03a9f4", dark="#01579b", contrastText="#ffffff")
    success: _ColorVariant = _ColorVariant(main="#2e7d32", light="#4caf50", dark="#1b5e20", contrastText="#ffffff")
    divider: str = "#1F000000"
    background: _BackgroundColor = _BackgroundColor(paper="#ffffff", default="#ffffff")
    text: _TextColor = _TextColor(
        primary="#DF000000",
        secondary="#99000000",
        disabled="#61000000",
    )
    action: _ActionColor = _ActionColor(
        active="#8A000000",
        hover="#0A000000",
        hoverOpacity=0.04,
        selected="#14000000",
        selectedOpacity=0.08,
        disabled="#42000000",
        disabledBackground="#1F000000",
        disabledOpacity=0.38,
        focus="#1F000000",
        focusOpacity=0.12,
        activatedOpacity=0.12,
    )


class _DarkColor(BaseColor):
    primary: _ColorVariant = _ColorVariant(main="#90caf9", light="#e3f2fd", dark="#42a5f5", contrastText="#DF000000")
    secondary: _ColorVariant = _ColorVariant(main="#ce93d8", light="#f3e5f5", dark="#ab47bc", contrastText="#DF000000")
    error: _ColorVariant = _ColorVariant(main="#f44336", light="#e57373", dark="#d32f2f", contrastText="#ffffff")
    warning: _ColorVariant = _ColorVariant(main="#ffa726", light="#ffb74d", dark="#f57c00", contrastText="#DF000000")
    info: _ColorVariant = _ColorVariant(main="#29b6f6", light="#4fc3f7", dark="#0288d1", contrastText="#DF000000")
    success: _ColorVariant = _ColorVariant(main="#66bb6a", light="#81c784", dark="#388e3c", contrastText="#DF000000")
    divider: str = "#1FFFFFFF"
    background: _BackgroundColor = _BackgroundColor(paper="#333333", default="#212121")
    text: _TextColor = _TextColor(
        primary="#ffffff",
        secondary="#B3FFFFFF",
        disabled="#80FFFFFF",
    )
    action: _ActionColor = _ActionColor(
        active="#ffffff",
        hover="#14FFFFFF",
        hoverOpacity=0.08,
        selected="#29FFFFFF",
        selectedOpacity=0.16,
        disabled="#4DFFFFFF",
        disabledBackground="#1FFFFFFF",
        disabledOpacity=0.38,
        focus="#1FFFFFFF",
        focusOpacity=0.12,
        activatedOpacity=0.24,
    )


LightColor: _LightColor = _LightColor()
DarkColor: _DarkColor = _DarkColor()
