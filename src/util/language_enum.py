from enum import Enum
from pathlib import Path

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from config.res_config import res


class LanguageEnum(Enum):
    en = "en"
    zh_CN = 'zh_CN'


Translator_File_Map: dict[LanguageEnum, list[Path]] = {
    LanguageEnum.en: [
        res.locales.app_en,
        res.locales.qtbase_en
    ],
    LanguageEnum.zh_CN: [
        res.locales.app_zh_c_n,
        res.locales.qtbase_zh_c_n
    ],
}

assert len(Translator_File_Map) == len(LanguageEnum)

_all_translator: list[QTranslator] = []


def install_translator_helper(app: QApplication, language: LanguageEnum):
    qm_list = Translator_File_Map[language]

    for i in _all_translator:
        app.removeTranslator(i)

    for qm in qm_list:
        translator = QTranslator()
        translator.load(str(qm))
        app.installTranslator(translator)
        _all_translator.append(translator)
