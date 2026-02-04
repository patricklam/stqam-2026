# Code from The Fuzzing Book, https://www.fuzzingbook.org

from itertools import combinations

import os
from option_grammar_miner import *
from grammar_fuzzer import *
from ebnf import *

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
autopep8_grammar = convert_ebnf_grammar(autopep8_ebnf_grammar)
option_list = autopep8_ebnf_grammar["<option>"]
pairs = list(combinations(option_list, 2))
print (len(pairs))
print (pairs[:20])

def pairwise(option_list):
    return [option_1 + option_2
            for (option_1, option_2) in combinations(option_list, 2)]

pairwise_autopep8_grammar = extend_grammar(autopep8_grammar)
pairwise_autopep8_grammar["<option>"] = pairwise(autopep8_grammar["<option>"])
assert is_valid_grammar(pairwise_autopep8_grammar)

pairwise_autopep8_fuzzer = GrammarFuzzer(pairwise_autopep8_grammar, max_nonterminals=4)
for i in range(10):
    print (pairwise_autopep8_fuzzer.fuzz())
