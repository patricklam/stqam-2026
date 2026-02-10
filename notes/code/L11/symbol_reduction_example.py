from grammars import *
from mystery_runner import *
from reducer import *

expr_input = "1 + (2 * 3)"
derivation_tree, *_ = EarleyParser(EXPR_GRAMMAR).parse(expr_input)
mystery = MysteryRunner()
grammar_reducer = GrammarReducer(
      mystery,
      EarleyParser(EXPR_GRAMMAR),
      log_reduce=True)

print ([all_terminals(t) for t in grammar_reducer.subtrees_with_symbol(derivation_tree, "<expr>")])
print ([all_terminals(t) for t in grammar_reducer.alternate_reductions(derivation_tree, "<expr>")])
print ([all_terminals(t) for t in grammar_reducer.symbol_reductions(derivation_tree, "<expr>")])

print ([all_terminals(t) for t in grammar_reducer.symbol_reductions(derivation_tree, "<term>")])

