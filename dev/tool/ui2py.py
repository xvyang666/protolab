"""
转换 ui 到指定位置生成 py

### 手动转换 设置-工具-外部工具配置
# 名称: ui2py
# 程序: $ProjectFileDir$/.venv/Scripts/python.exe
# 实参: $ProjectFileDir$/dev/tool/ui2py.py $FilePath$

### 自动转换 设置-工具-FileWatcher
# 名字: ui2py_auto
# 文件类型: 自定义一个  [设置-编辑器-文件类型-添加`QtDesigner文件`并绑定上*.ui]
# 作用域: 原始ui文件的目录
# 程序: $ProjectFileDir$/.venv/Scripts/python.exe
# 实参: $ProjectFileDir$/dev/tool/ui2py.py $FilePath$
# 要刷新的路径: $ProjectFileDir$/src/ui

"""

from pathlib import Path
import subprocess
import sys

_file = Path(__file__)
project = _file.parent.parent.parent

uic_exe =  project / ".venv/Scripts/pyside6-uic.exe"
ui_file = Path(sys.argv[1]).resolve()

dev_ui_dir = project / 'dev' / "ui"
src_py_dir = project / "src" / "ui"

relative = ui_file.relative_to(dev_ui_dir)
output = src_py_dir / relative.with_suffix(".py")
output.parent.mkdir(parents=True, exist_ok=True)
subprocess.run([uic_exe, str(ui_file), "-o", str(output)], check=True)

