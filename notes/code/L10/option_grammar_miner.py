# Code from The Fuzzing Book, https://www.fuzzingbook.org

from typing import Dict, List, Tuple, Optional, Set, Callable
type Expansion = str
type Grammar = Dict[str, List[Expansion]]

from ebnf import *
import inspect

class ParseInterrupt(Exception):
    pass

class OptionGrammarMiner:
    """Helper class for extracting option grammars"""

    def __init__(self, function: Callable, log: bool = False):
        """Constructor.
        `function` - a function processing arguments using argparse()
        `log` - output diagnostics if True
        """
        self.function = function
        self.log = log

    OPTION_SYMBOL = "<option>"
    ARGUMENTS_SYMBOL = "<arguments>"

    def mine_ebnf_grammar(self):
        """Extract EBNF option grammar"""
        self.grammar = {
            START_SYMBOL: ["(" + self.OPTION_SYMBOL + ")*" + self.ARGUMENTS_SYMBOL],
            self.OPTION_SYMBOL: [],
            self.ARGUMENTS_SYMBOL: []
        }
        self.current_group = self.OPTION_SYMBOL

        old_trace = sys.gettrace()
        sys.settrace(self.traceit)
        try:
            self.function()
        except ParseInterrupt:
            pass
        sys.settrace(old_trace)

        return self.grammar

    def mine_grammar(self):
        """Extract BNF option grammar"""
        return convert_ebnf_grammar(self.mine_ebnf_grammar())

    def traceit(self, frame, event, arg):
        if event != "call":
            return

        if "self" not in frame.f_locals:
            return

        self_var = frame.f_locals["self"]
        method_name = frame.f_code.co_name

        if method_name == "add_argument":
            in_group = repr(type(self_var)).find("Group") >= 0
            self.process_argument(frame.f_locals, in_group)
        elif method_name == "add_mutually_exclusive_group":
            self.add_group(frame.f_locals, exclusive=True)
        elif method_name == "add_argument_group":
            # self.add_group(frame.f_locals, exclusive=False)
            pass
        elif method_name == "parse_args":
            raise ParseInterrupt

        return self.traceit

    def process_argument(self, locals, in_group):
        args = locals["args"]
        kwargs = locals["kwargs"]

        if self.log:
            print(args)
            print(kwargs)
            print()

        for arg in args:
            self.process_arg(arg, in_group, kwargs)

    def process_arg(self, arg, in_group, kwargs):
        if arg.startswith('-'):
            if not in_group:
                target = self.OPTION_SYMBOL
            else:
                target = self.current_group
            metavar = None
            arg = " " + arg
        else:
            target = self.ARGUMENTS_SYMBOL
            metavar = arg
            arg = ""

        if "nargs" in kwargs:
            nargs = kwargs["nargs"]
        else:
            nargs = 1

        param = self.add_parameter(kwargs, metavar)
        if param == "":
            nargs = 0

        if isinstance(nargs, int):
            for i in range(nargs):
                arg += param
        else:
            assert nargs in "?+*"
            arg += '(' + param + ')' + nargs

        if target == self.OPTION_SYMBOL:
            self.grammar[target].append(arg)
        else:
            self.grammar[target].append(arg)

    def add_parameter(self, kwargs, metavar):
        if "action" in kwargs:
            # No parameter
            return ""

        type_ = "str"
        if "type" in kwargs:
            given_type = kwargs["type"]
            # int types come as '<class int>'
            if inspect.isclass(given_type) and issubclass(given_type, int):
                type_ = "int"

        if metavar is None:
            if "metavar" in kwargs:
                metavar = kwargs["metavar"]
            else:
                metavar = type_

        self.add_type_rule(type_)
        if metavar != type_:
            self.add_metavar_rule(metavar, type_)

        param = " <" + metavar + ">"

        return param

    def add_type_rule(self, type_):
        if type_ == "int":
            self.add_int_rule()
        else:
            self.add_str_rule()

    def add_int_rule(self):
        self.grammar["<int>"] = ["(-)?<digit>+"]
        self.grammar["<digit>"] = crange('0', '9')

    def add_str_rule(self):
        self.grammar["<str>"] = ["<char>+"]
        self.grammar["<char>"] = srange(
            string.digits
            + string.ascii_letters
            + string.punctuation)

    def add_metavar_rule(self, metavar, type_):
        self.grammar["<" + metavar + ">"] = ["<" + type_ + ">"]

    def add_group(self, locals, exclusive):
        kwargs = locals["kwargs"]
        if self.log:
            print(kwargs)

        required = kwargs.get("required", False)
        group = new_symbol(self.grammar, "<group>")

        if required and exclusive:
            group_expansion = group
        if required and not exclusive:
            group_expansion = group + "+"
        if not required and exclusive:
            group_expansion = group + "?"
        if not required and not exclusive:
            group_expansion = group + "*"

        self.grammar[START_SYMBOL][0] = group_expansion + \
            self.grammar[START_SYMBOL][0]
        self.grammar[group] = []
        self.current_group = group

