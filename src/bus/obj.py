from config.path_config import PathConfig
from theme.t import Theme
from util.logger import Logger

logger: Logger = Logger(PathConfig.proj_dir)
theme: Theme = Theme()
