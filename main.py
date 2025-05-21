import sys
from classifier import classify_provision

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your provision text here\"")
        sys.exit(1)

    provision_text = sys.argv[1]
    result = classify_provision(provision_text)

    print("Classification Result:\n", result)