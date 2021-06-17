from classes import AddressBook, Record, Phone, Birthday
from os import name
import sys
import pickle
from pathlib import Path
from faker import Faker

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

    def hello_f(*args):
        return 'How can I help you?'

    def exit_f(name, phone, contacts):
        return None

    def add_f(addressbook):
        #  сначала создает запись с именем
        #  потом последовательно вызывает функции
        # для заполнения телефона, д/р, заметки, и т.д.
        name = pretty_input('Введите имя ')
        record = Record(name)
        addressbook.add_record(record)

        add_phone(record)
        change_bd(record)
        change_adr(record)
        change_eml(record)
        add_note(record)

        pretty_print(f'в адресную книгу внесена запись: \n{record}')
        return True

    def add_note(record):
        pass

    def change_note(record):
        pass

    def change_eml(record):
        pass

    def change_adr(record):
        pass

    def change_name(record):
        name = pretty_input('Введите новое имя ')
        addressbook.del_record(name)
        record.change_name(name)
        addressbook(record)

    def change_bd(record):
        birthday_str = pretty_input(
            'введите день рождения в формате дд-мм-гггг ("ввод" - пропустить): ')
        if birthday_str:
            result = record.add_birthday(birthday_str)
            if isinstance(result, Exception):
                return result
            return f'в запись добавлен день рождения: \n {record}'
        else:
            return 'абоненту день рождения не добавлен'

    def add_phone(record):
        # позволяет добавить в запись дополнительный телефон
        phone = pretty_input('Entry phone number ')
        result = record.add_phone(phone)

        if isinstance(result, Exception):
            return result
        return f'в запись добавлен новый телефон: \n {record}'

    def change_phone(record):

        pretty_print(record)
        old_phone = pretty_input(
            'What number you want to change (enter item number) ')

        new_phone = pretty_input('Entry new phone number ')
        result = record.change_phone(old_phone, new_phone)
        if isinstance(result, Exception):
            return result
        return f'в запись добавлен новый телефон: \n {record}'

    def change_f(addressbook):
        # была закоментирована, так как по сути своей совершенно бессмысленная функция
        name = pretty_input('Введите имя ')
        record = addressbook[name]
        pretty_print(record)
        pretty_print(menu_change)
        item_number = input('>>>  ')
        return func_change[item_number](record)

    def search(addressbook):
        user_input = pretty_input('What are you looking for?  ')
        # осуществляет поиск введенной строки во всех текстовых полях адресной книги
        result = addressbook.search(user_input)

        if not result:
            raise Exception('По данному запросу ничего не найдено')

        return result

    def delete_f(addressbook):
        name = pretty_input('Введите имя ')
        result = addressbook.del_record(name)
        return result

    def show_all_f(addressbook, N=10):
        # выводит на экран всю адресную книгу блоками по N записей. Основная обработка
        # реализована как метод класса addressbook, что позволяет использовать аналогичный
        # вывод для результатов поиска по запросам, так как функции поиска возвращают
        # объект типа addressbook с результатами
        n = int(N)
        print(f'всего к выводу {len(addressbook)} записей: ')
        for block in addressbook.out_iterator(n):
            print(block)
            print('---------------------------------------------------------------------------------------------------')
            input('для продолжения вывода нажмите "ввод"')
        return 'вывод окончен'

    def unrecognize_f(name, raw_string, x):
        # Константин, твой выход !
        return 'ввод не распознан. Для получения помощи введите "help"'

    menu_change = ''' 
    What you want to change:    1. name 
                                2. change phone 
                                3. add phone
                                4. change birthday
                                5. change e-mail
                                6. change address
                                7. change note
                                8. add note
    '''

    func_change = {'1':  change_name,
                   '2': change_phone,
                   '3': add_phone,
                   '4': change_bd,
                   '5': change_eml,
                   '6': change_adr,
                   '7': change_note,
                   '8': add_note}

    HANDLING = {
        '1': add_f,
        '2': change_f,
        '3': delete_f,
        '4': search,
        '5': show_all_f,
        '6': exit_f,
        'hello': hello_f,
        'exit': exit_f,
        '.': exit_f,
        'good bye': exit_f,
        'close': exit_f,
        'add': add_f,
        'show all': show_all_f,
        'phone': search,
        'search': search,
        'change': change_f,
        'unrecognize': unrecognize_f,
        'help': help_f,
        'other phone': add_phone,
        'bd add': change_bd
    }

    result = HANDLING.get
    return HANDLING[res_pars](addressbook)


def pretty_input(text):
    # функция для Ярослава
    # print(chr(3196)*80)
    user_input = input(text)
    print(chr(3196)*80)
    return user_input


def pretty_print(text):
    # функция для Ярослава
    print(text)
    print(chr(3196)*80)


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

    menu = '''You can :
                1. add abonent to addressbook
                2. change abonent's record in addressbook
                3. delete abonent from addressbook
                4. seek abonent or phone
                5. show all 
                6. end 
            Choose menu item number'''

    while True:
        # addressbook.add_fake_records(40)

        pretty_print(menu)
        input_string = input('>>>  ')
        # убираем разбор строки на слова и поиск команды
        #res_pars = parse(input_string)

        # сейчас input_string  должен содержать только номер команду - действие

        result = get_handler(input_string, addressbook)
        if not result:
            serialize_users(addressbook, path_file)
            print('Good bye!')
            break
        print(result)


if __name__ == '__main__':
    main()
