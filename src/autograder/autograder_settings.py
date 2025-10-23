import dataclasses
from dataclasses import dataclass
from .code_test import CodeTest
from .project_settings import ProjectSettings
from typing import Any, cast

@dataclass
class AutograderSettings:
    projects: dict[str, ProjectSettings] = dataclasses.field(default_factory=dict) # type: ignore
    tests:    dict[str, CodeTest]        = dataclasses.field(default_factory=dict) # type: ignore
    criteria: dict[str, float]           = dataclasses.field(default_factory=dict) # type: ignore

    def updateFromDict(self, a_data: dict[str, Any]) -> None:
        self.projects = {key: ProjectSettings.fromDict(project) for key, project in cast(dict[str, Any], a_data["projects"]).items()}
        self.tests = {key: CodeTest.fromDict(test) for key, test in cast(dict[str, Any], a_data["tests"]).items()}
        self.criteria = a_data["criteria"]
    
    def addTests(self, a_testData: dict[str, Any]) -> None:
        self.tests.update({key: CodeTest.fromDict(test) for key, test in a_testData.items()})
    
    def toDict(self) -> dict[str, Any]:
        """Convert to a dict.
        """
        return {
            "projects": {
                key: project.toDict() for key, project in self.projects.items()
            },
            "tests": {
                key: test.toDict() for key, test in self.tests.items()
            },
            "criteria": self.criteria
        }