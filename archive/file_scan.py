import json
import os
import ast

DIR_PATH = os.path.join(os.path.dirname(os.path.expanduser(os.path.expandvars(__file__))), 'error')
DATA = {}

for file_name in os.listdir(DIR_PATH):
    full_path = os.path.join(DIR_PATH, file_name)
    with open(full_path, 'r') as f:
        for line in f.readlines():
            try:
                data = ast.literal_eval(line)
            except:
                pass
                # print(file_name)
            else:
                for key, item in data.items():
                    if key not in DATA:
                        DATA[key] = []
                    if item not in DATA[key]:
                        DATA[key].append(item)


print(json.dumps(DATA, indent=4))

