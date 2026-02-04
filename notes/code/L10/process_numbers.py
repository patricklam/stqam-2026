# Code from The Fuzzing Book, https://www.fuzzingbook.org

import argparse
import sys

def process_numbers(args=None):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sum', dest='accumulate', action='store_const',
                       const=sum,
                       help='sum the integers')
    group.add_argument('--min', dest='accumulate', action='store_const',
                       const=min,
                       help='compute the minimum')
    group.add_argument('--max', dest='accumulate', action='store_const',
                       const=max,
                       help='compute the maximum')

    if args is not None:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()
    print(args.accumulate(args.integers))

if __name__ == "__main__":
    process_numbers()
