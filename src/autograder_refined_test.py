import os
import textwrap
from enum import IntEnum, auto
from project.project import Project
from utils.util import intput
from autograder.autograder_application import Autograder
from typing import Any

class Screen(IntEnum):
    MAIN     = auto()
    PROJECTS = auto()
    TESTS    = auto()
    CRITERIA = auto()
    RESULTS  = auto()
    EXIT     = auto()

# ===============================
# MAIN EXECUTION
# ===============================
def main():
    screen: Screen = Screen.MAIN

    grader: Autograder = Autograder()
    grader.loadConfiguration("Configurations/config.json")
    
    grader.extension_manager.loadFromDirectory("./Extensions")
    grader.extension_manager.importExtensions()

    testsToRun: list[str] = []

    data: dict[str, Any] = {
        "autograder": grader
    }
    while screen != Screen.EXIT:
        match screen:
            case Screen.MAIN:
                print("|-------------------------<=    MENU    =>-------------------------|")
                print("1) Manage Projects")
                print("2) Manage Tests")
                print("3) Manage Criteria")
                print("4) Run Tests")
                print("5) Quit\n")
                match intput("Choice: "):
                    case 1:
                        screen = Screen.PROJECTS
                    case 2:
                        screen = Screen.TESTS
                    case 3:
                        screen = Screen.CRITERIA
                    case 4:
                        screen = Screen.RESULTS
                    case 5:
                        screen = Screen.EXIT
            case Screen.PROJECTS:
                print("|-------------------------<=  PROJECTS  =>-------------------------|")
                print("\n[======>------------------<==============>------------------<======]\n".join([f"{project.name}\n{"\n".join(textwrap.wrap(project.dir, 68))}" for project in grader.instanceData.projects.values()]))
                print("+------------------------------------------------------------------+")
                print("1) Add Project")
                print("2) Remove Project")
                print("3) Back\n")
                match intput("Choice: "):
                    case 1:
                        grader.instanceData.projects[internalName] = Project(internalName := input("Internal name to use for the project: "), f"{os.getcwd()}\\{input("Path to the project root directory: ")}")
                    case 2:
                        if grader.instanceData.projects.pop(deleteName := input("Internal name of the project to remove: "), None) is None:
                            print(f"There is no project named {deleteName}.")
                    case 3:
                        screen = Screen.MAIN
            case Screen.TESTS:
                print("|-------------------------<= CODE TESTS =>-------------------------|")
                print("\n".join([f"[{"X" if testID in testsToRun else " "}] {testID}\n      > {test.type}" for testID, test in grader.settings.tests.items()]))
                print("+------------------------------------------------------------------+")
                print("1) Toggle Test")
                #print("2) ")
                print("2) Back\n")
                match intput("Choice: "):
                    case 1:
                        if (test := input("Name of the test to toggle: ")) in grader.settings.tests:
                            if test in testsToRun:
                                testsToRun.remove(test)
                            else:
                                testsToRun.append(test)
                        else:
                            print(f"There is no test named {test}.")
                    case 2:
                        screen = Screen.MAIN
            case Screen.CRITERIA:
                print("|-------------------------<=  CRITERIA  =>-------------------------|")
                print("\n".join([f"{key}: {value}" for key, value in grader.settings.criteria.items()]))
                print("+------------------------------------------------------------------+")
                print("1) Set Criteria")
                print("2) Remove Criteria")
                print("3) Back\n")
                match intput("Choice: "):
                    case 1:
                        name: str = input("Name of the criteria: ")
                        grader.settings.criteria[name] = intput("Weight of the criteria: ")
                    case 2:
                        if grader.settings.criteria.pop(criteria := input("Name of the criteria: "), None) is None:
                            print(f"There is no criteria named {criteria}.")
                    case 3:
                        screen = Screen.MAIN
            case Screen.RESULTS:
                [grader.settings.tests[test].runTest(grader, data) for test in testsToRun]
                returned: tuple[str, float, str]|None = grader.instanceData.report.proccessModifiers()
                print(returned)

                print("|-------------------------<=   RESULT   =>-------------------------|")
                print(f"{'Criterion':<20} {'Passed':<8} {'Weight':<6} {'Points':<6} Feedback")

                print("-"*80)
                normalValue: float = 0
                maxValue: float = 0
                if returned:
                    print(f"{returned[0]:<20} {str(False):<8} {100:<6} {returned[1]:<6} {returned[2]}")
                else:
                    for criterion, (message, amount, maxAmount, passes) in grader.instanceData.report.usable(grader.settings.criteria).items():
                        normalValue += amount
                        maxValue += maxAmount
                        print(f"{criterion:<20} {str(passes):<8} {grader.settings.criteria[criterion]:<6} {amount:<6} {message}")
                print("\n=== Final Grade ===")
                print(f"Score: {normalValue}/{maxValue} (Breakdown: {grader.settings.criteria})")
                input()

if __name__ == "__main__":
    main()