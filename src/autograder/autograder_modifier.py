from dataclasses import dataclass
from enum import StrEnum, auto

class ModifierType(StrEnum):
    """The type of the modifier.
    """
    ADDITION = auto()
    MULTIPLY = auto()
    OVERRIDE = auto()
    OVERKILL = auto()

@dataclass(unsafe_hash=True)
class AutograderModifier:
    """A modifier for the autograder, has the criterion, modifier type, value, maximum value, and whether it's a passing modifier.
    """
    criterion: str
    modifierType: ModifierType
    modifierValue: float
    maxValue: float
    passes: bool
