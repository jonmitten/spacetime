import time
import unittest
from datetime import datetime
from spacetime import Times, Spaces

class TimesTestCase(unittest.TestCase):

    def setUp(self):
        self.times = Times()
        self.unix_ts_1 = 233409600  # May 25, 1977 at noon GMT
        self.iso_star_wars = '1977-05-25T12:00:00'
        self.unix_ts_2 = 327715200  # May 21, 1980
        self.gps_ts_1 = 11750400    # May 21, 1980
        self.iso_rotj = '1980-05-21T12:00:00'
        self.gps_ts_2 = 1414281600  # Oct 26, 2014




    def test_ticks(self):
        self.assertEqual(self.times.TICKS, 315964800)

    def test_current_unix_time(self):
        """
        expect integer of seconds since unix epoch
        :return: integer - seconds since unix epoch
        """
        t_time = self.times.current_time()
        u_time = time.gmtime()
        u_time = self.times.intstruct(u_time)
        self.assertEqual(round(u_time, 0), t_time)

    def test_current_gps_time(self):
        u_time = time.time()
        u_gps = self.times.current_time(fmt='gps')

    def test_current_iso_time(self):
        # rsplitting the end of these allows for +/- 59 seconds for the test to run.
        # the test is really asserting that the timezones and dates and times are the same,
        # so seconds aren't really too relevant here.
        current_iso_time = (datetime.utcnow()
                            .replace(microsecond=0)
                            .isoformat()).rsplit(':', 1)[0]
        t_iso_time = self.times.iso_time(self.times.current_time()).rsplit(':', 1)[0]
        print(current_iso_time)
        print(t_iso_time)
        self.assertEqual(current_iso_time, t_iso_time)

    def test_unix_iso_time(self):
        sw_unix = self.unix_ts_1
        sw_iso = self.iso_star_wars
        convert = self.times.iso_time(sw_unix, 'unix')
        self.assertEqual(convert, sw_iso)

    def test_unix_gps_time(self):
        rotj_unix = self.unix_ts_2
        rotj_gps = self.gps_ts_1
        self.assertEqual(rotj_unix, self.times.unix_time(rotj_gps, 'gps'))
        self.assertEqual(self.times.gps_time(rotj_unix, 'unix'), rotj_gps)

    def test_gps_iso_time(self):
        rotj_gps = self.gps_ts_1
        rotj_iso = self.iso_rotj
        self.assertEqual(rotj_gps, self.times.gps_time(rotj_iso, 'iso'))
        self.assertEqual(rotj_iso, self.times.iso_time(rotj_gps, 'gps'))

class SpacesTestCase(unittest.TestCase):
    def setUp(self):
        self.spaces = Spaces()

if __name__ == '__main__':
    unittest.main()
