from .tokenizer import Tokenizer


class Transpiler:

    def __init__(self):
        self.skip = 0
        self.token_list = []
        self.output = None
        self.indent_level = 0

        self.functions = []

    def get_next_token(self, i, move=1) -> str:
        self.skip += (1 * move)
        return self.token_list[i + self.skip]

    def get_current_token(self, i) -> str:
        return self.token_list[i + self.skip]

    def has_another_token(self, i) -> bool:
        return len(self.token_list) > (i + self.skip + 1)

    def step_back_a_token(self, count=1) -> None:
        self.skip -= 1 * count

    def step_forward_a_token(self, count=1) -> None:
        self.skip += 1 * count

    def write(self, value) -> None:
        self.output.write(("\t" * self.indent_level) + value + "\n")

    @staticmethod
    def pseudo_type_to_py_type(type) -> str:
        typeMap = {
            "integer": "int",
            "real": "float",
            "string": "str",
            "array": "array",
            "character": "str",
            "boolean": "bool"
        }

        if not type.lower() in typeMap:
            raise Exception(f"Unknown type: {type}")

        return typeMap[type.lower()]

    def is_operator(self, i) -> bool:
        operatorList = [
            "set", "send", "receive", "if", "else", "end", "repeat", "until",
            "while", "for", "each", "from", "to", "do", "read", "write",
            "then", "step", "procedure", "function", "return"
        ]

        return self.get_current_token(i).lower() in operatorList

    def transpile(self, tokens, output_file):
        self.output = open(output_file, "w")
        self.token_list = tokens

        for i in range(len(self.token_list)):
            item = self.token_list[i].lower()

            if self.skip > 0:
                self.skip -= 1
                continue

            print("Transpiling command", self.token_list[i])

            match item:
                case "set":
                    variableName = self.get_next_token(i)
                    self.get_next_token(i)  # Literally just the 'TO' operator
                    setValues = []

                    while True:
                        if not self.has_another_token(i):
                            break

                        token = self.get_next_token(i)

                        if self.is_operator(i):
                            self.step_back_a_token()
                            break

                        token = token.replace("=", "==")

                        if token.lower() in self.functions:
                            setValues.append(token + self.get_next_token(i))
                        else:
                            setValues.append(token)

                    self.write(variableName + " = " + ' '.join(setValues))
                case "send":
                    data = []

                    while True:
                        if not self.has_another_token(i):
                            break

                        token = self.get_next_token(i)

                        if self.is_operator(i):
                            break

                        data.append(token)

                    location = self.get_next_token(i).lower()

                    if location == "display":
                        self.write(f"print({' '.join(data)})")
                case "receive":
                    variableName = self.get_next_token(i)
                    self.get_next_token(i)  # Ignore
                    type = self.pseudo_type_to_py_type(
                        self.get_next_token(i).strip("()[]{}"))
                    inputDevice = self.get_next_token(i)

                    if inputDevice == "keyboard":
                        self.write(
                            f"{variableName} = {type}(input('Please input {variableName}: '))"
                        )
                case "read":
                    fileName = self.get_next_token(i)
                    variableToReadInto = self.get_next_token(i)

                    self.write(
                        f"{variableToReadInto} = open('{fileName}', 'r').read()")

                case "write":
                    fileName = self.get_next_token(i)
                    insideOfArray = "["

                    while True:
                        if not self.has_another_token(i):
                            break

                        token = self.get_next_token(i)

                        if self.is_operator(i):
                            break

                        insideOfArray += token

                    self.step_back_a_token()

                    insideOfArray += "]"
                    self.write(f"file = open('{fileName}', 'w')")
                    self.write(f"for item in {insideOfArray}:")
                    self.write("\tfile.write(str(item))")

                case "const":
                    type = self.pseudo_type_to_py_type(self.get_next_token(i))
                    variableName = self.get_next_token(i)
                    self.write(f"{variableName}: {type}")

                case "if":
                    condition = []

                    while True:
                        if not self.has_another_token(i):
                            break

                        token = self.get_next_token(i)

                        if self.is_operator(i):
                            break

                        token = token.replace("=", "==")

                        if token.lower() in self.functions:
                            condition.append(token + self.get_next_token(i))
                        else:
                            condition.append(token)

                    self.write(f"if {' '.join(condition)}:")
                    self.indent_level += 1

                case "end":
                    endCondition = self.get_next_token(i).lower()

                    if endCondition in ["while", "if", "procedure", "function", "for", "foreach", "repeat"]:
                        self.indent_level -= 1

                    self.write("")  # Just add some indenting for readability

                case "else":
                    self.indent_level -= 1
                    self.write("else:")
                    self.indent_level += 1

                case "while":
                    condition = []

                    while True:
                        if not self.has_another_token(i):
                            break

                        token = self.get_next_token(i)

                        if self.is_operator(i):
                            break

                        token = token.replace("=", "==")

                        condition.append(token)

                    self.write(f"while {' '.join(condition)}:")
                    self.indent_level += 1

                case "repeat":
                    if self.get_next_token(i, 2) == "TIMES":
                        self.step_back_a_token()
                        self.write(f"for _ in range({self.get_current_token(i)}):")
                        self.step_forward_a_token()
                    else:
                        self.write("while True:")
                        self.step_back_a_token(2)
                    self.indent_level += 1

                case "for":
                    if self.get_next_token(i) == "EACH":
                        itemId = self.get_next_token(i)
                        self.step_forward_a_token()
                        sourceArray = self.get_next_token(i)
                        self.step_forward_a_token()

                        self.write(f"for {itemId} in {sourceArray}:")
                        self.indent_level += 1

                        continue

                    self.step_back_a_token()

                    hasStep = False
                    step = ""

                    indexName = self.get_next_token(i)
                    self.step_forward_a_token()
                    start = self.get_next_token(i)
                    self.step_forward_a_token()
                    end = self.get_next_token(i)

                    if self.get_next_token(i) == "STEP":
                        step = self.get_next_token(i)
                        hasStep = True
                        self.step_forward_a_token()

                    writeValue = f"for {indexName} in range({start}, {end}"

                    if hasStep:
                        writeValue += f", {step}):"
                    else:
                        writeValue += "):"

                    self.write(writeValue)
                    self.indent_level += 1

                case "until":
                    condition = []

                    while True:
                        if not self.has_another_token(i):
                            break

                        token = self.get_next_token(i)

                        if self.is_operator(i):
                            break

                        token = token.replace("=", "==")

                        condition.append(token)
                    self.step_back_a_token()

                    self.write(f"if {' '.join(condition)}:")
                    self.indent_level += 1
                    self.write(f"break")
                    self.indent_level -= 2

                    self.write("")

                case "procedure":
                    functionName = self.get_next_token(i)
                    params = self.get_next_token(i)

                    self.step_forward_a_token(2)

                    self.write(f"def {functionName}{params}:")
                    self.indent_level += 1

                    self.functions.append(functionName.lower())

                case "function":
                    functionName = self.get_next_token(i)
                    params = self.get_next_token(i)

                    self.step_forward_a_token(2)

                    self.write(f"def {functionName}{params}:")
                    self.indent_level += 1

                    self.functions.append(functionName.lower())

                case "return":
                    self.write(f"return {self.get_next_token(i)}")

            if item in self.functions:
                self.write(f"{self.get_current_token(i)}{self.get_next_token(i)}")
                self.write("")

        self.output.close()
