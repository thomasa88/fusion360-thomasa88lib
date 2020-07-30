import inspect
import json
import os

def read():
    caller_file = os.path.abspath((inspect.stack()[1])[1])
    manifest_path = caller_file.replace('.py', '.manifest')
    with open(manifest_path, encoding='utf-8') as manifest_file:
        return json.load(manifest_file)