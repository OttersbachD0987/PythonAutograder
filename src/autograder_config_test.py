from project.project import Project
from autograder.code_test import CodeTest
from autograder.autograder_application import Autograder
from autograder.autograder_instance_data import AutograderInstanceData
from autograder.autograder_settings import AutograderSettings
from enum import IntEnum, auto
from dataclasses import dataclass
from typing import Any
from util import intput
import dataclasses, os

from autograder import code_test_kinds

class Screen(IntEnum):
    MAIN = auto()
    MANAGE_PROJECTS = auto()
    MANAGE_TESTS = auto()
    MANAGE_CRITERIA = auto()
    MANAGE_PRESETS = auto()
    EDIT_PROJECT = auto()
    EDIT_TEST = auto()
    EDIT_CRITERIA = auto()
    A = auto()

@dataclass
class AppConfigState:
    run: bool = True
    screen: Screen = Screen.MAIN
    grader: Autograder = dataclasses.field(default_factory=Autograder)
    data: dict[str, Any] = dataclasses.field(default_factory=dict)

def handleInput(a_app: AppConfigState):
    """Handle the input of the function.
    """
    match a_app.screen:
        case Screen.MAIN:
            # 1) Manage Projects
            # 2) Manage Tests
            # 3) Manage Criteria
            # 4) Manage Presets
            # 5) Quit
            match intput("Options:\n1) Manage Projects\n2) Manage Tests\n3) Manage Criteria\n4) Manage Presets\n5) Quit\nChoice: "):
                case 1:
                    a_app.screen = Screen.MANAGE_PROJECTS
                case 2:
                    a_app.screen = Screen.MANAGE_TESTS
                case 3:
                    a_app.screen = Screen.MANAGE_CRITERIA
                case 4:
                    a_app.screen = Screen.MANAGE_PRESETS
                case 5:
                    a_app.run = False
        case Screen.MANAGE_PROJECTS:
            # 1) List Projects
            # 2) Add Project
            # 3) Edit Project
            # 4) Remove Project
            # 5) Back
            match intput("Options:\n1) List Projects\n2) Add Project\n3) Edit Project\n4) Remove Project\n5) Back\nChoice: "):
                case 1:
                    print(f"Projects:\n{"\n".join(a_app.grader.instanceData.projects.keys())}")
                case 2:
                    path: str = input("Path to the project folder: ")
                    name: str = input("Name of the project: ")
                    if os.path.isdir(path) and name not in a_app.grader.instanceData.projects:
                        a_app.grader.instanceData.projects[name] = Project(name, path)
                case 3:
                    name: str = input("Name of the project to edit: ")
                    if name in a_app.grader.instanceData.projects:
                        a_app.data["project_name"] = name
                        a_app.screen = Screen.EDIT_PROJECT
                case 4:
                    name: str = input("Name of the project to remove: ")
                    if name in a_app.grader.instanceData.projects and input(f"Are you sure you want to remove the project {name} (Y/n): ") == "Y":
                        del a_app.grader.instanceData.projects[name]
                case 5:
                    a_app.screen = Screen.MAIN
        case Screen.MANAGE_CRITERIA:
            # 1) List Criteria
            # 2) Add Criteria
            # 3) Edit Criteria
            # 4) Remove Criteria
            # 5) Back
            match intput("Options:\n1) List Critera\n2) Add Criteria\n3) Edit Criteria\n4) Remove Criteria\n5) Back\nChoice: "):
                case 1:
                    ...
                case 5:
                    a_app.screen = Screen.MAIN
        case Screen.MANAGE_TESTS:
            # 1) List Tests
            # 2) Add Test
            # 3) Edit Test
            # 4) Remove Test
            # 5) Back
            match intput("Options:\n1) List Tests\n2) Add Test\n3) Edit Test\n4) Remove Test\n5) Back\nChoice: "):
                case 1:
                    print(f"Tests:\n{"\n".join(a_app.grader.settings.tests.keys())}")
                case 2:
                    name: str = input("Name of the test: ")
                    if name not in a_app.grader.settings.tests:
                        a_app.grader.settings.tests[name] = CodeTest(name, {})
                case 3:
                    name: str = input("Name of the test to edit: ")
                    if name in a_app.grader.settings.tests:
                        a_app.data["test_name"] = name
                        a_app.screen = Screen.EDIT_TEST
                case 4:
                    name: str = input("Name of the test to remove: ")
                    if name in a_app.grader.settings.tests and input(f"Are you sure you want to remove the test {name} (Y/n): ") == "Y":
                        del a_app.grader.settings.tests[name]
                case 5:
                    a_app.screen = Screen.MAIN
        case Screen.EDIT_PROJECT:
            # 1) Rename
            # 2) Back
            match intput("Options:\n1) Rename\n2) Back\nChoice: "):
                case 1:
                    name: str = input("New name of the project: ")
                    if name in a_app.grader.instanceData.projects:
                        print(f"{name} is already a used name.")
                    else:
                        a_app.grader.instanceData.projects[name] = a_app.grader.instanceData.projects[a_app.data["project_name"]]
                        del a_app.grader.instanceData.projects[a_app.data["project_name"]]
                        a_app.data["project_name"] = name
                case 2:
                    a_app.screen = Screen.MANAGE_PROJECTS
                    del a_app.data["project_name"]
        case Screen.EDIT_TEST:
            # 1) Rename
            # 2) Back
            match intput("Options:\n1) Rename\n2) Back\nChoice: "):
                case 1:
                    name: str = input("New name of the Test: ")
                    if name in a_app.grader.settings.tests:
                        print(f"{name} is already a used name.")
                    else:
                        a_app.grader.settings.tests[name] = a_app.grader.settings.tests[a_app.data["test_name"]]
                        del a_app.grader.settings.tests[a_app.data["test_name"]]
                        a_app.data["test_name"] = name
                case 2:
                    a_app.screen = Screen.MANAGE_TESTS
                    del a_app.data["test_name"]
        case Screen.EDIT_CRITERIA:
            # 1) Rename
            # 2) Back
            match intput("Options:\n1) Rename\n2) Back\nChoice: "):
                case 1:
                    name: str = input("New name of the project: ")
                    if name in a_app.grader.instanceData.projects:
                        print(f"{name} is already a used name.")
                    else:
                        a_app.grader.instanceData.projects[name] = a_app.grader.instanceData.projects[a_app.data["project_name"]]
                        del a_app.grader.instanceData.projects[a_app.data["project_name"]]
                        a_app.data["project_name"] = name
                case 2:
                    a_app.screen = Screen.MANAGE_CRITERIA
                    del a_app.data["project_name"]


# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    app: AppConfigState = AppConfigState()


    while app.run:
        handleInput(app)
        match app.screen:
            case Screen.MAIN:
                ...
