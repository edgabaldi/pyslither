import datetime
from decimal import Decimal
from unittest import TestCase

from pyslither.column import (Column, MONEY_WITH_IMPLIED_DECIMAL,
                              FormattedStringExceedsLengthError)


class ColumnInstanceTestCase(TestCase):

    def setUp(self):
        name = 'name'
        length = 10
        self.column = Column(name, length)

    def test_should_have_a_name(self):
        self.assertEqual('name', self.column.name)

    def test_should_have_a_length(self):
        self.assertEqual(10, self.column.length)

    def test_should_have_a_default_alignment(self):
        self.assertEqual('right', self.column.alignment)

    def test_should_have_a_default_padding(self):
        self.assertEqual(' ',self.column.padding)


class ColumnParseTestCase(TestCase):
    """
    When parsing a value from a file
    """

    def test_parse_default_a_string(self):
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


class ColumnSpecifyAlignmentTestCase(TestCase):
    """
    When specifying an alignment
    """

    def test_should_override_default_value(self):
        column = Column('name', 10, align='left')
        self.assertEqual('left', column.alignment)

    def test_should_only_accept_right_or_left_for_an_alignment(self):
        with self.assertRaises(AssertionError):
            column = Column('name', 10, align='bogus')


class ColumnApplyingFormattingOptionsTestCase(TestCase):
    """
    When applying formatting options
    """

    def test_should_respect_a_right_alignment(self):
        column = Column('name', 5, align='right')
        self.assertEqual('   25', column.format(25))

    def test_should_respect_a_left_alignment(self):
        column = Column('name', 5, align='left')
        self.assertEqual('25   ', column.format(25))

    def test_should_respect_padding_with_spaces(self):
        column = Column('amount', 5, padding=' ')
        self.assertEqual('   25', column.format(25))

    def test_should_respect_padding_with_zeros_with_integer_type(self):
        column = Column('amount', 5, padding='0', type=int)
        self.assertEqual('00025', column.format(25))

    def test_should_respect_padding_with_zeros_aligned_right_with_decimal_type(self):
        column = Column('amount', 5, type=Decimal, padding='0', align='right')
        self.assertEqual('04.45', column.format(4.45))

    def test_should_respect_padding_with_zeros_aligned_left_with_decimal_type(self):
        column = Column('amount', 5, type=Decimal, padding='0', align='left')
        self.assertEqual('4.450', column.format(4.45))


class ColumnFormattingTestCase(TestCase):
    """
    When formatting values for a file
    """

    def setUp(self):
        self.length = 10

    def test_should_default_to_a_string(self):
        column = Column('name', self.length)
        self.assertEqual('      Bill', column.format('Bill'))

    def test_should_raise_an_error_if_truncate_is_false(self):
        value = "XX" * self.length
        with self.assertRaises(FormattedStringExceedsLengthError):
            column = Column('name', self.length)
            column.format(value)

    def test_should_truncate_from_the_left_if_truncate_is_true_and_aligned_left(self):
        column = Column('name', self.length, truncate=True, align='left')
        self.assertEqual('This is to', column.format('This is too long'))

    def test_should_truncate_from_the_left_if_truncate_is_true_and_aligned_right(self):
        column = Column('name', self.length, truncate=True, align='right')
        self.assertEqual('s too long', column.format("This is too long"))

