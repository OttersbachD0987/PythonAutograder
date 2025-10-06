from typing import TYPE_CHECKING
from .autograder_report import AutograderReport
if TYPE_CHECKING:
    from project.project import Project

class AutograderInstanceData:
    def __init__(self):
        self.projects: dict[str, Project] = {}
        self.report: AutograderReport = AutograderReport()