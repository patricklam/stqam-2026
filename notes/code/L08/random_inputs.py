from typing import Tuple, List, Callable, Set, Any
from urllib.parse import urlparse
from fuzzer import Fuzzer

def url_consumer(url: str) -> bool:
    supported_schemes = ["http", "https"]
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + 
                         repr(supported_schemes))
    if result.netloc == '':
        raise ValueError("Host must be non-empty")

    # Do something with the URL
    return True

def main():
    for i in range(1000):
        try:
            fuzzer = Fuzzer()
            url = fuzzer.fuzz()
            result = url_consumer(url)
            print("Success!")
        except ValueError:
            pass

if __name__ == "__main__":
    main()
