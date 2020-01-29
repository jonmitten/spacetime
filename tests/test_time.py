import time
import unittest
from bitstring import Bits
from datetime import datetime
from spacetime import Times, Spaces

class TimesTestCase(unittest.TestCase):

    def setUp(self):
        self.times = Times()
        self.unix_ts_1 = 233409600  # May 25, 1977 at noon GMT
        self.iso_star_wars = '1977-05-25T12:00:00'
        self.unix_rotj = 327715200  # May 21, 1980 Midnight
        self.gps_rotj = 11750400    # May 21, 1980 Midnight
        self.iso_rotj = '1980-05-21T00:00:00'
        self.unix_interstellar = 1414281600  # Oct 26, 2014
        self.gps_interstellar = 1098316800  # Oct 26, 2014
        self.iso_interstellar = '2014-10-26T00:00:00'
        self.hex_gps_interstellar = '4176FC00'  # Oct 26, 2014


    def test_ticks(self):
        self.assertEqual(self.times.TICKS, 315964800)

    # def test_current_unix_time(self):
    #     """
    #     expect integer of whole_seconds since unix epoch
    #     :return: integer - whole_seconds since unix epoch
    #     """
    #     t_time = self.times.current_time()
    #     u_time = time.gmtime()
    #     u_time = self.times.struct_time_to_int(u_time)
    #     self.assertEqual(round(u_time, 0), t_time)

    def test_current_gps_time(self):
        u_time = time.time()
        u_gps = self.times.current_time(fmt='gps')

    def test_current_iso_time(self):
        # rsplitting the end of these allows for +/- 59 whole_seconds for the test to run.
        # the test is really asserting that the timezones and dates and times are the same,
        # so whole_seconds aren't really too relevant here.
        current_iso_time = (datetime.utcnow()
                            .replace(microsecond=0)
                            .isoformat()).rsplit(':', 1)[0]
        t_iso_time = self.times.iso_time(self.times.current_time()).rsplit(':', 1)[0]
        self.assertEqual(current_iso_time, t_iso_time)

    def test_unix_iso_time(self):
        sw_unix = self.unix_ts_1
        sw_iso = self.iso_star_wars
        convert = self.times.iso_time(sw_unix, 'unix')
        self.assertEqual(convert, sw_iso)

    def test_unix_gps_time(self):
        rotj_unix = self.unix_rotj
        rotj_gps = self.gps_rotj
        self.assertEqual(self.times.gps_time(rotj_unix, 'unix'), rotj_gps)

    def test_unix_gps_time2(self):
        rotj_unix = self.unix_rotj
        rotj_gps = self.gps_rotj
        self.assertEqual(rotj_unix, self.times.unix_time(rotj_gps, 'gps'))

    def test_gps_iso_time(self):
        rotj_gps = self.gps_rotj
        rotj_iso = self.iso_rotj
        self.assertEqual(rotj_gps, self.times.gps_time(rotj_iso, 'iso'))

    def test_gps_iso_time2(self):
        rotj_gps = self.gps_rotj
        rotj_iso = self.iso_rotj
        self.assertEqual(rotj_iso, self.times.iso_time(rotj_gps, 'gps'))

    def test_interstellar_time_unix2gps(self):
        gps = self.gps_interstellar
        uni = self.unix_interstellar
        self.assertEqual(gps, self.times.gps_time(uni, 'unix'))

    def test_interstellar_time_iso2gps(self):
        gps = self.gps_interstellar
        iso = self.iso_interstellar
        self.assertEqual(gps, self.times.gps_time(iso, 'iso'))

    def test_interstellar_time_hex2gps(self):
        gps = self.gps_interstellar
        gex = self.hex_gps_interstellar
        self.assertEqual(gps, self.times.gps_time(gex, 'hexgps'))

    def test_interstellar_time_gps2unix(self):
        gps = self.gps_interstellar
        uni = self.unix_interstellar
        self.assertEqual(uni, self.times.unix_time(gps, 'gps'))

    def test_interstellar_time_iso2unix(self):
        uni = self.unix_interstellar
        iso = self.iso_interstellar
        self.assertEqual(uni, self.times.unix_time(iso, 'iso'))

    def test_interstellar_time_hex2unix(self):
        uni = self.unix_interstellar
        gex = self.hex_gps_interstellar
        self.assertEqual(uni, self.times.unix_time(gex, 'hexgps'))

    def test_interstellar_time_unix2iso(self):
        uni = self.unix_interstellar
        iso = self.iso_interstellar
        self.assertEqual(iso, self.times.iso_time(uni, 'unix'))

    def test_interstellar_time_gps2iso(self):
        gps = self.gps_interstellar
        iso = self.iso_interstellar
        self.assertEqual(iso, self.times.iso_time(gps, 'gps'))

    def test_interstellar_time_hex2iso(self):
        iso = self.iso_interstellar
        gex = self.hex_gps_interstellar
        self.assertEqual(iso, self.times.iso_time(gex, 'hexgps'))

    def test_interstellar_time_unix2hex(self):
        uni = self.unix_interstellar
        gex = self.hex_gps_interstellar
        self.assertEqual(gex, self.times.gpshex_time(uni, 'unix'))

    def test_interstellar_time_gps2hex(self):
        gps = self.gps_interstellar
        gex = self.hex_gps_interstellar
        self.assertEqual(gex, self.times.gpshex_time(gps, 'gps'))

    def test_interstellar_time_iso2hex(self):
        iso = self.iso_interstellar
        gex = self.hex_gps_interstellar
        self.assertEqual(gex, self.times.gpshex_time(iso, 'iso'))


class SpacesTestCase(unittest.TestCase):
    def setUp(self):
        self.spaces = Spaces()
        # https://www.google.com/maps/place/Seattle-Tacoma+International+Airport/@47.4502535,-122.3110052,17z/data=!3m1!4b1!4m5!3m4!1s0x5490435542eafefd:0x99d3d9c4c7dc37b7!8m2!3d47.4502499!4d-122.3088165
        self.sea_tac = {'lat': '47.4502535', 'lng': '-122.3110052'}
        # https://www.google.com/maps/place/CenturyLink+Field/@47.5951554,-122.3338281,17z/data=!3m1!4b1!4m5!3m4!1s0x54906aa3b9f1182b:0xa636cd513bba22dc!8m2!3d47.5951518!4d-122.3316393
        self.seahawk = {'lat': '47.5951554', 'lng': '-122.3338281'}
        # https://www.google.com/maps/place/Saint+Mark's+Episcopal+Cathedral/@47.6319035,-122.3235561,17z/data=!3m1!4b1!4m5!3m4!1s0x5490152704c0b379:0xcf502443093063c2!8m2!3d47.6318999!4d-122.3213674
        self.st_mark = {'lat': '47.6319035', 'lng': '-122.3235561'}
        # https://www.google.com/maps/place/Nintendo+of+America/@47.4940088,-121.7987785,17z/data=!3m1!4b1!4m5!3m4!1s0x54907c3ef37fa90f:0x3c657ad69d166698!8m2!3d47.4940053!4d-121.7966809
        self.lat_test = '00946527'
        self.lat_test_dec = 52.17016
        self.lng_test = 'FEA1C83D'
        self.lng_test_dec = -123.12345
        self.nint_na = {'lat': '47.4940088', 'lng': '-121.7987785'}
        self.loc_1 = ['LOCATION', '005D8545', 'FEB28E4B', '4A6F75A9', 17, 17]
        self.loc_2 = ['LOCATION', '005D8545', 'FEB28E4B', '4A6F7225', 17, 17]
        self.loc_3 = ['LOCATION', '005D8544', 'FEB28E47', '4A6F6EA1', 17, 17]
        self.loc_4 = ['LOCATION', '005D8545', 'FEB28E4B', '4A6F6B1E', 17, 17]

    def test_hex_prefix(self):
        self.assertEqual('0x00946527', self.spaces.hex_prefix(self.lat_test))

    def test_lat_hex_to_float(self):
        self.assertEqual(self.lat_test_dec, self.spaces.lat_hex_to_float(self.lat_test))

    def test_lng_hex_to_float(self):
        self.assertEqual(self.lng_test_dec, self.spaces.lng_hex_to_float(self.lng_test))

if __name__ == '__main__':
    unittest.main()
