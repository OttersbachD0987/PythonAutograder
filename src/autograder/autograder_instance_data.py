from __future__ import annotations

#fmt: off

import dataclasses
from dataclasses import dataclass
from .autograder_report import AutograderReport
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from project.project import Project

@dataclass
class AutograderInstanceData:
    """The instance data of an autograder.
    """
    projects: dict[str, Project] = dataclasses.field(default_factory=dict)
    report: AutograderReport = dataclasses.field(default_factory=AutograderReport)