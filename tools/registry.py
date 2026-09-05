from tools.calculator_tool import calculator
from tools.python_tool import run_python
from tools.file_tool import read_file


TOOLS = {
    "calculator": calculator,
    "run_python": run_python,
    "read_file": read_file,
}


def get_tool(name):
    return TOOLS.get(name)
