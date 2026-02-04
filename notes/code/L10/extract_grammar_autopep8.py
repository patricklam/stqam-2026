# Code from The Fuzzing Book, https://www.fuzzingbook.org

import os
from option_grammar_miner import *
from grammar_fuzzer import *

def find_executable(name):
    for path in os.get_exec_path():
        qualified_name = os.path.join(path, name)
        if os.path.exists(qualified_name):
            return qualified_name
    return None

def autopep8():
    executable = find_executable("autopep8")

    # First line has to contain "/usr/bin/env python" or like
    first_line = open(executable).readline()
    assert first_line.find("python") >= 0

    contents = open(executable).read()
    exec(contents)

autopep8_miner = OptionGrammarMiner(autopep8)
autopep8_ebnf_grammar = autopep8_miner.mine_ebnf_grammar()

print (autopep8_ebnf_grammar["<option>"])
print (autopep8_ebnf_grammar["<line>"])
print (autopep8_ebnf_grammar["<arguments>"])
print (autopep8_ebnf_grammar["<files>"])

autopep8_ebnf_grammar["<arguments>"] = [" <files>"]
autopep8_ebnf_grammar["<files>"] = ["foo.py"]
assert is_valid_grammar(autopep8_ebnf_grammar)

autopep8_grammar = convert_ebnf_grammar(autopep8_ebnf_grammar)
assert is_valid_grammar(autopep8_grammar)

f = GrammarFuzzer(autopep8_grammar, max_nonterminals=4)
for i in range(10):
    print(f.fuzz())
