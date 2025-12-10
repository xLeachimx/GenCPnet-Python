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
    # For running the program independently.
    # Nested main/function defs to clear imports.
    import argparse as ap
    from sys import argv, stderr
    EXIT_FAILURE = 1
    # Construction of the command line argument parser
    arg_parser = ap.ArgumentParser(prog="GenCPYNet",
                                   usage="%(prog)s <options> <directory>",
                                   description="A program for generating acyclic CP-nets uniformly at random.")
    arg_parser.add_argument("-n",
                            args=1,
                            type=int,
                            required=True,
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
    arg_parser.add_argument('output_directory',
                            help="directory to output the generated XML files to.")
    def main():
        # Parse provided command line arguments
        args = arg_parser.parse_args(argv[1:])

        # Check if arguments are valid, and potentially reassign
        # Check in-degree bound
        if args.c < 0:
            args.c = 5 if args.n > 6 else args.n-1
        elif args.c >= args.n:
            args.c = args.n-1

        # Check number of attributes
        if args.n < 0:
            print("Error: Number of nodes n > 0 must be specified.", file=stderr)
            exit(EXIT_FAILURE)
        elif args.n > 63:
            print("Error: Number of nodes n must be less than 64.", file=stderr)
            exit(EXIT_FAILURE)

        # Check Hamming Distance
        if args.h < 0 or args.h > args.n:
            print("Error: Hamming distance must be the range [0, n].", file=stderr)
            exit(EXIT_FAILURE)

        # Check incompleteness degree
        if args.i < 0 or args.i >= 1:
            print("Error: degree of incompleteness must be in range [0.0, 1.0).", file=stderr)
            exit(EXIT_FAILURE)

        # Show parameters after alignment
        if args.verbose:
            print("Building distribution tables for CP-nets with the following specs:")
            print(f"Number of nodes: {args.n}")
            print(f"Bound on in-degree: {args.c}")
            print(f"Homogeneous domains of size {args.d}")
            print(f"Probability of incompleteness {args.i}")

        # TODO: Add in new feasibility

        # Continue on main.cc at line 220 once completed with Netcount class.



