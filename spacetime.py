import argparse
import calendar
import pytz
import time

from datetime import datetime


class Times:

    def __init__(self):
        self.TICKS = 315964800  # whole_seconds between gps and unix epoch
        self.parser = argparse.ArgumentParser(description='Process some times.')
        self.parser.add_argument('fmt', metavar='N', type=str, nargs='+', help='Return time in format provided.')
        self.utc = pytz.timezone('UTC')
        self.iso_fmt = '%Y-%m-%dT%H:%M:%S'

    def dt_ticks(self):
        return datetime.utcfromtimestamp(self.TICKS)

    def whole_seconds(self, timestamp):
        """
        Return a timestamp rounded to the nearest second.
        :param timestamp: float - a Unix timestamp with milliseconds right of the decimal.
        :return:
        """
        if isinstance(timestamp, float):
            return round(timestamp, 0)
        elif isinstance(timestamp, time.struct_time):
            # ts = self.whole_seconds(time.mktime(timestamp))  # trouble maker
            dt = datetime.fromtimestamp(calendar.timegm(timestamp))
            ts = (dt - datetime(1970, 1, 1)).total_seconds()
            print(ts)
            return ts
        elif isinstance(timestamp, int):
            return timestamp
        elif isinstance(timestamp, datetime):
            return timestamp

    def intstruct(self, timestamp):
        """
        Return a float formatted timestamp from a time.struct_time object.
        :param timestamp: time.struct_time object - the time to convert
        :return: float - converted timestamp to whole_seconds since epoch
        """
        try:
            return calendar.timegm(timestamp)
        except TypeError as te:
            print('instruct() had a type error: {}'.format(te))

    def int_to_hex(self, int_in):
        """
        Convert integer to evoIS usable hexadecimal
        in String format.

        :param int_in:
        :return:
        """
        hex_in = hex(int_in)
        hex_from_int = self.hex_strip_lead_chars(hex_in)
        return hex_from_int

    def hex_to_int(self, hex_in):
        """
        Convert hexadecimal string to integer.

        :return int: converted hex string to int
        """
        try:
            ret = int(str(hex_in), 16)
        except ValueError as e:
            return None
        return ret

    def hex_strip_lead_chars(self, hex_in):
        """
        Strips the leading characters from a hexadecimal number.
        """
        return str(hex_in[2:]).upper()

    def current_time(self, fmt='unix'):
        """
        Returns the current time in the preferred format
        rounding to the nearest second.

        :param fmt: string - optional string
        :return:
        """
        if fmt == 'unix':
            cur_time = time.time()
            return self.whole_seconds(cur_time)
        elif fmt == 'gps':
            return self.whole_seconds(self.gps_time(time.gmtime()))
        elif fmt == 'iso':
            return self.iso_time(self.whole_seconds(time.gmtime()))

    def unix_time(self, timestamp, fmt='gps'):
        if fmt == 'gps':
            return timestamp + self.TICKS
        elif fmt == 'iso':
            dt = datetime.strptime(timestamp, self.iso_fmt)
            ts = (dt - datetime(1970, 1, 1)).total_seconds()
            return ts
        elif fmt == 'gpshex' or fmt == 'hexgps':
            gps = self.hex_to_int(timestamp)
            return self.unix_time(gps, 'gps')

    def gpshex_time(self, timestamp, fmt='gps'):
        """
        Output a hexadecimal string from the provided input.
        GPS time is assumed as output.
        :param timestamp: int or string - the provided timestamp
        :param fmt: string - the input format.
        :return: string - a hexadecimal timestamp in GPS time
        """
        if fmt == 'gps':
            if isinstance(timestamp, float):
                timestamp = int(timestamp)
            try:
                return self.int_to_hex(timestamp)
            except:
                return "GPSHex() has an issue with 'gps' type."
        elif fmt == 'unix':
            try:
                gps = self.gps_time(timestamp, 'unix')
                return self.gpshex_time(gps, 'gps')
            except:
                return "GPSHex() had an issue with 'unix' type."
        elif fmt == 'iso':
            try:
                gps = self.gps_time(timestamp, 'iso')
                return self.gpshex_time(gps, 'gps')
            except:
                return "GPSHex() had an issue with 'iso' type."
        else:
            return "input type not accepted."

    def gps_time(self, timestamp, fmt='unix'):
        """
        Returns the GPS time
        converted from a declared format.
        :param timestamp
        :param fmt:
        :return:
        """
        if fmt == 'unix':
            if isinstance(timestamp, int):
                return timestamp - self.TICKS
            elif isinstance(timestamp, float):
                return self.whole_seconds(timestamp) - self.TICKS
            elif isinstance(timestamp, time.struct_time):
                ts = self.intstruct(timestamp)
                ts = self.whole_seconds(ts)
                return ts - self.TICKS
        elif fmt == 'iso':
            if isinstance(timestamp, str):
                try:
                    # convert to unix timestamp
                    dt = datetime.strptime(timestamp, self.iso_fmt)
                    print(type(dt))
                    diff = self.dt_ticks()
                    # subtract ticks
                    gps_dt = (dt - diff).total_seconds()
                    print(gps_dt)
                    return gps_dt
                except TypeError as te:
                    dt = datetime.strptime(timestamp, self.iso_fmt)
                    print(dt)
                    print('gps_time() had trouble converting {} from iso to gps timestamp:{}'.format(dt, te))
        elif fmt == 'hexgps' or fmt == 'gpshex':
            try:
                gps = self.hex_to_int(timestamp)
                return gps
            except:
                "Something went wrong in gps_time()"

    def iso_time(self, timestamp, fmt='unix'):
        """
        Returns the provided time in human-readable
        ISO 8601 format, of resolution to the nearest second
        :param timestamp: The timestamp to convert to ISO 8601 format
        :param fmt: string - the input format of the timestamp
        :return:
        """
        if fmt == 'unix':
            if isinstance(timestamp, float):
                try:
                    timestamp = self.whole_seconds(timestamp)
                    return datetime.utcfromtimestamp(timestamp).isoformat()
                except TypeError as te:
                    print(te)
            if isinstance(timestamp, int):
                try:
                    return datetime.utcfromtimestamp(timestamp).isoformat().rsplit('+', 1)[0]
                except TypeError as te:
                    print('iso_time could not convert due to {}'.format(te))
            if isinstance(timestamp, time.struct_time):
                try:
                    ts = calendar.timegm(timestamp)
                    return self.whole_seconds(ts)
                except TypeError as te:
                    print(te)
        elif fmt == 'gps':
            if isinstance(timestamp, int):
                return self.iso_time(self.unix_time(timestamp), 'unix')
        elif fmt == 'gpshex' or fmt == 'hexgps':
            if isinstance(timestamp, str):
                gps = self.hex_to_int(timestamp)
                return self.iso_time(gps, 'gps')


class Spaces:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Process some times.')
        self.parser.add_argument('fmt', metavar='N', type=str, nargs='+', help='Return time in format provided.')
