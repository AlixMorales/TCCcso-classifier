from classifier import classify_provision

if __name__ == "__main__":
    provision = "A public benefit organization shall notify the Registrar when receiving foreign funds."
    result = classify_provision(provision)
    print("Classification Result:\n", result)