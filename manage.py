#!/bin/python

from sys import argv, exit
from commands import find_command, list_commands, execute_command

# from commands.chalk import red, green, yellow, noticeRed, noticeGreen, noticeYellow


def execute_selected_command(command_name, *args):
    commands = sorted(list_commands(), key=lambda x: x['index'])
    if command_name == 'all':
        for command in commands:
            execute_command(command)
        return

    to_execute = find_command(command_name, commands)
    if to_execute is None:
        print('No such stript.')
        exit(1)

    return execute_command(to_execute)


def list_all_commands(*args):
    commands = sorted(list_commands(), key=lambda x: x['index'] or 0)
    for command in commands:
        print('{} / {}'.format(command['unparsed_index'], command['name']))


command = argv[1]
commands = {
    'list': list_all_commands,
    'exec': execute_selected_command,
}

if command not in commands:
    print('No such command.')
    exit(1)

commands[command](*argv[2:])
