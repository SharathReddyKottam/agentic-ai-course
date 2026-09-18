import ast
import textwrap

def show_tree(code: str) -> None:
    """Pretty-print an AST node tree with indentation."""
    print("\n--- SOURCE ---")
    print(code.strip())
    print("\n--- AST dump ---")
    tree = ast.parse(code)
    print(ast.dump(tree, indent=2))

# Example 1: Simple expression
print("=" * 60)
print("EXAMPLE 1: Simple Expression")
print("=" * 60)
show_tree("x = 1 + 2")

# Example 2: Function definition
print("\n" + "=" * 60)
print("EXAMPLE 2: Function Definition")
print("=" * 60)
show_tree("""
def greet(name: str) -> str:
    return f"Hello, {name}!"
""")

# Example 3: Class definition
print("\n" + "=" * 60)
print("EXAMPLE 3: Class Definition")
print("=" * 60)
show_tree("""
class User:
    def __init__(self, name: str):
        self.name = name
    
    def get_name(self) -> str:
        return self.name
""")
