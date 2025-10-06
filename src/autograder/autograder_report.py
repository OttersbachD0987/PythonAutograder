import dataclasses
from dataclasses import dataclass
import time
from .autograder_modifier import AutograderModifier, ModifierType

@dataclass
class AutograderReport:
    messages:  dict[str, list[tuple[int, str]]]                     = dataclasses.field(default_factory=dict)
    modifiers: list[AutograderModifier]                             = dataclasses.field(default_factory=list)
    final: dict[str, tuple[float, float, float, bool, float, bool]] = dataclasses.field(default_factory=dict)

    def postLog(self, a_criterion: str, a_message: str) -> None:
        self.messages[a_criterion] = [*self.messages.get(a_criterion, []), (time.time_ns(), a_message)]
    
    def addModifier(self, a_modifier: AutograderModifier) -> None:
        self.modifiers.append(a_modifier)

    def proccessModifiers(self) -> tuple[str, float, str]|None:
        for modifier in self.modifiers:
            match modifier.modifierType:
                case ModifierType.ADDITION:
                    self.final[modifier.criterion] = (self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[0] + modifier.modifierValue, self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[1], self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[2], self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[3], modifier.maxValue, self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[5] and modifier.passes)
                case ModifierType.MULTIPLY:
                    self.final[modifier.criterion] = (self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[0], self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[1] * modifier.modifierValue, self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[2], self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[3], modifier.maxValue, self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[5] and modifier.passes)
                case ModifierType.OVERRIDE:
                    self.final[modifier.criterion] = (self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[0], self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[1], modifier.modifierValue, True, modifier.maxValue, self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[5] and modifier.passes)
                case ModifierType.OVERKILL:
                    self.final[modifier.criterion] = (self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[0], self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[1], modifier.modifierValue, True, modifier.maxValue, self.final.get(modifier.criterion, (0, 1, 0, False, 0, True))[5] and modifier.passes)
                    return (modifier.criterion, modifier.modifierValue, ", ".join([message for _, message in self.messages.get(modifier.criterion, [])]))
        return None

    def usable(self, a_criteria: dict[str, float]) -> dict[str, tuple[str, float, float, bool]]:
        return {
            criterion: (", ".join([message for _, message in self.messages.get(criterion, [])]), override * a_criteria.get(criterion, 1) if overriden else base * mult * a_criteria.get(criterion, 1), maxValue * a_criteria.get(criterion, 1), passes) for criterion, (base, mult, override, overriden, maxValue, passes) in self.final.items()
        }        
    
    def clear(self) -> None:
        self.messages = {}
        self.modifiers = []
        self.final = {}
