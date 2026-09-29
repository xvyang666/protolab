from PySide6.QtWidgets import QComboBox


def combobox_set_default(combo_box: QComboBox, v: object):
    index = combo_box.findData(v)
    if index != -1:
        combo_box.setCurrentIndex(index)