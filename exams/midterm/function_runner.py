## coverage-based fuzzing

from typing import Callable, Dict, Type, Set, List, Union, Any, Tuple, Optional
from fuzzer import Runner
from random_inputs import url_consumer

class FunctionRunner(Runner):
    def __init__(self, function: Callable) -> None:
        """Initialize.  `function` is a function to be executed"""
        self.function = function

    def run_function(self, inp: str) -> Any:
        return self.function(inp)

    def run(self, inp: str) -> Tuple[Any, str]:
        try:
            result = self.run_function(inp)
            outcome = self.PASS
        except Exception:
            result = None
            outcome = self.FAIL

        return result, outcome

if __name__ == "__main__":
    from urllib.parse import urlparse
    
    # view output from urlconsumer_runner:
    urlconsumer_runner = FunctionRunner(url_consumer)
    print (urlconsumer_runner.run("https://foo.bar"))
    
