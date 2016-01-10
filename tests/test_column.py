import datetime
from decimal import Decimal
from unittest import TestCase

from pyslither.column import Column, MONEY_WITH_IMPLIED_DECIMAL


class ColumnTestCase(TestCase):

    def test_parse_default_as_string(self):
        column = Column('name', 10)
        self.assertEqual('name', column.parse('    name '))
        self.assertEqual('234', column.parse('    234'))
        self.assertEqual('0000234', column.parse('0000234'))
        self.assertEqual('12.34', column.parse('12.34'))

    def test_parse_should_support_integer_type(self):
        column = Column('amount', 10, type=int)

        self.assertEqual(234, column.parse('234     '))
        self.assertEqual(234, column.parse('     234'))
        self.assertEqual(234, column.parse('00000234'))
        self.assertEqual(0, column.parse('Ryan'))
        self.assertEqual(23, column.parse('00023.45'))

    def test_parse_should_support_decimal_type(self):
        column = Column('amount', 10, type=Decimal)

        self.assertEqual(Decimal('234.45'), column.parse('  234.45'))
        self.assertEqual(Decimal('234.56'), column.parse('234.5600'))
        self.assertEqual(Decimal('234'), column.parse('   234'))
        self.assertEqual(Decimal('234'), column.parse('0000234'))
        self.assertEqual(Decimal('0'), column.parse('Ryan'))
        self.assertEqual(Decimal('23.45'), column.parse('00023.45'))

    def test_parse_should_support_money_with_implied_decimal_type(self):
        column = Column('amount', 10, type=MONEY_WITH_IMPLIED_DECIMAL)
        self.assertEqual(Decimal('234.45'),column.parse('   23445'))

    def test_parse_should_support_date_type(self):
        column = Column('date', 10, type=datetime.date)
        date = column.parse('2016-01-10')
        self.assertEqual(datetime.date(2016, 1, 10), date)
        self.assertTrue(isinstance(date, datetime.date))

    def test_parse_should_use_format_option_with_date_type_if_avaliable(self):
        column = Column('date', 10, type=datetime.date, format='%d/%m/%Y')
        date = column.parse('10/01/2016')
        self.assertEqual(datetime.date(2016, 1, 10), date)


