from ctypes import cast

class User:
    age: int
    name: str
    
    def __init__(self,age=None, name=None):
        self.age = age
        self.name = name
        
    def __str__(self):
        return self.name
    
    def __int__(self):
        return self.age
