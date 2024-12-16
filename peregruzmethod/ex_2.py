from datetime import date
from functools import singledispatchmethod

class BirthInfo:
    def __init__(self, birth_date):
        self.birth_date = self._parse_birth_date(birth_date)

    @singledispatchmethod
    def _parse_birth_date(self, birth_date):
        raise TypeError("Аргумент переданного типа не поддерживается")

    @_parse_birth_date.register
    def _(self, birth_date: date):
        return birth_date

    @_parse_birth_date.register
    def _(self, birth_date: str):
        if len(birth_date) == 10 and birth_date[4] == '-' and birth_date[7] == '-':
            year, month, day = birth_date.split('-')
            if year.isdigit() and month.isdigit() and day.isdigit():
                return date(int(year), int(month), int(day))
        raise TypeError("Аргумент переданного типа не поддерживается")

    @_parse_birth_date.register
    def _(self, birth_date: (list| tuple)):
        if len(birth_date) == 3 and all(isinstance(i, int) for i in birth_date):
            return date(*birth_date)
        raise TypeError("Аргумент переданного типа не поддерживается")


    @property
    def age(self):
        today = date.today()
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years


birthinfo1 = BirthInfo(date(2024, 12, 17))
birthinfo2 = BirthInfo("2000-01-01")
birthinfo3 = BirthInfo([1990, 5, 15])

print(birthinfo1.age)
print(birthinfo2.age)
print(birthinfo3.age)

