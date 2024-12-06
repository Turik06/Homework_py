class USADate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def format(self):
        return f"{self.month:02d}-{self.day:02d}-{self.year}"

    def iso_format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"


class ItalianDate(USADate):
    def __init__(self, year, month, day):
        super().__init__(year, month, day)

    def format(self):
        return f"{self.day:02d}-{self.month:02d}-{self.year}"

    def iso_format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

usa_date = USADate(2024, 12, 5)
print(usa_date.format())
print(usa_date.iso_format())


italian_date = ItalianDate(2024, 12, 5)
print(italian_date.format())
print(italian_date.iso_format())
