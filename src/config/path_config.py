_file = Path(__file__)

class PathConfig:
    RootDir = _file.parent.parent.parent
    SrcDir = RootDir / "src"
    ResDir = RootDir / "res"