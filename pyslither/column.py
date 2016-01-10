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
            try:
                value = int(float(value))
            except ValueError:
                value = 0
            return value
        elif self.type is Decimal:
            try:
                value = Decimal(value)
            except:
                value = Decimal(0)
            return value
        elif self.type is MONEY_WITH_IMPLIED_DECIMAL:
            try:
                value = Decimal(value)
            except:
                value = Decimal(0)
            return value / 100
        elif self.type is datetime.date:
            if 'format' in self.options.keys():
                format = self.options['format']
            else:
                format = '%Y-%m-%d'
            return datetime.datetime.strptime(value, format).date()
        return value.strip()
