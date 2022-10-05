# PseudoCodeTranspiler

[Pearson Standard Pseudocode](https://tools.withcode.uk/ks4pseudo/media/edexcel_pseudocode.pdf) transpiler to generate python source code.
Implements the standard exactly and creates executable source code.


## Installation
Install pip requirements:
```shell
pip install -r requirements.txt
```

Execute the main.py file with the following arguments:
```shell
Usage: main.py [OPTIONS] INPUT_PATH OUTPUT_PATH
```
This will convert an input pseudocode file into an executable python file

## Issues
At the moment the standard will transpile perfectly fine and the code will run perfectly fine however there is very
little error checking so most mistypes or syntax issues will not be picked up, and you will end up with malformed output
or failed execution during the transpilation.