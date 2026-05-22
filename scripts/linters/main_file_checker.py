import ast
import sys
import pathlib

# Disallowed node types
DISALLOWED = {
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.AsyncFor,
    ast.AsyncWith,
}

class MainFileChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit(self, node):
        if isinstance(node, tuple(DISALLOWED)):
            self.errors.append(f"Forbidden node type in src/main.py: {type(node).__name__}")
        self.generic_visit(node)

def check_main(path):
    with open(path, "r") as f:
        tree = ast.parse(f.read())
        checker = MainFileChecker()
        checker.visit(tree)
        return checker.errors

if __name__ == "__main__":
    path = pathlib.Path("src/main.py")
    errors = check_main(path)
    if errors:
        for error in errors:
            print(f"Error: {error}")
        sys.exit(1)
