from src.autograder.code_test import CodeTest, CodeTestNode, ProjectTestNode, LiteralTestNode, ASTPatternTestNode
from src.autograder.code_test_type import IParameterGroup, ParameterRepresentation, OptionalParameter, ExclusiveParameters
from subprocess import Popen, PIPE
from typing import TYPE_CHECKING, cast
from src.autograder.code_walker import ASTWalker
import re
import difflib
from difflib import Match

if TYPE_CHECKING:
    from src.autograder.autograder_application import Autograder
    from src.project.python_file import PythonFile

def compareOutput(a_arguments: dict[str, CodeTestNode], a_app: "Autograder") -> tuple[float, bool]:
    """
    """
    grade: int = 0
    VALID_OUTPUTS: set[str] = {"Match", "No Match", "Ignore"}
    if isinstance(baseProject := a_arguments["base_project"], ProjectTestNode) and isinstance(testProject := a_arguments["test_project"], ProjectTestNode):
        subBase: Popen[str] = Popen(" ".join([
                "py", f"{(projectDir := a_app.instanceData.projects[baseProject.projectName].dir)}\\{baseProject.projectEntrypoint}", 
                *[f"\"{node.literalValue}\"" for node in baseProject.projectArguments.nodes.values() if isinstance(node, LiteralTestNode)]]), 
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            cwd=projectDir, 
            text=True)

        stdoutBase, stderrBase = subBase.communicate("\n".join(baseProject.projectInputs), timeout=10.0)

        subTest: Popen[str] = Popen(" ".join([
                "py", f"{(projectDir := a_app.instanceData.projects[testProject.projectName].dir)}\\{testProject.projectEntrypoint}", 
                *[f"\"{node.literalValue}\"" for node in testProject.projectArguments.nodes.values() if isinstance(node, LiteralTestNode)]]), 
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            cwd=projectDir, 
            text=True)

        stdoutTest, stderrTest = subTest.communicate("\n".join(testProject.projectInputs), timeout=10.0)

        match (value if (isinstance(node := a_arguments["stdout"], LiteralTestNode) and node.literalType == "string" and ((value := node.literalValue) in VALID_OUTPUTS)) else "Match"):
            case "Ignore":
                grade += 1
            case "Match"    if stdoutBase == stdoutTest:
                grade += 1
            case "No Match" if stdoutBase != stdoutTest:
                grade += 1

        match (value if (isinstance(node := a_arguments["stderr"], LiteralTestNode) and node.literalType == "string" and ((value := node.literalValue) in VALID_OUTPUTS)) else "Match"):
            case "Ignore":
                grade += 1
            case "Match"    if stderrBase == stderrTest:
                grade += 1
            case "No Match" if stderrBase != stderrTest:
                grade += 1

        match (value if (isinstance(node := a_arguments["return_code"], LiteralTestNode) and node.literalType == "string" and ((value := node.literalValue) in VALID_OUTPUTS)) else "Match"):
            case "Ignore":
                grade += 1
            case "Match"    if subBase.returncode == subTest.returncode:
                grade += 1
            case "No Match" if subBase.returncode != subTest.returncode:
                grade += 1
    
    return grade / 3.0, grade == 3

def compareOutputParameters() -> list[IParameterGroup]:
    return [
        cast(IParameterGroup, ParameterRepresentation("", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("", "string", {}))
    ]

def assertOutput(a_arguments: dict[str, CodeTestNode], a_app: "Autograder") -> tuple[float, bool]:
    """
    """
    grade: int = 0
    if isinstance(testProject := a_arguments["test_project"], ProjectTestNode):
        sub: Popen[str] = Popen(" ".join([
                "py", f"{(projectDir := a_app.instanceData.projects[testProject.projectName].dir)}\\{testProject.projectEntrypoint}", 
                *[f"\"{node.literalValue}\"" for node in testProject.projectArguments.nodes.values() if isinstance(node, LiteralTestNode)]]), 
            stdin=PIPE, 
            stdout=PIPE,
            stderr=PIPE,
            cwd=projectDir, 
            text=True)
        
        stdout, stderr = sub.communicate("\n".join(testProject.projectInputs), timeout=10.0)

        if re.match(node.literalValue if isinstance(node := a_arguments["stdout"], LiteralTestNode) and node.literalType == "string" else ".*", stdout.strip()):
            grade += 1
        if re.match(node.literalValue if isinstance(node := a_arguments["stderr"], LiteralTestNode) and node.literalType == "string" else ".*", stderr.strip()):
            grade += 1
        if re.match(node.literalValue if isinstance(node := a_arguments["return_code"], LiteralTestNode) and node.literalType == "string" else ".*", f"{sub.returncode}"):
            grade += 1
        
    return grade / 3.0, grade == 3

def assertOutputParameters() -> list[IParameterGroup]:
    return [
        cast(IParameterGroup, ParameterRepresentation("", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("", "string", {}))
    ]

#def walkAST(a_arguments: dict[str, CodeTestNode], a_app: "Autograder") -> tuple[float, bool]:
#    """
#    """
#    return ((amount := ASTWalker(testPattern.pattern).visit(cast("PythonFile", [file for file in a_app.instanceData.projects[testProject.projectName].files if file.name == testProject.projectEntrypoint][0]).ast)), amount > 0) if (isinstance(testProject := a_arguments["test_project"], ProjectTestNode) and isinstance(testPattern := a_arguments["pattern"], ASTPatternTestNode)) else (0, False)
    

CodeTest.registerTestType("compare_output", compareOutput, compareOutputParameters)
CodeTest.registerTestType("assert_output", assertOutput, assertOutputParameters)
CodeTest.registerTestType(
    "walk_ast", 
    lambda a_arguments, a_app: (((amount := ASTWalker(testPattern.pattern).visit(cast("PythonFile", [file for file in a_app.instanceData.projects[testProject.projectName].files if file.name == testProject.projectEntrypoint][0]).ast)), amount > 0) if (isinstance(testProject := a_arguments["test_project"], ProjectTestNode) and isinstance(testPattern := a_arguments["pattern"], ASTPatternTestNode)) else (0, False)), 
    lambda: [
        cast(IParameterGroup, ParameterRepresentation("", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("", "string", {}))
    ])

#region Outline
###
## Compare Output
# Baseline Project
# - Arguments
# - Inputs
# Test Project
# - Arguments
# - Inputs
# stdout
# * Match
# * Ignore
# stderr
# * Match
# * Ignore
# Return Code
# * Match
# * Ignore
# ?Found
# - Action
# ?Not Found
# - Action
###
## Assert Output
# Test Project
# - Arguments
# - Inputs
# stdout
# * Match (Regex)
# * Ignore
# stderr
# * Match (Regex)
# * Ignore
# Return Code
# * Match (Regex)
# * Ignore
# ?Found
# - Action
# ?Not Found
# - Action
###
## File Assert Output
# Test Project
# - Arguments
# - Inputs
# stdout
# * Match (File)
# * Ignore
# stderr
# * Match (File)
# * Ignore
# Return Code
# * Match (File)
# * Ignore
# ?Found
# - Action
# ?Not Found
# - Action
###
## Walk AST
# Test Project
# - Arguments
# - Inputs
# Patterns
# - Pattern Params
# ?Found
# - Action
# ?Not Found
# - Action
###

## Pattern
# Type
# Test
#endregion