import unittest

from decimal import Decimal

from deprechaun.asset import Asset
from deprechaun.method import straight_line


class TestStraightLine(unittest.TestCase):
    def test_whole_year(self):
        res = [(None, Asset(Decimal('1'), Decimal('5'), straight_line))]

        expect = [
            (None, Asset(Decimal('1'), Decimal('5'), straight_line)),
            (Decimal('0.2'), Asset(Decimal('0.8'), Decimal('4'), straight_line)),
            (Decimal('0.2'), Asset(Decimal('0.6'), Decimal('3'), straight_line)),
            (Decimal('0.2'), Asset(Decimal('0.4'), Decimal('2'), straight_line)),
            (Decimal('0.2'), Asset(Decimal('0.2'), Decimal('1'), straight_line)),
            (Decimal('0.2'), Asset(Decimal('0.0'), Decimal('0'), straight_line)),
            (Decimal('0.0'), Asset(Decimal('0.0'), Decimal('0'), straight_line)),  # doesn't keep depreciating
        ]

        for i in range(6):
            res.append(straight_line(res[-1][1]))
        self.assertEqual(expect, res)
