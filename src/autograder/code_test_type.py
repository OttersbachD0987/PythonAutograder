from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from code_test import CodeTestNode
    from autograder.autograder_application import Autograder

class IParameterGroup:
    ...

@dataclass
class ParameterRepresentation(IParameterGroup):
    id: str
    kind: str
    values: dict[str, IParameterGroup]

@dataclass
class OptionalParameter(IParameterGroup):
    parameter: IParameterGroup

@dataclass
class ExclusiveParameters(IParameterGroup):
    parameters: dict[str, IParameterGroup]

@dataclass
class CodeTestType:
    name: str
    testFunction: Callable[[dict[str, "CodeTestNode"], "Autograder"], tuple[float, bool]]
    parameters: Callable[[], list[IParameterGroup]]