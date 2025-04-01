from classifier import classify_provision

if __name__ == "__main__":
    provision = "A public benefit organization may determine its own internal governance structure in accordance with its constitution and bylaws"
    result = classify_provision(provision)
    print("Classification Result:\n", result)