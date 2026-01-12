# adapted from https://www.fuzzingbook.org/html/Coverage.html

import sys
import dis
import inspect
from types import FrameType, TracebackType
from typing import Any, Dict, List, Set, Optional, Union, Tuple, Type, Callable
Location = Tuple[str,int]

class Coverage:
    """Track coverage within a `with` block.
    targets list allows tracking coverage on functions not in global scope when this class was defined.

    Use as
    ```
    with Coverage([f, g]) as cov:
        f()
        g()
    executed_lines = cov.executed_lines()
    executable_lines = cov.executable_lines()
    succ = cov.succ()
    cov.print_coverage_stats()
    ```

    Example run on cgi_decode:
    >>> from cgi_decode import *
    >>> with Coverage([cd]) as cov:
    ...   cd("a+b")
    'a b'
    >>> cov.coverage_stats()
    (15, 22, 20, 31)
    >>> sorted(cov.executable_lines())
    [('cd', 1), ('cd', 8), ('cd', 9), ('cd', 10), ('cd', 11), ('cd', 12), ('cd', 15), ('cd', 16), ('cd', 17), ('cd', 18), ('cd', 19), ('cd', 20), ('cd', 21), ('cd', 22), ('cd', 23), ('cd', 24), ('cd', 25), ('cd', 26), ('cd', 28), ('cd', 30), ('cd', 31), ('cd', 32)]
    >>> sorted(cov.executed_branches())
    [(('cd', 8), ('cd', 9)), (('cd', 8), ('cd', 10)), (('cd', 8), ('cd', 11)), (('cd', 8), ('cd', 12)), (('cd', 8), ('cd', 15)), (('cd', 9), ('cd', 8)), (('cd', 10), ('cd', 8)), (('cd', 11), ('cd', 8)), (('cd', 12), ('cd', 8)), (('cd', 15), ('cd', 16)), (('cd', 16), ('cd', 17)), (('cd', 17), ('cd', 18)), (('cd', 17), ('cd', 32)), (('cd', 18), ('cd', 19)), (('cd', 19), ('cd', 20)), (('cd', 19), ('cd', 21)), (('cd', 20), ('cd', 31)), (('cd', 21), ('cd', 30)), (('cd', 30), ('cd', 31)), (('cd', 31), ('cd', 17))]
    >>> t = ""
    >>> for key in sorted(cov.succ()):
    ...   t += f"{key} => {sorted(cov.succ()[key])} "
    >>> t
    "('cd', 1) => [('cd', 8)] ('cd', 8) => [('cd', 9), ('cd', 10), ('cd', 11), ('cd', 12), ('cd', 15)] ('cd', 9) => [('cd', 8)] ('cd', 10) => [('cd', 8)] ('cd', 11) => [('cd', 8)] ('cd', 12) => [('cd', 8)] ('cd', 15) => [('cd', 16)] ('cd', 16) => [('cd', 17)] ('cd', 17) => [('cd', 18), ('cd', 32)] ('cd', 18) => [('cd', 19)] ('cd', 19) => [('cd', 20), ('cd', 21)] ('cd', 20) => [('cd', 21), ('cd', 31)] ('cd', 21) => [('cd', 22), ('cd', 30)] ('cd', 22) => [('cd', 23)] ('cd', 23) => [('cd', 24)] ('cd', 24) => [('cd', 25), ('cd', 28)] ('cd', 25) => [('cd', 26)] ('cd', 26) => [('cd', 28), ('cd', 31)] ('cd', 28) => [('cd', 30)] ('cd', 30) => [('cd', 31)] ('cd', 31) => [('cd', 17)] "
    """

    class Cfg(dict):
        """A dict that returns a fresh empty set when asked for a missing key"""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        def _default_func(self):
            return set()
        def __missing__(self, key):
            self[key] = val = self._default_func()
            return val

    def __init__(self, targets) -> None:
        self._targets = targets
        self._trace: List[Location] = []
        self._lines: List[Location] = []
        self._branches: List[Tuple[Location,Location]] = []
        # a mapping of line numbers to a set of line-number successors
        self._succ: Dict[Tuple[Location, Location], Set[Tuple[Location, Location]]] = self.Cfg()

    def traceit(self, frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
        """Tracing function. To be overloaded in subclasses."""
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        if event == "line":
            function_name = frame.f_code.co_name
            lineno = frame.f_lineno
            if function_name != '__exit__':  # avoid tracing ourselves:
                self._trace.append((function_name, lineno))

        return self.traceit

    def __enter__(self) -> Any:
        """Start of `with` block. Turn on tracing."""
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    def __exit__(self, exc_type: Type, exc_value: BaseException,
                 tb: TracebackType) -> Optional[bool]:
        """End of `with` block. Turn off tracing and calculate stats."""
        sys.settrace(self.original_trace_function)
        self.populate_executable_lines()
        self.populate_succ()

        return None  # default: pass all exceptions

    def trace(self) -> List[Location]:
        """The list of executed lines, as (function_name, line_number) pairs"""
        return self._trace

    def executable_lines(self) -> Set[Location]:
        """The list of executable lines, as (function_name, line_number) pairs"""
        return set(self._lines)

    def executed_lines(self) -> Set[Location]:
        """The set of executed lines, as (function_name, line_number) pairs"""
        return set(self.trace())

    def succ(self) -> Dict[Tuple[Location, Location], Set[Tuple[Location, Location]]]:
        """The succ relation, as ((function name, line_number), (function_name, line_number)) pairs"""
        return self._succ

    def executed_branches(self) -> Set[Tuple[Location, Location]]:
        # TODO (5 points) write code here; you may adapt the code from https://mybinder.org/v2/gh/uds-se/fuzzingbook/HEAD?labpath=docs%2Fnotebooks/Coverage.ipynb#Exercises
        executed_succ = set()

        return set(sorted(executed_succ))

    def function_names(self) -> Set[str]:
        """The set of function names seen"""
        return set(function_name for (function_name, line_number) in self.executed_lines())

    def populate_executable_lines(self) -> None:
        """Populates the internal list _lines of executable lines"""
        for function_name in self.function_names():
            try:
                fun = next(func for func in self._targets if func.__name__ == function_name)
            except StopIteration:
                try:
                    fun = eval(function_name)
                except Exception as exc:
                    print (f"Skipping {function_name}: {exc}")
                    continue

            function_bytecode = dis.Bytecode(fun)
            # TODO (5 points) you can do this with 2 or 3 lines of code here, populating self._lines, using function_bytecode as the source of data.

    def populate_succ(self) -> None:
        """Populates the internal control-flow graph _succ of successors"""
        for function_name in self.function_names():
            try:
                fun = next(func for func in self._targets if func.__name__ == function_name)
            except StopIteration:
                try:
                    fun = eval(function_name)
                except Exception as exc:
                    print (f"Skipping {function_name}: {exc}")
                    continue

            function_instructions = dis.get_instructions(fun.__code__)
            
            # TODO (20 points) suggested code outline:
            # (1) iterate on function_instructions and collect a mapping of offsets to line numbers;
            # (2) get a fresh set of instructions for fun.__code__; iterate on it and add pairs for jump targets as well as from the previous instruction to the current instruction, but skip self-loops (e.g. from line 31 to line 31).
            # prev->current is similar to what is in executed_branches
            # you are not required to omit the prev->current edge when there is an unconditional branch

            # PL's solution has 17 lines of code; Alex's solution uses an API to compute (1), uses a single loop, and has 10 lines of code.
            
    def coverage_stats(self) -> Tuple[int, int, int, int]:
        (lines, executable_lines) = (len(self.executed_lines()), len(self.executable_lines()))
        branches = len(self.executed_branches())
        executable_branches = 0
        for src, dest_list in self.succ().items():
            executable_branches += len(dest_list)
        return (lines, executable_lines, branches, executable_branches)
                
    def print_coverage_stats(self) -> None:
        """Prints out coverage statistics"""
        (lines, executable_lines, branches, executable_branches) = self.coverage_stats()
        print ("Line coverage: %d/%d (%.3f)" % (lines, executable_lines, lines / executable_lines))
        print ("Branch coverage: %d/%d (%.3f)" % (branches, executable_branches, branches / executable_branches))

    def __repr__(self) -> str:
        """Return a string representation of this object.
           Show covered (and uncovered) program code"""
        t = ""
        for function_name in self.function_names():
            # Similar code as in the example above
            try:
                fun = next((func for func in self._targets if func.__name__ == function_name), eval(function_name))
            except Exception as exc:
                t += f"Skipping {function_name}: {exc}"
                continue

            source_lines, start_line_number = inspect.getsourcelines(fun)
            for lineno in range(start_line_number, start_line_number + len(source_lines)):
                #if (function_name, lineno) in self.succ():
                #    t += str(self.succ()[(function_name, lineno)])
                if (function_name, lineno) not in self.executable_lines():
                    t += " "
                else:
                    t += "x"
                if (function_name, lineno) not in self.trace():
                    t += "# "
                else:
                    t += "  "
                t += "%2d  " % lineno
                t += source_lines[lineno - start_line_number]
        return t

if (__name__ == '__main__'):
    #from cgi_decode import *

    # since we did an import * it's not strictly necessary to pass cd to the Coverage constructor
    #with Coverage([cd]) as cov:
    #    cd("a+b")
    #cov.print_coverage_stats()

    # can also run the doctest in Coverage:
    import doctest
    doctest.testmod()
