#!/usr/bin/env python3
# Author: Pekka Marjamäki - Suolenkainen
# https://github.com/suolenkainen/economy

## utilities.py
## Functions that are commonly used in modules.

import os

# Function is used to return an object based on the attributes in the file
class file_to_object:
    def __init__(self, filename, path):
        stlm = open(os.path.join(path, filename), "r")
        self.filename = filename

        # set attributes to object based on the file
        while True:
            line = stlm.readline()
            if not line:
                break
            attr = line.strip().split("=")
            setattr(self, attr[0], attr[1])


def attributes_to_text(attrs):
    text = []
    for key in attrs:
        # print(key, attrs[key])
        text.append(key + "=" + str(attrs[key]) + "\n")
    print(text)
    return text


if __name__ == "__main__":

    attributes = {}
    attributes["type"] = "hauling"
    attributes["destination"] = "settlement_1"
    attributes["speed"] = 0
    attributes["maxspeed"] = 5
    attributes["distance"] = 0
    attributes["progression"] = 0
    attributes["goods"] = []
    attributes["capacity"] = 100

    print(attributes_to_text(attributes))