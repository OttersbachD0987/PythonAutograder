import os
from project.project import Project
from autograder.autograder_application import Autograder
from autograder.project_settings import Requirement
from typing import Any

# ===============================
# MAIN EXECUTION
# ===============================
def main():
    program1Name: str = "program_one"
    program1Directory: str = "Tests\\program1_auto_grader"
    program1: Project = Project(program1Name, f"{os.getcwd()}\\{program1Directory}")
    program2Name: str = "program_two"
    program2Directory: str = "Tests\\program2"
    program2: Project = Project(program2Name, f"{os.getcwd()}\\{program2Directory}")

    grader: Autograder = Autograder()
    grader.setConfigurationFromDict({
        "projects": {
            "default": {
                "import_default": Requirement.ALLOWED,
                "import_overrides": {},  #key: int(requirement) for key, requirement in self.importOverrides.items()
                "import_local": Requirement.ALLOWED
            },
            program1Name: {
                "import_default": Requirement.ALLOWED,
                "import_overrides": {},  #key: int(requirement) for key, requirement in self.importOverrides.items()
                "import_local": Requirement.ALLOWED
            },
            program2Name: {
                "import_default": Requirement.ALLOWED,
                "import_overrides": {},  #key: int(requirement) for key, requirement in self.importOverrides.items()
                "import_local": Requirement.ALLOWED
            }
        },  #key: project.ToDict() for key, project in self.projects.items()
        "tests": {
            "no_errors_while": {
                "type": "walk_ast",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": program1Name,
                        "project_entrypoint": "no_errors.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": []
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
                            "node_message": "While True/variable usage."
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
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "structure",
                            "node_message": "Correct usage of while loops."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "structure",
                            "modifier_type": "addition",
                            "modifier_value": 1,
                            "max_value": 1,
                            "passes": True
                        }
                    ]
                }
            },
            "first_comparison": {
                "type": "compare_output",
                "arguments": {
                    "base_project": {
                        "node_id": "project",
                        "project_name": program1Name,
                        "project_entrypoint": "instructor_solution_file.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": [
                            "Jelo",
                            "12",
                            "45",
                            "Done"
                        ]
                    },
                    "test_project": {
                        "node_id": "project",
                        "project_name": program1Name,
                        "project_entrypoint": "no_errors.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": [
                            "Jelo",
                            "12",
                            "45",
                            "Done"
                        ]
                    },
                    "stdout": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "Match"
                    },
                    "stderr": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "Match"
                    },
                    "return_code": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "Match"
                    }
                },  #key: node.ToDict() for key, node in self.arguments.items()
                "found": {
                    "node_id": "post_grade_modifier",
                    "criterion": "output",
                    "modifier_type": "addition",
                    "modifier_value": 1,
                    "max_value": 1,
                    "passes": True
                },
                "notFound": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "output",
                            "node_message": "The output is incorrect."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "output",
                            "modifier_type": "addition",
                            "modifier_value": 0,
                            "max_value": 1,
                            "passes": False
                        }
                    ]
                }
            },
            "no_errors_variables": {
                "type": "walk_ast",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": program1Name,
                        "project_entrypoint": "no_errors.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": []
                    },
                    "pattern": {
                        "node_id": "ast_pattern",
                        "node_type": "assign",
                        "pattern": {
                            "node_id": "ast_pattern",
                            "node_type": "assign",
                            "match_kind": "target_pattern",
                            "target_pattern": {
                                "node_id": "ast_pattern",
                                "node_type": "name",
                                "name": r"[a-zA-Z_]\w+"
                            }
                        }
                    }
                },  #key: node.ToDict() for key, node in self.arguments.items()
                "found": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "variables",
                            "modifier_type": "addition",
                            "modifier_value": 1,
                            "max_value": 1,
                            "passes": True
                        }
                    ]
                },
                "notFound": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "variables",
                            "node_message": "Variables named incorrectly."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "variables",
                            "modifier_type": "addition",
                            "modifier_value": 0,
                            "max_value": 1,
                            "passes": False
                        }
                    ]
                }
            },
            "no_errors_functions": {
                "type": "walk_ast",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": program1Name,
                        "project_entrypoint": "no_errors.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": []
                    },
                    "pattern": {
                        "node_id": "ast_pattern",
                        "node_type": "function_def",
                        "pattern": {
                            "node_id": "ast_pattern",
                            "node_type": "function_def"
                        }
                    }
                },  #key: node.ToDict() for key, node in self.arguments.items()
                "found": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "functions",
                            "modifier_type": "addition",
                            "modifier_value": 1,
                            "max_value": 1,
                            "passes": True
                        }
                    ]
                },
                "notFound": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "functions",
                            "node_message": "No functions."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "functions",
                            "modifier_type": "addition",
                            "modifier_value": 0,
                            "max_value": 1,
                            "passes": False
                        }
                    ]
                }
            },
            "program2_while": {
                "type": "walk_ast",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": program2Name,
                        "project_entrypoint": "program2_stu_correct.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": []
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
                            "node_message": "While True/variable usage."
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
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "structure",
                            "node_message": "Correct usage of while loops."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "structure",
                            "modifier_type": "addition",
                            "modifier_value": 1,
                            "max_value": 1,
                            "passes": True
                        }
                    ]
                }
            },
            "second_comparison": {
                "type": "compare_output",
                "arguments": {
                    "base_project": {
                        "node_id": "project",
                        "project_name": program2Name,
                        "project_entrypoint": "program2_solution.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": [
                            "6"
                        ]
                    },
                    "test_project": {
                        "node_id": "project",
                        "project_name": program2Name,
                        "project_entrypoint": "program2_stu_correct.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": [
                            "6"
                        ]
                    },
                    "stdout": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "Match"
                    },
                    "stderr": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "Match"
                    },
                    "return_code": {
                        "node_id": "literal",
                        "literalType": "string",
                        "literalValue": "Match"
                    }
                },  #key: node.ToDict() for key, node in self.arguments.items()
                "found": {
                    "node_id": "post_grade_modifier",
                    "criterion": "output",
                    "modifier_type": "addition",
                    "modifier_value": 1,
                    "max_value": 1,
                    "passes": True
                },
                "notFound": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "output",
                            "node_message": "The output is incorrect."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "output",
                            "modifier_type": "addition",
                            "modifier_value": 0,
                            "max_value": 1,
                            "passes": False
                        }
                    ]
                }
            },
            "program2_variables": {
                "type": "walk_ast",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": program2Name,
                        "project_entrypoint": "program2_stu_correct.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": []
                    },
                    "pattern": {
                        "node_id": "ast_pattern",
                        "node_type": "assign",
                        "pattern": {
                            "node_id": "ast_pattern",
                            "node_type": "assign",
                            "match_kind": "target_pattern",
                            "target_pattern": {
                                "node_id": "ast_pattern",
                                "node_type": "name",
                                "name": r"[a-zA-Z_]\w+"
                            }
                        }
                    }
                },  #key: node.ToDict() for key, node in self.arguments.items()
                "found": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "variables",
                            "modifier_type": "addition",
                            "modifier_value": 1,
                            "max_value": 1,
                            "passes": True
                        }
                    ]
                },
                "notFound": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "variables",
                            "node_message": "Variables named incorrectly."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "variables",
                            "modifier_type": "addition",
                            "modifier_value": 0,
                            "max_value": 1,
                            "passes": False
                        }
                    ]
                }
            },
            "program2_functions": {
                "type": "walk_ast",
                "arguments": {
                    "test_project": {
                        "node_id": "project",
                        "project_name": program2Name,
                        "project_entrypoint": "program2_stu_correct.py",
                        "project_arguments": {
                            "node_id": "dictionary",
                            "nodes": {}
                        },
                        "project_inputs": []
                    },
                    "pattern": {
                        "node_id": "ast_pattern",
                        "node_type": "function_def",
                        "pattern": {
                            "node_id": "ast_pattern",
                            "node_type": "function_def"
                        }
                    }
                },  #key: node.ToDict() for key, node in self.arguments.items()
                "found": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "functions",
                            "modifier_type": "addition",
                            "modifier_value": 1,
                            "max_value": 1,
                            "passes": True
                        }
                    ]
                },
                "notFound": {
                    "node_id": "block",
                    "nodes": [
                        {
                            "node_id": "post_message",
                            "criterion": "functions",
                            "node_message": "No functions."
                        },
                        {
                            "node_id": "post_grade_modifier",
                            "criterion": "functions",
                            "modifier_type": "addition",
                            "modifier_value": 0,
                            "max_value": 1,
                            "passes": False
                        }
                    ]
                }
            }
        },  #key: test.ToDict() for key, test in self.tests.items()
        "criteria": {
            "structure": 20,
            "output": 50,
            "functions": 10,
            "psuedocode":5,
            "variables": 5,
        }   #self.criteria
    })

    grader.instanceData.projects[program1Name] = program1
    grader.instanceData.projects[program2Name] = program2

    data: dict[str, Any] = {
        "autograder": grader
    }

    option: int = -1

    while option != 3:
        grader.instanceData.report.clear()
        print("\n\n1) Program 1\n2) Program 2\n3) Exit")
        option = int(input("Option: "))
        match option:
            case 1:
                grader.settings.tests["no_errors_while"].runTest(grader, data)
                grader.settings.tests["first_comparison"].runTest(grader, data)
                grader.settings.tests["no_errors_variables"].runTest(grader, data)
                grader.settings.tests["no_errors_functions"].runTest(grader, data)
            case 2:
                grader.settings.tests["program2_while"].runTest(grader, data)
                grader.settings.tests["second_comparison"].runTest(grader, data)
                grader.settings.tests["program2_variables"].runTest(grader, data)
                grader.settings.tests["program2_functions"].runTest(grader, data)
            case 3:
                break
            case _:
                print(f"Invalid option: {option}")
                continue
            
        returned: tuple[str, float, str]|None = grader.instanceData.report.proccessModifiers()

        print("\n=== Rubric ===")
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
    

    

    

    # No implementation for variables because that requires us to be able to parse natural language, which hasn't been covered yet.
    # Also with no specifications of what is being checked, and no structure, there is no implementation I could do that would make sense.

    #print("---")
    #for section in grader.instanceData.report.messages.items():
    #    print(f"{time}: {message}")
    

    


import autograder.code_test_kinds


if __name__ == "__main__":
    main()




            