# Stack-Based Mathematical Expression Evaluator

## Overview
This assignment uses a Python program that reads mathematical expressions from `input.txt`, evaluates them using stack data structures, and writes results to `output.txt`.


## Files
- `main.py` — stack implementation, expression parser, evaluator, and file handling
- `input.txt` — sample expressions, one per line
- `output.txt` — generated results
- `REPORT.docx` — written assignment report

## How to run
1. Put `main.py` and `input.txt` in the same folder.
2. Open that folder in Visual Studio Code.
3. Open the terminal in VS Code (`Terminal` → `New Terminal`).
4. Run:

   ```bash
   python main.py
   ```

5. Open `output.txt` to see the results.


## Input format
- Put one arithmetic expression on each line.
- Use `+`, `-`, `*`, `/`, and parentheses.
- Decimal and negative numbers are supported.
- A separator line made up of three or more hyphens (for example `-----`) is preserved in the output.
- Blank lines are preserved.

## Output format
Each expression is replaced by its result. Separator and blank lines remain in the same positions. Invalid expressions and division by zero produce an error message on that line, allowing the program to continue processing later lines.

## Implementation notes
- `Stack` provides `push`, `pop`, `peek`, `is_empty`, and `size`.
- The shunting-yard algorithm converts infix expressions to postfix notation while respecting parentheses and operator precedence.
- Postfix expressions are evaluated with a second stack.
- The program does not use Python's `eval()`.

## Assumptions and limitations
- Supported operators are addition, subtraction, multiplication, and division.
- Exponents, variables, and functions such as `sin()` are not supported.
- Expressions should use standard arithmetic notation; implicit multiplication like `2(3+4)` is not supported.
- The sample input includes division by zero to demonstrate error handling; remove or replace that line if your lecturer expects every sample line to be a valid expression.
