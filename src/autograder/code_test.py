from dataclasses import dataclass
from typing import ClassVar, Callable, Any, Self, TYPE_CHECKING, cast
from abc import ABC, abstractmethod
from .code_walker import ASTPattern
from .autograder_modifier import AutograderModifier, ModifierType
if TYPE_CHECKING:
    from .autograder_application import Autograder

@dataclass
class CodeTestNode(ABC):
    nodeID: str

    @abstractmethod
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        pass

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
class ListTestNode(CodeTestNode):
    nodes: list[CodeTestNode]

    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "nodes": [node.toDict() for node in self.nodes]
        }

@dataclass
class DictionaryTestNode(CodeTestNode):
    nodes: dict[str, CodeTestNode]

    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "nodes": {key: node.toDict() for key, node in self.nodes.items()}
        }

@dataclass
class LiteralTestNode(ICanReturnBool, ICanReturnStr, ICanReturnInt, ICanReturnFloat):
    literalType: str
    literalValue: Any
    
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "literal_type": self.literalType,
            "literal_value": self.literalValue
        }
    
    def evaluateBool(self, a_data: dict[str, Any]) -> bool:
        return self.literalValue if self.literalType == "boolean" else False

    def evaluateStr(self, a_data: dict[str, Any]) -> str:
        return self.literalValue if self.literalType == "string" else ""
    
    def evaluateInt(self, a_data: dict[str, Any]) -> int:
        return self.literalValue if self.literalType == "int" else -1
    
    def evaluateFloat(self, a_data: dict[str, Any]) -> float:
        return self.literalValue if self.literalType == "float" else 0
    
    def evaluateAny(self, a_data: dict[str, Any]) -> Any:
        return self.literalType

@dataclass
class ASTNodeTestNode(ICanReturnBool, ICanReturnStr, ICanReturnInt, ICanReturnFloat):
    toCall: str
    
    def toDict(self) -> dict[str, str]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "to_call": "toCall"
        }
    
    def evaluateBool(self, a_data: dict[str, Any]) -> bool:
        return eval(self.toCall)

    def evaluateStr(self, a_data: dict[str, Any]) -> str:
        return eval(self.toCall)
    
    def evaluateInt(self, a_data: dict[str, Any]) -> int:
        return eval(self.toCall)
    
    def evaluateFloat(self, a_data: dict[str, Any]) -> float:
        return eval(self.toCall)
    
    def evaluateAny(self, a_data: dict[str, Any]) -> Any:
        return eval(self.toCall)

@dataclass
class ProjectTestNode(CodeTestNode):
    projectName: str
    projectEntrypoint: str
    projectArguments: DictionaryTestNode
    projectInputs: list[str]

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

@dataclass
class InvalidTestNode(CodeTestNode):
    data: dict[str, Any]

    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            **self.data
        }
    
@dataclass
class ComparisonTestNode(ICanReturnBool):
    left: ICanReturnAny
    operator: str
    right: ICanReturnAny

    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "left": self.left.toDict(),
            "operator": self.operator,
            "right": self.right.toDict()
        }
    
    def evaluateBool(self, a_data: dict[str, Any]) -> bool:
        left: Any = self.left.evaluateAny(a_data)
        right: Any = self.right.evaluateAny(a_data)
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
    
    def evaluateAny(self, a_data: dict[str, Any]):
        return self.evaluateBool(a_data)

#region AST Related Nodes
@dataclass
class ASTPatternTestNode(CodeTestNode):
    nodeType: str
    pattern: ASTPattern

    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "node_type": self.nodeType,
            "pattern": self.pattern.toDict()
        }

@dataclass
class ASTWalkTestNode(CodeTestNode):
    nodeType: str
    test: ICanReturnBool

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

    def toDict(self) -> dict[str, str]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "criterion": self.criterion,
            "node_message": self.nodeMessage
        }

    def execute(self, a_data: dict[str, Any]) -> None:
        #print(a_data)
        eval(f"cast(\"Autograder\", a_data[\"autograder\"]).instanceData.report.postLog(\"{self.criterion}\", f\"{self.nodeMessage}\")")

@dataclass
class PostGradeModifierTestNode(IExecutable):
    criterion: str
    modifierType: ModifierType
    modifierValue: float
    maxValue: float
    passes: bool

    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "node_id": self.nodeID,
            "criterion": self.criterion,
            "modifier_type": str(self.modifierType),
            "modifier_value": self.modifierValue,
            "max_value": self.maxValue,
            "passes": self.passes
        }

    def execute(self, a_data: dict[str, Any]) -> None:
        #print(a_data)
        cast("Autograder", a_data["autograder"]).instanceData.report.addModifier(AutograderModifier(self.criterion, self.modifierType, self.modifierValue, self.maxValue, self.passes))

@dataclass
class BlockTestNode(IExecutable):
    nodes: list[IExecutable]

    def toDict(self) -> dict[str, Any]:
        return {
            "node_id": self.nodeID,
            "nodes": [node.toDict() for node in self.nodes]
        }
    
    def execute(self, a_data: dict[str, Any]) -> None:
        for node in self.nodes:
            node.execute(a_data)
#endregion

@dataclass
class CodeTest:
    TestTypes: ClassVar[dict[str, Callable[[dict[str, CodeTestNode], "Autograder"], tuple[float, bool]]]] = {}
    type: str
    arguments: dict[str, CodeTestNode]
    found: CodeTestNode|None    = None
    notFound: CodeTestNode|None = None

    @classmethod
    def fromDict(cls, a_data: dict[str, Any]) -> Self:
        """Load a code test from a dict.
        """
        return cls(
            a_data["type"],
            {key: parseCodeTestNode(argument) for key, argument in cast(dict[str, dict[str, Any]], a_data.get("arguments", {})).items()},
            parseCodeTestNode(a_data["found"]) if "found" in a_data else None,
            parseCodeTestNode(a_data["notFound"]) if "notFound" in a_data else None
        )
    
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "type": self.type,
            "arguments": {key: node.toDict() for key, node in self.arguments.items()}
        }
    
    @classmethod
    def registerTestType(cls, a_id: str, a_testFunction: Callable[[dict[str, CodeTestNode], "Autograder"], tuple[float, bool]]) -> None:
        CodeTest.TestTypes[a_id] = a_testFunction
    
    def runTest(self, a_grader: "Autograder", a_data: dict[str, Any]) -> tuple[float, bool]:
        factor, success = CodeTest.TestTypes[self.type](self.arguments, a_grader)
        a_data["factor"]  = factor
        a_data["success"] = success
        if success:
            if self.found:
                executeCodeTestNode(cast(IExecutable, self.found), a_data)
        elif self.notFound:
            executeCodeTestNode(cast(IExecutable, self.notFound), a_data)
        del a_data["factor"]
        del a_data["success"]
        return factor, success

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
            return BlockTestNode(nodeID, [cast(IExecutable, parseCodeTestNode(node)) for node in nodes if isinstance(parseCodeTestNode(node), IExecutable)])
        case {"node_id": nodeID, "criterion": criterion, "node_message": nodeMessage} if nodeID == "post_message":
            return PostMessageTestNode(nodeID, criterion, nodeMessage)
        case {"node_id": nodeID, "nodes": nodes} if nodeID == "dictionary" and isinstance(nodes, dict):
            return DictionaryTestNode(nodeID, {key: parseCodeTestNode(node) for key, node in nodes.items()})
        case {"node_id": nodeID, "left": left, "operator": operator, "right": right} if nodeID == "comparison":
            leftParsed:  CodeTestNode|ICanReturnAny = parseCodeTestNode(left)
            rightParsed: CodeTestNode|ICanReturnAny = parseCodeTestNode(right)
            if isinstance(leftParsed, ICanReturnAny) and isinstance(rightParsed, ICanReturnAny):
                return ComparisonTestNode(nodeID, leftParsed, operator, rightParsed)
        case {"node_id": nodeID, "node_type": nodeType, "test": test} if nodeID == "ast_walk":
            testParsed: CodeTestNode|ICanReturnBool = parseCodeTestNode(test)
            if isinstance(testParsed, ICanReturnBool):
                return ASTWalkTestNode(nodeID, nodeType, testParsed)
        case {"node_id": nodeID, "project_name": projectName, "project_entrypoint": projectEntrypoint, "project_arguments": projectArguments, "project_inputs": projectInputs} if nodeID == "project":
            parsed: CodeTestNode|DictionaryTestNode = parseCodeTestNode(projectArguments)
            if isinstance(parsed, DictionaryTestNode):
                return ProjectTestNode(nodeID, projectName, projectEntrypoint, parsed, projectInputs)
        case {"node_id": nodeID, "node_type": nodeType, "pattern": pattern} if nodeID == "ast_pattern":
            return ASTPatternTestNode(nodeID, nodeType, ASTPattern.fromDict(pattern))
        case {"node_id": nodeID, "criterion": criterion, "modifier_type": modifierType, "modifier_value": modifierValue, "max_value": maxValue, "passes": passes} if nodeID == "post_grade_modifier":
            #print(f"{nodeID}:{criterion}:{modifierType}|{ModifierType(modifierType)}:{modifierValue}:{maxValue}:{passes}")
            return PostGradeModifierTestNode(nodeID, criterion, ModifierType(modifierType), modifierValue, maxValue, passes)
    return InvalidTestNode("invalid", a_node)

def evaluateCodeTestNode(a_node: ICanReturnAny, a_data: dict[str, Any]) -> Any:
    return a_node.evaluateAny(a_data)
        
def executeCodeTestNode(a_node: IExecutable, a_data: dict[str, Any]) -> None:
    a_node.execute(a_data)