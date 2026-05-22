import ast
import sys
import pathlib

# List of forbidden patterns (as strings for simple matching)
FORBIDDEN = {"patch", "monkeypatch"}

class ForbiddenVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.errors = []

    def visit_Call(self, node):
        # Detect: patch(...)
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN:
            self.report(node, f"Forbidden call: {node.func.id}")
        # Detect: unittest.mock.patch(...)
        elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN:
            self.report(node, f"Forbidden call: {node.func.attr}")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Detect: @patch(...)
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id in FORBIDDEN:
                self.report(node, f"Forbidden decorator: @{decorator.func.id}")
            elif isinstance(decorator, ast.Name) and decorator.id in FORBIDDEN:
                self.report(node, f"Forbidden decorator: @{decorator.id}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Detect: from unittest.mock import patch
        if node.module and "mock" in node.module or node.module == "unittest":
            for alias in node.names:
                if alias.name in FORBIDDEN:
                    self.report(node, f"Forbidden import: {alias.name}")
        self.generic_visit(node)

    def report(self, node, message):
        self.errors.append(f"{self.filename}:{node.lineno}: {message}")

def check_file(path):
    with open(path, "r") as f:
        tree = ast.parse(f.read())
        visitor = ForbiddenVisitor(path)
        visitor.visit(tree)
        return visitor.errors

if __name__ == "__main__":
    paths = list(pathlib.Path("src").rglob("*.py")) + list(pathlib.Path("tests").rglob("*.py"))
    all_errors = []
    
    # Exclude conftest.py as allowed by current standard
    paths = [p for p in paths if p.name != "conftest.py"]
    
    for path in paths:
        all_errors.extend(check_file(path))
        
    if all_errors:
        for error in all_errors:
            print(f"Error: {error}")
        sys.exit(1)
