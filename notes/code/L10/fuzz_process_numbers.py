# Code from The Fuzzing Book, https://www.fuzzingbook.org

from grammars import *
from ebnf import *
from grammar_fuzzer import *
from process_numbers import *

PROCESS_NUMBERS_EBNF_GRAMMAR: Grammar = {
    "<start>": ["<operator> <integers>"],
    "<operator>": ["--sum", "--min", "--max"],
    "<integers>": ["<integer>", "<integers> <integer>"],
    "<integer>": ["<digit>+"],
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(PROCESS_NUMBERS_EBNF_GRAMMAR)
PROCESS_NUMBERS_GRAMMAR = convert_ebnf_grammar(PROCESS_NUMBERS_EBNF_GRAMMAR)

if __name__ == "__main__":
    f = GrammarFuzzer(PROCESS_NUMBERS_GRAMMAR, min_nonterminals=10)
    for i in range(3):
        args = f.fuzz().split()
        print(args)
        process_numbers(args)
