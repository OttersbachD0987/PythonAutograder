from src.autograder.code_test import CodeTest, CodeTestNode, ProjectTestNode, LiteralTestNode, executeCodeTestNode, ASTWalkTestNode, ASTPatternTestNode
from subprocess import Popen, PIPE
from typing import TYPE_CHECKING, cast, Optional
from re import Pattern
from src.autograder.code_walker import ASTWalker
from io import StringIO
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
    VALID_OUTPUTS: tuple[str, str, str] = ("Match", "No Match", "Ignore")

    baseProject: Optional[ProjectTestNode] = project if isinstance(project := a_arguments["base_project"], ProjectTestNode) else None
    testProject: Optional[ProjectTestNode] = project if isinstance(project := a_arguments["test_project"], ProjectTestNode) else None

    if not (testProject and baseProject):
        return grade, False
    
    stdoutMode:     str = literalValue if (isinstance(literalNode := a_arguments["stdout"],      LiteralTestNode) and literalNode.literalType == "string" and ((literalValue := literalNode.literalValue) in VALID_OUTPUTS)) else "Match"
    stderrMode:     str = literalValue if (isinstance(literalNode := a_arguments["stderr"],      LiteralTestNode) and literalNode.literalType == "string" and ((literalValue := literalNode.literalValue) in VALID_OUTPUTS)) else "Match"
    returnCodeMode: str = literalValue if (isinstance(literalNode := a_arguments["return_code"], LiteralTestNode) and literalNode.literalType == "string" and ((literalValue := literalNode.literalValue) in VALID_OUTPUTS)) else "Match"
    
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
    
    #for projectInput in baseProject.projectInputs:
    #    cast(StringIO, subBase.stdin).write(f"{projectInput}\n")

    stdoutBase, stderrBase = subBase.communicate("\n".join(baseProject.projectInputs), timeout=10.0)

    #print(f"Out: {stdoutBase}")
    
    subTest: Popen[str] = Popen(" ".join([
            "py", f"{projectTest.dir}\\{testProject.projectEntrypoint}", 
            *[f"\"{node.literalValue}\"" for node in testProject.projectArguments.nodes.values() if isinstance(node, LiteralTestNode)]]), 
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        cwd=projectTest.dir, 
        text=True)

    
    #for projectInput in testProject.projectInputs:
    #    cast(StringIO, subTest.stdin).write(f"{projectInput}\n")

    stdoutTest, stderrTest = subTest.communicate("\n".join(testProject.projectInputs), timeout=10.0)

    #print(f"Out: {difflib.SequenceMatcher(None, stdoutBase, stdoutTest).ratio()}\nErr: {difflib.SequenceMatcher(None, stderrBase, stderrTest).ratio()}\n")

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
    grade: int = 0
    testProject: Optional[ProjectTestNode] = project if isinstance(project := a_arguments["test_project"], ProjectTestNode) else None

    if not testProject:
        return grade, False

    stdoutMode:     Pattern = re.compile(literalNode.literalValue if isinstance(literalNode := a_arguments["stdout"],      LiteralTestNode) and literalNode.literalType == "string" else ".*")
    stderrMode:     Pattern = re.compile(literalNode.literalValue if isinstance(literalNode := a_arguments["stderr"],      LiteralTestNode) and literalNode.literalType == "string" else ".*")
    returnCodeMode: Pattern = re.compile(literalNode.literalValue if isinstance(literalNode := a_arguments["return_code"], LiteralTestNode) and literalNode.literalType == "string" else ".*")

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

    if stdoutMode.match(stdout.strip()):
        grade += 1
    if stderrMode.match(stderr.strip()):
        grade += 1
    if returnCodeMode.match(f"{sub.returncode}"):
        grade += 1
    
    return grade / 3.0, grade == 3

#def walkAST(a_arguments: dict[str, CodeTestNode], a_app: "Autograder") -> tuple[float, bool]:
#    """
#    """
#    return ((amount := ASTWalker(testPattern.pattern).visit(cast("PythonFile", [file for file in a_app.instanceData.projects[testProject.projectName].files if file.name == testProject.projectEntrypoint][0]).ast)), amount > 0) if (isinstance(testProject := a_arguments["test_project"], ProjectTestNode) and isinstance(testPattern := a_arguments["pattern"], ASTPatternTestNode)) else (0, False)
    

CodeTest.registerTestType("compare_output", compareOutput)
CodeTest.registerTestType("assert_output", assertOutput)
CodeTest.registerTestType("walk_ast", lambda a_arguments, a_app: (((amount := ASTWalker(testPattern.pattern).visit(cast("PythonFile", [file for file in a_app.instanceData.projects[testProject.projectName].files if file.name == testProject.projectEntrypoint][0]).ast)), amount > 0) if (isinstance(testProject := a_arguments["test_project"], ProjectTestNode) and isinstance(testPattern := a_arguments["pattern"], ASTPatternTestNode)) else (0, False)))

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