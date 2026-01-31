from typing import Dict, List, Tuple, Optional, Set, Callable, Any, Union
from fuzzer import Fuzzer
from grammars import *
from derivation_tree import *
from opts import *
from grammar_fuzzer import *
import random

def main():
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)

    print("Before expand_node_randomly():")
    expr_tree = ("<integer>", None)
    print (expr_tree)
    print (display_tree(expr_tree))

    expr_tree = f.expand_node_randomly(expr_tree)
    print("After expand_node_randomly():")
    print (expr_tree)
    print (display_tree(expr_tree))

if __name__ == "__main__":
    main()
