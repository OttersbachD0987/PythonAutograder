from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .file_type import FileType

class Project:
    def __init__(self, a_name: str, a_dir: str) -> None:
        self.name: str = a_name
        self.dir: str = a_dir
        self.files: list[FileType] = utils.util.getFiles(a_dir)

import utils.util