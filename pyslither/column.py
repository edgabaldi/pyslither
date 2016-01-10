import datetime
from decimal import Decimal

MONEY_WITH_IMPLIED_DECIMAL = 'MONEY_WITH_IMPLIED_DECIMAL'

class Column:

    def __init__(self, name, length, type=str, **options):
        self.assert_valid_options(options)
        self.name = name
        self.length = length
        self.type = type
        self.options = options
        self.alignment = options.get('align', 'right')
        self.padding = options.get('padding', ' ')

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

    def format(self, value):
        value = str(value)

        if self.alignment == 'right':
            formated = value.rjust(self.length)
        else:
            formated = value.ljust(self.length)

        if self.padding == '0':
            formated = formated.replace(' ', '0')

        return formated

    def assert_valid_options(self, options):

        if 'align' in options.keys():
            assert options['align'] in ['right', 'left']

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
