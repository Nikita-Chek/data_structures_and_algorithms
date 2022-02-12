from models.model1 import User
from typing import Mapping, Sequence, cast


user = User(32, "John")
print(cast(int, user))
print(cast(    str, user))

age = cast( int,user)
name = cast( str,    user) # cast(user, float)

cast(Sequence[str], name)
cast(Mapping[str, str], age)