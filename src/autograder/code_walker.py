import ast
import re
from ast import NodeVisitor, While, Constant, Compare, expr, Call, UnaryOp, Not, Gt, GtE, Lt, LtE, Eq, NotEq, FunctionDef, ImportFrom, Name, Load, Set, Del, AST, Add, alias, And, AnnAssign, arg, arguments, Assert, Assign, AsyncFor, AsyncFunctionDef, AsyncWith, Attribute, AugAssign, Await, BinOp, BitAnd, BitOr, BitXor, BoolOp, boolop, Break, ClassDef, cmpop, comprehension, Continue, Delete, Dict, DictComp, Div, ExceptHandler, excepthandler, Expr, expr_context, Expression, FloorDiv, For, FormattedValue, FunctionType, GeneratorExp, Global, If, IfExp, Import, In, Interactive, Invert, Is, IsNot, JoinedStr, keyword, Lambda, List, ListComp, LShift, Match, match_case, MatchAs, MatchClass, MatchMapping, MatchOr, MatchSequence, MatchSingleton, MatchStar, MatchValue, MatMult, Mod, mod, Module, Mult, NamedExpr, NodeTransformer, Nonlocal, NotIn, operator, Or, ParamSpec, Pass, pattern, Pow, Raise, Return, RShift, SetComp, Slice, Starred, stmt, Store, Sub, Subscript, Try, TryStar, Tuple, type_ignore, type_param, TypeAlias, TypeIgnore, TypeVar, TypeVarTuple, UAdd, unaryop, USub, With, withitem, Yield, YieldFrom, iter_fields
from typing import Any, cast, TYPE_CHECKING, Self, Optional
from enum import StrEnum, auto
from dataclasses import dataclass

if TYPE_CHECKING:
    from project_settings import ProjectSettings
    from project.project import Project

class ASTNodeType(StrEnum):
    WHILE                    = auto()
    CONSTANT                 = auto()
    COMPARE                  = auto()
    CALL                     = auto()
    UNARY_OP                 = auto()
    NOT                      = auto()
    GREATER_THAN             = auto()
    GREATER_THAN_OR_EQUAL_TO = auto()
    LESS_THAN                = auto()
    LESS_THAN_OR_EQUAL_TO    = auto()
    EQUAL                    = auto()
    NOT_EQUAL                = auto()
    FUNCTION_DEF             = auto()
    IMPORT                   = auto()
    IMPORT_FROM              = auto()
    NAME                     = auto()
    LOAD                     = auto()
    SET                      = auto()
    DEL                      = auto()
    ADD                      = auto()
    ALIAS                    = auto()
    AND                      = auto()
    ANN_ASSIGN               = auto()
    ARG                      = auto()
    ARGUMENTS                = auto()
    ASSERT                   = auto()
    ASSIGN                   = auto()
    ASYNC_FOR                = auto()
    ASYNC_FUNCTION_DEF       = auto()
    ASYNC_WITH               = auto()
    ATTRIBUTE                = auto()
    AUG_ASSIGN               = auto()
    AWAIT                    = auto()
    BIN_OP                   = auto()
    BIT_AND                  = auto()
    BIT_OR                   = auto()
    BIT_XOR                  = auto()
    BOOL_OP                  = auto()
    BREAK                    = auto()
    CLASS_DEF                = auto()
    CMPOP                    = auto()
    COMPREHENSION            = auto()
    CONTINUE                 = auto()
    DELETE                   = auto()
    DICT                     = auto()
    DICT_COMP                = auto()
    DIV                      = auto()
    EXCEPT_HANDLER           = auto() # ExceptHandler
    EXPR                     = auto()
    EXPR_CONTEXT             = auto()
    EXPRESSION               = auto()
    FLOOR_DIV                = auto()
    FOR                      = auto()
    FORMATTED_VALUE          = auto()
    FUNCTION_TYPE            = auto()
    GENERATOR_EXP            = auto()
    GLOBAL                   = auto()
    IF                       = auto()
    IF_EXP                   = auto()
    IN                       = auto()
    INTERACTIVE              = auto()
    INVERT                   = auto()
    IS                       = auto()
    IS_NOT                   = auto()
    JOINED_STR               = auto()
    KEYWORD                  = auto()
    LAMBDA                   = auto()
    LIST                     = auto()
    LIST_COMP                = auto()
    L_SHIFT                  = auto()
    MATCH                    = auto()
    MATCH_CASE               = auto()
    MATCH_AS                 = auto()
    MATCH_CLASS              = auto()
    MATCH_MAPPING            = auto()
    MATCH_OR                 = auto()
    MATCH_SEQUENCE           = auto()
    MATCH_SINGLETON          = auto()
    MATCH_STAR               = auto()
    MATCH_VALUE              = auto()
    MAT_MULT                 = auto()
    MOD                      = auto() # Mod
    MODULE                   = auto()
    MULT                     = auto()
    NAMED_EXPR               = auto()
    NONLOCAL                 = auto()
    NOT_IN                   = auto()
    OPERATOR                 = auto()
    OR                       = auto()
    PARAM_SPEC               = auto()
    PASS                     = auto()
    PATTERN                  = auto()
    POW                      = auto()
    RAISE                    = auto()
    RETURN                   = auto()
    R_SHIFT                  = auto()
    SET_COMP                 = auto()
    SLICE                    = auto()
    STARRED                  = auto()
    STMT                     = auto()
    STORE                    = auto()
    SUB                      = auto()
    SUBSCRIPT                = auto()
    TRY                      = auto()
    TRY_STAR                 = auto()
    TUPLE                    = auto()
    TYPE_PARAM               = auto()
    TYPE_ALIAS               = auto()
    TYPE_IGNORE              = auto() # TypeIgnore
    TYPE_VAR                 = auto()
    TYPE_VAR_TUPLE           = auto()
    U_ADD                    = auto()
    UNARY_OPERATOR           = auto() # unaryop
    U_SUB                    = auto()
    WITH                     = auto()
    WITH_ITEM                = auto()
    YIELD                    = auto()
    YIELD_FROM               = auto()
    ERROR                    = auto()
    

def isTrue(a_node: expr, a_default: bool = False) -> bool:
    """Check if an expression is true, with a default.

    Args:
        a_node (expr): The expression to parse for being true.
        a_default (bool): The default value if a_node fails to parse.

    Returns:
        (bool): ...
    """
    try:
        if isinstance(a_node, UnaryOp) and isinstance(a_node.op, Not):
            return not isTrue(a_node.operand, a_default)
        else:
            return ast.literal_eval(a_node)
    except ValueError as e:
        print(e)
    return a_default

class ASTPattern:
    def __init__(self, a_nodeType: str|ASTNodeType, a_comparisonData: dict[str, Any]|None = None) -> None:
        """
        Args:
            a_nodeType (str|ASTNodeType): The node type of the ASTPattern, either in string form, or a ASTNodeType enum.
            a_comparisonData (dict[str, Any]|None): The comparison data for the ASTPattern to use, if none then an empty dictionary.
        """
        self.nodeType: ASTNodeType = ASTNodeType(a_nodeType) if isinstance(a_nodeType, str) else a_nodeType
        self.comparisonData: dict[str, Any] = {} if a_comparisonData is None else a_comparisonData
    
    @classmethod
    def fromDict(cls, a_data: dict[str, Any]) -> "ASTPattern":
        """Load an ASTPattern from a serialized dictionary.

        Args:
            a_data (dict[str, Any]): A dictionary contianing the serialized ASTPattern information.

        Returns:
            (ASTPattern): The new ASTPattern instance.
        """
        #print(a_data)
        astTo: ASTPattern = ASTPattern(ASTNodeType(a_data["node_type"]), {})
        match astTo.nodeType:
            case ASTNodeType.WHILE:
                if "match_kind" in a_data:
                    astTo.comparisonData["match_kind"] = a_data["match_kind"]
                    match a_data["match_kind"]:
                        case "test_pattern":
                            astTo.comparisonData["test_pattern"] = ASTPattern.fromDict(a_data["test_pattern"])
                        case "test_patterns":
                            astTo.comparisonData["test_patterns"] = [ASTPattern.fromDict(testPattern) for testPattern in a_data["test_patterns"]]
            case ASTNodeType.IF_EXP:
                match (matchKind := (matchData := a_data.get("test_match", {"match_kind": "none"}))["match_kind"]):
                    case "test_pattern":
                        astTo.comparisonData["test_match"] = {"match_kind": matchKind, "test_pattern": ASTPattern.fromDict(matchData["test_pattern"])}
                    case "test_patterns":
                        astTo.comparisonData["test_match"] = {"match_kind": matchKind, "test_patterns": [ASTPattern.fromDict(testPattern) for testPattern in matchData["test_patterns"]]}
                    case _:
                        astTo.comparisonData["test_match"] = {"match_kind": matchKind}
                match (matchKind := (matchData := a_data.get("body_match", {"match_kind": "none"}))["match_kind"]):
                    case "test_pattern":
                        astTo.comparisonData["body_match"] = {"match_kind": matchKind, "test_pattern": ASTPattern.fromDict(matchData["test_pattern"])}
                    case "test_patterns":
                        astTo.comparisonData["body_match"] = {"match_kind": matchKind, "test_patterns": [ASTPattern.fromDict(testPattern) for testPattern in matchData["test_patterns"]]}
                    case _:
                        astTo.comparisonData["body_match"] = {"match_kind": matchKind}
                match (matchKind := (matchData := a_data.get("orelse_match", {"match_kind": "none"}))["match_kind"]):
                    case "test_pattern":
                        astTo.comparisonData["orelse_match"] = {"match_kind": matchKind, "test_pattern": ASTPattern.fromDict(matchData["test_pattern"])}
                    case "test_patterns":
                        astTo.comparisonData["orelse_match"] = {"match_kind": matchKind, "test_patterns": [ASTPattern.fromDict(testPattern) for testPattern in matchData["test_patterns"]]}
                    case _:
                        astTo.comparisonData["orelse_match"] = {"match_kind": matchKind}
            case ASTNodeType.CONSTANT:
                if "match_kind" in a_data:
                    astTo.comparisonData["match_kind"] = a_data["match_kind"]
                    match a_data["match_kind"]:
                        case "regex":
                            astTo.comparisonData["kind_match"] = a_data.get("kind_match", ".*")
                            astTo.comparisonData["value_match"] = a_data.get("value_match", ".*")
                        case "is_true":
                            astTo.comparisonData["default_val"] = a_data.get("default_val", False)
                            astTo.comparisonData["value"] = a_data.get("value", True)
            case ASTNodeType.NAME:
                astTo.comparisonData["name"] = a_data.get("name", ".*")
                if "context" in a_data:
                    astTo.comparisonData["context"] = ASTPattern.fromDict(a_data["context"])
            case ASTNodeType.ASSIGN:
                if "match_kind" in a_data:
                    astTo.comparisonData["match_kind"] = a_data["match_kind"]
                    match a_data["match_kind"]:
                        case "target_pattern":
                            astTo.comparisonData["target_pattern"] = ASTPattern.fromDict(a_data["target_pattern"])
            case ASTNodeType.CALL:
                ...
            case ASTNodeType.UNARY_OP:
                ...
            case ASTNodeType.ARG:
                astTo.comparisonData["name"] = a_data.get("name", ".*")
        
        return astTo

    def toDict(self) -> dict[str, Any]:
        """Convert to a dictionary.

        Returns:
            (dict[str, Any]): ...
        """
        return {
            "a": 1
        }

class ASTWalker(NodeVisitor):
    def __init__(self, a_pattern: ASTPattern):
        self.pattern: ASTPattern = a_pattern
    
    def generic_visit(self, node: AST) -> int:
        collection: int = self.visiting(node, self.pattern)
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        collection += self.visit(item)
            elif isinstance(value, AST):
                collection += self.visit(value)
        return collection
    
    def visiting(self, a_node: AST, a_pattern: ASTPattern) -> int:
        """Function to handle visiting a node.

        Args:
            a_node (AST): The node to test the pattern against.
            a_pattern (ASTPattern): The pattern to evaluate.
        
        Returns:
            (int): The number of proper occurences matching the node.
        """
        match a_pattern.nodeType:
            case ASTNodeType.WHILE:
                if isinstance(a_node, While):
                    if "match_kind" in a_pattern.comparisonData:
                        match a_pattern.comparisonData["match_kind"]:
                            case "test_pattern":
                                return self.visiting(a_node.test, a_pattern.comparisonData["test_pattern"])
                            case "test_patterns":
                                return 1 if any([0 < self.visiting(a_node.test, testPattern) for testPattern in a_pattern.comparisonData["test_patterns"]]) else 0
                    return 1
            case ASTNodeType.CONSTANT:
                if isinstance(a_node, Constant):
                    if "match_kind" in a_pattern.comparisonData:
                        match a_pattern.comparisonData["match_kind"]:
                            case "regex":
                                return 1 if re.search(cast(str, a_pattern.comparisonData["kind_match"]), str(a_node.kind)) and re.search(a_pattern.comparisonData["value_match"], str(a_node.value)) else 0
                            case "is_true":
                                return 1 if isTrue(a_node, a_pattern.comparisonData["default_val"]) == a_pattern.comparisonData["value"] else 0
                    return 1
            case ASTNodeType.COMPARE:
                if isinstance(a_node, Compare):
                    
                    return 1
            case ASTNodeType.CALL:
                if isinstance(a_node, Call):
                    a_node.func
                    a_node.keywords
                    a_node.args
                    return 1
            case ASTNodeType.UNARY_OP:
                if isinstance(a_node, UnaryOp):
                    
                    a_node.op
                    a_node.operand
                    return 1
            case ASTNodeType.NOT:
                if isinstance(a_node, Not):
                    return 1
            case ASTNodeType.GREATER_THAN:
                if isinstance(a_node, Gt):
                    return 1
            case ASTNodeType.GREATER_THAN_OR_EQUAL_TO:
                if isinstance(a_node, GtE):
                    return 1
            case ASTNodeType.LESS_THAN:
                if isinstance(a_node, Lt):
                    return 1
            case ASTNodeType.LESS_THAN_OR_EQUAL_TO:
                if isinstance(a_node, LtE):
                    return 1
            case ASTNodeType.EQUAL:
                if isinstance(a_node, Eq):
                    return 1
            case ASTNodeType.NOT_EQUAL:
                if isinstance(a_node, NotEq):
                    return 1
            case ASTNodeType.FUNCTION_DEF:
                if isinstance(a_node, FunctionDef):
                    return 1
            case ASTNodeType.IMPORT:
                if isinstance(a_node, Import):
                    a = Import()

                    for aliass in a.names:
                        aliass.name
                    return 1
            case ASTNodeType.IMPORT_FROM:
                if isinstance(a_node, ImportFrom):
                    return 1
            case ASTNodeType.NAME:
                if isinstance(a_node, Name):
                    if "context" in a_pattern.comparisonData and self.visiting(a_node.ctx, a_pattern.comparisonData["context"]) == 0:
                        return 0
                    return 1 if re.search(a_pattern.comparisonData["name"], a_node.id) else 0
            case ASTNodeType.LOAD:
                if isinstance(a_node, Load):
                    return 1
            case ASTNodeType.SET:
                if isinstance(a_node, Set):
                    return 1
            case ASTNodeType.DEL:
                if isinstance(a_node, Del):
                    return 1
            case ASTNodeType.ADD:
                if isinstance(a_node, Add):
                    return 1
            case ASTNodeType.ALIAS:
                if isinstance(a_node, alias):
                    return 1 if (re.search(a_pattern.comparisonData["alias_name"], cast(str, a_node.asname)) and re.search(a_pattern.comparisonData["imported_module"], a_node.name)) else 0
            case ASTNodeType.AND:
                if isinstance(a_node, And):
                    return 1
            case ASTNodeType.ANN_ASSIGN:
                if isinstance(a_node, AnnAssign):
                    a_node.annotation
                    a_node.simple
                    a_node.target
                    a_node.value
                    return 1
            case ASTNodeType.ARG:
                if isinstance(a_node, arg):
                    return 1 if re.search(a_pattern.comparisonData["name"], a_node.arg) else 0
            case ASTNodeType.ARGUMENTS:
                if isinstance(a_node, arguments):
                    a_node.args
                    a_node.defaults
                    a_node.kw_defaults
                    a_node.kwarg
                    a_node.kwonlyargs
                    a_node.posonlyargs
                    a_node.vararg
                    return 1
            case ASTNodeType.ASSERT:
                if isinstance(a_node, Assert):
                    a_node.msg
                    a_node.test
                    return 1
            case ASTNodeType.ASSIGN:
                if isinstance(a_node, Assign):
                    if "match_kind" in a_pattern.comparisonData:
                        match a_pattern.comparisonData["match_kind"]:
                            case "target_pattern":
                                return self.visiting(a_node.targets[0], a_pattern.comparisonData["target_pattern"])
                    else:
                        return 1
            case ASTNodeType.ASYNC_FOR:
                ...
            case ASTNodeType.ASYNC_FUNCTION_DEF:
                ...
            case ASTNodeType.ASYNC_WITH:
                ...
            case ASTNodeType.ATTRIBUTE:
                ...
            case ASTNodeType.AUG_ASSIGN:
                ...
            case ASTNodeType.AWAIT:
                ...
            case ASTNodeType.BIN_OP:
                ...
            case ASTNodeType.BIT_AND:
                ...
            case ASTNodeType.BIT_OR:
                ...
            case ASTNodeType.BIT_XOR:
                ...
            case ASTNodeType.BOOL_OP:
                ...
            case ASTNodeType.BREAK:
                if isinstance(a_node, Break):
                    return 1
            case ASTNodeType.CLASS_DEF:
                ...
            case ASTNodeType.CMPOP:
                if isinstance(a_node, cmpop):
                    return 1
            case ASTNodeType.COMPREHENSION:
                if isinstance(a_node, comprehension):
                    a_node.ifs
                    a_node.is_async
                    a_node.iter
                    a_node.target
                    return 1
            case ASTNodeType.CONTINUE:
                if isinstance(a_node, Continue):
                    return 1
            case ASTNodeType.DELETE:
                if isinstance(a_node, Delete):
                    return 1
            case ASTNodeType.DICT:
                if isinstance(a_node, Dict):
                    a_node.keys
                    a_node.values
                    return 1
            case ASTNodeType.DICT_COMP:
                if isinstance(a_node, DictComp):
                    a_node.generators
                    a_node.key
                    a_node.value
                    return 1
            case ASTNodeType.DIV:
                if isinstance(a_node, Div):
                    return 1
            case ASTNodeType.EXCEPT_HANDLER:
                if isinstance(a_node, ExceptHandler):
                    a_node.body
                    a_node.name
                    a_node.type
                    return 1
            case ASTNodeType.EXPR:
                ...
            case ASTNodeType.EXPR_CONTEXT:
                ...
            case ASTNodeType.EXPRESSION:
                if isinstance(a_node, Expression):
                    a_node.body
                    return 1
            case ASTNodeType.FLOOR_DIV:
                if isinstance(a_node, FloorDiv):
                    return 1
            case ASTNodeType.FOR:
                ...
            case ASTNodeType.FORMATTED_VALUE:
                ...
            case ASTNodeType.FUNCTION_TYPE:
                ...
            case ASTNodeType.GENERATOR_EXP:
                ...
            case ASTNodeType.GLOBAL:
                ...
            case ASTNodeType.IF:
                if isinstance(a_node, If):
                    if "match_kind" in a_pattern.comparisonData:
                        match a_pattern.comparisonData["match_kind"]:
                            case "test_pattern":
                                return self.visiting(a_node.test, a_pattern.comparisonData["test_pattern"])
                            case "test_patterns":
                                return 1 if any([0 < self.visiting(a_node.test, testPattern) for testPattern in a_pattern.comparisonData["test_patterns"]]) else 0
                    for statement in a_node.body:
                        ...
                    for statement in a_node.orelse:
                        ...
                    return 1
            case ASTNodeType.IF_EXP:
                if isinstance(a_node, IfExp):
                    match a_pattern.comparisonData["test_match"]["match_kind"]:
                        case "test_pattern":
                            if self.visiting(a_node.test, a_pattern.comparisonData["test_match"]["test_pattern"]) == 0:
                                return 0
                        case "test_patterns":
                            if all([0 == self.visiting(a_node.test, testPattern) for testPattern in a_pattern.comparisonData["test_match"]["test_patterns"]]):
                                return 0
                    match a_pattern.comparisonData.get("body_match", {"match_kind": "none"})["match_kind"]:
                        case "test_pattern":
                            if self.visiting(a_node.body, a_pattern.comparisonData["body_match"]["test_pattern"]) == 0:
                                return 0
                        case "test_patterns":
                            if all([0 == self.visiting(a_node.body, testPattern) for testPattern in a_pattern.comparisonData["body_match"]["test_patterns"]]):
                                return 0
                    match a_pattern.comparisonData.get("orelse_match", {"match_kind": "none"})["match_kind"]:
                        case "test_pattern":
                            if self.visiting(a_node.orelse, a_pattern.comparisonData["orelse_match"]["test_pattern"]) == 0:
                                return 0
                        case "test_patterns":
                            if all([0 == self.visiting(a_node.orelse, testPattern) for testPattern in a_pattern.comparisonData["orelse_match"]["test_patterns"]]):
                                return 0
                    return 1
            case ASTNodeType.IN:
                if isinstance(a_node, In):
                    return 1
            case ASTNodeType.INTERACTIVE:
                if isinstance(a_node, Interactive):
                    a_node.body
                    return 1
            case ASTNodeType.INVERT:
                if isinstance(a_node, Invert):
                    return 1
            case ASTNodeType.IS:
                if isinstance(a_node, Is):
                    return 1
            case ASTNodeType.IS_NOT:
                if isinstance(a_node, IsNot):
                    return 1
            case ASTNodeType.JOINED_STR:
                if isinstance(a_node, JoinedStr):
                    return 1
            case ASTNodeType.KEYWORD:
                if isinstance(a_node, keyword):
                    a_node.arg
                    a_node.value
                    return 1
            case ASTNodeType.LAMBDA:
                if isinstance(a_node, Lambda):
                    a_node.args
                    a_node.body
                    return 1
            case ASTNodeType.LIST:
                if isinstance(a_node, List):
                    a_node.ctx
                    a_node.elts
                    return 1
            case ASTNodeType.LIST_COMP:
                if isinstance(a_node, ListComp):
                    a_node.elt
                    a_node.generators
                    return 1
            case ASTNodeType.L_SHIFT:
                if isinstance(a_node, LShift):
                    return 1
            case ASTNodeType.MATCH:
                ...
            case ASTNodeType.MATCH_CASE:
                ...
            case ASTNodeType.MATCH_AS:
                ...
            case ASTNodeType.MATCH_CLASS:
                ...
            case ASTNodeType.MATCH_MAPPING:
                ...
            case ASTNodeType.MATCH_OR:
                ...
            case ASTNodeType.MATCH_SEQUENCE:
                ...
            case ASTNodeType.MATCH_SINGLETON:
                ...
            case ASTNodeType.MATCH_STAR:
                ...
            case ASTNodeType.MATCH_VALUE:
                ...
            case ASTNodeType.MAT_MULT:
                if isinstance(a_node, MatMult):
                    return 1
            case ASTNodeType.MOD:
                if isinstance(a_node, Mod):
                    return 1
            case ASTNodeType.MODULE:
                if isinstance(a_node, Module):
                    a_node.body
                    a_node.type_ignores
                    return 1
            case ASTNodeType.MULT:
                if isinstance(a_node, Mult):
                    return 1
            case ASTNodeType.NAMED_EXPR:
                ...
            case ASTNodeType.NONLOCAL:
                ...
            case ASTNodeType.NOT_IN:
                if isinstance(a_node, NotIn):
                    return 1
            case ASTNodeType.OPERATOR:
                if isinstance(a_node, operator):
                    return 1
            case ASTNodeType.OR:
                if isinstance(a_node, Or):
                    return 1
            case ASTNodeType.PARAM_SPEC:
                if isinstance(a_node, ParamSpec):
                    a_node.name
                    return 1
            case ASTNodeType.PASS:
                if isinstance(a_node, Pass):
                    return 1
            case ASTNodeType.PATTERN:
                if isinstance(a_node, pattern):
                    return 1
            case ASTNodeType.POW:
                if isinstance(a_node, Pow):
                    return 1
            case ASTNodeType.RAISE:
                if isinstance(a_node, Raise):
                    a_node.cause
                    a_node.exc
                    return 1
            case ASTNodeType.RETURN:
                if isinstance(a_node, Return):
                    a_node.value
                    return 1
            case ASTNodeType.R_SHIFT:
                if isinstance(a_node, RShift):
                    return 1
            case ASTNodeType.SET_COMP:
                ...
            case ASTNodeType.SLICE:
                ...
            case ASTNodeType.STARRED:
                ...
            case ASTNodeType.STMT:
                if isinstance(a_node, stmt):
                    return 1
            case ASTNodeType.STORE:
                if isinstance(a_node, Store):
                    return 1
            case ASTNodeType.SUB:
                if isinstance(a_node, Sub):
                    return 1
            case ASTNodeType.SUBSCRIPT:
                if isinstance(a_node, Subscript):
                    a_node.ctx
                    a_node.slice
                    a_node.value
                    return 1
            case ASTNodeType.TRY:
                ...
            case ASTNodeType.TRY_STAR:
                ...
            case ASTNodeType.TUPLE:
                ...
            case ASTNodeType.TYPE_PARAM:
                ...
            case ASTNodeType.TYPE_ALIAS:
                ...
            case ASTNodeType.TYPE_IGNORE:
                ...
            case ASTNodeType.TYPE_VAR:
                ...
            case ASTNodeType.TYPE_VAR_TUPLE:
                ...
            case ASTNodeType.U_ADD:
                ...
            case ASTNodeType.UNARY_OPERATOR:
                ...
            case ASTNodeType.U_SUB:
                ...
            case ASTNodeType.WITH:
                if isinstance(a_node, With):
                    a_node.body
                    a_node.items
                    a_node.type_comment
                    return 1
            case ASTNodeType.WITH_ITEM:
                if isinstance(a_node, withitem):
                    a_node.context_expr
                    a_node.optional_vars
                    return 1
            case ASTNodeType.YIELD:
                if isinstance(a_node, Yield):
                    a_node.value
                    return 1
            case ASTNodeType.YIELD_FROM:
                if isinstance(a_node, YieldFrom):
                    a_node.value
                    return 1
        return 0

@dataclass
class ImportData:
    local: bool
    name: str

class CodeWalker(NodeVisitor):
    def __init__(self, a_project: "Project", a_projectSettings: "ProjectSettings") -> None:
        self.project: "Project" = a_project
        self.filenames: list[str] = [file.name for file in a_project.files]
        self.projectSettings: "ProjectSettings" = a_projectSettings
        self.imports: set[ImportData] = set()
    
    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        return
    
    def visit_Import(self, node: Import) -> Any:
        self.imports.update([ImportData(name.name in self.filenames, name.name) for name in node.names])

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
        self.imports.update([ImportData(name.name in self.filenames, name.name) for name in node.names])
    
    def visit_While(self, node: While) -> Any:
        print(ast.dump(node.test, include_attributes=True, indent=2))
        
        return

def parseExpression(a_node: expr) -> Any:
    """Parse an expression.
    """
    if isinstance(a_node, Constant):
        return ast.literal_eval(a_node)

def isExpressionTrue(a_node: expr) -> bool:
    """Check if an expression is true.
    """
    if isinstance(a_node, Constant):
        return ast.literal_eval(a_node)
    elif isinstance(a_node, Compare):
        left = parseExpression(a_node)
        right = parseExpression(a_node.comparators[0])
        if left == None or right == None:
            return False
        if isinstance(a_node.ops[0], Gt):
            return left > right
        elif isinstance(a_node.ops[0], GtE):
            return left >= right
        elif isinstance(a_node.ops[0], Lt):
            return left < right
        elif isinstance(a_node.ops[0], LtE):
            return left <= right
        elif isinstance(a_node.ops[0], Eq):
            return left == right
        elif isinstance(a_node.ops[0], NotEq):
            return left != right
    elif isinstance(a_node, UnaryOp):
        if isinstance(a_node.op, Not):
            return not isExpressionTrue(a_node.operand)
    return False