import sys

from stats.stats import Statistics
from parse.parser import Parser


# when invvoked on the command line include debug as an argument to print debug info
debug = False
if len(sys.argv) > 1 and sys.argv[1].lower() == "debug":
    debug = True


def main():
    statistics = Statistics()
    parser = Parser(statistics, debug)

    parser.parse()

    statistics.generate_statistics()
    statistics.output_statistics()
   

if __name__ == "__main__":
    main()
