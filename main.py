# Pearson Pseudocode Transpiler
import os
import click

from transpiler import Transpiler
from transpiler.tokenizer import Tokenizer


# TODOs:
# - Add Error checking

@click.command()
@click.argument('input_path')
@click.argument('output_path', default="null")
def transpile(input_path, output_path):
    if not os.path.exists(input_path):
        print("Failed to find the input file")
        exit(1)

    input_data = open(input_path, "r")

    if output_path == "null":
        if not os.path.exists("output"): 
            os.mkdir("output")
        output_path = "output/" + os.path.basename(input_path) + ".py"

    tokenizer = Tokenizer()
    tokenizer.tokenize(input_data.read())

    transpiler = Transpiler()
    transpiler.transpile(tokenizer.token_list, output_path)

    input_data.close()


if __name__ == "__main__":
    transpile()
