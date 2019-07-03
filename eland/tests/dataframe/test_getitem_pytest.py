# File called _pytest for PyCharm compatability
from eland.tests.common import TestData

import pandas as pd
import io

from pandas.util.testing import (
    assert_series_equal, assert_frame_equal)

class TestDataFrameGetItem(TestData):

    def test_getitem_basic(self):
        # Test 1 attribute
        pd_carrier = self.pd_flights()['Carrier']
        ed_carrier = self.ed_flights()['Carrier']

        # pandas returns a Series here
        assert_series_equal(pd_carrier.head(100), ed_carrier.head(100))

        pd_3_items = self.pd_flights()[['Dest','Carrier','FlightDelay']]
        ed_3_items = self.ed_flights()[['Dest','Carrier','FlightDelay']]

        assert_frame_equal(pd_3_items.head(100), ed_3_items.head(100))

        # Test numerics
        numerics = ['DistanceMiles', 'AvgTicketPrice', 'FlightTimeMin']
        ed_numerics = self.ed_flights()[numerics]
        pd_numerics = self.pd_flights()[numerics]

        assert_frame_equal(pd_numerics.head(100), ed_numerics.head(100))

        # just test headers
        ed_numerics_describe = ed_numerics.describe()
        assert ed_numerics_describe.columns.tolist() == numerics

    def test_getattr_basic(self):
        # Test 1 attribute
        pd_carrier = self.pd_flights().Carrier
        ed_carrier = self.ed_flights().Carrier

        assert_series_equal(pd_carrier.head(100), ed_carrier.head(100))

        pd_avgticketprice = self.pd_flights().AvgTicketPrice
        ed_avgticketprice = self.ed_flights().AvgTicketPrice

        assert_series_equal(pd_avgticketprice.head(100), ed_avgticketprice.head(100))

