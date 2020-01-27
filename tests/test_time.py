import time
import unittest
from datetime import datetime, timezone
from spacetime import Times, Spaces

class TimesTestCase(unittest.TestCase):

    def setUp(self):
        self.times = Times()
        self.unix_ts_1 = 233366400  # May 25, 1977
        self.unix_ts_2 = 327715200  # May 21, 1980
        self.gps_ts_1 = 11750400    # May 21, 1980
        self.gps_ts_2 = 1414281600  # Oct 26, 2014



    def test_ticks(self):
        self.assertEqual(self.times.TICKS, 315964800)

    def test_current_time(self):
        t_time = self.times.current_time()
        u_time = time.gmtime()
        u_time = self.times.intstruct(u_time)
        self.assertEqual(round(u_time, 0), t_time)

    def test_current_gps_time(self):
        u_time = time.time()
        u_gps = self.times.current_time(fmt='gps')

    def test_current_iso_time(self):
        current_iso_time = (datetime.utcnow()
                            .replace(microsecond=0)
                            .isoformat())
        t_iso_time = self.times.iso_time(self.times.current_time())
        self.assertEqual(current_iso_time, t_iso_time)

class SpacesTestCase(unittest.TestCase):
    def setUp(self):
        self.spaces = Spaces()

if __name__ == '__main__':
    unittest.main()
