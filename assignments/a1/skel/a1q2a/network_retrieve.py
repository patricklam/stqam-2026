import aiohttp
import asyncio
import threading
import time
from random import random
from . import settings

# Requires aiohttp.
# You probably want to `pip install aiohttp requests`.
# If you want things to be tidier, use a virtual environment (venv) and pip install inside it.
# venv docs: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
# On my system, I can apt install python3-aiohttp.

result = None

# please leave the TODO comments for ease of grading
# TODO-1 you can add code right below here:

async def retriever():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://git.uwaterloo.ca', allow_redirects=False) as resp:
            global result
            # (don't remove this; in grading mode tests should run quickly)
            if not settings.GRADING:
                time.sleep(random() * 10)
            else:
                time.sleep(0.5)
            result = await resp.text()
            # TODO-2 add something about events here:

def run_event_loop():
    asyncio.run(retriever())

def network_retrieve():
    """
    Issue  python -m doctest thisfile.py  to run the doctests.

    >>> print(network_retrieve())
    <html><body>You are being <a href="https://git.uwaterloo.ca/users/sign_in">redirected</a>.</body></html>
    """

    # start a new thread which starts the async io loop
    # (yes, this is contrived, but gets the point I want to make across)
    thread = threading.Thread(target=run_event_loop)
    thread.start()
    if not settings.GRADING:
        time.sleep(5)
    # TODO-3 also add something about events here too:
    
    return result

if __name__ == "__main__":
    network_retrieve()

