from google.genai import types


TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="calculator",
        description="Calculate a mathematical expression safely.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "expression": types.Schema(
                    type="STRING",
                    description="Mathematical expression to calculate."
                )
            },
            required=["expression"],
        ),
    ),

    types.FunctionDeclaration(
        name="run_python",
        description="Execute restricted Python code for calculations and data analysis.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "code": types.Schema(
                    type="STRING",
                    description="Python code to execute."
                )
            },
            required=["code"],
        ),
    ),

    types.FunctionDeclaration(
        name="read_file",
        description="Read an allowed file from the documents folder.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "filename": types.Schema(
                    type="STRING",
                    description="Name of the file to read."
                )
            },
            required=["filename"],
        ),
    ),
]


TOOL = types.Tool(
    function_declarations=TOOL_DECLARATIONS
)
