import json

path = "../data/data.json"


def read_json():
    file = open(path, "r")
    data = json.load(file)
    # print(data)
    return data


if __name__ == "__main__":
    read_json()
