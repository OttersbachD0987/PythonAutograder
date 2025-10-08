import dataclasses
from dataclasses import dataclass
import time
from .autograder_modifier import AutograderModifier, ModifierType
from typing import NamedTuple

class FinalModifier(NamedTuple):
    addition:       int
    multiplication: int
    override:       int
    overridden:     bool
    maxValue:       int
    passes:         bool

DEFAULT_MODIFIER: FinalModifier = FinalModifier(0, 1, 0, False, 0, True)

class RubricGrade(NamedTuple):
    message:   str
    amount:    int
    maxAmount: int
    passes:    bool

@dataclass
class AutograderReport:
    messages:  dict[str, list[tuple[int, str]]] = dataclasses.field(default_factory=dict)
    modifiers: list[AutograderModifier]         = dataclasses.field(default_factory=list)
    final:     dict[str, FinalModifier]         = dataclasses.field(default_factory=dict)

    def postLog(self, a_criterion: str, a_message: str) -> None:
        self.messages[a_criterion] = [*self.messages.get(a_criterion, []), (time.time_ns(), a_message)]
    
    def addModifier(self, a_modifier: AutograderModifier) -> None:
        self.modifiers.append(a_modifier)

    def proccessModifiers(self) -> tuple[str, float, str]|None:
        for modifier in self.modifiers:
            match modifier.modifierType:
                case ModifierType.ADDITION:
                    self.final[modifier.criterion] = FinalModifier(int(self.final.get(modifier.criterion, DEFAULT_MODIFIER).addition + modifier.modifierValue), self.final.get(modifier.criterion, DEFAULT_MODIFIER).multiplication, self.final.get(modifier.criterion, DEFAULT_MODIFIER).override, self.final.get(modifier.criterion, DEFAULT_MODIFIER).overridden, int(modifier.maxValue), self.final.get(modifier.criterion, DEFAULT_MODIFIER).passes and modifier.passes)
                case ModifierType.MULTIPLY:
                    self.final[modifier.criterion] = FinalModifier(self.final.get(modifier.criterion, DEFAULT_MODIFIER).addition, int(self.final.get(modifier.criterion, DEFAULT_MODIFIER).multiplication * modifier.modifierValue), self.final.get(modifier.criterion, DEFAULT_MODIFIER).override, self.final.get(modifier.criterion, DEFAULT_MODIFIER).overridden, int(modifier.maxValue), self.final.get(modifier.criterion, DEFAULT_MODIFIER).passes and modifier.passes)
                case ModifierType.OVERRIDE:
                    self.final[modifier.criterion] = FinalModifier(self.final.get(modifier.criterion, DEFAULT_MODIFIER).addition, self.final.get(modifier.criterion, DEFAULT_MODIFIER)[1], int(modifier.modifierValue), True, int(modifier.maxValue), self.final.get(modifier.criterion, DEFAULT_MODIFIER)[5] and modifier.passes)
                case ModifierType.OVERKILL:
                    self.final.clear()
                    self.final[modifier.criterion] = FinalModifier(DEFAULT_MODIFIER.addition, DEFAULT_MODIFIER.multiplication, int(modifier.modifierValue), True, int(modifier.maxValue), modifier.passes)
                    for otherModifier in (set(self.modifiers) - {modifier}):
                        self.final[otherModifier.criterion] = FinalModifier(self.final.get(modifier.criterion, DEFAULT_MODIFIER)[0], self.final.get(modifier.criterion, DEFAULT_MODIFIER)[1], self.final.get(modifier.criterion, DEFAULT_MODIFIER)[2], self.final.get(modifier.criterion, DEFAULT_MODIFIER)[3], int(modifier.maxValue), self.final.get(modifier.criterion, DEFAULT_MODIFIER)[5] and modifier.passes)
                    return (modifier.criterion, modifier.modifierValue, ", ".join([message for _, message in self.messages.get(modifier.criterion, [])]))
        return None

    def usable(self, a_criteria: dict[str, float]) -> dict[str, RubricGrade]:
        return {
            criterion: RubricGrade(", ".join([message for _, message in self.messages.get(criterion, [])]), int(override * a_criteria.get(criterion, 1) if overriden else base * mult * a_criteria.get(criterion, 1)), int(maxValue * a_criteria.get(criterion, 1)), passes) for criterion, (base, mult, override, overriden, maxValue, passes) in self.final.items()
        }        
    
    def clear(self) -> None:
        self.messages = {}
        self.modifiers = []
        self.final = {}
