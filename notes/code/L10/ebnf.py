# Code from The Fuzzing Book, https://www.fuzzingbook.org

from grammars import *

nonterminal_grammar = extend_grammar(nonterminal_grammar,
                                     {
                                         "<idchar>": (srange(string.ascii_letters) + 
                                                      srange(string.digits) + 
                                                      srange("-_"))
                                     }
                                     )

nonterminal_ebnf_grammar = extend_grammar(nonterminal_grammar,
                                          {
                                              "<identifier>": ["<idchar>+"]
                                          }
                                          )

EXPR_EBNF_GRAMMAR: Grammar = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["<sign>?<factor>", "(<expr>)", "<integer>(.<integer>)?"],

    "<sign>":
        ["+", "-"],

    "<integer>":
        ["<digit>+"],

    "<digit>":
        srange(string.digits)
}

def new_symbol(grammar: Grammar, symbol_name: str = "<symbol>") -> str:
    """Return a new symbol for `grammar` based on `symbol_name`"""
    if symbol_name not in grammar:
        return symbol_name

    count = 1
    while True:
        tentative_symbol_name = symbol_name[:-1] + "-" + repr(count) + ">"
        if tentative_symbol_name not in grammar:
            return tentative_symbol_name
        count += 1

RE_PARENTHESIZED_EXPR = re.compile(r'\([^()]*\)[?+*]')

def parenthesized_expressions(expansion: Expansion) -> List[str]:
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_PARENTHESIZED_EXPR, expansion)

def convert_ebnf_parentheses(ebnf_grammar: Grammar) -> Grammar:
    """Convert a grammar in extended BNF to BNF"""
    grammar = extend_grammar(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]
            if not isinstance(expansion, str):
                expansion = expansion[0]

            while True:
                parenthesized_exprs = parenthesized_expressions(expansion)
                if len(parenthesized_exprs) == 0:
                    break

                for expr in parenthesized_exprs:
                    operator = expr[-1:]
                    contents = expr[1:-2]

                    new_sym = new_symbol(grammar)

                    exp = grammar[nonterminal][i]
                    opts = None
                    if isinstance(exp, tuple):
                        (exp, opts) = exp
                    assert isinstance(exp, str)

                    expansion = exp.replace(expr, new_sym + operator, 1)
                    if opts:
                        grammar[nonterminal][i] = (expansion, opts)
                    else:
                        grammar[nonterminal][i] = expansion

                    grammar[new_sym] = [contents]

    return grammar

RE_EXTENDED_NONTERMINAL = re.compile(r'(<[^<> ]*>[?+*])')

def extended_nonterminals(expansion: Expansion) -> List[str]:
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_EXTENDED_NONTERMINAL, expansion)

def convert_ebnf_operators(ebnf_grammar: Grammar) -> Grammar:
    """Convert a grammar in extended BNF to BNF"""
    grammar = extend_grammar(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]
            extended_symbols = extended_nonterminals(expansion)

            for extended_symbol in extended_symbols:
                operator = extended_symbol[-1:]
                original_symbol = extended_symbol[:-1]
                assert original_symbol in ebnf_grammar, \
                    f"{original_symbol} is not defined in grammar"

                new_sym = new_symbol(grammar, original_symbol)

                exp = grammar[nonterminal][i]
                opts = None
                if isinstance(exp, tuple):
                    (exp, opts) = exp
                assert isinstance(exp, str)

                new_exp = exp.replace(extended_symbol, new_sym, 1)
                if opts:
                    grammar[nonterminal][i] = (new_exp, opts)
                else:
                    grammar[nonterminal][i] = new_exp

                if operator == '?':
                    grammar[new_sym] = ["", original_symbol]
                elif operator == '*':
                    grammar[new_sym] = ["", original_symbol + new_sym]
                elif operator == '+':
                    grammar[new_sym] = [
                        original_symbol, original_symbol + new_sym]

    return grammar

def convert_ebnf_grammar(ebnf_grammar: Grammar) -> Grammar:
    return convert_ebnf_operators(convert_ebnf_parentheses(ebnf_grammar))

def main():
    assert new_symbol(EXPR_EBNF_GRAMMAR, '<expr>') == '<expr-1>'

    assert parenthesized_expressions("(<foo>)* (<foo><bar>)+ (+<foo>)? <integer>(.<integer>)?") == [
        '(<foo>)*', '(<foo><bar>)+', '(+<foo>)?', '(.<integer>)?']

    print (convert_ebnf_parentheses({"<number>": ["<integer>(.<integer>)?"]}))
    print (convert_ebnf_parentheses({"<foo>": ["((<foo>)?)+"]}))
    assert extended_nonterminals(
        "<foo>* <bar>+ <elem>? <none>") == ['<foo>*', '<bar>+', '<elem>?']
    print (convert_ebnf_operators({"<integer>": ["<digit>+"], "<digit>": ["0"]}))

    print (convert_ebnf_grammar({"<authority>": ["(<userinfo>@)?<host>(:<port>)?"]}))

    expr_grammar = convert_ebnf_grammar(EXPR_EBNF_GRAMMAR)
    print (expr_grammar)
    assert is_valid_grammar(URL_GRAMMAR)

if __name__ == "__main__":
    main()
