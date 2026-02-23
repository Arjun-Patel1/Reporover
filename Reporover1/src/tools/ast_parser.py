import ast

class ASTParserTool:
    @staticmethod
    def validate_code(code: str):
        """
        Checks if the provided Python code string has valid syntax.
        
        Returns:
            dict: {"valid": bool, "error": str or None}
        """
        try:
            ast.parse(code)
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {
                "valid": False, 
                "error": f"SyntaxError on line {e.lineno}: {e.msg}"
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

if __name__ == "__main__":
    # Test valid code
    code_good = "def hello():\n    print('world')"
    print(f"Good Code: {ASTParserTool.validate_code(code_good)}")

    # Test invalid code (missing colon)
    code_bad = "def hello()\n    print('world')"
    print(f"Bad Code:  {ASTParserTool.validate_code(code_bad)}")