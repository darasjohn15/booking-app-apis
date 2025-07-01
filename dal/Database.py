import json

class DatabaseObject:

    def __init__(self, fileName):
        self._fileName = "./Data/" + fileName

        with open(self._fileName, "r") as f:
            data = json.load(f)

        self._data = data['_data']
        

    def save(self):

        json_object = json.dumps(self, default=lambda o: o.__dict__, indent=4)

        with open(self._fileName, "w") as outFile:
            outFile.write(json_object)

    def reload(self):
        with open(self._fileName, "r") as f:
            data = json.load(f)

        self._data = data['_data']
