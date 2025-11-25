import os
import textwrap
import json
from enum import IntEnum, auto
from project.project import Project
from utils.util import intput, floatput
import pandas as pd
from pandas import DataFrame
from autograder.autograder_application import Autograder
from autograder.project_settings import Requirement
from autograder.code_test_type import IParameterGroup, ParameterRepresentation
from autograder.code_test import CodeTest, DictionaryTestNode, LiteralTestNode, ProjectTestNode, CodeTestNode
from typing import Any, cast

class Screen(IntEnum):
    MAIN             = auto()
    PROJECTS         = auto()
    PROJECT_SETTINGS = auto()
    TESTS            = auto()
    TESTS_SETTINGS   = auto()
    CRITERIA         = auto()
    RESULTS          = auto()
    EXIT             = auto()

# ===============================
# MAIN EXECUTION
# ===============================
def main():
    screen: Screen = Screen.MAIN

    grader: Autograder = Autograder()
    grader.loadConfiguration("Configurations/config.json")
    
    grader.extension_manager.loadFromDirectory("./Extensions")
    grader.extension_manager.importExtensions()

    context: str = ""
    testsToRun: list[str] = []

    data: dict[str, Any] = {
        "autograder": grader
    }

    while screen != Screen.EXIT: # type: ignore
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
                    case _:
                        print("Invalid choice.")
            case Screen.PROJECTS:
                print("|-------------------------<=  PROJECTS  =>-------------------------|")
                print("\n[======>------------------<==============>------------------<======]\n".join([f"Name: {project.name}\n{"\n".join(textwrap.wrap(project.dir, 68))}\n\n{grader.settings.projects.get(project.name, grader.settings.projects["default"])}" for project in grader.instanceData.projects.values()]))
                print("+------------------------------------------------------------------+")
                print("1) Add Project")
                print("2) Remove Project")
                print("3) Edit Project Settings")
                print("4) Back\n")
                match intput("Choice: "):
                    case 1:
                        grader.instanceData.projects[internalName] = Project(internalName := input("Internal name to use for the project: "), f"{os.getcwd()}\\{input("Path to the project root directory: ")}")
                    case 2:
                        if grader.instanceData.projects.pop(deleteName := input("Internal name of the project to remove: "), None) is None:
                            print(f"There is no project named {deleteName}.")
                    case 3:
                        if (name := input("Internal name of the project whose settings to edit: ")) in grader.instanceData.projects:
                            context = name
                            screen = Screen.PROJECT_SETTINGS
                        else:
                            print(f"There is no project named {name}.")
                    case 4:
                        screen = Screen.MAIN
                    case _:
                        print("Invalid choice.")
            case Screen.PROJECT_SETTINGS:
                grader.settings.projects[project.name] = (projectSettings := grader.settings.projects.get((project := grader.instanceData.projects[context]).name, grader.settings.projects["default"].copy()))
                print("|-------------------------<=  SETTINGS  =>-------------------------|")
                print(f"Name: {project.name}\n{"\n".join(textwrap.wrap(project.dir, 68))}\n\n{projectSettings}")
                print("+------------------------------------------------------------------+")
                print("1) Set Import Default")
                print("2) Set Import Override")
                print("3) Remove Import Override")
                print("4) Set Import Local")
                print("5) Back\n")


                match intput("Choice: "):
                    case 1:
                        match input("New Requirement (Required/Allowed/Forbidden): ").lower().strip():
                            case "required":
                                projectSettings.importDefault = Requirement.REQUIRED
                            case "allowed":
                                projectSettings.importDefault = Requirement.ALLOWED
                            case "forbidden":
                                projectSettings.importDefault = Requirement.FORBIDDEN
                            case _ as requirement:
                                print(f"{requirement.upper()} is not a valid Requirement type (Required/Allowed/Forbidden).")
                    case 2:
                        name: str = input("Name of import to override: ")
                        match input("New Requirement (Required/Allowed/Forbidden): ").lower().strip():
                            case "required":
                                projectSettings.importOverrides[name] = Requirement.REQUIRED
                            case "allowed":
                                projectSettings.importOverrides[name] = Requirement.ALLOWED
                            case "forbidden":
                                projectSettings.importOverrides[name] = Requirement.FORBIDDEN
                            case _ as requirement:
                                print(f"{requirement.upper()} is not a valid Requirement type (Required/Allowed/Forbidden).")
                    case 3:
                        if projectSettings.importOverrides.pop(name := input("Name of import to remove: "), None) is None:
                            print(f"There is no import override named {name}.")
                    case 4:
                        match input("New Requirement (Required/Allowed/Forbidden): ").lower().strip():
                            case "required":
                                projectSettings.importLocal = Requirement.REQUIRED
                            case "allowed":
                                projectSettings.importLocal = Requirement.ALLOWED
                            case "forbidden":
                                projectSettings.importLocal = Requirement.FORBIDDEN
                            case _ as requirement:
                                print(f"{requirement.upper()} is not a valid Requirement type (Required/Allowed/Forbidden).")
                    case 5:
                        context = ""
                        screen = Screen.PROJECTS
                    case _:
                        print("Invalid choice.")
            case Screen.TESTS:
                print("|-------------------------<= CODE TESTS =>-------------------------|")
                print("\n".join([f"[{"X" if testID in testsToRun else " "}] {testID}\n      > {test.type}" for testID, test in grader.settings.tests.items()]))
                print("+------------------------------------------------------------------+")
                print("1) Toggle Test")
                print("2) Import Tests")
                print("3) Remove Test")
                print("4) Edit Test")
                print("5) Rename Test")
                print("6) Back\n")
                match intput("Choice: "):
                    case 1:
                        if (testType := input("Name of the test to toggle: ")) in grader.settings.tests:
                            if testType in testsToRun:
                                testsToRun.remove(testType)
                            else:
                                testsToRun.append(testType)
                        else:
                            print(f"There is no test named {testType}.")
                    case 2:
                        if os.path.isfile(filepath := input("Path to the file with the tests: ")):
                            with open(filepath) as file:
                                grader.settings.addTests(json.load(file))
                    case 3:
                        if grader.settings.tests.pop(testType := input("Name of the test: "), None) is None:
                            print(f"There is no test named {testType}.")
                    case 4:
                        if (name := input("Name of the test to edit: ")) in grader.settings.tests:
                            context = name
                            screen = Screen.TESTS_SETTINGS
                        else:
                            print(f"There is no project named {name}.")
                    case 5:
                        if (name := input("Name of the test to rename: ")) in grader.settings.tests:
                            if (new_name := input("New name for the test: ")) not in grader.settings.tests:
                                grader.settings.tests[new_name] = grader.settings.tests.pop(name)
                                if name in testsToRun:
                                    testsToRun[testsToRun.index(name)] = new_name
                            else:
                                print(f"There is already a test named {new_name}.")
                        else:
                            print(f"There is no test named {name}.")
                    case 6:
                        screen = Screen.MAIN
                    case _:
                        print("Invalid choice.")
            case Screen.TESTS_SETTINGS:
                print("|-------------------------<=  SETTINGS  =>-------------------------|")
                test: CodeTestNode = grader.settings.tests[context]
                print(f"[{"X" if context in testsToRun else " "}] {context}\n      > {(testType := test.type)}")
                displayParams: list[IParameterGroup] = CodeTest.TestTypes[testType].parameters()
                uses: dict[str, CodeTestNode] = {}
                for param in displayParams:
                    if isinstance(param, ParameterRepresentation):
                        match param.kind:
                            case "ProjectTestNode":
                                uses.setdefault((projectNode := cast(ProjectTestNode, test.arguments[param.id])).nodeID, projectNode)
                                print(f"{projectNode.nodeID}: \n  Project Target: {projectNode.projectName}\n  Project Entrypoint: {projectNode.projectEntrypoint}\n  Inputs:\n    {"\n    ".join([f"{index}: {value}" for index, value in enumerate(projectNode.projectInputs)])}")
                            case "string"|"integer"|"boolean":
                                uses.setdefault((literalNode := cast(LiteralTestNode, test.arguments[param.id])).nodeID, literalNode)
                                print(f"{literalNode.nodeID} ({literalNode.literalType}): {literalNode.literalValue}")
                print("+------------------------------------------------------------------+")
                print("1) Edit Value")
                print("2) Back\n")
                match intput("Choice: "):
                    case 1:
                        if (name := input("Name of the value to edit: ")) in uses:
                            node: CodeTestNode = uses[name]
                            print("Properties:")
                            if isinstance(node, ProjectTestNode):
                                option: int = 0
                                print("1) Project Target\n2) Project Entrypoint\n3) Inputs\n4) Cancel\n")
                                while option != 4:
                                    match (option := intput("Property to set: ")):
                                        case 1:
                                            node.projectName = input("New Project Target: ")
                                        case 2:
                                            node.projectEntrypoint = input("New Project Entrypoint: ")
                                        case 3:
                                            print("\nEdit Options:\n1) Insert Input\n2) Remove Input\n3) Cancel\n")
                                            innerOption: int = 0
                                            while innerOption != 3:
                                                match (innerOption := intput("Choice: ")):
                                                    case 1:
                                                        node.projectInputs.insert(intput("Index to insert at: "), input("The value to insert: "))
                                                    case 2:
                                                        node.projectInputs.pop(intput("Index of the input to remove: "))
                                                    case 3:
                                                        ...
                                                    case _:
                                                        print("Invalid choice.")
                                        case 4:
                                            ...
                                        case _:
                                            print("Invalid choice.")
                            elif isinstance(node, LiteralTestNode):
                                title: str = node.nodeID.replace("_", " ").title()
                                match node.literalType:
                                    case "string":
                                        node.literalValue = input(f"New value for {title} (String): ")
                                    case "float":
                                        node.literalValue = floatput(f"New value for {title} (Float): ")
                                    case "integer":
                                        node.literalValue = intput(f"New value for {title} (Integer): ")
                                    case _:
                                        print("Unsupported Type.")
                        else:
                            print(f"There is no value named {name}.")
                    case 2:
                        screen = Screen.MAIN
                    case _:
                        print("Invalid choice.")
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
                    case _:
                        print("Invalid choice.")
            case Screen.RESULTS:
                [grader.settings.tests[test].runTest(grader, data) for test in testsToRun]
                returned: tuple[str, float, str]|None = grader.instanceData.report.proccessModifiers()
                print("|-------------------------<=   RESULT   =>-------------------------|")
                print("====== Rubric ======")
                print(f"{'Criterion':<20} {'Passed':<8} {'Weight':<6} {'Points':<6} Feedback")

                print("-"*68)
                normalValue: float = 0
                maxValue: float = 0
                frame: DataFrame = DataFrame([], ["Passed", "Weight", "Points", "Feedback"])
                if returned:
                    print(f"{returned[0]:<20} {str(False):<8} {100:<6} {returned[1]:<6} {returned[2]}")
                    frame[returned[0]] = {
                        "Passed": False,
                        "Weight": 100,
                        "Points": returned[1],
                        "Feedback": returned[2]
                    }
                else:
                    for criterion, (message, amount, maxAmount, passes) in grader.instanceData.report.usable(grader.settings.criteria).items():
                        normalValue += amount
                        maxValue += maxAmount
                        frame[criterion] = {
                            "Passed": passes,
                            "Weight": grader.settings.criteria[criterion],
                            "Points": amount,
                            "Feedback": message
                        }
                        print(f"{criterion:<20} {str(passes):<8} {grader.settings.criteria[criterion]:<6} {amount:<6} {message}")
                print("\n=== Final Grades ===")
                print(f"Score: {normalValue}/{maxValue} (Breakdown: {grader.settings.criteria})")
                print(frame)
                input("\nContinue")
                screen = Screen.MAIN

if __name__ == "__main__":
    
    main()