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
        """Create an extension from a dictionary.

        Args:
            a_data (dict[str, Any]): The data loaded in from the extension.
            a_path (str): The path the extension was loaded from.

        Returns:
            out (Self): The extension data from the data.
        """
        return cls(
            a_data.get("name", a_path),
            a_data.get("description", ""),
            a_path,
            Version.init(a_data.get("version", "0000.0000.0000.0000"))
        )

    def toDict(self) -> dict[str, Any]:
        """_summary_

        Returns:
            out (dict[str, Any]): _description_
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": str(self.version)
        }