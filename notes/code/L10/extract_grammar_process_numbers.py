# Code from The Fuzzing Book, https://www.fuzzingbook.org

from option_grammar_miner import *
from grammar_fuzzer import *
from process_numbers import *

miner = OptionGrammarMiner(process_numbers, log=True)
process_numbers_grammar = miner.mine_ebnf_grammar()
print (process_numbers_grammar)

assert is_valid_grammar(process_numbers_grammar)

grammar = convert_ebnf_grammar(process_numbers_grammar)
assert is_valid_grammar(grammar)

f = GrammarFuzzer(grammar)
for i in range(10):
    print(f.fuzz())
