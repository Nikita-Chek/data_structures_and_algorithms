Example command:

user> python3 main.py -f your_directory/type_cast_project


Задача: написать скрипт, который убирает все вызовы typing.cast()
из кода, то есть если где-то в модуле 
проекта используется выражение с cast’ом типа:
var2 = cast(<какой то тип>, var1) то заменить его на:
var2 = <какой-то тип>(var1) это любой тип, 
будь то int, bool, Sequence[str], Mapping[str, str] и т. д, 
фактически это любое выражение, определяющее 
тип var1 может быть любым выражением