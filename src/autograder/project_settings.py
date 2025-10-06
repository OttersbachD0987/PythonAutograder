from enum import IntEnum, auto
from typing import Any, Self
from util import tryCast, tryGetCast
from dataclasses import dataclass

class Requirement(IntEnum):
    REQUIRED  = auto()
    ALLOWED   = auto()
    FORBIDDEN = auto()

@dataclass
class ProjectSettings:
    importDefault: Requirement
    importOverrides: dict[str, Requirement]
    importLocal: Requirement

    @classmethod
    def fromDict(cls, a_data: dict[str, Any]) -> Self:
        """Create a Project Settings from a dict.
        """
        toReturn: ProjectSettings = cls(
            tryGetCast(
                a_data,
                "import_default",
                lambda a_key: Requirement(a_key),
                Requirement.FORBIDDEN
            ), 
            {
                key: tryCast(
                    value,
                    Requirement,
                    Requirement.ALLOWED
                ) for key, value in a_data.get("import_overrides", {}).items()
            }, 
            tryGetCast(
                a_data,
                "import_local",
                Requirement,
                Requirement.ALLOWED
            )
        )
        
        return toReturn
    
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "import_default": int(self.importDefault),
            "import_overrides": {
                key: int(requirement) for key, requirement in self.importOverrides.items()
            },
            "import_local": int(self.importLocal)
        }