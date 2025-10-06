from .code_test import CodeTest, CodeTestNode, ProjectTestNode, LiteralTestNode, executeCodeTestNode, ASTWalkTestNode, ASTPatternTestNode
from subprocess import Popen, PIPE
from typing import TYPE_CHECKING, cast
from re import Pattern
from .code_walker import ASTWalker
import re

if TYPE_CHECKING:
    from .autograder_application import Autograder
    from project.python_file import PythonFile

def compareOutput(a_arguments: dict[str, CodeTestNode], a_app: "Autograder") -> tuple[float, bool]:
    """
    """
    VALID_OUTPUTS: tuple[str, str, str] = ("Match", "No Match", "Ignore")
    baseProject:    ProjectTestNode|None = a_arguments["base_project"] if isinstance(a_arguments["base_project"], ProjectTestNode) else None
    testProject:    ProjectTestNode|None = a_arguments["test_project"] if isinstance(a_arguments["test_project"], ProjectTestNode) else None
    stdoutMode:     str = a_arguments["stdout"].literalValue      if isinstance(a_arguments["stdout"], LiteralTestNode)      and a_arguments["stdout"].literalType      == "string" and a_arguments["stdout"].literalValue      in VALID_OUTPUTS else "Match"
    stderrMode:     str = a_arguments["stderr"].literalValue      if isinstance(a_arguments["stderr"], LiteralTestNode)      and a_arguments["stderr"].literalType      == "string" and a_arguments["stderr"].literalValue      in VALID_OUTPUTS else "Match"
    returnCodeMode: str = a_arguments["return_code"].literalValue if isinstance(a_arguments["return_code"], LiteralTestNode) and a_arguments["return_code"].literalType == "string" and a_arguments["return_code"].literalValue in VALID_OUTPUTS else "Match"

    grade: int = 0

    if testProject is None or baseProject is None:
        return grade, False
    
    projectBase = a_app.instanceData.projects[baseProject.projectName]
    projectTest = a_app.instanceData.projects[testProject.projectName]

    subBase: Popen[str] = Popen(" ".join([
            "py", f"{projectBase.dir}\\{baseProject.projectEntrypoint}", 
            *[f"\"{node.literalValue}\"" for node in baseProject.projectArguments.nodes.values() if isinstance(node, LiteralTestNode)]]), 
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        cwd=projectBase.dir, 
        text=True)

    stdoutBase, stderrBase = subBase.communicate("\n".join(baseProject.projectInputs), timeout=10.0)
    
    subTest: Popen[str] = Popen(" ".join([
            "py", f"{projectTest.dir}\\{testProject.projectEntrypoint}", 
            *[f"\"{node.literalValue}\"" for node in testProject.projectArguments.nodes.values() if isinstance(node, LiteralTestNode)]]), 
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        cwd=projectTest.dir, 
        text=True)

    stdoutTest, stderrTest = subTest.communicate("\n".join(testProject.projectInputs), timeout=10.0)

    match stdoutMode:
        case "Ignore":
            grade += 1
        case "Match":
            #print(stdoutBase == stdoutTest)
            if stdoutBase == stdoutTest:
                grade += 1
        case "No Match":
            #print(stdoutBase != stdoutTest)
            if stdoutBase != stdoutTest:
                grade += 1

    match stderrMode:
        case "Ignore":
            grade += 1
        case "Match":
            #print(stderrBase == stderrTest)
            if stderrBase == stderrTest:
                grade += 1
        case "No Match":
            #print(stderrBase != stderrTest)
            if stderrBase != stderrTest:
                grade += 1

    match returnCodeMode:
        case "Ignore":
            grade += 1
        case "Match":
            #print(subBase.returncode == subTest.returncode)
            if subBase.returncode == subTest.returncode:
                grade += 1
        case "No Match":
            #print(subBase.returncode != subTest.returncode)
            if subBase.returncode != subTest.returncode:
                grade += 1
    
    return grade / 3.0, grade == 3

def assertOutput(a_arguments: dict[str, CodeTestNode], a_app: "Autograder") -> tuple[float, bool]:
    """
    """
    testProject: ProjectTestNode|None = a_arguments["test_project"] if isinstance(a_arguments["test_project"], ProjectTestNode) else None

    stdoutMode:     Pattern = re.compile(a_arguments["stdout"].literalValue      if isinstance(a_arguments["stdout"], LiteralTestNode)      and a_arguments["stdout"].literalType      == "string" else ".*")
    stderrMode:     Pattern = re.compile(a_arguments["stderr"].literalValue      if isinstance(a_arguments["stderr"], LiteralTestNode)      and a_arguments["stderr"].literalType      == "string" else ".*")
    returnCodeMode: Pattern = re.compile(a_arguments["return_code"].literalValue if isinstance(a_arguments["return_code"], LiteralTestNode) and a_arguments["return_code"].literalType == "string" else ".*")

    grade: int = 0

    if testProject is None:
        return grade, False
    
    project = a_app.instanceData.projects[testProject.projectName]

    sub: Popen[str] = Popen(" ".join([
            "py", f"{project.dir}\\{testProject.projectEntrypoint}", 
            *[f"\"{node.literalValue}\"" for node in testProject.projectArguments.nodes.values() if isinstance(node, LiteralTestNode)]]), 
        stdin=PIPE, 
        stdout=PIPE,
        stderr=PIPE,
        cwd=project.dir, 
        text=True)
    
    stdout, stderr = sub.communicate("\n".join(testProject.projectInputs), timeout=10.0)
        
    #if sub.stdout != None:
    #    print(f"stdout:\n {stdout.strip()}\n")
    #if sub.stderr != None:
    #    print(f"stderr:\n {stderr.strip()}\n")

    #print(F"{stdoutMode.match(stdout.strip())}")
    #print(F"{stderrMode.match(stderr.strip())}")
    #print(F"{returnCodeMode.match(f"{sub.returncode}")}")

    #print(f"Return Code: {sub.returncode} : {2}")

    if stdoutMode.match(stdout.strip()) is not None:
        grade += 1
    if stderrMode.match(stderr.strip()) is not None:
        grade += 1
    if returnCodeMode.match(f"{sub.returncode}") is not None:
        grade += 1
    
    return grade / 3.0, grade == 3

def walkAST(a_arguments: dict[str, CodeTestNode], a_app: "Autograder") -> tuple[float, bool]:
    """
    """
    #print("a")
    testProject: ProjectTestNode|None = a_arguments["test_project"] if isinstance(a_arguments["test_project"], ProjectTestNode) else None
    #print("b")
    pattern: ASTPatternTestNode|None = a_arguments["pattern"] if isinstance(a_arguments["pattern"], ASTPatternTestNode) else None
    #print("c")
    maxGrade: int = 0
    grade: int = 0

    if not testProject or not pattern:
        #print("Leave")
        return grade, False
    #print("d")
    walker: ASTWalker = ASTWalker(pattern.pattern)
    #print("e")
    bon = list(filter(lambda file: file.name == testProject.projectEntrypoint, a_app.instanceData.projects[testProject.projectName].files))
    #print(bon)
    amount: int = walker.visit(cast("PythonFile", bon[0]).ast)
    #print("f")
    #print(amount)
    return amount, amount > 0

CodeTest.registerTestType("compare_output", compareOutput)
CodeTest.registerTestType("assert_output", assertOutput)
CodeTest.registerTestType("walk_ast", walkAST)

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