# File: __init__.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2025
# License: GNU GPLv3
# Created On: 10 Dec 2025
# Purpose:
#   Package for the duplication of the GenCPNet program
# Notes:

__VERSION = 0.1

if __name__ == "__main__":
    import argparse as ap
    from sys import argv
    # For running the program independently.
    # Nested main/function defs to clear imports.
    arg_parser = ap.ArgumentParser(prog="GenCPYNet",
                                   description="A program for generating acyclic CP-nets uniformly at random.")
    arg_parser.add_argument("-n",
                            args=1,
                            type=int,
                            help="number of features/nodes [required]")
    arg_parser.add_argument('-c',
                            nargs=1,
                            type=int,
                            default=5,
                            help="bound on indegree for all nodes (default: 5)",
                            dest="indegree")
    arg_parser.add_argument("--count",
                            action="store_true",
                            help="outputs the number of CP-nets (given n, c, d) [No generation]")
    arg_parser.add_argument("--countdegs",
                            action="store_true",
                            help="outputs number of graphs (given n, c) [no generation]")
    arg_parser.add_argument("-d",
                            nargs=1,
                            type=int,
                            default=2,
                            help="domain size, homogeneous for all features (default: 2)")
    arg_parser.add_argument("-g",
                            nargs=1,
                            type=int,
                            default=1,
                            help="number of CP-nets to generate (default 1)")
    arg_parser.add_argument("-i",
                            nargs=1,
                            type=float,
                            default=0.0,
                            help="probability that a given rule is missing (default: 0.0)")
    arg_parser.add_argument("-h",
                            "Hamming distance of outcome pairs (optional and only used in conjunction with the -t option)")
    arg_parser.add_argument("-t",
                            nargs=1,
                            type=int,
                            default=0,
                            help="also generates XML files each with a pair of outcomes for dominance testing experiments (default: 0)")

    arg_parser.add_argument("-V", "--verbose",
                            action="store_true",
                            help="output generation details to standard error for debugging")
    arg_parser.add_argument("--version",
                            action="version",
                            version="%(prog)s " + str(__VERSION) + " based on GenCPNet 0.70")
    def main():
        # Parse provided command line arguments
        arguments = arg_parser.parse_args(argv[1:])