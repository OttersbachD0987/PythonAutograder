from dataclasses import dataclass
from typing import Any, Self
from utils.version import Version

@dataclass
class Extension:
    """_summary_
    
    _description_
    """
    name: str
    description: str
    path: str
    version: Version
    
    @classmethod
    def fromDict(cls, a_data: dict[str, Any], a_path: str) -> Self:
        """_summary_

        Args:
            data (dict[str, Any]): _description_

        Returns:
            Self: _description_
        """
        return Extension(
            a_data.get("name", a_path),
            a_data.get("description", ""),
            a_path,
            Version.init(a_data.get("version", "0000.0000.0000.0000"))
        )

    def toDict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": str(self.version)
        }