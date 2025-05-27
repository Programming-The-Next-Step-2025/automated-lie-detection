import argparse
from .utility import modelprediction

def main():
    parser = argparse.ArgumentParser(description="Automated Lie Detection CLI")
    parser.add_argument("statement", type=str, help="The statement to classify (in quotes)")
    args = parser.parse_args()

    result = modelprediction(args.statement)
    print(result)

if __name__ == "__main__":
    main()