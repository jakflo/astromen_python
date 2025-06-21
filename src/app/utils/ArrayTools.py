from collections import Counter


class ArrayTools:
    @staticmethod
    def arrayColumn(input, keyName):
        output = []
        for x in input:
            try:
                output.append(x[keyName])
            except KeyError:
                output.append(None)
        return output
        
    @staticmethod
    def arrayUnique(input: list) -> list:
        return list(set(input))

    @staticmethod
    def searchInMultiarray(input, key: str, value):
        output = []
        for item in input:
            if item[key] == value:
                output.append(item)
        return output

    @staticmethod
    def arrayDiff(array1: list, array2: list) -> list:
        counter1 = Counter(array1)
        counter2 = Counter(array2)
        diff = counter1 - counter2
        return list(diff.elements())

#    narozdil od normalniho remove, tohle odstrani vsechny vyskyty a nekousne se, kdyz vec tam neni vubec
    @staticmethod
    def remove(input, value):
        for x in range(input.count(value)):
            input.remove(value)
