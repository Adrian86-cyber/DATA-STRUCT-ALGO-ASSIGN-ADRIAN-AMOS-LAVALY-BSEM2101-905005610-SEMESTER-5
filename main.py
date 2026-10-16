"""
Stack-based Mathematical Expression Evaluator
"""

import re
from pathlib import Path


class Stack:
    """A simple last-in, first-out stack (LIFO)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


TOKEN_PATTERN = re.compile(r"\d+(?:\.\d+)?|[()+\-*/]")


def tokenize(expression):
    """Convert an expression into number, operator, and parenthesis tokens."""
    expression = expression.replace(" ", "").replace("\t", "")
    if not expression:
        raise ValueError("Expression is empty.")

    tokens = TOKEN_PATTERN.findall(expression)
    if "".join(tokens) != expression:
        raise ValueError(f"Invalid character or malformed number in: {expression}")

    # Identify unary + and - (for example, -5 or 3 * -2).
    normalized = []
    previous = None
    for token in tokens:
        if token in ("+", "-") and (
            previous is None or previous in ("+", "-", "*", "/", "(", "u+", "u-")
        ):
            token = "u" + token
        normalized.append(token)
        previous = token
    return normalized


def to_postfix(tokens):
    """Use the shunting-yard algorithm to convert infix tokens to postfix."""
    output = []
    operators = Stack()
    precedence = {"u+": 3, "u-": 3, "*": 2, "/": 2, "+": 1, "-": 1}
    right_associative = {"u+", "u-"}

    expect_operand = True
    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            if not expect_operand:
                raise ValueError("Missing operator between numbers.")
            output.append(token)
            expect_operand = False
        elif token == "(":
            if not expect_operand:
                raise ValueError("Missing operator before '('.")
            operators.push(token)
            expect_operand = True
        elif token == ")":
            if expect_operand:
                raise ValueError("Unexpected ')' or missing operand.")
            found_open = False
            while not operators.is_empty():
                top = operators.pop()
                if top == "(":
                    found_open = True
                    break
                output.append(top)
            if not found_open:
                raise ValueError("Mismatched parentheses.")
            expect_operand = False
        elif token in precedence:
            if token not in ("u+", "u-") and expect_operand:
                raise ValueError(f"Operator '{token}' is missing a left operand.")
            while not operators.is_empty() and operators.peek() in precedence:
                top = operators.peek()
                should_pop = (
                    precedence[top] > precedence[token]
                    or (precedence[top] == precedence[token]
                        and token not in right_associative)
                )
                if not should_pop:
                    break
                output.append(operators.pop())
            operators.push(token)
            expect_operand = True
        else:
            raise ValueError(f"Unknown token: {token}")

    if expect_operand:
        raise ValueError("Expression ends with an operator or is incomplete.")

    while not operators.is_empty():
        top = operators.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses.")
        output.append(top)
    return output


def evaluate_postfix(postfix):
    """Evaluate postfix tokens using a stack."""
    values = Stack()
    for token in postfix:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            values.push(float(token))
        elif token in ("u+", "u-"):
            if values.size() < 1:
                raise ValueError("Unary operator is missing an operand.")
            value = values.pop()
            values.push(value if token == "u+" else -value)
        else:
            if values.size() < 2:
                raise ValueError(f"Operator '{token}' is missing an operand.")
            right = values.pop()
            left = values.pop()
            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            elif token == "/":
                if right == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = left / right
            else:
                raise ValueError(f"Unsupported operator: {token}")
            values.push(result)

    if values.size() != 1:
        raise ValueError("Invalid expression.")
    return values.pop()


def evaluate_expression(expression):
    """Evaluate one infix expression and return a clean numeric string."""
    result = evaluate_postfix(to_postfix(tokenize(expression)))
    if result.is_integer():
        return str(int(result))
    return f"{result:.10g}"


def is_separator(line):
    """Treat a line made only of at least three hyphens as a separator."""
    stripped = line.strip()
    return len(stripped) >= 3 and all(char == "-" for char in stripped)


def process_files(input_path="input.txt", output_path="output.txt"):
    """Evaluate each non-separator line and preserve separator lines."""
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file '{input_file}' was not found. "
            "Place it in the same folder as main.py."
        )

    output_lines = []
    for line_number, raw_line in enumerate(
        input_file.read_text(encoding="utf-8").splitlines(), start=1
    ):
        stripped = raw_line.strip()
        if not stripped:
            output_lines.append("")
        elif is_separator(raw_line):
            output_lines.append(raw_line)
        else:
            try:
                output_lines.append(evaluate_expression(stripped))
            except (ValueError, ZeroDivisionError, IndexError) as error:
                output_lines.append(f"ERROR on line {line_number}: {error}")

    output_file.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print(f"Finished. Results have been written to '{output_file}'.")


if __name__ == "__main__":
    try:
        process_files()
    except (FileNotFoundError, OSError) as error:
        print(f"File error: {error}")
