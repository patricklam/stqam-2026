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

def is_valid_url(url:str) -> bool:
    try:
        result = url_consumer(url)
        return True
    except ValueError:
        return False

import random

def fuzzer(max_length: int = 100, char_start: int = 32,
           char_range: int = 32) -> str:
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`)"""
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

def main():
    for i in range(1000):
        try:
            url = fuzzer()
            result = url_consumer(url)
            print("Success!")
        except ValueError:
            pass

if __name__ == "__main__":
    main()
