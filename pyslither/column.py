import datetime
from decimal import Decimal

MONEY_WITH_IMPLIED_DECIMAL = 'MONEY_WITH_IMPLIED_DECIMAL'

class Column:

    def __init__(self, name, length, type=str, **options):
        self.name = name
        self.length = length
        self.type = type
        self.options = options

    def parse(self, value):

        if self.type is int:
            return self.to_int(value)

        elif self.type is Decimal:
            return self.to_decimal(value)

        elif self.type is MONEY_WITH_IMPLIED_DECIMAL:
            value = self.to_decimal(value)
            return value / 100

        elif self.type is datetime.date:
            return self.to_date(value)

        return self.to_str(value)

    def to_str(self, value):
        return value.strip()

    def to_int(self, value):
        try:
            value = int(float(value))
        except ValueError:
            value = 0
        return value

    def to_decimal(self, value):
        try:
            value = Decimal(value)
        except:
            value = Decimal(0)
        return value

    def to_date(self, value):
        if 'format' in self.options.keys():
            format = self.options['format']
        else:
            format = '%Y-%m-%d'
        return datetime.datetime.strptime(value, format).date()
