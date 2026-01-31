from typing import Dict, List, Tuple, Optional, Set, Callable, Any, Union
from fuzzer import Fuzzer
from grammars import *
from derivation_tree import *
from opts import *
from grammar_fuzzer import *
from ebnf import *
import random

def main():
    expr_grammar = convert_ebnf_grammar(EXPR_EBNF_GRAMMAR)
    print (expr_grammar)

    f = GrammarFuzzer(expr_grammar, max_nonterminals=10)
    print (f.fuzz())

if __name__ == "__main__":
    main()
