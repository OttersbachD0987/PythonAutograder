from .autograder_settings import AutograderSettings
from .autograder_instance_data import AutograderInstanceData
from typing import Any
import json

class Autograder:
    def __init__(self):
        self.settings: AutograderSettings = AutograderSettings()
        self.instanceData: AutograderInstanceData = AutograderInstanceData()

    def setConfigurationFromDict(self, a_data: dict[str, Any]):
        self.settings.updateFromDict(a_data)
    
    def loadConfiguration(self, a_path: str) -> None:
        try:
            with open(a_path, "r") as configurationFile:
                self.setConfigurationFromDict(json.load(configurationFile))
        except FileNotFoundError as e:
            print(f"The file {e.filename} does not exist.")
    
    def saveConfiguration(self, a_path: str) -> None:
        try:
            with open(a_path, "w") as configurationFile:
                json.dump(self.settings.toDict(), configurationFile)
        except PermissionError as e:
            print(f"Error: {e}")
        except IsADirectoryError as e:
            print(f"Error: {e}")