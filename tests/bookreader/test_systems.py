from datetime import date
from decimal import Decimal
import unittest

from deprechaun.asset import Asset
from deprechaun.bookreader import BookAsset
from deprechaun.bookreader.systems import time_system_hydrate, time_system_step, time_system_translate, TimeSystemData, TimeSystemOffsetSubstitute
from deprechaun.method import straight_line


class TestTimeSystem(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.base = BookAsset(
            name='base',
            acquired=date(2023, 1, 1),
            basis_start=Decimal('100'),
            basis_impairment=[Decimal('0')],
            basis_adjustment=[Decimal('0')],
            system='time',
            system_data=TimeSystemData(
                life=Decimal('5'),
                offset=Decimal('0'),
                method=straight_line,
            ),
        )

    def test_hydrate_noop(self):
        self.assertEqual([self.base], time_system_hydrate([self.base]))

    def test_hydrate_day(self):
        a = self.base._replace(
            system_data=self.base.system_data._replace(offset=TimeSystemOffsetSubstitute.DAY),
        )
        self.assertEqual(
            [self.base._replace(
                system_data=self.base.system_data._replace(offset=Decimal('0')),
            )],
            time_system_hydrate([a]),
        )

        a = self.base._replace(
            acquired=date(2023, 2, 1),
            system_data=self.base.system_data._replace(offset=TimeSystemOffsetSubstitute.DAY),
        )
        self.assertEqual(
            [self.base._replace(
                acquired=date(2023, 2, 1),
                system_data=self.base.system_data._replace(offset=Decimal('31') / 365),
            )],
            time_system_hydrate([a]),
        )

    def test_hydrate_month(self):
        a = self.base._replace(
            system_data=self.base.system_data._replace(offset=TimeSystemOffsetSubstitute.MONTH),
        )
        self.assertEqual(
            [self.base._replace(
                system_data=self.base.system_data._replace(offset=Decimal('0')),
            )],
            time_system_hydrate([a]),
        )

        a = self.base._replace(
            acquired=date(2023, 2, 6),
            system_data=self.base.system_data._replace(offset=TimeSystemOffsetSubstitute.MONTH),
        )
        self.assertEqual(
            [self.base._replace(
                acquired=date(2023, 2, 6),
                system_data=self.base.system_data._replace(offset=Decimal('1') / 12),
            )],
            time_system_hydrate([a]),
        )

    def test_translate(self):
        a = self.base
        self.assertEqual(
            Asset(
                basis=Decimal('100'),
                life=Decimal('5'),
                method=straight_line,
                precision=None,
            ),
            time_system_translate(a),
        )

        a = self.base._replace(
            basis_impairment=[Decimal('20')],
            basis_adjustment=[Decimal('10')],
            system_data=self.base.system_data._replace(offset=Decimal('0.5')),
            precision=-2,
        )
        self.assertEqual(
            Asset(
                basis=Decimal('130'),
                life=Decimal('5'),
                method=straight_line,
                precision=-2,
            ),
            time_system_translate(a),
        )

    def test_step(self):
        a = self.base
        self.assertEqual(
            Decimal('1'),
            time_system_step(a, 2023),
        )
        self.assertEqual(
            Decimal('1'),
            time_system_step(a, 2024),
        )

        a = self.base._replace(
            acquired=date(2023, 2, 6),
            system_data=self.base.system_data._replace(offset=Decimal('1') / 12),
        )
        self.assertEqual(
            Decimal('11') / 12,
            time_system_step(a, 2023),
        )
        self.assertEqual(
            Decimal('1'),
            time_system_step(a, 2024),
        )
