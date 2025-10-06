from abc import ABC

class FileType(ABC):
    def __init__(self, a_path: str, a_name: str) -> None:
        self.path: str = a_path
        self.name: str = a_name