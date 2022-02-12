from ctypes import cast
import re


class Product:
    price: float
    name: str
    
    def __init__(self, price=None, name="product"):
        self.price = price
        self.name = name
        
    def __str__(self):
        return self.name
    
    def __float__(self):
        return float(self.price)