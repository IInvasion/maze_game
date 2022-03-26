"""Library of functions for maze_game TUI."""


def separating_string(prompt=None):
    """Separating string."""
    if not prompt:
        print('-' * 40)
    else:
        print(prompt)
        print('-' * 40)


def choice(commands, prompt):
    """Choice command."""
    print(prompt + '\n')
    print('Available commands:')
    for i, command in enumerate(commands, 1):
        print(i, '-', command)
    while True:
        separating_string()
        command = input('Please enter command: ')
        if command.isdigit() and (1 <= int(command) < len(commands) + 1):
            return commands[int(command) - 1]
        print('Incorrect command')


def yes_no(prompt):
    """Confirm or deny a proposed choice."""
    prompt = prompt + ' (yes/no) '
    while True:
        cmd = input(prompt).lower()
        if cmd in ('y', 'yes'):
            return True
        if cmd in ('n', 'no'):
            return False

        print('Your choice is incorrect, please try again')
