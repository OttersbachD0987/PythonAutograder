import dataclasses
from dataclasses import dataclass
import time
from .autograder_modifier import AutograderModifier, ModifierType
from typing import NamedTuple, Optional

class FinalModifier(NamedTuple):
    """The final modifier of a grade.
    """
    addition:       float
    multiplication: float
    override:       float
    overridden:     bool
    maxValue:       float
    passes:         bool

DEFAULT_MODIFIER: FinalModifier = FinalModifier(0, 1, 0, False, 0, True)

class RubricGrade(NamedTuple):
    """A rubric grade for management.
    """
    message:   str
    amount:    float
    maxAmount: float
    passes:    bool

@dataclass
class AutograderReport:
    """A report of a grading session.
    """
    messages:  dict[str, list[tuple[int, str]]] = dataclasses.field(default_factory=dict) # type: ignore
    modifiers: list[AutograderModifier]         = dataclasses.field(default_factory=list) # type: ignore
    final:     dict[str, FinalModifier]         = dataclasses.field(default_factory=dict) # type: ignore

    def postLog(self, a_criterion: str, a_message: str) -> None:
        """Post a log to the grade report regarding a specific criterion.

        Args:
            a_criterion (str): The criterion this log pertains too.
            a_message (str): The message contents of the log.
        """
        self.messages[a_criterion] = [*self.messages.get(a_criterion, []), (time.time_ns(), a_message)]
    
    def addModifier(self, a_modifier: AutograderModifier) -> None:
        """Add a new modifier to the grade report.

        Args:
            a_modifier (AutograderModifier): The modifer to add to the grade report.
        """
        self.modifiers.append(a_modifier)

    def proccessModifiers(self) -> Optional[tuple[str, float, str]]:
        """Process the modifiers of this grade report and return either an override value, or None if all were processed.

        Returns:
            Optional[tuple[str, float, str]]: An override value if an overkill modifier was present.
        """
        for modifier in self.modifiers:
            match modifier.modifierType:
                case ModifierType.ADDITION:
                    self.final[modifier.criterion] = FinalModifier(self.final.get(modifier.criterion, DEFAULT_MODIFIER).addition + modifier.modifierValue, self.final.get(modifier.criterion, DEFAULT_MODIFIER).multiplication, self.final.get(modifier.criterion, DEFAULT_MODIFIER).override, self.final.get(modifier.criterion, DEFAULT_MODIFIER).overridden, modifier.maxValue, self.final.get(modifier.criterion, DEFAULT_MODIFIER).passes and modifier.passes)
                case ModifierType.MULTIPLY:
                    self.final[modifier.criterion] = FinalModifier(self.final.get(modifier.criterion, DEFAULT_MODIFIER).addition, self.final.get(modifier.criterion, DEFAULT_MODIFIER).multiplication * modifier.modifierValue, self.final.get(modifier.criterion, DEFAULT_MODIFIER).override, self.final.get(modifier.criterion, DEFAULT_MODIFIER).overridden, modifier.maxValue, self.final.get(modifier.criterion, DEFAULT_MODIFIER).passes and modifier.passes)
                case ModifierType.OVERRIDE:
                    self.final[modifier.criterion] = FinalModifier(self.final.get(modifier.criterion, DEFAULT_MODIFIER).addition, self.final.get(modifier.criterion, DEFAULT_MODIFIER)[1], modifier.modifierValue, True, modifier.maxValue, self.final.get(modifier.criterion, DEFAULT_MODIFIER)[5] and modifier.passes)
                case ModifierType.OVERKILL:
                    self.final.clear()
                    self.final[modifier.criterion] = FinalModifier(DEFAULT_MODIFIER.addition, DEFAULT_MODIFIER.multiplication, modifier.modifierValue, True, modifier.maxValue, modifier.passes)
                    for otherModifier in (set(self.modifiers) - {modifier}):
                        self.final[otherModifier.criterion] = FinalModifier(self.final.get(modifier.criterion, DEFAULT_MODIFIER)[0], self.final.get(modifier.criterion, DEFAULT_MODIFIER)[1], self.final.get(modifier.criterion, DEFAULT_MODIFIER)[2], self.final.get(modifier.criterion, DEFAULT_MODIFIER)[3], modifier.maxValue, self.final.get(modifier.criterion, DEFAULT_MODIFIER)[5] and modifier.passes)
                    return (modifier.criterion, modifier.modifierValue, ", ".join([message for _, message in self.messages.get(modifier.criterion, [])]))
        return None

    def usable(self, a_criteria: dict[str, float]) -> dict[str, RubricGrade]:
        """Get the report in a usable format after all processing is finished.

        Args:
            a_criteria (dict[str, float]): The criteria and their relative weights.

        Returns:
            dict[str, RubricGrade]: The final usable report data.
        """
        return {
            criterion: RubricGrade(", ".join([message for _, message in self.messages.get(criterion, [])]), round(override * a_criteria.get(criterion, 1) if overriden else base * mult * a_criteria.get(criterion, 1)), round(maxValue * a_criteria.get(criterion, 1)), passes) for criterion, (base, mult, override, overriden, maxValue, passes) in self.final.items()
        }        
    
    def clear(self) -> None:
        """Clear the report.
        """
        self.messages = {}
        self.modifiers = []
        self.final = {}
