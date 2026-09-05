import re
from tools.calculator_tool import calculator

text = "Calculate 15% of 2,000,000."

match = re.search(
    r"(\d+(?:\.\d+)?)%\s+of\s+([\d,]+(?:\.\d+)?)",
    text,
    re.IGNORECASE
)

print("Match:", match.groups() if match else None)

if match:
    percentage = match.group(1)
    number = match.group(2).replace(",", "")
    expression = f"{percentage} * {number} / 100"

    print("Expression:", expression)
    print("Result:", calculator(expression))
