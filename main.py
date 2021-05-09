from commands import (
    Bookmarks,
    AddBookmarkCommand,
    ListBookmarkCommand,
    EditBookmarkCommand,
    DeleteBookmarkCommand,
    ImportGithubStarsCommand,
    QuitCommand
)


class Option:
    def __init__(self, name: str, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.name


def print_options(options: dict):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice: str, options: dict):
    return choice in options or choice.upper() in options


def get_option_choice(options: dict):
    choice = input('Выберите вариант действия: ')
    while not option_choice_is_valid(choice, options):
        print('Недопустимый вариант')
        choice = input('Выберите вариант действия: ')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}:') or None
    while required and not value:
        value = input(f'{label}:') or None
    return value


def get_new_bookmark_data():
    return {
        'title': get_user_input('Title', required=True),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes')
    }


def get_bookmark_by_id():
    return get_user_input('Введите id закладки: ')


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete: ')


def get_bookmark_for_edit():
    current_id = get_user_input('Введите id закладки: ')
    current_data = get_new_bookmark_data()
    data = {'id': int(current_id)}
    data.update(current_data)
    return data


def get_github_import_options():
    return {
        'github_username': get_user_input('Пользовательское имя GitHub: '),
        'preserve_timestamps': get_user_input(
            'Сохранить метки времени [Д/н]',
            required=False
        ) in {'Д', 'д', None},
    }


options = {
    'A': Option(
        'Добавить закладку',
        AddBookmarkCommand(),
        prep_call=get_new_bookmark_data
    ),
    'B': Option(
        'Показать список закладок по дате',
        ListBookmarkCommand()
    ),
    'T': Option(
        'Показать список закладок по заголовку',
        ListBookmarkCommand(order_by=Bookmarks.title)
    ),
    'D': Option(
        'Удалить закладку',
        DeleteBookmarkCommand(),
        prep_call=get_bookmark_id_for_deletion
    ),
    'G': Option(
        'Импортировать звезды GitHub',
        ImportGithubStarsCommand(),
        prep_call=get_github_import_options
    ),
    'E': Option(
        'Изменить закладку',
        EditBookmarkCommand(),
        prep_call=get_bookmark_for_edit
    ),
    'Q': Option(
        'Выйти',
        QuitCommand()
    ),
}


def clear_screen():
    import os

    os.system(
        'cls'
        if os.name == 'nt' else 'clear'
    )


def loop():
    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()


if __name__ == '__main__':
    while True:
        loop()
