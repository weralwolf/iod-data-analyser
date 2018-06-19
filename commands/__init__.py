from os import listdir
from re import match
from fnmatch import fnmatch
from os.path import dirname, basename, realpath
from importlib import import_module
from commands.utils.logger import logger  # noqa:F401

CURRENT_DIR = realpath(dirname(__file__))


def list_commands():
    commands = []
    for fname in listdir(CURRENT_DIR):
        own_name = basename(fname)
        if fnmatch(fname, '*.py') and own_name != 'chalk.py':
            pattern_match = match('^c(\d*)?_?(.*)\.py$', own_name)
            if pattern_match is None:
                continue
            unparsed_index, name = pattern_match.groups()
            index = None if unparsed_index == '' else int(unparsed_index)
            commands.append(dict(
                index=index,
                unparsed_index=unparsed_index,
                name=name,
                module_name='commands.{}'.format(own_name[:-3]),
            ))
    return commands


def find_command(id, commands):
    for command in commands:
        if id in (command['index'], command['unparsed_index'], command['name']):
            return command


def execute_command(command):
    command_module = import_module(command['module_name'])
    command_module.main()
