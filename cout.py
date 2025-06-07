class Cout:
    def __init__(self):
        self.buffer = ""

    def __lshift__(self, other):
        print(other, end='')
        if other:
            return self
    def __getstate__(self):
        return 
class Cin:
    def __init__(self):
        pass
    def __iter__(self):
        return self
    def __next__(self):
        return input()
    def getline(self):
        return input()
    def __rshift__(self, other):
        return other
cout=Cout()
endl='\n'
class std:
    endl='\n'
    cout=Cout()
    cin=Cin()
    cerr=cout


