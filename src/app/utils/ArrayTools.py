class ArrayTools:
    @staticmethod
    def arrayColumn(input, keyName):
        output = []
        for x in input:
            output.append(x[keyName])
        return output

    @staticmethod
    def searchInMultiarray(input, key: str, value):
        output = []
        for item in input:
            if item[key] == value:
                output.append(item)
        return output
