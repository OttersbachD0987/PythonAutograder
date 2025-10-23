from enum import IntEnum, auto
from typing import Any, Self
from utils.util import tryCast, tryGetCast
from dataclasses import dataclass

class Requirement(IntEnum):
    REQUIRED  = auto()
    ALLOWED   = auto()
    FORBIDDEN = auto()

    def __repr__(self) -> str:
        match self:
            case Requirement.REQUIRED:
                return "Required"
            case Requirement.ALLOWED:
                return "Allowed"
            case Requirement.FORBIDDEN:
                return "Forbidden"

@dataclass(repr=False)
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
            ), {
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
    
    def copy(self) -> "ProjectSettings":
        return ProjectSettings(self.importDefault, self.importOverrides.copy(), self.importLocal)
    
    def __repr__(self) -> str:
        return f"Import Default: {repr(self.importDefault)}\nImport Overrides: \n{"\n".join([f"  {key}: {repr(requirement)}" for key, requirement in self.importOverrides.items()])}\nImport Local: {repr(self.importLocal)}"