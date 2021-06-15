import re
from collections import UserDict

class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __eq__(self, ob) -> bool:
        # два объекта равны если равны строковые значения сохраненных телефонов
        return self.__value == ob.__value

    def __repr__(self):
        return self.__value

class Name(Field):

    def __init__(self, value):
        self.value = value


class Phone(Field):

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):

        # проверка данных на корректность.
        # паттерн  pattern_phone указан в начале программы
        # if re.fullmatch(pattern_phone, new_value):
        # усилием воли было принято решение не применять проверку на корректность
        # просто из строки удалить  все не цифры
        # если количество цифр меньше шести телефон не записывается
        new_value = re.sub(r'[^\d]', '', value)
        if len(new_value) > 6:
            self.__value = new_value

        else:
            self.__value = None
            raise Exception(
                'телефон при вводе может содержать от 3 до 20 цифр и символы: пробел +-()xX.[]_')

            


class Birthday(Field):

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        # предполагаю, что new_value  может быть записан с любыми разделителями
        # извлекаю оттуда только числа
        numbers_date = re.findall(r'\d+', str(new_value))

        # если передали None , или там не три числа
        # значит создаем объект с value = None
        
        # надо продумать вариант когда передали только число и месяц без года
        #  как сохранить эту дату. Возможно в 0004 году
        
        if len(numbers_date) != 3:
            self.__value = None

        # преобразую в кортеж чисел

        # не продумано в каком порядке получаю числа
        # (год, месяц, число) или (число, месяц, год)
        # сейчас написано только для (год, месяц, число)
        numbers_date = tuple(map(int, numbers_date))

        try:
            # если из этих чисел получается дата
            real_time = datetime.datetime.now().date()
            date_birthday = datetime.datetime(*numbers_date).date()
            checking_age = real_time.year - date_birthday.year
            # и эта дата не из будущего и не сильно в прошлом
            if checking_age >= 100:
                self.__value = None
                raise Exception(
                    f'Hey, grandpa! You are too old) Check if you have entered correct birthday date.')
            elif checking_age <= 1:
                self.__value = None
                raise Exception(
                    f'Hey, baby! You are too young) Check if you have entered correct birthday date.')
``
            # присваиваем новое значение даты
            self.__value = date_birthday

        except TypeError:
            self.__value = None
            raise Exception("Incorrect birthday format, expected day-month-year")

    def __repr__(self):
        return self.value.strftime('%d-%m-%Y')

    @property
    def days_to_birthday(self):
        now = datetime.datetime.today().date()

        # отдельный случай  - день рождения 29 февраля
        # чтобы избежать столкновения с 29/2  будем  брать в расчет
        # день на день позже дня рождения.
        # после всех вычислений мы  отнимем один день
        if (self.value.day, self.value.month) == (29, 2):
            bd = self.value + datetime.timedelta(days=1)
        else:
            bd = self.value

        # получаю дату дня  рождения в этому году
        bd_that_year = bd.replace(year=now.year)

        # дельта от дня рождения до сегодня
        delta = bd_that_year - now

        # если она отрицательна, то значит др в этом году уже прошел
        if delta.days <= 0:

            # надо брать дату дня рождения следующего года
            bd_that_year = bd_that_year.replace(year=now.year+1)

            # дельта от дня рождения в следующем году до сегодня
            delta = bd_that_year - now

        if (self.value.day, self.value.month) == (29, 2):
            return delta.days - 1
        return delta.days

class Record():

    def __init__(self, name, phone='', birthday=Birthday(None)):
        self.name = name
        self.phones = [phone]
        self.birthday = birthday
    
    def add_phone(self, phone):
        self.phones.append(phone)

    def del_phone(self, phone):
        # удаляет телефон из записи. При попытке удалить несуществующий номер
        # телефона - генерирует исключение
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise Exception(
                'операция удаления: такого телефона нет в данной записи')

    def change_phone(self, old_phone, new_phone):
        # замена номера телефона - удаление старого и добавление нового
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday):
        # добавляет день рождения в существующую запись
        self.birthday = birthday

    def search(self, pattern):
        # просматривает текстовые поля записи (name, phone). Если встречает \
        # сответствие паттерну - возвращает экземпляр записи. Иначе возвращает\
        # False
        if pattern.casefold() in self.name.casefold(): # 'self.name.casefold() это работает? разве не self.name.value.casefold()
            return self
        #for phone in self.phones:
        #    if pattern.casefold() in phone.value:
        #        return self
        
        # должно сработать, так как переопределен метод __eq__
        if pattern in self.phones :
            return self
        return False

    # нужно написать 
    def search_nearest_birthday(self, N):
        #функцию, которая будет искать абонентов, 
        # дни рождения которых будут в ближайшие N  дней.
        # удобно использовать метод Birthday.days_to_birthday
        pass

    def search_birthday(self, data_start, data_stop=False, year: bool = False):
        # если дата рождения находится в интервале от data до data_stop\
        # возвращает экзкмпляр записи, иначе возвращает False. Если \
        # date_stop=False, то сравнение проходит не по интервалу дат, а по\
        # одной дате date. Если year=False - то при сравнении год не \
        # учитывается, иначе год участвует в сравнении
        if not self.birthday.value:
            # если дата рождения не записана - возвращаем None
            return None

        data_start_local = datetime.strptime(data_start, "%d-%m-%Y")
        data_stop_local = datetime.strptime(
            data_stop, "%d-%m-%Y") if data_stop else datetime.strptime(data_start, "%d-%m-%Y") + timedelta(days=1)
        data_record_local = self.birthday.birthday

        if not year:
            # если year=False то все даты приводятся к текущему году (сравниваются только\
            # по числу и месяцу )
            current_year = date.today().year
            data_start_local = data_start_local.replace(year=current_year)
            data_stop_local = data_stop_local.replace(year=current_year)
            data_record_local = data_record_local.replace(year=current_year)

        if data_start_local <= data_record_local < data_stop_local:
            return self
        # если дата рождения попадает в интервал - возвращаем экземпляр записи, иначе False
        return False

    def __repr__(self):
        # форматирует и выводит одну запись в читаемом виде одной или нескольких строк
        # (если запись содержит несколько телефонов)
        # этот метод надо передалать Ярославу.
        st = f"| {self.name:.<40}| {self.birthday.__repr__(): <11} | {self.phones[0].__repr__() if self.phones else '': <20} |\n"
        if len(self.phones) > 1:
            for elem in self.phones[1:]:
                st += f" |                                         |             | {elem.__repr__(): <20} |\n"
        return st

class AddressBook(UserDict):

    """
    The class inherits from UserDict class.

    Creates <dict> for saving record for even abonent, where key is abonent's name.

    Methods defined in the class are:

    <add_record(self, record)>, takes contact's  record, 
    
    returns dict with new element.

    <iterator(self, n)>, method returns a record generator, 
    
    takes <n> - number of records in <self.data> that will be returned in 
    
    one generator call

    <search_contacts(self, user_input)>, method searches contact's data by the given from a user partial info



    """
    # два следующих метода  - инструкции для сериализации
    # и десериализации  экземпляра класса  AddressBook
    # ----------------------------------
    def __getstate__(self):
        # deepcopy  для перестраховки.
        atr = copy.deepcopy(self.__dict__)
        return atr

    def __setstate__(self, atr):
        self.__dict__ = atr
    # -----------------------------------

    def add_record(self, record: Record):
        # добавляет новую запись в существующую адресную книгу.


        # метод на входе не пропустит аргумент не классса Record
        # но при этом программа вернет ошибку
        # нужно ли нам это? как перехватить эту ошибку ?
        # или проще написать свой тест :
        #if not isinstance(record, Record):
        #    raise Exception(
        #        'В метод передан не объект класса Record')


        # Если запись с таким ключем (именем) уже существует - генерирует исключение
        if record.name in self:
            raise Exception(
                'Запись с таким именем уже существует в адресной книге')
        # ? self[record.name] = record
        self[record.name.value] = record
    
    def del_record(self, name: str):
        # удаляет запись с ключем name (строка)
        # из существующей адресной книги. Если такого имени нет - генерирует исключение
        if name in self:
            self.pop(name)
        else:
            raise Exception('записи с таким именем нет в адресной книге')

    def search(self, user_input):
        # возвращает объект класса AdressBook, содержащий
        # все записи, которые при проверке методом Record.search вернут значение
        result = AdressBook()

        for record in self.values():
            res_rec = record.search(user_input)
            if res_rec:
                result.add_record(res_rec)
        return result

    def search_birthday(self, data_start, data_stop=False, year: bool = False):
        # возвращает объект класса AdressBook, содержащий записи, для которых \
        # день рождения попадает в интервал дат data_start и data_stop. \
        # Для всех аргументов действуют те же правила, что и для метода \
        # Birthday.search_bithday()
        result = AdressBook()
        for record in self.values():
            res_rec = record.search_birthday(data_start, data_stop, year)
            if res_rec:
                result.add_record(res_rec)
        return result

    def iterator(self, n):
        '''
        метод возвращает на каждой итерации объект класса AdressBook, 
        содержащий n записей из вызывающего метод объекта AdressBook,
        на последнем шаге (исчерпание записей вызывающего объекта) выводятся
        оставшиеся записи
        '''
        # количество элементов выводимых за один вызов метода
        self.n = n
        # счетчик общего количества выведенных записей
        self.k = 0
        # список из ключей вызывающего метод объекта AdressBook
        key_list = list(self)
        # общее кличество записей, которые должны быть выведены
        len_key_list = len(key_list)
        while self.k < len_key_list:
            result = AdressBook()
            # определяем сколько записей можно вывести на текущем шаге (на последнем шаге
            # выводим меньше чем n)
            #max_iter = key_list_max if len(
            #    key_list[self.k:]) < self.n else self.k + self.n
            
            max_iter = min(len_key_list, self.k + self.n)

            for i in range(self.k, max_iter):
                result.add_record(self[key_list[i]])
                self.k += 1
            yield result

    def __repr__(self) -> str:
        #  это метод проверить Ярославу
        # правильно ли он работает в связке с record.__repr__
        res = ''
        for elem in self.values():
            res += elem.__repr__()
        return res

    def add_fake_records(self, n):
        '''
        рабочий метод, для отладки и демонстрации
        заполняет словарь фейковыми данными
        '''
        fake = Faker(['uk_UA', 'ru_RU'])
        for i in range(n):
            name = fake.name()
            phone = fake.phone_number()
            date_of_birth = fake.date_of_birth(
                minimum_age=10, maximum_age=115).strftime('%d-%m-%Y')
            record = Record(name, date_of_birth).add_phone(phone)
            self.add_record(record)
            print(f'Добавлена запись: {name}  {date_of_birth}  {phone}')
            print(
                f'вид в record: {record.name}  {record.birthday.birthday:%d-%m-%Y}  {record.phones[0].phone}')


if __name__ == '__main__':
    pass
