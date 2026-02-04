# Code from The Fuzzing Book, https://www.fuzzingbook.org

from typing import Dict, List, Any
from grammars import *
type Option = Dict[str, Any]

def opts(**kwargs: Any) -> Dict[str, Any]:
    return kwargs

def exp_string(expansion: Expansion) -> str:
    """Return the string to be expanded"""
    if isinstance(expansion, str):
        return expansion
    return expansion[0]

def exp_opts(expansion: Expansion) -> Dict[str, Any]:
    """Return the options of an expansion.  If options are not defined, return {}"""
    if isinstance(expansion, str):
        return {}
    return expansion[1]

def exp_opt(expansion: Expansion, attribute: str) -> Any:
    """Return the given attribution of an expansion.
    If attribute is not defined, return None"""
    return exp_opts(expansion).get(attribute, None)

def set_opts(grammar: Grammar, symbol: str, expansion: Expansion, 
             opts: Option = {}) -> None:
    """Set the options of the given expansion of grammar[symbol] to opts"""
    expansions = grammar[symbol]
    for i, exp in enumerate(expansions):
        if exp_string(exp) != exp_string(expansion):
            continue

        new_opts = exp_opts(exp)
        if opts == {} or new_opts == {}:
            new_opts = opts
        else:
            for key in opts:
                new_opts[key] = opts[key]

        if new_opts == {}:
            grammar[symbol][i] = exp_string(exp)
        else:
            grammar[symbol][i] = (exp_string(exp), new_opts)

        return

    raise KeyError(
        "no expansion " +
        repr(symbol) +
        " -> " +
        repr(
            exp_string(expansion)))

def main():
    print (opts(min_depth=10))
    print (exp_string(("<term> + <expr>", opts(min_depth=10))))
    print (exp_opts(("<term> + <expr>", opts(min_depth=10))))
    print (exp_opt(("<term> - <expr>", opts(max_depth=2)), 'max_depth'))

if __name__ == "__main__":
    main()
