from fuzzer import *
from crash_midterm import *

for i in range(100000):
  crash_midterm(fuzzer())

