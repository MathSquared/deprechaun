import unittest

from decimal import Decimal

from deprechaun.asset import Asset
from deprechaun.method import straight_line


class TestStraightLine(unittest.TestCase):
    def test_whole_year(self):
        self.assertEqual(Decimal('0.2'), straight_line(Asset(Decimal('1'), Decimal('5'), straight_line)))
        self.assertEqual(Decimal('0.2'), straight_line(Asset(Decimal('0.8'), Decimal('4'), straight_line)))
        self.assertEqual(Decimal('0.2'), straight_line(Asset(Decimal('0.6'), Decimal('3'), straight_line)))
        self.assertEqual(Decimal('0.2'), straight_line(Asset(Decimal('0.4'), Decimal('2'), straight_line)))
        self.assertEqual(Decimal('0.2'), straight_line(Asset(Decimal('0.2'), Decimal('1'), straight_line)))
        self.assertEqual(Decimal('0'), straight_line(Asset(Decimal('0'), Decimal('0'), straight_line)))

    def test_fractional_year(self):
        self.assertEqual(Decimal('2'), straight_line(Asset(Decimal('3'), Decimal('1.5'), straight_line)))
        self.assertEqual(Decimal('1'), straight_line(Asset(Decimal('1'), Decimal('0.5'), straight_line)))
        self.assertEqual(Decimal('0'), straight_line(Asset(Decimal('0'), Decimal('0'), straight_line)))

    def test_fractional_period(self):
        self.assertEqual(Decimal('1'), straight_line(Asset(Decimal('4'), Decimal('2'), straight_line), period=Decimal('0.5')))
