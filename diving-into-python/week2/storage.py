import argparse
import os
import json
import tempfile


def file_manipulation(file_mode, data=''):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    try:
        with open(storage_path, file_mode, encoding='UTF-8') as storage_file:
            if file_mode == 'w':
                json.dump(data, storage_file)
            elif file_mode == 'r':
                try:
                    return json.load(storage_file)
                except json.decoder.JSONDecodeError:
                    return {}
    except FileNotFoundError:   # create empty file if don't exist
        open(storage_path, 'a').close()
        return {}


parser = argparse.ArgumentParser()
parser.add_argument('--key', help="key name of argument")
parser.add_argument('--val', help="value of argument")

args = parser.parse_args()

if args.key and args.val:
    file_data = file_manipulation(file_mode='r')    # read existing key-values
    if args.key in file_data:
        values = file_data[args.key]
        if isinstance(values, list):
            values.append(args.val)
            file_data[args.key] = values
        else:
            file_data[args.key] = [values, args.val]
    else:
        file_data[args.key] = args.val
    file_manipulation(file_mode='w', data=file_data)    # add new key-value to file
elif args.key:
    file_data = file_manipulation(file_mode='r')    # try to get value from storage
    value = file_data.get(args.key)
    if isinstance(value, list):
        print(*value, sep=', ')
    else:
        print(value)
