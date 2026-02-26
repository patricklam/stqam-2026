#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Code Coverage" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Coverage.html
# Last change: 2025-10-26 19:00:30+01:00
#
# Copyright (c) 2021-2025 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Fuzzing Book - Code Coverage

This file can be _executed_ as a script, running all experiments:

    $ python Coverage.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.Coverage import <identifier>

but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/Coverage.html

**Note**: The examples in this section only work after the rest of the cells have been executed.

For more details, source, and documentation, see
"The Fuzzing Book - Code Coverage"
at https://www.fuzzingbook.org/html/Coverage.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Code Coverage
# =============

if __name__ == '__main__':
    print('# Code Coverage')



## A CGI Decoder
## -------------

if __name__ == '__main__':
    print('\n## A CGI Decoder')



def cgi_decode(s: str) -> str:
    """Decode the CGI-encoded string `s`:
       * replace '+' by ' '
       * replace "%xx" by the character with hex number xx.
       Return the decoded string.  Raise `ValueError` for invalid inputs."""

    # Mapping of hex digits to their integer values
    hex_values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    }

    t = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == '+':
            t += ' '
        elif c == '%':
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if digit_high in hex_values and digit_low in hex_values:
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else:
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t

if __name__ == '__main__':
    cgi_decode("Hello+world")

## Black-Box Testing
## -----------------

if __name__ == '__main__':
    print('\n## Black-Box Testing')



if __name__ == '__main__':
    assert cgi_decode('+') == ' '
    assert cgi_decode('%20') == ' '
    assert cgi_decode('abc') == 'abc'

    try:
        cgi_decode('%?a')
        assert False
    except ValueError:
        pass

## White-Box Testing
## -----------------

if __name__ == '__main__':
    print('\n## White-Box Testing')



## Tracing Executions
## ------------------

if __name__ == '__main__':
    print('\n## Tracing Executions')



if __name__ == '__main__':
    cgi_decode("a+b")

from types import FrameType, TracebackType
from typing import Any, Optional, Callable, Tuple, Type, List, Set

if __name__ == '__main__':
    coverage = []

def traceit(frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
    """Trace program execution. To be passed to sys.settrace()."""
    if event == 'line':
        global coverage
        function_name = frame.f_code.co_name
        lineno = frame.f_lineno
        coverage.append(lineno)

    return traceit

import sys

def cgi_decode_traced(s: str) -> None:
    global coverage
    coverage = []
    sys.settrace(traceit)  # Turn on
    cgi_decode(s)
    sys.settrace(None)    # Turn off

if __name__ == '__main__':
    cgi_decode_traced("a+b")
    print(coverage)

import inspect

if __name__ == '__main__':
    cgi_decode_code = inspect.getsource(cgi_decode)

if __name__ == '__main__':
    print_content(cgi_decode_code[:300] + "...", ".py")

if __name__ == '__main__':
    cgi_decode_lines = [""] + cgi_decode_code.splitlines()

if __name__ == '__main__':
    cgi_decode_lines[1]

if __name__ == '__main__':
    cgi_decode_lines[9:13]

if __name__ == '__main__':
    cgi_decode_lines[15]

if __name__ == '__main__':
    covered_lines = set(coverage)
    print(covered_lines)

if __name__ == '__main__':
    for lineno in range(1, len(cgi_decode_lines)):
        if lineno not in covered_lines:
            print("# ", end="")
        else:
            print("  ", end="")
        print("%2d  " % lineno, end="")
        print_content(cgi_decode_lines[lineno], '.py')
        print()

## A Coverage Class
## ----------------

if __name__ == '__main__':
    print('\n## A Coverage Class')



Location = Tuple[str, int]

class Coverage:
    """Track coverage within a `with` block. Use as
    ```
    with Coverage() as cov:
        function_to_be_traced()
    c = cov.coverage()
    ```
    """

    def __init__(self) -> None:
        """Constructor"""
        self._trace: List[Location] = []

    # Trace function
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
        """End of `with` block. Turn off tracing."""
        sys.settrace(self.original_trace_function)
        return None  # default: pass all exceptions

    def trace(self) -> List[Location]:
        """The list of executed lines, as (function_name, line_number) pairs"""
        return self._trace

    def coverage(self) -> Set[Location]:
        """The set of executed lines, as (function_name, line_number) pairs"""
        return set(self.trace())

    def function_names(self) -> Set[str]:
        """The set of function names seen"""
        return set(function_name for (function_name, line_number) in self.coverage())

    def __repr__(self) -> str:
        """Return a string representation of this object.
           Show covered (and uncovered) program code"""
        t = ""
        for function_name in self.function_names():
            # Similar code as in the example above
            try:
                fun = eval(function_name)
            except Exception as exc:
                t += f"Skipping {function_name}: {exc}"
                continue

            source_lines, start_line_number = inspect.getsourcelines(fun)
            for lineno in range(start_line_number, start_line_number + len(source_lines)):
                if (function_name, lineno) not in self.trace():
                    t += "# "
                else:
                    t += "  "
                t += "%2d  " % lineno
                t += source_lines[lineno - start_line_number]

        return t

if __name__ == '__main__':
    with Coverage() as cov:
        cgi_decode("a+b")

    print(cov.coverage())

if __name__ == '__main__':
    print(cov)

## Comparing Coverage
## ------------------

if __name__ == '__main__':
    print('\n## Comparing Coverage')



if __name__ == '__main__':
    with Coverage() as cov_plus:
        cgi_decode("a+b")
    with Coverage() as cov_standard:
        cgi_decode("abc")

    cov_plus.coverage() - cov_standard.coverage()

if __name__ == '__main__':
    with Coverage() as cov_max:
        cgi_decode('+')
        cgi_decode('%20')
        cgi_decode('abc')
        try:
            cgi_decode('%?a')
        except Exception:
            pass

if __name__ == '__main__':
    cov_max.coverage() - cov_plus.coverage()

##  Coverage of Basic Fuzzing
## --------------------------

if __name__ == '__main__':
    print('\n##  Coverage of Basic Fuzzing')
