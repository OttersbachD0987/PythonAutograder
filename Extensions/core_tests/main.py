from __future__ import annotations

# fmt: off

from src.autograder.code_test import CodeTest, CodeTestNode, ProjectTestNode, LiteralTestNode, ASTPatternTestNode
from src.autograder.code_test_type import IParameterGroup, ParameterRepresentation
from subprocess import Popen, PIPE
from typing import TYPE_CHECKING, cast
from src.autograder.code_walker import ASTWalker
import re
import difflib

if TYPE_CHECKING:
    from src.autograder.autograder_application import Autograder
    from src.project.python_file import PythonFile

VALID_COMPARE_MATCHES: set[str] = {"Match", "Diff", "No Match", "Ignore"}

def compareOutput(a_arguments: dict[str, CodeTestNode], a_app: Autograder) -> tuple[float, bool]:
    """
    """
    grade: float = 0
    
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
        #print(f"{a_arguments["stdout"]} : {isinstance(node := a_arguments["stdout"], LiteralTestNode)} : {node.literalType} : {(value := node.literalValue)} : {value in VALID_COMPARE_MATCHES}")

        match (value if (isinstance(node := a_arguments["stdout"], LiteralTestNode) and node.literalType == "string" and ((value := node.literalValue) in VALID_COMPARE_MATCHES)) else "Match"):
            case "Ignore":
                grade += 1
            case "Match"    if stdoutBase == stdoutTest:
                grade += 1
            case "Diff":
                grade += difflib.SequenceMatcher(None, stdoutBase, stdoutTest).ratio()
            case "No Match" if stdoutBase != stdoutTest:
                grade += 1
            case _:
                ...

        match (value if (isinstance(node := a_arguments["stderr"], LiteralTestNode) and node.literalType == "string" and ((value := node.literalValue) in VALID_COMPARE_MATCHES)) else "Match"):
            case "Ignore":
                grade += 1
            case "Match"    if stderrBase == stderrTest:
                grade += 1
            case "Diff":
                grade += difflib.SequenceMatcher(None, stderrBase, stderrTest).ratio()
            case "No Match" if stderrBase != stderrTest:
                grade += 1
            case _:
                ...

        match (value if (isinstance(node := a_arguments["return_code"], LiteralTestNode) and node.literalType == "string" and ((value := node.literalValue) in VALID_COMPARE_MATCHES)) else "Match"):
            case "Ignore":
                grade += 1
            case "Match"    if subBase.returncode == subTest.returncode:
                grade += 1
            case "No Match" if subBase.returncode != subTest.returncode:
                grade += 1
            case _:
                ...
    
    return grade / 3.0, grade == 3

def compareOutputParameters() -> list[IParameterGroup]:
    return [
        cast(IParameterGroup, ParameterRepresentation("type", "string", {})),
        ProjectTestNode.parameterRepresentation("base_project"),
        ProjectTestNode.parameterRepresentation("test_project"),
        cast(IParameterGroup, ParameterRepresentation("stdout", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("stderr", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("return_code", "string", {}))
    ]

def assertOutput(a_arguments: dict[str, CodeTestNode], a_app: Autograder) -> tuple[float, bool]:
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
        cast(IParameterGroup, ParameterRepresentation("type", "string", {})),
        ProjectTestNode.parameterRepresentation("test_project"),
        cast(IParameterGroup, ParameterRepresentation("stdout", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("stderr", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("return_code", "string", {}))
    ]

VALID_FILE_MATCHES: set[str] = {"Match", "Diff", "No Match"}

def compareFiles(a_arguments: dict[str, CodeTestNode], a_app: Autograder) -> tuple[float, bool]:
    grade: float = 0
    
    if isinstance(baseProject := a_arguments["base_project"], ProjectTestNode) and isinstance(testProject := a_arguments["test_project"], ProjectTestNode) and (isinstance(baseFile := a_arguments["base_file"], LiteralTestNode) and baseFile.literalType == "string") and (isinstance(testFile := a_arguments["test_file"], LiteralTestNode) and testFile.literalType == "string"):
        baseContents: str = ""
        with open(f"{a_app.instanceData.projects[baseProject.projectName].dir}\\{baseFile.literalValue}") as file:
            baseContents = file.read()
            
        testContents: str = ""
        with open(f"{a_app.instanceData.projects[testProject.projectName].dir}\\{testFile.literalValue}") as file:
            testContents = file.read()
        
        match (value if (isinstance(node := a_arguments["match"], LiteralTestNode) and node.literalType == "string" and ((value := node.literalValue) in VALID_FILE_MATCHES)) else "Match"):
            case "Match"    if baseContents == testContents:
                grade += 1
            case "Diff":
                grade += difflib.SequenceMatcher(None, baseContents, testContents).ratio()
            case "No Match" if baseContents != testContents:
                grade += 1
            case _:
                ...
    
    return grade, grade == 1

def compareFilesParameters() -> list[IParameterGroup]:
    return [
        cast(IParameterGroup, ParameterRepresentation("type", "string", {})),
        ProjectTestNode.parameterRepresentation("base_project"),
        ProjectTestNode.parameterRepresentation("test_project"),
        cast(IParameterGroup, ParameterRepresentation("base_file", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("test_file", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("match", "string", {}))
    ]

def assertFile(a_arguments: dict[str, CodeTestNode], a_app: Autograder) -> tuple[float, bool]:
    """
    """
    grade: int = 0
    if isinstance(testProject := a_arguments["test_project"], ProjectTestNode) and (isinstance(testFile := a_arguments["test_file"], LiteralTestNode) and testFile.literalType == "string"):
        content: str = ""
        with open(f"{a_app.instanceData.projects[testProject.projectName].dir}\\{testFile.literalValue}") as file:
            content = file.read()

        if re.match(node.literalValue if isinstance(node := a_arguments["match"], LiteralTestNode) and node.literalType == "string" else ".*", content):
            grade += 1
        
    return grade, grade == 1

def assertFileParameters() -> list[IParameterGroup]:
    return [
        cast(IParameterGroup, ParameterRepresentation("type", "string", {})),
        ProjectTestNode.parameterRepresentation("test_project"),
        cast(IParameterGroup, ParameterRepresentation("test_file", "string", {})),
        cast(IParameterGroup, ParameterRepresentation("match", "string", {}))
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
CodeTest.registerTestType("compare_files", compareFiles, compareFilesParameters)
CodeTest.registerTestType("assert_file", assertFile, assertFileParameters)

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

