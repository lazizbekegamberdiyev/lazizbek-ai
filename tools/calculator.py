import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

                raise ValueError("Only numbers are allowed.")

            if isinstance(node, ast.BinOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Operator is not supported.")

                left = evaluate(node.left)
                right = evaluate(node.right)

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Operator is not supported.")

                return operation(evaluate(node.operand))

            raise ValueError("Invalid mathematical expression.")

        return evaluate(tree.body)

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(calculate("15 * 2000000 / 100"))
    print(calculate("(100 + 50) * 2"))
    print(calculate("2 ** 10"))
