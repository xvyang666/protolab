from PySide6.QtGui import QColor

c = QColor("rgba(255, 255, 255, 0.12)")
# c = QColor("#1effffff")

print("是否有效:", c.isValid())
print("Hex 格式 (#RRGGBB):", c.name())
print("HexArgb 格式 (#AARRGGBB):", c.name(QColor.NameFormat.HexArgb))
