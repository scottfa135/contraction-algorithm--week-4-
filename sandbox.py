import cProfile

class foo():
    def __init__(self):
        self.a=10
    
    def __repr__(self):
        if self.a>1:
            self.a -= 1
            self.__repr__()
        return str(self.a)

    @property
    def identity(self):
        return self
a={1:1,2:2,3:4}
b=a.keys()

with open("kargerMinCut.txt",'r') as inputFile:
    lines = [[x for x in a.split('\t')] for a in inputFile.readlines()]

with open("formattedKarger.txt",'x') as outputFile:
    for line in lines:
        outputFile.write(" ".join(line))