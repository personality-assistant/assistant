import re
from collections import UserDict
from datetime import datetime

from faker import Faker


class Record:

    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def del_phone(self, phone):
        self.phones.remove(Phone(phone))

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def __repr__(self):
        return self.name


class Phone:

    def __init__(self, phone):
        self._phones = []
        self.phone = phone

    @property
    def phone(self):
        return self._phones

    @phone.setter
    def phone(self, value):
        try:
            value = str(value)
            treatment = (value.strip()
                         .replace('+', '')
                         .replace(')', '')
                         .replace('(', '')
                         .replace('-', '')
                         .replace(' ', '')
                         )
            validate = re.fullmatch('\\d{5,20}', treatment)
            if validate:
                self._phones = treatment
            else:
                print(f'Expected number in format +ХХХХХХХХХХХ or ХХХХХХХХХХ and 5-20 digits')
        except Exception as error:
            print(f'Bad request, expected string. {error}')

    def __repr__(self):
        return self._phones


class Birthday:

    def __init__(self, birthday: str):
        self._birthday = 'Дата не установлена'
        self.birthday = birthday

    @property
    def birthday(self):
        if isinstance(self._birthday, datetime):
            return self._birthday.date()
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        try:
            self._birthday = datetime.strptime(value, '%d-%m-%Y')
        except TypeError:
            print("Incorrect birthday format, expected day-month-year")

    def days_to_birthday(self):
        if self.birthday:
            now_date = datetime.now()
            birthday_date = datetime.strptime(self.birthday, '%d.%m.%Y')
            delta1 = datetime(now_date.year, birthday_date.month, birthday_date.day)
            delta2 = datetime(now_date.year + 1, birthday_date.month, birthday_date.day)
            days = (max(delta1, delta2) - now_date).days + 1
            if days >= 365:
                return days - 365
            else:
                return days

    def __repr__(self):
        if isinstance(self._birthday, datetime):
            return f'{self._birthday.date()}'


class AddressBook(UserDict):

    def add_record(self, record):
        self[record.name] = f'-Phone(s): {record.phones}\n-Birthday_date: {record.birthday}\n'

    def find_contact(self, obj: str):
        result = []
        for key, value in self.items():
            str_data = f'''Name: {key}
---Phone: {value}'''
            if re.findall(obj.casefold(), str_data.casefold()):
                result.append(str_data)
        return result

    def iterable(self, n):
        self.i = 0
        lenght = len(self)
        users_list = list(self)
        while self.i < lenght:
            result = []
            next_iter = lenght if len(users_list[self.i:]) < int(n) else self.i + int(n)
            for j in range(self.i, next_iter):
                user = f'\n{users_list[j]}\n{self[users_list[j]]}\n'
                result.append(user)
                self.i += 1
            yield result


    def add_fake_records(self, n):
        fake = Faker(['uk_UA'])
        for i in range(n):
            name = fake.name()
            phone = fake.phone_number()
            date_of_birth = fake.date_of_birth(
                minimum_age=10, maximum_age=100).strftime('%d-%m-%Y')
            record = Record(name)
            record.add_phone(phone)
            record.add_birthday(date_of_birth)
            self.add_record(record)

    def __repr__(self):
        return self.data
