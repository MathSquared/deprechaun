import unittest

from decimal import Decimal

from deprechaun.asset import Asset
from deprechaun.method import declining_balance_macrs, declining_balance_only, straight_line


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


class TestDecliningBalanceOnly(unittest.TestCase):
    def test_memo(self):
        self.assertEqual(declining_balance_only(200), declining_balance_only(200))
        self.assertEqual(declining_balance_only(200), declining_balance_only(Decimal('200')))
        self.assertNotEqual(declining_balance_only(200), declining_balance_only(150))

    def test_whole_year(self):
        self.assertEqual(Decimal('0.4'), declining_balance_only(40)(Asset(Decimal('1'), Decimal('5'), declining_balance_only(40))))

    def test_period(self):
        self.assertEqual(Decimal('0.2'), declining_balance_only(40)(Asset(Decimal('1'), Decimal('5'), declining_balance_only(40)), period=Decimal('0.5')))

    def test_end(self):
        # Declining-balance is asymptotic and will not recover the whole value
        # (that's why MACRS switches to straight-line)
        self.assertEqual(Decimal('0.2'), declining_balance_only(40)(Asset(Decimal('1'), Decimal('0.5'), declining_balance_only(40))))


class TestDecliningBalanceMacrs(unittest.TestCase):
    def test_memo(self):
        self.assertEqual(declining_balance_macrs(200), declining_balance_macrs(200))
        self.assertEqual(declining_balance_macrs(200), declining_balance_macrs(Decimal('200')))
        self.assertNotEqual(declining_balance_macrs(200), declining_balance_macrs(150))

    def test_hy_5(self):
        # See IRS, "How to Depreciate Property," Publication 946 (2022), 69, table A-1.
        a = Asset(Decimal('100'), Decimal('5'), declining_balance_macrs(40), -2)
        deps = []
        
        dep, a = a.depreciate(period=Decimal('0.5'))
        deps.append(dep)
        for _ in range(6):  # one more off the end
            dep, a = a.depreciate()
            deps.append(dep)

        self.assertEqual(deps, [
            Decimal('20'), Decimal('32'), Decimal('19.2'), Decimal('11.52'), Decimal('11.52'), Decimal('5.76'), Decimal('0'),
        ])
