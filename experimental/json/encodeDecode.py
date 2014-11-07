# example of turning dictionaries into json and vice versa.

import json

# recursive function I stole to strip unicode from dictionaries
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# make empty dictionary
dictOne = {}

# add some various elements
dictOne["cats"] = 8
dictOne["pi"] = 3.14159
dictOne["name"] = "Bobert"
dictOne["data"] = [77, "yellow", False]
dictOne["2"] = 0
print("Original dictionary:\n" + str(dictOne))

# turn it into json
jsonText = json.dumps(dictOne)
print("\nJSON:\n" + str(jsonText))

# this is where the JSON would be sent over the network

# turn it back into a dictionary
dictTwo = convert(json.loads(jsonText))
print("\nFinal data:\n" + str(dictTwo))

