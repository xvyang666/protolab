import enum
import os
import sys
from datetime import datetime
from functools import cached_property
from pathlib import Path
from traceback import format_exception

from pydantic import BaseModel

from config.path_config import PathConfig

if None:
    from loguru import Record


class Log(BaseModel):
    class Key(enum.Enum):
        default = 1
        api = 2
        queue = 4
        timed = 5

    class Level(enum.Enum):
        TRACE = 1
        DEBUG = 2
        INFO = 3
        SUCCESS = 4
        WARNING = 5
        ERROR = 6
        CRITICAL = 7

    key: Key
    file: str
    line: int
    level: Level
    message: str
    exception: str
    created_time: datetime


class Logger:
    def __init__(self, pycharm_proj_root: Path):
        self._lg = _LoggerGetter(pycharm_proj_root)

    @cached_property
    def default(self):
        return self._lg.get(key=Log.Key.default, console=True, file=True)


class _LoggerGetter[T]:
    _key_name = 'k'

    def __init__(self, pycharm_proj_root: Path):
        """
        :param pycharm_proj_root: 这个是 pycharm 的打开项目的根路径, 用于输出到控制台时能点击跳转
        """

        from loguru import logger
        self._logger = logger
        self._logger.remove()  # 清除默认 handler

        self.pycharm_proj_root = pycharm_proj_root

    def get(self, key: T, console: bool = True, file: bool = False):
        """
        :param key: 日志标识
        :param console: 是否输出到控制台
        :param file: 是否输出到文件
        :return:
        """
        if console:
            self._logger.add(
                sink=sys.stdout,
                enqueue=True,  # 由于输出到控制台是一个io, 这里在新线程写入, 不阻塞事件循环
                format=self.__console_format,
                filter=lambda r: self.__filter(r, key),
            )

        if file:
            self._logger.add(
                sink=PathConfig.log_dir / key.name / 'log.txt',
                rotation='5 MB',
                enqueue=True,
                filter=lambda r: self.__filter(r, key),
            )

        return self._logger.bind(**{self._key_name: key})

    def __filter(self, record: 'Record', key: T):
        return record['extra'].get(self._key_name) == key

    def __console_format(self, record: 'Record'):
        rel_path = os.path.relpath(record["file"].path, self.pycharm_proj_root)
        safe_message = self._safe_message(record["message"])

        # 判断是否有异常堆栈
        safe_stack_info = ''
        if exception := record["exception"]:
            stack_info = ''.join(format_exception(exception.type, exception.value, exception.traceback))
            safe_stack_info = self._safe_message(stack_info)

        return (
            f"🕒 {record['time'].strftime('%Y-%m-%d %H:%M:%S')} "
            f"{record['level'].icon} {record['level'].name} "
            f'📄 File "{rel_path}", line {record["line"]} '  # 格式化 绝对路径 到 pycharm 的打开项目的根路径 的 相对路径, 以能点击跳转
            f"📢 {safe_message}\n"
            f"{safe_stack_info}"
        )

    @staticmethod
    def _safe_message(msg: str):
        """
        当字符串出现 {'page': 1 ... } 这样的时候, 里面的内容会被当成占位符, 但这就是一个原始字符串, 这里替换一下, 最终就会输出正常的 {}
        包括 <> 这样的标签也会 当成颜色标签 影响输出, 也进行转义
        :param msg:
        :return:
        """
        return (
            msg
            .replace("{", "{{")
            .replace("}", "}}")
            .replace("<", "\\<")
        )
