from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .file_type import FileType
    from autograder.project_settings import ProjectSettings

class Project:
    def __init__(self, a_name: str, a_dir: str) -> None:
        self.name: str = a_name
        self.dir: str = a_dir
        self.files: list[FileType] = util.getFiles(a_dir)

    # BROKEN
    def evaluateImports(self, a_projectSettings: "ProjectSettings") -> None:
        ...

import util