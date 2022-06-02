'''
Open a json file and add a size field to each object.
'''

def addSize(jsonFile):
    '''
    Open a json file and add a size field to each object. with an indent of 4.
    '''
    import json
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    for i in data.values():
        i["size"] = "font-size: 1rem;"
    with open(jsonFile, 'w') as f:
        json.dump(data, f, indent=4)

addSize("temp2 copy.json")