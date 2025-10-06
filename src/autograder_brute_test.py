import subprocess
import ast
import tokenize
import symtable
import os
from project.project import Project
from autograder.autograder_application import Autograder
from autograder.project_settings import Requirement
from typing import Any

# ===============================
# MAIN EXECUTION
# ===============================
def main():
    instructorProjectName: str = input("Internal name to use for the project: ")
    instructorProjectDirectory: str = input("Path to instructor project directory: ")
    instructorProject: Project = Project(instructorProjectName, f"{os.getcwd()}\\{instructorProjectDirectory}")
    studentProjectName: str = input("Internal name to use for the project: ")
    studentProjectDirectory: str = input("Path to student project directory: ")
    studentProject: Project = Project(studentProjectName, f"{os.getcwd()}\\{studentProjectDirectory}")

    grader: Autograder = Autograder()
    grader.setConfigurationFromDict({
        "projects": {
            "default": {
                "import_default": Requirement.ALLOWED,
                "import_overrides": {},  #key: int(requirement) for key, requirement in self.importOverrides.items()
                "import_local": Requirement.ALLOWED
            },
            instructorProjectName: {
                "import_default": Requirement.ALLOWED,
                "import_overrides": {},  #key: int(requirement) for key, requirement in self.importOverrides.items()
                "import_local": Requirement.ALLOWED
            },
            studentProjectName: {
                "import_default": Requirement.ALLOWED,
                "import_overrides": {},  #key: int(requirement) for key, requirement in self.importOverrides.items()
                "import_local": Requirement.ALLOWED
            }
        },  #key: project.ToDict() for key, project in self.projects.items()
        "tests": {
            "fancy_assertion": {
                "type": "walk_ast",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": instructorProjectName,
                        "project_entrypoint": "main.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {
                                "a": {
                                    "node_id": "literal",
                                    "literalType": "string",
                                    "literalValue": "a"
                                }
                            }
                        },
                        "project_inputs": [
                            "Moo",
                            "Conker"
                        ]
                    },
                    "pattern": {
                        "node_id": "ast_pattern",
                        "node_type": "while",
                        "pattern": {
                            "node_type": "while",
                            "match_kind": "test_patterns",
                            "test_patterns": [
                                {
                                    "node_id": "ast_pattern",
                                    "node_type": "constant"
                                }, {
                                    "node_id": "ast_pattern",
                                    "node_type": "name"
                                }
                            ]
                        }
                    }
                },  #key: node.ToDict() for key, node in self.arguments.items()
                "found": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "structure",
                            "node_message": "I am are monkey: {a_data['factor']:.2f}"
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "structure",
                            "modifier_type": "overkill",
                            "modifier_value": 1,
                            "max_value": 1,
                            "passes": False
                        }
                    ]
                },
                "notFound": {
                    "node_id": "block",
                    "nodes": []
                }
            },
            "first_assertion": {
                "type": "assert_output",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": instructorProjectName,
                        "project_entrypoint": "main.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {
                                "a": {
                                    "node_id": "literal",
                                    "literalType": "string",
                                    "literalValue": "a"
                                }
                            }
                        },
                        "project_inputs": [
                            "Moo",
                            "Conker"
                        ]
                    },
                    "stdout": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "a"
                    },
                    "stderr": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "b"
                    },
                    "return_code": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "[0-9]*"
                    }
                }   #key: node.ToDict() for key, node in self.arguments.items()
            },
            "second_assertion": {
                "type": "assert_output",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": studentProjectName,
                        "project_entrypoint": "main.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {
                                "a": {
                                    "node_id": "literal",
                                    "literalType": "string",
                                    "literalValue": "a"
                                }
                            }
                        },
                        "project_inputs": [
                            "Moo",
                            "Conker"
                        ]
                    },
                    "stdout": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "a"
                    },
                    "stderr": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "b"
                    },
                    "return_code": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "c"
                    }
                }   #key: node.ToDict() for key, node in self.arguments.items()
            },
            "first_comparison": {
                "type": "compare_output",
                "arguments": {
                    "base_project": {
                        "node_id": "project",
                        "project_name": instructorProjectName,
                        "project_entrypoint": "main.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {
                                "a": {
                                    "node_id": "literal",
                                    "literalType": "string",
                                    "literalValue": "a"
                                }
                            }
                        },
                        "project_inputs": [
                            "Moo",
                            "Conker"
                        ]
                    },
                    "test_project": {
                        "node_id": "project",
                        "project_name": studentProjectName,
                        "project_entrypoint": "main.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {
                                "a": {
                                    "node_id": "literal",
                                    "literalType": "string",
                                    "literalValue": "a"
                                }
                            }
                        },
                        "project_inputs": [
                            "Moo",
                            "Conker"
                        ]
                    },
                    "stdout": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "a"
                    },
                    "stderr": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "b"
                    },
                    "return_code": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "c"
                    }
                }   #key: node.ToDict() for key, node in self.arguments.items()
            }
        },  #key: test.ToDict() for key, test in self.tests.items()
        "criteria": {
            "foo": 1
        }   #self.criteria
    })

    grader.instanceData.projects[instructorProjectName] = instructorProject
    grader.instanceData.projects[studentProjectName] = studentProject

    data: dict[str, Any] = {
        "autograder": grader
    }

    print("1")
    grader.settings.tests["fancy_assertion"].runTest(grader, data)
    print("2")
    grader.settings.tests["first_assertion"].runTest(grader, data)
    print("3")
    grader.settings.tests["second_assertion"].runTest(grader, data)
    print("4")
    grader.settings.tests["first_comparison"].runTest(grader, data)

    print("---")
    #for section in grader.instanceData.report.messages.items():
    #    print(f"{time}: {message}")
    

    returned: tuple[str, float, str]|None = grader.instanceData.report.proccessModifiers()
    print(returned)

    print("=== Rubric ===")
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


import autograder.code_test_kinds

if __name__ == "__main__":
    main()