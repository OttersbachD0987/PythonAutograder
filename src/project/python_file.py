import ast
from ast import Module, Import, ImportFrom
import symtable
from symtable import SymbolTable
import tokenize
from tokenize import TokenInfo, TokenError
from .file_type import FileType
#from autograder import code_walker

class PythonFile(FileType):
    def __init__(self, a_path: str, a_name: str):
        super().__init__(a_path, a_name)

        try:
            with open(f"{a_path}\\{a_name}", "r") as file:
                self.contents: str = file.read()
                self.errors: list[tuple[str, str]] = []
                try:
                    self.ast: Module = ast.parse(self.contents, a_name)
                    #for node in ast.walk(self.ast):
                    #    if isinstance(node, Import):
                    #        for name in node.names:
                    #            print(f"{name.name} as {name.asname}")
                    #    elif isinstance(node, ImportFrom):
                    #        print(f"Level: {node.level}")
                    #        print(f"Module: {node.module}")
                    #        for name in node.names:
                    #            print(f"{name.name} as {name.asname}")

                    #print(f"---------")
                    self.imports = [name for node in ast.walk(self.ast) if isinstance(node, Import) for name in node.names]
                except SyntaxError as e:
                    print(f"Syntax error:\n{e}")
                    self.errors.append(("Syntax", f"{e.lineno}\xA1{e.end_lineno}\xA0{e.offset}\xA1{e.end_offset}\xA0{e.text}"))
                file.seek(0)
                try:
                    self.tokens: list[TokenInfo] = [token for token in tokenize.generate_tokens(file.read)]
                except TokenError as e:
                    print(f"Token error from {a_name}")
                    
                try:
                    self.symtable: SymbolTable = symtable.symtable(self.contents, self.name, "exec")
                except SyntaxError as e:
                    print(f"Syntax Error from {a_name}")
        except FileNotFoundError as e:
            print(f"The file {e.filename} does not exist.")
        except PermissionError as e:
            print(f"You do not have sufficient permissions to access the file {e.filename}.")
        except IsADirectoryError as e:
            print(f"{e.filename} is not a file, it is a directory.")
    
    def __repr__(self):
        return f"{self.path} | {self.name}"