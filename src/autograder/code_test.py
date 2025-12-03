from __future__ import annotations

# fmt: off

from dataclasses import dataclass
from typing import ClassVar, Any, Literal, Self, TYPE_CHECKING, cast, override
from abc import ABC, abstractmethod
from collections.abc import Callable

from .autograder_report import AutograderReport
from .code_walker import ASTPattern
from .autograder_modifier import AutograderModifier, ModifierType
from .code_test_type import CodeTestType, IParameterGroup, IParameterRepresentable, ParameterRepresentation
if TYPE_CHECKING:
    from .autograder_application import Autograder

@dataclass
class IDictSerializable(ABC):
    @abstractmethod
    def toDict(self) -> dict[str, Any]:
        ...

@dataclass
class CodeTestNode(IDictSerializable, ABC):
    nodeID: str

class IExecutable(CodeTestNode, ABC):
    @abstractmethod
    def execute(self, a_data: dict[str, Any]) -> None:
        pass

class ICanReturnAny(CodeTestNode, ABC):
    @abstractmethod
    def evaluateAny(self, a_data: dict[str, Any]) -> Any:
        pass

class ICanReturnBool(ICanReturnAny, ABC):
    @abstractmethod
    def evaluateBool(self, a_data: dict[str, Any]) -> bool:
        pass

class ICanReturnStr(ICanReturnAny, ABC):
    @abstractmethod
    def evaluateStr(self, a_data: dict[str, Any]) -> str:
        pass

class ICanReturnInt(ICanReturnAny, ABC):
    @abstractmethod
    def evaluateInt(self, a_data: dict[str, Any]) -> int:
        pass

class ICanReturnFloat(ICanReturnAny, ABC):
    @abstractmethod
    def evaluateFloat(self, a_data: dict[str, Any]) -> float:
        pass

@dataclass
class ListTestNode(CodeTestNode, IParameterRepresentable):
    nodes: list[CodeTestNode]

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "nodes": [node.toDict() for node in self.nodes]
        }

    @override
    @staticmethod
    def parameterRepresentation(a_id: str) -> IParameterGroup:
        return cast(IParameterGroup, ParameterRepresentation(a_id, "ListTestNode", {
            "node_id": cast(IParameterGroup, ParameterRepresentation("node_id", "string", {})),
            "nodes": cast(IParameterGroup, ParameterRepresentation("nodes", "list[CodeTestNode]", {}))
        }))

@dataclass
class DictionaryTestNode(CodeTestNode, IParameterRepresentable):
    nodes: dict[str, CodeTestNode]

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "nodes": {key: node.toDict() for key, node in self.nodes.items()}
        }

    @override
    @staticmethod
    def parameterRepresentation(a_id: str) -> IParameterGroup:
        return cast(IParameterGroup, ParameterRepresentation(a_id, "DictionaryTestNode", {
            "node_id": cast(IParameterGroup, ParameterRepresentation("node_id", "string", {})),
            "nodes": cast(IParameterGroup, ParameterRepresentation("nodes", "dict[str, CodeTestNode]", {}))
        }))

@dataclass
class LiteralTestNode(ICanReturnBool, ICanReturnStr, ICanReturnInt, ICanReturnFloat, IParameterRepresentable):
    literalType: str
    literalValue: Any
    
    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "literal_type": self.literalType,
            "literal_value": self.literalValue
        }
    
    @override
    def evaluateBool(self, a_data: dict[str, Any]) -> bool:
        return bool(self.literalValue) if self.literalType == "boolean" else False

    @override
    def evaluateStr(self, a_data: dict[str, Any]) -> str:
        return str(self.literalValue) if self.literalType == "string" else ""
    
    @override
    def evaluateInt(self, a_data: dict[str, Any]) -> int:
        return int(self.literalValue) if self.literalType == "int" else -1
    
    @override
    def evaluateFloat(self, a_data: dict[str, Any]) -> float:
        return float(self.literalValue) if self.literalType == "float" else 0
    
    @override
    def evaluateAny(self, a_data: dict[str, Any]) -> Any:
        return self.literalType

    @override
    @staticmethod
    def parameterRepresentation(a_id: str) -> IParameterGroup:
        return cast(IParameterGroup, ParameterRepresentation(a_id, "LiteralTestNode", {
            "node_id": cast(IParameterGroup, ParameterRepresentation("node_id", "string", {})),
            "literal_type": cast(IParameterGroup, ParameterRepresentation("literal_type", "string", {})),
            "literal_value": cast(IParameterGroup, ParameterRepresentation("literal_value", "Any", {}))
        }))

@dataclass
class ASTNodeTestNode(ICanReturnBool, ICanReturnStr, ICanReturnInt, ICanReturnFloat, IParameterRepresentable):
    toCall: str
    
    @override
    def toDict(self) -> dict[str, str]:
        """Convert to a dictionary representation.

        Returns:
            out (dict[str, str]): The dictionary representation of the node.
        """
        return {
            "node_id": self.nodeID,
            "to_call": self.toCall
        }
    
    @override
    def evaluateBool(self, a_data: dict[str, Any]) -> bool:
        return eval(self.toCall)

    @override
    def evaluateStr(self, a_data: dict[str, Any]) -> str:
        return eval(self.toCall)
    
    @override
    def evaluateInt(self, a_data: dict[str, Any]) -> int:
        return eval(self.toCall)
    
    @override
    def evaluateFloat(self, a_data: dict[str, Any]) -> float:
        return eval(self.toCall)
    
    @override
    def evaluateAny(self, a_data: dict[str, Any]) -> Any:
        return eval(self.toCall)

    @override
    @staticmethod
    def parameterRepresentation(a_id: str) -> IParameterGroup:
        return cast(IParameterGroup, ParameterRepresentation(a_id, "ASTNodeTestNode", {
            "node_id": cast(IParameterGroup, ParameterRepresentation("node_id", "string", {})),
            "to_call": cast(IParameterGroup, ParameterRepresentation("to_call", "string", {}))
        }))

@dataclass
class ProjectTestNode(CodeTestNode, IParameterRepresentable):
    projectName: str
    projectEntrypoint: str
    projectArguments: DictionaryTestNode
    projectInputs: list[str]

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "project_name": self.projectName,
            "project_entrypoint": self.projectEntrypoint,
            "project_arguments": self.projectArguments.toDict(),
            "project_inputs": self.projectInputs
        }

    @override
    @staticmethod
    def parameterRepresentation(a_id: str) -> IParameterGroup:
        return cast(IParameterGroup, ParameterRepresentation(a_id, "ProjectTestNode", {
            "node_id": cast(IParameterGroup, ParameterRepresentation("node_id", "string", {})),
            "project_name": cast(IParameterGroup, ParameterRepresentation("project_name", "string", {})),
            "project_entrypoint": cast(IParameterGroup, ParameterRepresentation("project_entrypoint", "string", {})),
            "project_arguments": DictionaryTestNode.parameterRepresentation("project_arguments"),
            "project_inputs": cast(IParameterGroup, ParameterRepresentation("project_inputs", "list[string]", {}))
        }))

@dataclass
class InvalidTestNode(CodeTestNode):
    data: dict[str, Any]

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.

        Returns:
            (dict[str, Any]): A dictionary representation of the test node.
        """
        return {
            "node_id": self.nodeID,
            **self.data
        }
    
@dataclass
class ComparisonTestNode(ICanReturnBool, IParameterRepresentable):
    left: ICanReturnAny
    operator: Literal["GTE","GT","LTE","LT","EQ","NEQ","AND","OR","XOR","NAND","NOR"]
    right: ICanReturnAny

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "left": self.left.toDict(),
            "operator": self.operator,
            "right": self.right.toDict()
        }
    
    @override
    def evaluateBool(self, a_data: dict[str, Any]) -> bool:
        left, right = self.left.evaluateAny(a_data), self.right.evaluateAny(a_data)
        match self.operator:
            case "GTE":
                return left >= right
            case "GT":
                return left > right
            case "LTE":
                return left <= right
            case "LT":
                return left < right
            case "EQ":
                return left == right
            case "NEQ":
                return left != right
            case "AND":
                return left and right
            case "OR":
                return left or right
            case "XOR":
                return (left or right) and (left != right)
            case "NAND":
                return not (left and right)
            case "NOR":
                return not (left or right)
        return False
    
    @override
    def evaluateAny(self, a_data: dict[str, Any]) -> Any:
        return self.evaluateBool(a_data)

    @override
    @staticmethod
    def parameterRepresentation(a_id: str) -> IParameterGroup:
        return cast(IParameterGroup, ParameterRepresentation(a_id, "ComparisonTestNode", {
            "node_id": cast(IParameterGroup, ParameterRepresentation("node_id", "string", {})),
            "left": cast(IParameterGroup, ParameterRepresentation("left", "ICanReturnAny", {})),
            "operator": cast(IParameterGroup, ParameterRepresentation("operator", "string", {})),
            "right": cast(IParameterGroup, ParameterRepresentation("right", "ICanReturnAny", {}))
        }))

#region AST Related Nodes
@dataclass
class ASTPatternTestNode(CodeTestNode, IParameterRepresentable):
    nodeType: str
    pattern: ASTPattern

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "node_type": self.nodeType,
            "pattern": self.pattern.toDict()
        }

    @override
    @staticmethod
    def parameterRepresentation(a_id: str) -> IParameterGroup:
        return cast(IParameterGroup, ParameterRepresentation(a_id, "ASTPatternTestNode", {
            "node_id": cast(IParameterGroup, ParameterRepresentation("node_id", "string", {})),
            "node_type": cast(IParameterGroup, ParameterRepresentation("node_type", "string", {})),
            "pattern": ASTPattern.parameterRepresentation("pattern")

        }))

@dataclass
class ASTWalkTestNode(CodeTestNode):
    nodeType: str
    test: ICanReturnBool

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "node_type": self.nodeType,
            "test": self.test.toDict()
        }
#endregion

#region Execute
@dataclass
class PostMessageTestNode(IExecutable):
    criterion: str
    nodeMessage: str

    @override
    def toDict(self) -> dict[str, str]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "criterion": self.criterion,
            "node_message": self.nodeMessage
        }

    @override
    def execute(self, a_data: dict[str, Any]) -> None:
        eval(f"cast(\"Autograder\", a_data[\"autograder\"]).instanceData.reports[a_data[\"current_project\"]] = cast(\"Autograder\", a_data[\"autograder\"]).instanceData.reports.get(a_data[\"current_project\"], AutograderReport())\ncast(\"Autograder\", a_data[\"autograder\"]).instanceData.reports[a_data[\"current_project\"]].postLog(\"{self.criterion}\", f\"{self.nodeMessage}\")")

def CanReturnWrapper(a_value: Any|IDictSerializable) -> dict[str, Any]|Any:
    return a_value.toDict() if isinstance(a_value, IDictSerializable) else a_value

def EvaluateFloat(a_value: float|ICanReturnFloat, a_data: dict[str, Any]) -> float:
    return a_value.evaluateFloat(a_data) if isinstance(a_value, ICanReturnFloat) else a_value

def EvaluateBool(a_value: bool|ICanReturnBool, a_data: dict[str, Any]) -> bool:
    return a_value.evaluateBool(a_data) if isinstance(a_value, ICanReturnBool) else a_value

@dataclass
class PostGradeModifierTestNode(IExecutable):
    criterion: str
    modifierType: ModifierType
    modifierValue: float|ICanReturnFloat
    maxValue: float|ICanReturnFloat
    passes: bool|ICanReturnBool

    @override
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "criterion": self.criterion,
            "modifier_type": str(self.modifierType),
            "modifier_value": CanReturnWrapper(self.modifierValue),
            "max_value": CanReturnWrapper(self.maxValue),
            "passes": CanReturnWrapper(self.passes)
        }

    @override
    def execute(self, a_data: dict[str, Any]) -> None:
        cast("Autograder", a_data["autograder"]).instanceData.reports[a_data["current_project"]] = cast("Autograder", a_data["autograder"]).instanceData.reports.get(a_data["current_project"], AutograderReport())
        cast("Autograder", a_data["autograder"]).instanceData.reports[a_data["current_project"]].addModifier(AutograderModifier(self.criterion, self.modifierType, EvaluateFloat(self.modifierValue, a_data), EvaluateFloat(self.maxValue, a_data), EvaluateBool(self.passes, a_data)))

@dataclass
class BlockTestNode(IExecutable):
    nodes: list[IExecutable]

    @override
    def toDict(self) -> dict[str, Any]:
        return {
            "node_id": self.nodeID,
            "nodes": [node.toDict() for node in self.nodes]
        }
    
    @override
    def execute(self, a_data: dict[str, Any]) -> None:
        [node.execute(a_data) for node in self.nodes]
#endregion

@dataclass
class CodeTest:
    TestTypes: ClassVar[dict[str, CodeTestType]] = {}
    type:   str
    report: str
    arguments: dict[str, CodeTestNode]
    found:    CodeTestNode|None = None
    notFound: CodeTestNode|None = None

    @classmethod
    def fromDict(cls, a_data: dict[str, Any]) -> Self:
        """Load a code test from a dict.
        """
        return cls(
            a_data["type"],
            a_data["report"],
            {key: parseCodeTestNode(argument) for key, argument in cast(dict[str, dict[str, Any]], a_data.get("arguments", {})).items()},
            parseCodeTestNode(a_data["found"]) if "found" in a_data else None,
            parseCodeTestNode(a_data["notFound"]) if "notFound" in a_data else None
        )
    
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        toReturn: dict[str, Any] = {
            "type": self.type,
            "report": self.report,
            "arguments": {key: node.toDict() for key, node in self.arguments.items()}
        }
        if self.found is not None:
            toReturn["found"] = self.found.toDict()
        if self.notFound is not None:
            toReturn["notFound"] = self.notFound.toDict()
        return toReturn
    
    @staticmethod
    def registerTestType(a_id: str, a_testFunction: Callable[[dict[str, CodeTestNode], "Autograder"], tuple[float, bool]], a_parameters: Callable[[], list[IParameterGroup]]) -> None:
        CodeTest.TestTypes[a_id] = CodeTestType(a_id, a_testFunction, a_parameters)
    
    def runTest(self, a_grader: "Autograder", a_data: dict[str, Any]) -> tuple[float, bool]:
        a_data["factor"], a_data["success"] = CodeTest.TestTypes[self.type].testFunction(self.arguments, a_grader)
        a_data["current_project"] = self.report
        if a_data["success"]:
            if self.found is not None:
                executeCodeTestNode(cast(IExecutable, self.found), a_data)
        elif self.notFound is not None:
            executeCodeTestNode(cast(IExecutable, self.notFound), a_data)
        del a_data["current_project"]
        return a_data.pop("factor"), a_data.pop("success")

def parseCodeTestNode(a_node: dict[str, Any]) -> CodeTestNode:
    """Parses a code test node from a dict.
    """
    match a_node:
        case {"node_id": nodeID, "literal_type": literalType, "literal_value": literalValue} if nodeID == "literal":
            return LiteralTestNode(nodeID, literalType, literalValue)
        case {"node_id": nodeID, "to_call": toCall} if nodeID == "ast_node":
            return ASTNodeTestNode(nodeID, toCall)
        case {"node_id": nodeID, "nodes": nodes} if nodeID == "list":
            return ListTestNode(nodeID, [parseCodeTestNode(node) for node in nodes])
        case {"node_id": nodeID, "nodes": nodes} if nodeID == "block":
            return BlockTestNode(nodeID, [parsedNode for node in nodes if isinstance(parsedNode := parseCodeTestNode(node), IExecutable)])
        case {"node_id": nodeID, "criterion": criterion, "node_message": nodeMessage} if nodeID == "post_message":
            return PostMessageTestNode(nodeID, criterion, nodeMessage)
        case {"node_id": nodeID, "nodes": nodes} if nodeID == "dictionary" and isinstance(nodes, dict):
            return DictionaryTestNode(nodeID, {key: parseCodeTestNode(node) for key, node in nodes.items()})
        case {"node_id": nodeID, "left": left, "operator": operator, "right": right} if nodeID == "comparison" and isinstance(leftParsed := parseCodeTestNode(left), ICanReturnAny) and isinstance(rightParsed := parseCodeTestNode(right), ICanReturnAny):
            return ComparisonTestNode(nodeID, leftParsed, operator, rightParsed)
        case {"node_id": nodeID, "node_type": nodeType, "test": test} if nodeID == "ast_walk" and isinstance(testParsed := parseCodeTestNode(test), ICanReturnBool):
            return ASTWalkTestNode(nodeID, nodeType, testParsed)
        case {"node_id": nodeID, "project_name": projectName, "project_entrypoint": projectEntrypoint, "project_arguments": projectArguments, "project_inputs": projectInputs} if nodeID == "project" and isinstance(parsed := parseCodeTestNode(projectArguments), DictionaryTestNode):
            return ProjectTestNode(nodeID, projectName, projectEntrypoint, parsed, projectInputs)
        case {"node_id": nodeID, "node_type": nodeType, "pattern": pattern} if nodeID == "ast_pattern":
            return ASTPatternTestNode(nodeID, nodeType, ASTPattern.fromDict(pattern))
        case {"node_id": nodeID, "criterion": criterion, "modifier_type": modifierType, "modifier_value": modifierValue, "max_value": maxValue, "passes": passes} if (nodeID == "post_grade_modifier"
                and (isinstance(modifierValueUse := modifierValue, float|int) or isinstance(modifierValueUse := parseCodeTestNode(modifierValue), ICanReturnFloat))
                and (isinstance(maxValueUse := maxValue, float|int) or isinstance(maxValueUse := parseCodeTestNode(maxValue), ICanReturnFloat))
                and (isinstance(passesUse := passes, bool) or isinstance(passesUse := parseCodeTestNode(passes), ICanReturnBool))):
            return PostGradeModifierTestNode(nodeID, criterion, ModifierType(modifierType), modifierValueUse, maxValueUse, passesUse)
    #print(f"Invalid: {a_node}")
    return InvalidTestNode("invalid", a_node)

def evaluateCodeTestNode(a_node: ICanReturnAny, a_data: dict[str, Any]) -> Any:
    return a_node.evaluateAny(a_data)
        
def executeCodeTestNode(a_node: IExecutable, a_data: dict[str, Any]) -> None:
    a_node.execute(a_data)

