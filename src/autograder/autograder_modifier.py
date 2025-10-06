from dataclasses import dataclass
from enum import StrEnum, auto

class ModifierType(StrEnum):
    ADDITION = auto()
    MULTIPLY = auto()
    OVERRIDE = auto()
    OVERKILL = auto()

@dataclass
class AutograderModifier:
    criterion: str
    modifierType: ModifierType
    modifierValue: float
    maxValue: float
    passes: bool
