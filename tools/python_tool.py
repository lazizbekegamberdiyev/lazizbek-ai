import ast
import subprocess
import sys


BLOCKED_MODULES = {
    "os",
    "sys",
    "subprocess",
    "shutil",
    "socket",
    "requests",
    "urllib",
    "pathlib",
}

MAX_CODE_LENGTH = 5000
TIMEOUT_SECONDS = 10
MAX_OUTPUT_LENGTH = 10000


def validate_code(code):
    if len(code) > MAX_CODE_LENGTH:
        raise ValueError(
            f"Code is too long. Maximum is {MAX_CODE_LENGTH} characters."
        )

    tree = ast.parse(code, mode="exec")

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]

                if module in BLOCKED_MODULES:
                    raise ValueError(
                        f"Import blocked: {module}"
                    )

        if isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]

            if module in BLOCKED_MODULES:
                raise ValueError(
                    f"Import blocked: {module}"
                )

    return True


def run_python(code):
    try:
        validate_code(code)

        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS
        )

        output = result.stdout

        if result.returncode != 0:
            output = f"Error:\n{result.stderr}"

        if len(output) > MAX_OUTPUT_LENGTH:
            output = (
                output[:MAX_OUTPUT_LENGTH]
                + "\n...[output truncated]"
            )

        return output

    except SyntaxError as e:
        return f"Syntax Error: {e}"

    except ValueError as e:
        return f"Security Error: {e}"

    except subprocess.TimeoutExpired:
        return "Error: Python execution timed out."

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":

    print("Normal execution:")
    print(run_python("print(2 + 3)"))

    print("\nBlocked import:")
    print(run_python("import os"))

    print("\nLong code:")
    print(run_python("x = " + "1" * 5001))

    print("\nOutput limit:")
    print(run_python("print('A' * 12000)"))
