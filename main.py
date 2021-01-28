import sys

from stats.stats import Statistics
from parse.parser import Parser


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
