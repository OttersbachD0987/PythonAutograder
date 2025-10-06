import subprocess
import ast
import tokenize
import symtable
import os
from project.python_file import PythonFile
from project.project import Project
from typing import Any

# ===============================
# CONFIGURATION
# ===============================
CRITERIA = {
    "structure": 30,   # % weight for loop/structure
    "output": 50,      # % weight for correct output
    "functions": 10,   # % weight for using functions
    "pseudocode": 5,   # % weight for comments
    "variables": 5     # % weight for variable usage
}

# Weak, sad, truly unusable in it's lack of capabilites. This must be fixed post haste.

# ===============================
# FUNCTION: Run a Python file
# ===============================
def RunProgram(a_file: PythonFile) -> tuple[str, str, int]:
    """Run a Python program and return stdout, stderr, and exit code.
    """
    result = subprocess.run(
        ["python", f"{a_file.path}\\{a_file.name}"],   # program to run
        capture_output=True,             # capture what it prints
        text=True                        # result.stderr decode output as text instead of bytes
    )

    # result.returncode 0 means success
    # result.stdout the program's printed output. .strip() deletes leading and trailing space
    # error messages (if any)
    
    return result.stdout.strip(), result.stderr.strip(), result.returncode



# ===============================
# FUNCTION: Check loops / structure
# ===============================
def CheckLoops(a_file: PythonFile) -> tuple[bool, list[str]]:
    """Analyze loops in the student file using AST.
    
    Return: 
        passed (bool): Success.
        messages (list[str]): Any messages.
    """
    # TODO: implement loop checking
    passed: bool = True
    messages: list[str] = ["✅ Loop check not implemented yet."]
    return passed, messages


# ===============================
# FUNCTION: Check function usage
# ===============================
def CheckFunctions(a_file: PythonFile) -> tuple[bool, list[str]]:
    """Detect if student code defines functions.
    
    Return: 
        passed (bool): Success.
        messages (list[str]): Any messages.
    """
    # TODO: implement function checking
    passed: bool = True
    messages: list[str] = ["✅ Function check not implemented yet."]
    return passed, messages


# ===============================
# FUNCTION: Check comments
# ===============================
def CheckComments(a_file: PythonFile) -> tuple[bool, list[str]]:
    """Check for meaningful comments in the student code.
    
    Return: 
        passed (bool): Success.
        messages (list[str]): Any messages.
    """
    # TODO: implement comment checking
    passed: bool = True
    messages: list[str] = ["✅ Comment check not implemented yet."]
    return passed, messages


# ===============================
# FUNCTION: Check variable usage
# ===============================
def CheckVariables(a_file: PythonFile) -> tuple[bool, list[str]]:
    """Check variable usage and naming conventions.
    
    Return: 
        passed (bool): Success.
        messages (list[str]): Any messages.
    """
    # TODO: implement variable checking
    passed: bool = True
    messages: list[str] = ["✅ Variable check not implemented yet."]
    return passed, messages


# ===============================
# FUNCTION: Compare output
# ===============================
def CompareOutputs(a_firstFile: PythonFile, a_secondFile: PythonFile) -> tuple[bool, list[str]]:
    """Compare the student output to the solution output.
    
    Return: 
        passed (bool): Success.
        messages (list[str]): Any messages.
    """
    # TODO: implement output comparison
    passed: bool = True
    messages: list[str] = ["✅ Output comparison not implemented yet."]
    return passed, messages


# ===============================
# FUNCTION: Grade student
# ===============================
def GradeFile(a_solutionFile: PythonFile, a_studentFile: PythonFile) -> tuple[int, list[dict[str, Any]]]:
    """Run all checks and calculate weighted score.

    Returns: 
        total_score (int): 
        rubric (list[dict[str, Any]]): 
    """
    rubric: list[dict[str, Any]] = []
    total_score: int = 0

    # Loop / structure
    passed, messages = CheckLoops(a_studentFile)
    points = CRITERIA["structure"] if passed else 0
    total_score += points
    rubric.append({
        "Criterion": "Loop/Structure",
        "Passed": passed,
        "Weight": CRITERIA["structure"],
        "Points Earned": points,
        "Feedback": "; ".join(messages)
    })

    # Functions
    passed, messages = CheckFunctions(a_studentFile)
    points = CRITERIA["functions"] if passed else 0
    total_score += points
    rubric.append({
        "Criterion": "Function Usage",
        "Passed": passed,
        "Weight": CRITERIA["functions"],
        "Points Earned": points,
        "Feedback": "; ".join(messages)
    })

    # Comments
    passed, messages = CheckComments(a_studentFile)
    points = CRITERIA["comments"] if passed else 0
    total_score += points
    rubric.append({
        "Criterion": "Comments",
        "Passed": passed,
        "Weight": CRITERIA["comments"],
        "Points Earned": points,
        "Feedback": "; ".join(messages)
    })

    # Variables
    passed, messages = CheckVariables(a_studentFile)
    points = CRITERIA["variables"] if passed else 0
    total_score += points
    rubric.append({
        "Criterion": "Variables",
        "Passed": passed,
        "Weight": CRITERIA["variables"],
        "Points Earned": points,
        "Feedback": "; ".join(messages)
    })

    # Output
    passed, messages = CompareOutputs(a_solutionFile, a_studentFile)
    points = CRITERIA["output"] if passed else 0
    total_score += points
    rubric.append({
        "Criterion": "Output Correctness",
        "Passed": passed,
        "Weight": CRITERIA["output"],
        "Points Earned": points,
        "Feedback": "; ".join(messages)
    })

    return total_score, rubric


# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":

    instructorProjectDirectory: str = input("Path to instructor project directory: ")
    studentProjectDirectory:    str = input("Path to student project directory: ")

    instructorProject: Project = Project("a", f"{os.getcwd()}\\{instructorProjectDirectory}")
    studentProject:    Project = Project("b", f"{os.getcwd()}\\{studentProjectDirectory}")
    #score, rubric = GradeFile(instructorFile, studentFile)
    print("=== Rubric ===")
    print(f"{'Criterion':<20} {'Passed':<8} {'Weight':<6} {'Points':<6} Feedback")
    print("-"*80)
    #for item in rubric:
    #    print(f"{item['Criterion']:<20} {str(item['Passed']):<8} {item['Weight']:<6} "
    #          f"{item['Points Earned']:<6} {item['Feedback']}")
    #print("\n=== Final Grade ===")
    #print(f"Score: {score}/100 (Breakdown: {CRITERIA})")
