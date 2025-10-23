from .extension import Extension
import importlib, importlib.util, sys, os, json
from types import ModuleType
from typing import Optional

class ExtensionManager:
    def __init__(self):
        self.extensions: dict[str, tuple[Extension, Optional[ModuleType]]] = {}
    
    def loadFromDirectory(self, a_path: str) -> None:
        """_summary_

        Args:
            path (str): _description_
        """
        for dir in filter(lambda dir: dir.is_dir(), os.scandir(a_path)):
            try:
                with open(dir.path + "/extension.json") as extensionProperties:
                    self.extensions[dir.name] = (Extension.fromDict(json.load(extensionProperties), dir.path), None)
            except FileNotFoundError as e:
                print(f"The extension {dir.name} does not have an extension.json in it's root directory.")
    
    def importExtensions(self) -> None:
        for extension_id, (extension, _) in self.extensions.items():
            #with open(f"{extension.path}/main.py") as extensionFile:
            #    exec(extensionFile.read())
            #print([dir.path for dir in os.scandir(f"{extension.path}") if dir.is_dir()])
            spec = importlib.util.spec_from_file_location(extension_id, f"{extension.path}/main.py") # , submodule_search_locations=[dir.path for dir in os.scandir(f"{extension.path}") if dir.is_dir()]
            module = importlib.util.module_from_spec(spec)
            sys.modules[extension_id] = module
            spec.loader.exec_module(module)
            #self.extensions[extension_id] = (extension, module)