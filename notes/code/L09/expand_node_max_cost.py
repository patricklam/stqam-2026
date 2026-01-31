from typing import Dict, List, Tuple, Optional, Set, Callable, Any, Union
from fuzzer import Fuzzer
from grammars import *
from derivation_tree import *
from opts import *
from grammar_fuzzer import *
import random

def main():
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)

    f.expand_node = f.expand_node_max_cost

    derivation_tree = ("<start>",
                   [("<expr>",
                     [("<expr>", None),
                      (" + ", []),
                         ("<term>", None)]
                     )])
    print (derivation_tree)
    print (all_terminals(derivation_tree))

    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    print (derivation_tree)
    print (all_terminals(derivation_tree))

    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    print (derivation_tree)
    print (all_terminals(derivation_tree))

    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    print (derivation_tree)
    print (all_terminals(derivation_tree))

    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    print (derivation_tree)
    print (all_terminals(derivation_tree))

if __name__ == "__main__":
    main()
