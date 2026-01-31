from typing import Tuple, List, Optional, Any, Union, Set, Callable, Dict
from ebnf import EXPR_EBNF_GRAMMAR, convert_ebnf_grammar
from simple_grammar_fuzzer import simple_grammar_fuzzer
from grammars import Grammar, Expansion
from grammars import is_valid_grammar
from opts import exp_string

def main():
    expr_grammar = convert_ebnf_grammar(EXPR_EBNF_GRAMMAR)
    print (expr_grammar)

    from expect_error import ExpectTimeout
    with ExpectTimeout(1):
        simple_grammar_fuzzer(grammar=expr_grammar, max_nonterminals=3)

if __name__ == "__main__":
    main()
