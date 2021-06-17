import time

from classes import AddressBook, Record, Phone, Birthday
from os import name
import sys
import pickle
import time
from pathlib import Path
from faker import Faker
from prettytable import PrettyTable
from termcolor2 import colored

# директория может быть выбрана при запуске программы, имя файла - константа.
CONTACTS_FILE = 'contacts.dat'
CONTACTS_DIR = ''


def deserialize_users(path):
    """using the path "path" reads the file with contacts"""

    with open(path, "rb") as fh:
        addressbook = pickle.load(fh)

    return addressbook


def serialize_users(addressbook, path):
    """saves a file with contacts on the path (object pathlib.Path) to disk"""

    with open(path, "wb") as fh:
        pickle.dump(addressbook, fh)


def error_handler(func):
    # сюда вынесена обработка всех возникающих ошибок в ходе работы программы - как типов и
    # форматов, так и логические (дата рождения в будущем, попытка удалить несуществующий параметр и т.д.)
    def inner(*args):
        try:
            result = func(*args)
            return result
        except Exception as message:
            return message.args[0]
        except KeyError:
            return "No user with given name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name or command"

    return inner


def parse(input_string):  # --> ('key word', parameter)
    # извлекает команду и параметры из строки, возвращает в виде списка с
    # одним элементом - кортеж из двух элементов: команды и параметры

    def parse_phone(src):
        # функция принимает строку в качестве аргумента и ищет в ней номер телефона (справа)
        # Возвращает кортеж из двух аргументов - все, вплоть до номера телефона (без
        # пробелов слева и справа) и номера телефона. Если номер телефона не найден,
        # вместо него возвращается пустая строка.

        import re
        phone_regex = re.compile(r'[+]?[\d\-\(\)]{5,18}\s?$')
        match = phone_regex.search(src)
        if match is None:
            result = (src.strip(), '')
        else:
            result = (src[:match.start()].strip(), match.group())
        return result

    def parse_word(word):
        # фабричная функция. Производит функции синтаксического анализатора для
        # отдельных команд. Возвращает кортеж из команды, строку после команды
        # и номер телефона. Если номер телефона отсутствует, вместо него
        # возвращается пустая строка.

        l = len(word)

        def result(src):
            if src.casefold().startswith(word.casefold()):
                return word, *parse_phone(src[l:].lstrip())

        return result

    parse_scoup = [
        parse_word('hello'),
        parse_word('add'),
        # parse_word('change'),
        parse_word('phone'),
        parse_word('show all'),
        parse_word('exit'),
        parse_word('close'),
        parse_word('good bye'),
        parse_word('.'),
        parse_word('help'),
        parse_word('search'),
        parse_word('other phone'),
        parse_word('bd add')
    ]
    res_pars = [i(input_string) for i in parse_scoup if i(
        input_string)] or [('unrecognize', '', '')]

    return res_pars[0]


@error_handler
def get_handler(res_pars, addressbook):
    # получив результаты работы парсера функция управляет передачей параметров
    # и вызовм соотвествующего обработчика команды

    def help_f(*args):
        return '''формат команд:
        - add - формат: add name phone_number - добавляет новый контакт
        - other phone - формат: other phone name phone_number - добавляет дополнительный телефон в существующую запись
        - show all - формат: show all [N] - показывает всю адресную книгу. N - необязательный параметр - количество одновременно выводимых записей
        - exit/./close/goog bye - формат: exit - остановка работы с программой. Важно! чтобы сохранить все изменения и введенные данные - используйте эту команду
        - phone - формат: phone name - поиск телефона по имени. Можно ввести неполной имя либо его часть - программа выведет все совпадения
        - hello - формат: hello - просто Ваше привествие программе. Доброе слово - оно и для кода приятно)
        - bd add - формат: bd add name dd-mm-YYYY - ввод либо перезапись ранее введенной даты рождения. Соблюдайте формат ввода даты.
        - search - формат: search pattern - поиск совпадений по полям имени и телефонов. Будут выведены все записи в которых есть совпадения'''

    def add_f(addressbook):
        name = pretty_input('Введите имя \n')
        record = Record(name)
        phone = pretty_input('Введите телефон \n')
        record.add_phone(phone)
        birthday_str = pretty_input(
            'Введите дату рождения в формате(дд-мм-гггг) или нажмите "ввод", чтобы пропустить:\n')
        if birthday_str:
            record.add_birthday(birthday_str)
        addressbook.add_record(record)

        return colored(f'Контакт {name} успешно добавлен.', 'green')

    def hello_f(*args):
        return colored('How can I help you?', 'magenta')

    # def change_f(name, phone, contacts):
    # закоментирована, так как по сути своей совершенно бессмысленная функция
    #    if not contacts.get(name):
    #        raise Exception('this name is not in the contact list')
    #    old_phone = contacts[name]
    #    contacts[name] = phone#
    #
    #    return f'''for contact {name} number replaced
    #            old number: {old_phone}
    #            new number: {phone}'''

    def search(addressbook):
        user_input = pretty_input('What are you looking for?')
        # осуществляет поиск введенной строки во всех текстовых полях адресной книги
        result = addressbook.search(user_input)

        if not result:
            raise Exception('По данному запросу ничего не найдено')

        return result

    def show_all_f(addressbook, N=10):
        # выводит на экран всю адресную книгу блоками по N записей. Основная обработка
        # реализована как метод класса addressbook, что позволяет использовать аналогичный
        # вывод для результатов поиска по запросам, так как функции поиска возвращают
        # объект типа addressbook с результатами
        n = int(N)
        print(f'всего к выводу {len(addressbook)} записей: ')
        for block in addressbook.out_iterator(n):
            print(pretty(block))
            usr_choice = input(colored('Нажмите "Enter", или введите "q", что бы закончить просмотр.\n', 'yellow'))
            if usr_choice:
                '''Если пользователь вводит любой символ, его перебрасывает на основное меню.'''
                break
            continue
        return colored('Вывод окончен!', 'yellow')

    def pretty(block):
        '''
        Данная функция создана исключительно для обработки функции show_all,
        1. Принимает блок
        2. Парсит его
        3. Добавляет обработанную инфу в таблицу
        4. Возвращает таблицу
        '''
        table = PrettyTable(['Name', 'Birthday', 'Number(s)'])
        nx = str(block).split('\n')
        for j in range(len(nx) - 1):
            xr = nx[j].split('SP')
            a = str(xr.pop(2)).replace('[', '').replace(']', '').replace(',', '\n')
            xr.append(a)
            table.add_row(xr)
        return colored(table, 'green')

    def exit_f():
        return None

    def unrecognize_f(name, phone, contacts):
        return colored('Ввод не распознан. Для получения помощи введите "help"', 'yellow')

    def add_phone(name, phone, addressbook):
        # позволяет добавить в запись дополнительный телефон
        if name in addressbook:
            addressbook[name].add_phone(phone)
        else:
            return colored(f'Контакт {name} отсутствует в адресной книге', 'yellow')
        return f'В запись добавлен новый телефон: \n {addressbook[name]}'

    def bd_add_f(name, birthday_str, addressbook):
        # позволяет добавить (перезаписать, если ранее было введена) дату рождения в запись
        if name in addressbook:
            addressbook[name].add_birthday(birthday_str)
        else:
            return f'Контакт {name} отсутствует в адресной книге'
        return f'Контакту добавлена дата рождения: \n {addressbook[name]}'

    HANDLING = {
        'hello': hello_f,
        'exit': exit_f,
        '.': exit_f,
        'good bye': exit_f,
        'close': exit_f,
        'add': add_f,
        'show all': show_all_f,
        'phone': search,
        'search': search,
        # 'change': change_f,
        'unrecognize': unrecognize_f,
        'help': help_f,
        'other phone': add_phone,
        'bd add': bd_add_f
    }
    return HANDLING[res_pars](addressbook)


def pretty_input(text):
    # print(chr(3196)*80)
    user_input = input(text)
    print(colored(chr(3196) * 80, color='green'))

    return user_input


def main():
    # главный цикл работы программы
    if len(sys.argv) < 2:
        path = CONTACTS_DIR
        name = CONTACTS_FILE
        path_file = Path(path) / name
        addressbook = deserialize_users(
            path_file) if Path.exists(path_file) else AddressBook()

    else:
        path = sys.argv[1]
        name = CONTACTS_FILE
        path_file = Path(path) / name
        addressbook = deserialize_users(path_file)

    while True:
        # addressbook.add_fake_records(40)
        input_string = input('>>>  ')
        # убираем разбор строки на слова и поиск команды
        # res_pars = parse(input_string)

        # сейчас input_string  должен содержать только команду - действие

        result = get_handler(input_string, addressbook)
        if not result:
            serialize_users(addressbook, path_file)
            print('Good bye!')
            break
        print(result)


if __name__ == '__main__':
    main()
