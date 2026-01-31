from typing import Dict, List, Tuple, Optional, Set, Callable, Any, Union
from fuzzer import Fuzzer
from grammars import *
from derivation_tree import *
from opts import *
from grammar_fuzzer import *
import random

def main():
    f = GrammarFuzzer(EXPR_GRAMMAR)
    print (f.fuzz())
    #f = GrammarFuzzer(URL_GRAMMAR)
    #print (f.fuzz())
    #f = GrammarFuzzer(CGI_GRAMMAR)
    #print (f.fuzz())

if __name__ == "__main__":
    main()
