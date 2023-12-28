import ast
import json

FILE_PATH = 'output.json'
CONTENT = {}

with open(FILE_PATH, 'r') as f:
    for line in f.readlines():
        try:
            raw_line = ast.literal_eval(line)[0]
        except Exception as error:
            pass
        else:

            for key, value in raw_line.items():  # Fix: Iterate over key-value pairs
                if key not in CONTENT:
                    CONTENT[key] = 0
                CONTENT[key] += 1


                # if isinstance(raw_line[key], dict):
                #     for sub_key, sub_value in raw_line[key].items():
                #         if sub_key not in CONTENT[key]:
                #             CONTENT[key][sub_key] = []
                #         if sub_value not in CONTENT[key][sub_key]:
                #             CONTENT[key][sub_key].append(sub_value)
                # elif value not in CONTENT[key]:  # Fix: Check value, not raw_line[key]
                #     CONTENT[key].append(value)


print(json.dumps(CONTENT, indent=4))
