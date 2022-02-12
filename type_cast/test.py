"""Задача: написать скрипт, который убирает все вызовы typing.cast()
из кода, то есть если где-то в модуле 
проекта используется выражение с cast’ом типа:
var2 = cast(<какой то тип>, var1) то заменить его на:
var2 = <какой-то тип>(var1) это любой тип, 
будь то int, bool, Sequence[str], Mapping[str, str] и т. д, 
фактически это любое выражение, определяющее 
тип var1 может быть любым выражением"""


from argparse import ArgumentParser
import glob, os
import re


# regular expression for searching cast(<type>, var)
prog = re.compile(r'cast\(\s*[\w.\[\],\s]+,\s*[\w._]+\s*\)')


# shell arguments
parser = ArgumentParser()
parser.add_argument("-f", "--folder", dest="folder",
                    help="specified folder for project")

args = parser.parse_args()
folder = args.folder



# find all .py files in directory
path = folder + "/**/*.py"
files = [file for file in glob.glob(path, recursive=True)]



for file in files:
    
    # read files
    file_r = open(file)
    lines = file_r.readlines()
    file_r.close()
    print(file)
    
    
    with open(file, "w") as file_w:
        
        # searchin fo regex pattern in lines
        results = [prog.findall(line) for line in lines]
        
        for res, line in zip(results, lines):
            
            # if it was found convert to needed expression
            if res:
                for i in res:
                    i = i.strip()
                    type_start = i.index('(')
                    # find last comma that divide pattern into type and var
                    delimeter = i.rfind(',')
                    replacement = f"{i[5:delimeter].strip()}({i[delimeter+1:-1].strip()})"
                    file_w.write(re.sub(prog, replacement, line))
            else:
                file_w.write(line)
            