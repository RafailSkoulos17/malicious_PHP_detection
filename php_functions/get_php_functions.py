import json
import os
import subprocess
import re
import config as cfg

proc = subprocess.Popen("{} get_functions.php".format(cfg.PHP_PATH), shell=True, stdout=subprocess.PIPE)

script_response = proc.stdout.read()

mylist = []
for line in script_response.split("\n"):
    line = line.strip()
    mylist.append(line)

functions = []
regex = re.compile("[[][0-9]*[]] [=][>] (.)*")
for line in mylist:
    if line.startswith("[user]"):
        break
    elif re.match(regex, line):
        function_name = line.split()[-1]
        functions.append(function_name)
fin = os.path.join(os.path.dirname(os.path.abspath("php_functions")), "php_function_list.json")
with open(fin, "w") as f:
    json.dump(functions, f, indent=2, separators=(',', ':'))
