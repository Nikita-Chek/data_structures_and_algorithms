from models.model1 import User
from typing import Mapping, Sequence, cast


user = User(32, "John")
print(int(user))
print(str(user))

age = int(user)
name = str(user) # str(user)
name = user(float) # user(float)

Sequence[str](name)
Mapping[str, str](age)