import ast
import re


class EasyLangError(Exception):
    pass


class EasyLang:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    # Convert text into a number, string, or existing variable value.
    def get_value(self, text):
        text = text.strip()

        if text in self.variables:
            return self.variables[text]

        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return text

    # Replace variable names inside sentences.
    def show_text(self, text):
        text = text.strip()

        if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
            text = text[1:-1]

        def replace_variable(match):
            word = match.group(0)
            if word in self.variables:
                return str(self.variables[word])
            return word

        return re.sub(r"\b[A-Za-z_]\w*\b", replace_variable, text)

    # Check an EasyLang condition.
    def check_condition(self, condition):
        pattern = (
            r"(.+?)\s+is\s+"
            r"(greater than|less than|equal to|not equal to|"
            r"at least|at most)\s+(.+)"
        )

        match = re.fullmatch(pattern, condition.strip(), re.IGNORECASE)

        if not match:
            raise EasyLangError(
                f"Invalid condition: {condition}"
            )

        left = self.get_value(match.group(1))
        operator = match.group(2).lower()
        right = self.get_value(match.group(3))

        try:
            if operator == "greater than":
                return left > right
            if operator == "less than":
                return left < right
            if operator == "equal to":
                return left == right
            if operator == "not equal to":
                return left != right
            if operator == "at least":
                return left >= right
            if operator == "at most":
                return left <= right

        except TypeError:
            raise EasyLangError(
                "Cannot compare these two values."
            )

    # Find the matching End and optional Else in a block.
    def find_block(self, lines, start):
        depth = 1
        else_position = None

        for i in range(start + 1, len(lines)):
            command = lines[i].strip()
            lower = command.lower()

            if (
                lower.startswith("if ")
                or lower.startswith("repeat ")
                or lower.startswith("while ")
                or lower.startswith("create function ")
            ):
                depth += 1

            elif lower == "end":
                depth -= 1

                if depth == 0:
                    return i, else_position

            elif lower == "else" and depth == 1:
                else_position = i

        raise EasyLangError(
            f"Missing End for block starting on line {start + 1}."
        )

    # Run a section of EasyLang code.
    def execute_lines(self, lines, start=0, stop=None):
        if stop is None:
            stop = len(lines)

        i = start

        while i < stop:
            original = lines[i]
            command = original.strip()
            lower = command.lower()

            if not command or command.startswith("#"):
                i += 1
                continue

            # SHOW
            if lower.startswith("show "):
                message = command[5:]
                print(self.show_text(message))
                i += 1
                continue

            # MAKE
            if lower.startswith("make "):
                match = re.fullmatch(
                    r"Make\s+([A-Za-z_]\w*)\s*=\s*(.+)",
                    command,
                    re.IGNORECASE
                )

                if not match:
                    raise EasyLangError(
                        f"Invalid Make command on line {i + 1}."
                    )

                name = match.group(1)
                value = self.get_value(match.group(2))
                self.variables[name] = value

                i += 1
                continue

            # ADD
            arithmetic = re.fullmatch(
                r"Add\s+(.+?)\s+and\s+(.+?)\s+into\s+([A-Za-z_]\w*)",
                command,
                re.IGNORECASE
            )

            if arithmetic:
                a = self.get_value(arithmetic.group(1))
                b = self.get_value(arithmetic.group(2))
                result_name = arithmetic.group(3)
                self.variables[result_name] = a + b
                i += 1
                continue

            # SUBTRACT
            arithmetic = re.fullmatch(
                r"Subtract\s+(.+?)\s+from\s+(.+?)\s+into\s+([A-Za-z_]\w*)",
                command,
                re.IGNORECASE
            )

            if arithmetic:
                a = self.get_value(arithmetic.group(1))
                b = self.get_value(arithmetic.group(2))
                result_name = arithmetic.group(3)
                self.variables[result_name] = b - a
                i += 1
                continue

            # MULTIPLY
            arithmetic = re.fullmatch(
                r"Multiply\s+(.+?)\s+and\s+(.+?)\s+into\s+([A-Za-z_]\w*)",
                command,
                re.IGNORECASE
            )

            if arithmetic:
                a = self.get_value(arithmetic.group(1))
                b = self.get_value(arithmetic.group(2))
                result_name = arithmetic.group(3)
                self.variables[result_name] = a * b
                i += 1
                continue

            # DIVIDE
            arithmetic = re.fullmatch(
                r"Divide\s+(.+?)\s+(?:and|by)\s+(.+?)\s+into\s+([A-Za-z_]\w*)",
                command,
                re.IGNORECASE
            )

            if arithmetic:
                a = self.get_value(arithmetic.group(1))
                b = self.get_value(arithmetic.group(2))

                if b == 0:
                    raise EasyLangError("Cannot divide by zero.")

                result_name = arithmetic.group(3)
                self.variables[result_name] = a / b
                i += 1
                continue

            # ASK FOR USER INPUT
            ask = re.fullmatch(
                r"Ask\s+(.+?)\s+and\s+store\s+it\s+as\s+([A-Za-z_]\w*)",
                command,
                re.IGNORECASE
            )

            if ask:
                question = self.show_text(ask.group(1))
                answer = input(question + " ")
                self.variables[ask.group(2)] = answer
                i += 1
                continue

            # IF / ELSE
            if lower.startswith("if "):
                end, else_position = self.find_block(lines, i)
                condition = command[3:].strip()

                if self.check_condition(condition):
                    body_end = else_position if else_position is not None else end
                    self.execute_lines(lines, i + 1, body_end)
                elif else_position is not None:
                    self.execute_lines(lines, else_position + 1, end)

                i = end + 1
                continue

            # REPEAT
            if lower.startswith("repeat "):
                match = re.fullmatch(
                    r"Repeat\s+(.+?)\s+times",
                    command,
                    re.IGNORECASE
                )

                if not match:
                    raise EasyLangError(
                        f"Invalid Repeat command on line {i + 1}."
                    )

                count = self.get_value(match.group(1))

                if not isinstance(count, int) or count < 0:
                    raise EasyLangError(
                        "Repeat requires a non-negative whole number."
                    )

                end, _ = self.find_block(lines, i)

                if count > 10000:
                    raise EasyLangError(
                        "Repeat limit is 10,000 times."
                    )

                for _ in range(count):
                    self.execute_lines(lines, i + 1, end)

                i = end + 1
                continue

            # WHILE
            if lower.startswith("while "):
                end, _ = self.find_block(lines, i)
                condition = command[6:].strip()
                count = 0

                while self.check_condition(condition):
                    self.execute_lines(lines, i + 1, end)
                    count += 1

                    if count >= 10000:
                        raise EasyLangError(
                            "While loop stopped after 10,000 repetitions."
                        )

                i = end + 1
                continue

            # CREATE FUNCTION
            if lower.startswith("create function "):
                match = re.fullmatch(
                    r"Create\s+function\s+([A-Za-z_]\w*)"
                    r"(?:\s+with\s+(.+))?",
                    command,
                    re.IGNORECASE
                )

                if not match:
                    raise EasyLangError(
                        f"Invalid function declaration on line {i + 1}."
                    )

                function_name = match.group(1).lower()
                parameter_text = match.group(2)

                parameters = []

                if parameter_text:
                    parameters = [
                        item.strip()
                        for item in re.split(
                            r"\s+and\s+",
                            parameter_text,
                            flags=re.IGNORECASE
                        )
                    ]

                if len(parameters) != len(set(parameters)):
                    raise EasyLangError(
                        "Function parameter names must be unique."
                    )

                if any(
                    not re.fullmatch(r"[A-Za-z_]\w*", p)
                    for p in parameters
                ):
                    raise EasyLangError(
                        "Invalid function parameter name."
                    )

                end, _ = self.find_block(lines, i)

                self.functions[function_name] = (
                    parameters,
                    lines[i + 1:end]
                )

                i = end + 1
                continue

            # CALL FUNCTION
            if lower.startswith("call "):
                match = re.fullmatch(
                    r"Call\s+([A-Za-z_]\w*)"
                    r"(?:\s+with\s+(.+))?",
                    command,
                    re.IGNORECASE
                )

                if not match:
                    raise EasyLangError(
                        f"Invalid Call command on line {i + 1}."
                    )

                function_name = match.group(1).lower()
                argument_text = match.group(2)

                if function_name not in self.functions:
                    raise EasyLangError(
                        f"Function '{function_name}' does not exist."
                    )

                parameters, function_lines = self.functions[function_name]

                arguments = []

                if argument_text:
                    arguments = [
                        self.get_value(item.strip())
                        for item in re.split(
                            r"\s+and\s+",
                            argument_text,
                            flags=re.IGNORECASE
                        )
                    ]

                if len(arguments) != len(parameters):
                    raise EasyLangError(
                        f"Function '{function_name}' needs "
                        f"{len(parameters)} input(s), but received "
                        f"{len(arguments)}."
                    )

                old_values = {}

                for parameter, argument in zip(parameters, arguments):
                    old_values[parameter] = (
                        parameter in self.variables,
                        self.variables.get(parameter)
                    )
                    self.variables[parameter] = argument

                try:
                    self.execute_lines(function_lines)
                finally:
                    for parameter, (existed, old_value) in old_values.items():
                        if existed:
                            self.variables[parameter] = old_value
                        else:
                            self.variables.pop(parameter, None)

                i += 1
                continue

            raise EasyLangError(
                f"Unknown command on line {i + 1}: {command}"
            )


def execute_program(lines):
    language = EasyLang()

    try:
        language.execute_lines(lines)
    except EasyLangError as error:
        print(f"EasyLang Error: {error}")
    except Exception as error:
        print(f"EasyLang Error: {error}")