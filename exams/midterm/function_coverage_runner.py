from typing import Callable, Dict, Type, Set, List, Union, Any, Tuple, Optional
from Coverage import Coverage, Location
from function_runner import FunctionRunner
from random_inputs import url_consumer

class FunctionCoverageRunner(FunctionRunner):
    def run_function(self, inp: str) -> Any:
        with Coverage() as cov:
            try:
                result = super().run_function(inp)
            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc

        self._coverage = cov.coverage()
        return result

    def coverage(self) -> Set[Location]:
        return self._coverage

if __name__ == "__main__":
    from urllib.parse import urlparse

    # view output from urlconsumer_runner:
    urlconsumer_runner = FunctionCoverageRunner(url_consumer)
    urlconsumer_runner.run("https://foo.bar")

    print(list(urlconsumer_runner.coverage())[:5])
