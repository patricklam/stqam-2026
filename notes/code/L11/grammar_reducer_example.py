from grammars import *
from mystery_runner import *
from eval_mystery_runner import *
from reducer import *

expr_input = "1 + (2 * 3)"
eval_mystery = EvalMysteryRunner()
grammar_reducer = GrammarReducer(
      eval_mystery,
      EarleyParser(EXPR_GRAMMAR),
      log_test=True, log_reduce=True)

# grammar_reducer.reduce_tree = grammar_reducer.reduce_tree_with_depth

print (grammar_reducer.reduce(expr_input))
