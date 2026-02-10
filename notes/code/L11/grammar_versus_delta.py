from timer import Timer
from grammars import *
from grammar_fuzzer import *
from reducer import *
from eval_mystery_runner import *

long_expr_input = GrammarFuzzer(EXPR_GRAMMAR, min_nonterminals=100).fuzz()
eval_mystery = EvalMysteryRunner()

grammar_reducer = GrammarReducer(eval_mystery, EarleyParser(EXPR_GRAMMAR))
with Timer() as grammar_time:
    print(grammar_reducer.reduce(long_expr_input))
print ("Needed {} tests, time was {}s.".format(grammar_reducer.tests, grammar_time.elapsed_time()))

dd_reducer = DeltaDebuggingReducer(eval_mystery)
with Timer() as dd_time:
    print(dd_reducer.reduce(long_expr_input))
print ("Needed {} tests, time was {}s.".format(dd_reducer.tests, dd_time.elapsed_time()))
