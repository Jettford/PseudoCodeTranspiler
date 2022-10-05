class Tokenizer:
    def __init__(self):
        self.token_list = []

    def add_to_token_list(self, item):
        if not len(item) > 0:
            return

        self.token_list.append(item)

    def tokenize(self, input):
        for line in input.split("\n"):
            line = line.lstrip()

            parsingCluster = False
            exitToAwait = ""
            characterMap = {
                "[": "]",
                "(": ")",
                "'": "'",
                '"': '"',
                "{": "}"
            }

            lastReadWord = ""

            for i in range(len(line)):
                char = line[i]

                if lastReadWord == " ":
                    lastReadWord = ""

                if char == "#":
                    break

                if char == " " and not parsingCluster:
                    self.add_to_token_list(lastReadWord)
                    lastReadWord = ""
                    continue

                if char in characterMap and not parsingCluster:
                    parsingCluster = True
                    exitToAwait = characterMap[char]

                lastReadWord += char

                if char == exitToAwait and not lastReadWord in characterMap:
                    parsingCluster = False
                    self.add_to_token_list(lastReadWord)
                    lastReadWord = ""

            if len(lastReadWord) > 0:
                self.add_to_token_list(lastReadWord)
