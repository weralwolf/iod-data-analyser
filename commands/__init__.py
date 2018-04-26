from re import match
from os import listdir
from fnmatch import fnmatch
from os.path import basename, realpath, dirname
from importlib import import_module
from .logger import logger  # noqa:F401


CURRENT_DIR = realpath(dirname(__file__))


def list_commands():
    commands = []
    for fname in listdir(CURRENT_DIR):
        own_name = basename(fname)
        if fnmatch(fname, '*.py') and own_name != '__init__':
            unparsed_index, name = match('^(c\d*)?_?(.*)\.py$', own_name).groups()
            index = None if unparsed_index == '' else int(unparsed_index)
            commands.append(dict(
                index=index,
                unparsed_index=unparsed_index,
                name=name,
                module_name=own_name[:-3],
                package='commands',
            ))
    return commands


def find_command(id, commands):
    for command in commands:
        if id in (command['index'], command['unparsed_index'], command['name']):
            return command


def execute_command(command):
    command_module = import_module(command['module_name'], package=command['package'])
    command_module.main()
