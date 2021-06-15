import pickle
from hw_12_cls import AddressBook, Record, Phone

USERS = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'User not found'
        except ValueError:
            return 'Not supported items'
        except IndexError:
            return 'Input name and number in space'

    return inner


@input_error
def add_contact(args):
    phone = Phone(args[1])
    record = Record(str(args[0]).title())
    record.add_phone(phone)
    bd = input('Введи дату рождения в формате "день-месяц-год" или просто нажми Enter для пропуска...\n')
    if bd:
        while True:
            try:
                record.add_birthday(bd)
            except ValueError:
                bd = input('''Нужно ввести дату рождения в формате "01-01-2000", попробуй еще раз.
Если ты передумал добавлять дату, просто нажми Enter.\n''')
                if not bd:
                    break
            else:
                break
    USERS.add_record(record)
    return f'Contact {record} was successfully added!'


@input_error
def show_phone(x):
    name = str(x[0]).title()
    return USERS.get(name, ['Name not found'])


def all_contacts(value):
    n = value[0] if value else 3
    print(n)
    print(f'Всего в книге {len(USERS)} контактов.')
    for name in USERS.iterable(n):
        print(*name)
        answer = input('Нажми Enter что бы продолжить или введите любой символ, что бы закончить просмотр.\n')
        if not answer:
            continue
        break


def hello(x):
    return 'How can I help you?'


def load_data(x):
    try:
        with open('book.pickle', 'rb') as f:
            global USERS
            USERS.update(pickle.load(f))
    except FileNotFoundError:
        print('Записи не найдено.')


def save_data(x):
    with open('book.pickle', 'wb') as f:
        pickle.dump(USERS, f)


def find(value):
    print(value)
    result = USERS.find_contact(value[0])
    if not result:
        return 'Не найдено'
    pretty_view = ''
    for contact in result:
        pretty_view += contact + '\n'
    return pretty_view


def content(n):
    USERS.add_fake_records(100)


def help():
    print('''
    Добро пожалова в апк телефонная книга. Здесь ты можешь сохранить контакт, указав имя, один или несколько
    телефонов и дату рождения. 
    Поддерживаемые комманды: 
    1. hello - Обычное приветствие.
    2. add - Добавляет контакт в книгу. Пример ввода "add Дмитрий +380981234567". Дальше будет возможность
    ввести дату рождения контакта.
    3. info - Отображает информацию по контакту. Пример ввода "info Дмитрий". 
    4. all - Вывод всех имеющихся контактов в телефонной книге. Реализована пагинация по умолчанию в 3 контакта, можно
     передать значение пагинации. Пример ввода "all 5".
    5. save - Перезаписывает книгу в файл book.pickle 
    6. load - Подгружает ранее записанную книгу, если книги не существует, обрабатывает ошибку.
    7. find - Поиск контактов по паттерну. 
    8. content - Функция для тестирования, генерирует 100 тестовых записей, не принимает никаких параметров.
    9. help - Описание функционала.
    10. exit\\close - Завершение работы.(Книга автоматически не сохраняется, необходимо использовать комманду save)''')


commands = {
    'hello': hello,
    'add': add_contact,
    'info': show_phone,
    'all': all_contacts,
    'save': save_data,
    'load': load_data,
    'find': find,
    'content': content,
    'help': help
}


def main():
    help()
    while True:
        user_input = input().casefold()
        if user_input == '.':
            break

        brake_commands = ['exit', 'close']
        if user_input in brake_commands:
            print('Good bye!')
            break

        splt_user_input = user_input.split()
        try:
            command = splt_user_input.pop(0)
        except IndexError:
            return 'Команда не распознана'
        try:
            handler = commands.get(command)(splt_user_input)
        except TypeError as error:
            print('Error: ', error)
        else:
            if handler:
                print(handler)


if __name__ == '__main__':
    main()
