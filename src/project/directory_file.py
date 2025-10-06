from .file_type import FileType

class DirectoryFile(FileType):
    def __init__(self, a_path: str, a_name: str):
        super().__init__(a_path, a_name)

        self.files: list[FileType] = util.getFiles(self.path)

import util