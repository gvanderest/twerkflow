import ast
import os
import sys

def check_file(filename):
    with open(filename, "r") as f:
        tree = ast.parse(f.read())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    # Count arguments, excluding 'self'
                    args = [a for a in item.args.args if a.arg != 'self']
                    
                    if len(args) > 3:
                        # Check if any argument ends in 'Config'
                        has_config = any(arg.arg.endswith('Config') for arg in args)
                        if not has_config:
                            print(f"{filename}:{item.lineno}: Constructor has {len(args)} arguments (>3). "
                                  f"Please use a Pydantic *Config class.")
                            return False
    return True

if __name__ == "__main__":
    success = True
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                if not check_file(os.path.join(root, file)):
                    success = False
    
    if not success:
        sys.exit(1)
    sys.exit(0)
