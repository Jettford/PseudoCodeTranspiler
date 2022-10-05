# Pearson Pseudocode Transpiler
import click

from transpiler import Transpiler
from transpiler.tokenizer import Tokenizer


# TODOs:
# - Add Error checking

@click.command()
@click.argument('input_path')
@click.argument('output_path')
def transpile(input_path, output_path):
    input = open(input_path, "r")

    tokenizer = Tokenizer()
    tokenizer.tokenize(input.read())

    transpiler = Transpiler()
    transpiler.transpile(tokenizer.token_list, output_path)

    input.close()


if __name__ == "__main__":
    transpile()
