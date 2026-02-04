# Code from The Fuzzing Book, https://www.fuzzingbook.org

from typing import Dict, List, Tuple, Optional, Set
type Expansion = str
type Grammar = Dict[str, List[Expansion]]

import copy
import string
import re
import sys

RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

def nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return RE_NONTERMINAL.findall(expansion)

def is_nonterminal(s):
    return RE_NONTERMINAL.match(s)

START_SYMBOL = "<start>"

DIGIT_GRAMMAR = {
    "<start>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

EXPR_GRAMMAR: Grammar = {
    "<start>":
        ["<expr>"],
    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],
    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],
    "<factor>":
        ["+<factor>", "-<factor>",
         "(<expr>)",
         "<integer>.<integer>", "<integer>"],
    "<integer>":
        ["<digit><integer>", "<digit>"],
    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

CGI_GRAMMAR: Grammar = {
    "<start>":
        ["<string>"],
    "<string>":
        ["<letter>", "<letter><string>"],
    "<letter>":
        ["<plus>", "<percent>", "<other>"],
    "<plus>":
        ["+"],
    "<percent>":
        ["%<hexdigit><hexdigit>"],
    "<hexdigit>":
        ["0", "1", "2", "3", "4", "5", "6", "7",
            "8", "9", "a", "b", "c", "d", "e", "f"],
    "<other>":  # Actually, could be _all_ letters
        ["0", "1", "2", "3", "4", "5", "a", "b", "c", "d", "e", "-", "_"],
}

URL_GRAMMAR: Grammar = {
    "<start>":
        ["<url>"],
    "<url>":
        ["<scheme>://<authority><path><query>"],
    "<scheme>":
        ["http", "https", "ftp", "ftps"],
    "<authority>":
        ["<host>", "<host>:<port>", "<userinfo>@<host>", "<userinfo>@<host>:<port>"],
    "<host>":  # Just a few
        ["patricklam.ca", "www.google.com", "fuzzingbook.com"],
    "<port>":
        ["80", "8080", "<nat>"],
    "<nat>":
        ["<digit>", "<digit><digit>"],
    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<userinfo>":  # Just one
        ["user:password"],
    "<path>":  # Just a few
        ["", "/", "/<id>"],
    "<id>":  # Just a few
        ["abc", "def", "x<digit><digit>"],
    "<query>":
        ["", "?<params>"],
    "<params>":
        ["<param>", "<param>&<params>"],
    "<param>":  # Just a few
        ["<id>=<id>", "<id>=<nat>"],
}

# does not work with simple_grammar_fuzzer but works with GrammarFuzzer
simple_nonterminal_grammar: Grammar = {
    "<start>": ["<nonterminal>"],
    "<nonterminal>": ["<left-angle><identifier><right-angle>"],
    "<left-angle>": ["<"],
    "<right-angle>": [">"],
    "<identifier>": ["id"]  # for now
}

nonterminal_grammar = copy.deepcopy(simple_nonterminal_grammar)

def extend_grammar(grammar: Grammar, extension: Grammar = {}) -> Grammar:
    """Create a copy of `grammar`, updated with `extension`."""
    new_grammar = copy.deepcopy(grammar)
    new_grammar.update(extension)
    return new_grammar

def srange(characters: str) -> List[Expansion]:
    """Construct a list with all characters in the string"""
    return [c for c in characters]



def crange(character_start: str, character_end: str) -> List[Expansion]:
    return [chr(i)
            for i in range(ord(character_start), ord(character_end) + 1)]

def def_used_nonterminals(grammar: Grammar, start_symbol: 
                          str = START_SYMBOL) -> Tuple[Optional[Set[str]], 
                                                       Optional[Set[str]]]:
    """Return a pair (`defined_nonterminals`, `used_nonterminals`) in `grammar`.
    In case of error, return (`None`, `None`)."""

    defined_nonterminals = set()
    used_nonterminals = {start_symbol}

    for defined_nonterminal in grammar:
        defined_nonterminals.add(defined_nonterminal)
        expansions = grammar[defined_nonterminal]
        if not isinstance(expansions, list):
            print(repr(defined_nonterminal) + ": expansion is not a list",
                  file=sys.stderr)
            return None, None

        if len(expansions) == 0:
            print(repr(defined_nonterminal) + ": expansion list empty",
                  file=sys.stderr)
            return None, None

        for expansion in expansions:
            if isinstance(expansion, tuple):
                expansion = expansion[0]
            if not isinstance(expansion, str):
                print(repr(defined_nonterminal) + ": "
                      + repr(expansion) + ": not a string",
                      file=sys.stderr)
                return None, None

            for used_nonterminal in nonterminals(expansion):
                used_nonterminals.add(used_nonterminal)

    return defined_nonterminals, used_nonterminals

def reachable_nonterminals(grammar: Grammar,
                           start_symbol: str = START_SYMBOL) -> Set[str]:
    reachable = set()

    def _find_reachable_nonterminals(grammar, symbol):
        nonlocal reachable
        reachable.add(symbol)
        for expansion in grammar.get(symbol, []):
            for nonterminal in nonterminals(expansion):
                if nonterminal not in reachable:
                    _find_reachable_nonterminals(grammar, nonterminal)

    _find_reachable_nonterminals(grammar, start_symbol)
    return reachable

def unreachable_nonterminals(grammar: Grammar,
                             start_symbol=START_SYMBOL) -> Set[str]:
    return grammar.keys() - reachable_nonterminals(grammar, start_symbol)

def opts_used(grammar: Grammar) -> Set[str]:
    used_opts = set()
    for symbol in grammar:
        for expansion in grammar[symbol]:
            used_opts |= set(exp_opts(expansion).keys())
    return used_opts

def is_valid_grammar(grammar: Grammar,
                     start_symbol: str = START_SYMBOL, 
                     supported_opts: Set[str] = set()) -> bool:
    """Check if the given `grammar` is valid.
       `start_symbol`: optional start symbol (default: `<start>`)
       `supported_opts`: options supported (default: none)"""

    defined_nonterminals, used_nonterminals = \
        def_used_nonterminals(grammar, start_symbol)
    if defined_nonterminals is None or used_nonterminals is None:
        return False

    # Do not complain about '<start>' being not used,
    # even if start_symbol is different
    if START_SYMBOL in grammar:
        used_nonterminals.add(START_SYMBOL)

    for unused_nonterminal in defined_nonterminals - used_nonterminals:
        print(repr(unused_nonterminal) + ": defined, but not used. Consider applying trim_grammar() on the grammar",
              file=sys.stderr)
    for undefined_nonterminal in used_nonterminals - defined_nonterminals:
        print(repr(undefined_nonterminal) + ": used, but not defined",
              file=sys.stderr)

    # Symbols must be reachable either from <start> or given start symbol
    unreachable = unreachable_nonterminals(grammar, start_symbol)
    msg_start_symbol = start_symbol

    if START_SYMBOL in grammar:
        unreachable = unreachable - \
            reachable_nonterminals(grammar, START_SYMBOL)
        if start_symbol != START_SYMBOL:
            msg_start_symbol += " or " + START_SYMBOL

    for unreachable_nonterminal in unreachable:
        print(repr(unreachable_nonterminal) + ": unreachable from " + msg_start_symbol + ". Consider applying trim_grammar() on the grammar",
              file=sys.stderr)

    used_but_not_supported_opts = set()
    if len(supported_opts) > 0:
        used_but_not_supported_opts = opts_used(
            grammar).difference(supported_opts)
        for opt in used_but_not_supported_opts:
            print(
                "warning: option " +
                repr(opt) +
                " is not supported",
                file=sys.stderr)

    return used_nonterminals == defined_nonterminals and len(unreachable) == 0

def trim_grammar(grammar: Grammar, start_symbol=START_SYMBOL) -> Grammar:
    """Create a copy of `grammar` where all unused and unreachable nonterminals are removed."""
    new_grammar = extend_grammar(grammar)
    defined_nonterminals, used_nonterminals = \
        def_used_nonterminals(grammar, start_symbol)
    if defined_nonterminals is None or used_nonterminals is None:
        return new_grammar

    unused = defined_nonterminals - used_nonterminals
    unreachable = unreachable_nonterminals(grammar, start_symbol)
    for nonterminal in unused | unreachable:
        del new_grammar[nonterminal]

    return new_grammar

def main():
    print (EXPR_GRAMMAR["<digit>"])
    print ("<identifier>" in EXPR_GRAMMAR)
    assert nonterminals("<term> * <factor>") == ["<term>", "<factor>"]
    assert nonterminals("<digit><integer>") == ["<digit>", "<integer>"]
    assert nonterminals("1 < 3 > 2") == []
    assert nonterminals("1 <3> 2") == ["<3>"]
    assert nonterminals("1 + 2") == []
    assert nonterminals(("<1>", {'option': 'value'})) == ["<1>"]
    assert is_nonterminal("<abc>")
    assert is_nonterminal("<symbol-1>")
    assert not is_nonterminal("+")
    assert is_valid_grammar(EXPR_GRAMMAR)
    assert is_valid_grammar(CGI_GRAMMAR)
    assert is_valid_grammar(URL_GRAMMAR)
    assert not is_valid_grammar({"<start>": ["<x>"], "<y>": ["1"]})
    assert not is_valid_grammar({"<start>": "123"})
    assert not is_valid_grammar({"<start>": []})
    assert not is_valid_grammar({"<start>": [1, 2, 3]})

if __name__ == "__main__":
    main()
