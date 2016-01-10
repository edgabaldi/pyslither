from unittest import TestCase

from pyslither.column import Column


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

    def test_parse_should_support_float_type(self):
        pass

    def test_parse_should_support_money_with_implied_decimal_type(self):
        pass

    def test_parse_should_support_date_type(self):
        pass

    def test_parse_should_use_format_option_with_date_type_if_avaliable(self):
        pass


