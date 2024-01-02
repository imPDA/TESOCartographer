import json
import re
from enum import StrEnum
from pathlib import Path
from typing import AnyStr, Any

from luaparser import ast, astnodes

# change here
base_dir = Path.cwd().parent.parent
PATH = base_dir / 'static/mappins'
PATH_TO_FILE = PATH / 'MapPins_1_96_2.lua'


def open_file(path_to_file: Path) -> AnyStr:
    print(f"Opening {path_to_file}...")
    try:
        with open(path_to_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("File not found, check the path")
        raise


def find_locals(string: str):
    return re.findall(r'local\s+([a-zA-Z]+)={', string)


class ValueType(StrEnum):
    NUMBER = 'Number'
    TABLE = 'Table'
    STRING = 'String'
    UMINUSOP = 'UMinusOp'

    # CALL = 'Call'
    # TRUE = 'True'
    # FALSE = 'False'


def handle_number(raw_number):
    try:
        return raw_number['n']
    except KeyError:
        return 0  # all `0` assigned values doesn't have `n` key


def handle_negative_number(raw_negative):
    return -1 * raw_negative['operand']['Number']['n']


def handle_table(raw_table):
    output = []
    output_type = None

    if not raw_table.get('fields'):
        return

    for raw_field in raw_table['fields']:
        field = raw_field['Field']
        if field['key'].get('Name'):
            output_type = dict
            key = field['key']['Name']['id']
        elif field['key'].get('String'):
            output_type = dict
            key = field['key']['String']['s']
        elif field['key'].get('Number'):
            output_type = dict if field['key']['Number'].get('start_char') else list
            key = field['key']['Number']['n']
        else:
            raise Exception(f"'Unknown key type: {field['key']}'")
        value = handle_value(field['value'])
        output.append((key, value) if output_type == dict else value)
    return output_type(output)


def handle_string(raw_string):
    return raw_string['s']


def handle_value(raw_value: dict) -> Any:
    if len(raw_value) != 1:
        raise Exception(f'Wrong value: {raw_value}')

    type_, value = raw_value.popitem()
    try:
        value_type = ValueType(type_)
    except ValueError:
        print(f"{type_} will not be handled")
        return

    if value_type == ValueType.NUMBER:
        return handle_number(value)

    if value_type == ValueType.TABLE:
        return handle_table(value)

    if value_type == ValueType.STRING:
        return handle_string(value)

    if value_type == ValueType.UMINUSOP:
        return handle_negative_number(value)


def get_local_assigns(chunk: ast.Chunk):
    for statement in chunk.body.body:
        if not isinstance(statement, astnodes.LocalAssign):
            continue

        dict_ = json.loads(ast.to_pretty_json(statement))
        local_assign = dict_['LocalAssign']

        targets_dict: dict = local_assign['targets']
        target_names = [target['Name']['id'] for target in targets_dict]

        try:
            values_dict: dict = local_assign['values']
        except KeyError:
            print(f"{target_names} - no value(s) assigned")
            continue

        values = [handle_value(value) for value in values_dict]

        for k, v in zip(target_names, values):
            yield k, v


if __name__ == '__main__':
    file = open_file(PATH_TO_FILE)
    tree = ast.parse(file)

    with open(PATH_TO_FILE.parent / 'mappins_output_1_96_2.json', 'w+', encoding='utf-8') as f:
        json.dump({k: v for k, v in get_local_assigns(tree)}, f, indent=2)
