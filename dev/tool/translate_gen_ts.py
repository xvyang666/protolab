import subprocess
from pathlib import Path


def gen_ts(src_dir: Path, target_lang: str, ts_path: Path):
    exclude_dirs = {
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".git",
        "build",
        "dist",
    }
    py_files = []
    for p in src_dir.rglob("*.py"):
        if not any(part in exclude_dirs for part in p.parts):
            py_files.append(str(p))

    with open('tmp', 'w') as tmp_file:
        tmp_file.write('\n'.join(py_files))
        tmp_config_path = tmp_file.name

    try:
        lupdate_cmd = [
            "pyside6-lupdate",
            "-source-language",
            "zh",
            "-target-language",
            target_lang,
            f'@{tmp_config_path}',  # 传入配置文件路径
            "-ts",
            str(ts_path),
        ]

        print(f"正在扫描 {len(py_files)} 个文件并更新 {ts_path.name}...")
        subprocess.run(lupdate_cmd, check=True)

    finally:
        Path(tmp_config_path).unlink(missing_ok=True)


def gen_qm(ts_path: Path, qm_path: Path):
    lrelease_cmd = [
        "pyside6-lrelease",
        str(ts_path),
        "-qm",
        str(qm_path),
    ]
    subprocess.run(lrelease_cmd, check=True)
    print(f"编译成功: {qm_path.name}")


def main():
    _file = Path(__file__)
    proj_dir = _file.parent.parent.parent

    src_dir = proj_dir / 'src'

    for target_lang in ["app_zh_CN", "app_en"]:
        ts_path = proj_dir / 'dev' / 'locales' / f"{target_lang}.ts"
        ts_path.parent.mkdir(parents=True, exist_ok=True)

        qm_path = proj_dir / 'res' / 'locales' / f"{target_lang}.qm"
        qm_path.parent.mkdir(parents=True, exist_ok=True)

        gen_ts(src_dir, target_lang, ts_path)
        gen_qm(ts_path, qm_path)


if __name__ == '__main__':
    main()
