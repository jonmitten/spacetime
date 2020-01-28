import argparse
import calendar
import pytz
import time

from datetime import datetime



class Times:

    def __init__(self):
        self.TICKS = 315964800  # seconds between gps and unix epoch
        self.parser = argparse.ArgumentParser(description='Process some times.')
        self.parser.add_argument('fmt', metavar='N', type=str, nargs='+', help='Return time in format provided.')
        self.utc = pytz.timezone('UTC')
        self.iso_fmt = '%Y-%m-%dT%H:%M:%S'

    def dt_ticks(self):
        return datetime.fromtimestamp(self.TICKS)

    def seconds(self, timestamp):
        """
        Return a timestamp rounded to the nearest second.
        :param timestamp: float - a Unix timestamp with milliseconds right of the decimal.
        :return:
        """
        if isinstance(timestamp, float):
            return round(timestamp, 0)
        elif isinstance(timestamp, time.struct_time):
            # ts = self.seconds(time.mktime(timestamp))  # trouble maker
            dt = datetime.fromtimestamp(calendar.timegm(timestamp))
            ts = (dt - datetime(1970, 1, 1)).total_seconds()
            print(ts)
            return ts
        elif isinstance(timestamp, int):
            return timestamp
        elif isinstance(timestamp, datetime):
            return timestamp

    def current_time(self, fmt='unix'):
        """
        Returns the current time in the preferred format
        rounding to the nearest second.

        :param fmt: string - optional string
        :return:
        """
        if fmt == 'unix':
            cur_time = time.time()
            return self.seconds(cur_time)
        elif fmt == 'gps':
            return self.seconds(self.gps_time(time.gmtime()))
        elif fmt == 'iso':
            return self.iso_time(self.seconds(time.gmtime()))

    def unix_time(self, timestamp, fmt='gps'):
        if fmt == 'gps':
            return timestamp + self.TICKS

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
                return self.seconds(timestamp) - self.TICKS
            elif isinstance(timestamp, time.struct_time):
                ts = self.intstruct(timestamp)
                ts = self.seconds(ts)
                return ts - self.TICKS
        elif fmt == 'iso':
            if isinstance(timestamp, str):
                try:
                    dt = datetime.strptime(datetime, self.iso_fmt)
                    print(type(dt))
                    diff = self.dt_ticks()
                    gps_dt = dt - diff
                    print(gps_dt)
                    return gps_dt
                except TypeError as te:
                    print('gps_time() had trouble converting from iso to gps timestamp:{}'.format(te))

    def intstruct(self, timestamp):
        """
        Return a float formatted timestamp from a time.struct_time object.
        :param timestamp: time.struct_time object - the time to convert
        :return: float - converted timestamp to seconds since epoch
        """
        try:
            return calendar.timegm(timestamp)
        except TypeError as te:
            print('instruct() had a type error: {}'.format(te))

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
                    timestamp = self.seconds(timestamp)
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
                    return self.seconds(ts)
                except TypeError as te:
                    print(te)

        elif fmt == 'gps':
            if isinstance(timestamp, int):
                return self.iso_time(self.unix_time(timestamp), 'unix')


class Spaces:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Process some times.')
        self.parser.add_argument('fmt', metavar='N', type=str, nargs='+', help='Return time in format provided.')
