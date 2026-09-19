"""
自动生成 icon 枚举, 以 light 下的图标为基准

### 自动转换 设置-工具-FileWatcher
# 名称: 自动生成icon代码
# 文件: 任意
# 作用域: $ProjectFileDir$/res/icon/light
# 程序: $ProjectFileDir$/.venv/Scripts/python.exe
# 实参: $ProjectFileDir$/dev/tool/gen_icon_code.py
# 要刷新的路径: $ProjectFileDir$/src/theme/icon.py
"""

import re
from pathlib import Path


def _name(name: str) -> str:
    """将文件名或目录名转换为合法的 snake_case 标识符, 保留中文等字符."""
    name = Path(name).stem

    # 将连字符, 点号, 空白字符替换为下划线
    name = re.sub(r'[-.\s]', '_', name)

    # 将驼峰转换为蛇形
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    if name and name[0].isdigit():
        raise ValueError

    # 清理多余的连续下划线, 并去除首尾的下划线
    name = re.sub(r'_+', '_', name).strip('_')

    # 如果字符串为空, 提供一个保底的合法标识符
    if not name:
        raise ValueError

    return name


def build_tree(base_dir: Path) -> dict:
    """递归构建目录树字典."""
    tree = {}
    if not base_dir.exists():
        return tree

    for path in base_dir.rglob('*'):
        if not path.is_file():
            continue

        rel_parts = path.relative_to(base_dir).parts

        curr = tree
        for part in rel_parts[:-1]:
            part_name = _name(part)

            if part_name not in curr:
                curr[part_name] = {}

            curr = curr[part_name]

        curr[_name(rel_parts[-1])] = path.relative_to(base_dir).as_posix()

    return tree


def generate_res_code(tree: dict, indent: int = 4) -> list[str]:
    lines = []
    ind = ' ' * indent
    for k, v in sorted(tree.items()):
        if isinstance(v, dict):
            lines.append(f"{ind}class {k}(Icon):")
            if not v:
                lines.append(f"{ind}    ...")
            else:
                lines.extend(generate_res_code(v, indent + 4))
        else:
            lines.append(f"{ind}{k} = '{v}'")

    lines.append('')
    return lines


def main():
    _file = Path(__file__)
    proj_dir = _file.parent.parent.parent
    icon_dir = proj_dir / 'res' / 'icon'
    light_icon_dir = icon_dir / 'light'

    res_out_file = proj_dir / 'src' / 'theme' / 'icon.py'

    light_tree = build_tree(light_icon_dir)

    res_lines = [
        f"# 该文件由 {_file.relative_to(proj_dir).as_posix()} 自动生成, 勿手动修改",
        "from enum import Enum",
        "",
        "",
        "class Icon(Enum):",
        '    """ 该类仅作类型标注用 """',
        "",
        "",
        "class icon(Icon):"
    ]
    code = generate_res_code(light_tree, 4)
    if code:
        res_lines.extend(code)
    else:
        res_lines.append('    ...')

    res_out_file.parent.mkdir(parents=True, exist_ok=True)
    res_out_file.write_text("\n".join(res_lines), encoding='utf-8')


if __name__ == '__main__':
    main()
