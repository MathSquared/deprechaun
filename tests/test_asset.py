import unittest
from unittest.mock import MagicMock

from decimal import Decimal

from deprechaun.asset import Asset
from deprechaun.method import straight_line


class TestAsset(unittest.TestCase):
    def test_depreciate(self):
        a = Asset(Decimal('1'), Decimal('5'), straight_line)
        dep, b = a.depreciate()
        self.assertEqual(Decimal('0.2'), dep)
        self.assertEqual(Asset(Decimal('0.8'), Decimal('4'), straight_line), b)

    def test_depreciate_period(self):
        mock_method = MagicMock(return_value=Decimal('1'))
        a = Asset(Decimal('4'), Decimal('2'), mock_method)
        _, b = a.depreciate(period=Decimal('0.5'))
        mock_method.assert_called_with(a, period=Decimal('0.5'))
        self.assertEqual(Asset(Decimal('3'), Decimal('1.5'), mock_method), b)

    def test_depreciate_end(self):
        mock_method = MagicMock(return_value=Decimal('1'))
        a = Asset(Decimal('1'), Decimal('0.5'), mock_method)
        _, b = a.depreciate()
        mock_method.assert_called_with(a, period=Decimal('0.5'))
        self.assertEqual(Asset(Decimal('0'), Decimal('0'), mock_method), b)
