from fuzzer import *
import os
import tempfile
import subprocess

def fuzzing_campaign():
    trials = 100
    program = "bc"
    runs = []
    basename = "input.txt"
    tempdir = tempfile.mkdtemp()
    FILE = os.path.join(tempdir, basename)

    for i in range(trials):
        data = fuzzer()
        with open(FILE, "w") as f:
            f.write(data)
        result = subprocess.run([program, FILE],
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        runs.append((data, result))
    return runs
