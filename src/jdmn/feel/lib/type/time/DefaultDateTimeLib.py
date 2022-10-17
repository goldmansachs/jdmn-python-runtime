#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
import re
from datetime import date, time, datetime
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

import isodate
from isodate import Duration, tzinfo, FixedOffset

from jdmn.feel.lib.Types import STRING, DATE, TIME, DATE_TIME, DURATION, INTEGER, TIME_OR_DATE_TIME
from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.runtime.DMNRuntimeException import DMNRuntimeException

DAY_NAMES = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


class DefaultDateTimeLib:
    DATE_PART = r"\d{4}-\d{2}-\d{2}"
    # [T] HH : MM : SS [.S+] (DDDD | DD:DD | Z )
    TIME_PART = r"\d{2}:\d{2}:\d{2}([.]\d+)?([+-]\d{4}|[+-]\d{2}:\d{2}|[Zz])?"

    DATE_PATTERN = re.compile("^" + DATE_PART + "$")
    TIME_PATTERN = re.compile("^T?" + TIME_PART + "$")
    DATE_TIME_PATTERN = re.compile("^" + DATE_PART + "T" + TIME_PART + "$")

    #
    # Conversion functions
    #
    def date(self, *args) -> DATE:
        len_ = len(args)
        if len_ == 1:
            arg = args[0]
            if isinstance(arg, str):
                # From literal
                result = self.parseDate(arg)
            elif isinstance(arg, datetime) or isinstance(arg, date):
                # From date or datetime
                result = self.toDate(arg)
            else:
                result = None
        elif len_ == 3:
            # From year, month, day
            year = int(args[0])
            month = int(args[1])
            day = int(args[2])
            result = date(year, month, day)
        else:
            result = None
        return result if self.isValidDateValue(result) else None

    def time(self, *args) -> TIME:
        len_ = len(args)
        if len_ == 1:
            arg = args[0]
            if isinstance(arg, str):
                # From literal
                if '@' in arg:
                    parts = arg.split("@")
                    time_ = self.parseTime(parts[0])
                    result = self.mergeTzInfo(arg, time_, parts[1])
                else:
                    result = self.parseTime(arg)
            elif isinstance(arg, time) or isinstance(arg, datetime) or isinstance(arg, date):
                # From date, time or datetime
                result = self.toTime(arg)
            else:
                result = None
        elif len_ == 4:
            # From hour, minute, second, offset
            hour = int(args[0])
            minute = int(args[1])
            seconds = int(args[2])
            secondFraction = args[2] - seconds
            micros = int(secondFraction * Decimal(1e6))
            offset = self.toTzinfo(args[3])
            if offset is None:
                result = time(hour=hour, minute=minute, second=seconds, microsecond=micros)
            else:
                result = time(hour=hour, minute=minute, second=seconds, microsecond=micros, tzinfo=offset)
        else:
            result = None
        return result if self.isValidTimeValue(result) else None

    def dateAndTime(self, *args) -> DATE_TIME:
        len_ = len(args)
        if len_ == 1:
            arg = args[0]
            if isinstance(arg, str):
                # From literal (date or datetime)
                if "-" in arg and not ("T" in arg):
                    arg += "T00:00:00"
                if '@' in arg:
                    parts = arg.split("@")
                    dt = self.parseDateTime(parts[0])
                    result = self.mergeTzInfo(arg, dt, parts[1])
                else:
                    result = self.parseDateTime(arg)
            elif isinstance(arg, time):
                # From time
                result = arg
            else:
                result = None
        elif len_ == 2:
            # From date, time
            result = datetime.combine(args[0], args[1])
        else:
            result = None
        return result if self.isValidDateTimeValue(result) else None

    def parseDate(self, arg: str) -> date:
        if not bool(self.DATE_PATTERN.match(arg)):
            raise DMNRuntimeException("Illegal date format '{}'".format(arg))

        return date.fromisoformat(arg)

    def parseTime(self, arg: str) -> time:
        if not bool(self.TIME_PATTERN.match(arg)):
            raise DMNRuntimeException("Illegal time format '{}'".format(arg))

        arg = self.fixDateTimeFormat(arg)
        #        t = time.fromisoformat(arg)
        t = isodate.parse_time(arg)
        #        t = dateutil.parser.isoparse(arg)
        return t

    def parseDateTime(self, arg: str) -> datetime:
        if not bool(self.DATE_TIME_PATTERN.match(arg)):
            raise DMNRuntimeException("Illegal datetime format '{}'".format(arg))

        arg = self.fixDateTimeFormat(arg)
        #        dt = time.fromisoformat(arg)
        try:
            datestring, timestring = arg.split('T')
        except ValueError:
            raise DMNRuntimeException("ISO 8601 time designator 'T' missing. Unable to parse datetime string {}".format(arg))

        tmpdate = isodate.parse_date(datestring, defaultday=0, defaultmonth=0)
        tmptime = isodate.parse_time(timestring)
        dt = datetime.combine(tmpdate, tmptime)
        #        dt = dateutil.parser.isoparse(arg)
        return dt

    # Fix the format 2016-08-01T11:00:00.000+0000 to 2016-08-01T11:00:00.000+00:00
    # and T11:00:00.000+0000 to 11:00:00.000+00:00
    def fixDateTimeFormat(self, literal: STRING) -> STRING:
        if literal is None:
            return None
        if (literal.startswith("T")):
            literal = literal[1:]
        timeZoneStartIndex = len(literal) - 5
        if 0 <= timeZoneStartIndex < len(literal):
            timeZoneStart = literal[timeZoneStartIndex]
            if timeZoneStart == '+' or timeZoneStart == '-':
                timeZoneOffset = literal[timeZoneStartIndex + 1:]
                literal = literal[0:timeZoneStartIndex + 1] + timeZoneOffset[0:2] + ":" + timeZoneOffset[2:]
        # Python does not support Z or z as tzinfo
        literal = literal.upper()
        literal = literal.replace("Z", "+00:00")
        return literal

    def mergeTzInfo(self, arg, t: TIME_OR_DATE_TIME, zoneId: str) -> TIME_OR_DATE_TIME:
        if t.tzinfo is None:
            tz = ZoneInfo(zoneId)
            if tz is None:
                raise DMNRuntimeException("Illegal timezone '{}'".format(zoneId))

            result = t.replace(tzinfo=tz)
            return result
        else:
            if not (isinstance(time.tzinfo, isodate.tzinfo.Utc) and zoneId == "UTC"):
                raise DMNRuntimeException("Duplicated timezone in '{}'".format(arg))
            else:
                return t

    #
    # Date properties
    #
    def year(self, date: DATE) -> INTEGER:
        if date is None:
            return None

        return date.year

    def yearDateTime(self, dateTime: DATE_TIME) -> INTEGER:
        return self.year(dateTime)

    def month(self, date: DATE) -> INTEGER:
        if date is None:
            return None

        return date.month

    def monthDateTime(self, dateTime: DATE_TIME) -> INTEGER:
        return self.month(dateTime)

    def day(self, date: DATE) -> INTEGER:
        if date is None:
            return None

        return date.day

    def dayDateTime(self, dateTime: DATE_TIME) -> INTEGER:
        return self.day(dateTime)

    def weekday(self, date: DATE) -> INTEGER:
        if date is None:
            return None

        return date.weekday() + 1

    def weekdayDateTime(self, dateTime: DATE_TIME) -> INTEGER:
        return self.weekday(dateTime)

    #
    # Time properties
    #
    def hour(self, time: TIME_OR_DATE_TIME) -> INTEGER:
        if time is None:
            return None

        return time.hour

    def minute(self, time: TIME_OR_DATE_TIME) -> INTEGER:
        if time is None:
            return None

        return time.minute

    def second(self, time: TIME_OR_DATE_TIME) -> INTEGER:
        if time is None:
            return None

        return time.second

    def timeOffset(self, time: TIME_OR_DATE_TIME) -> DURATION:
        if time is None:
            return None

        return self.toDuration(time.tzinfo)

    def timezone(self, time: TIME_OR_DATE_TIME) -> STRING:
        if time is None:
            return None

        return time.tzname()

    #
    # Temporal functions
    #
    def dayOfYear(self, date: DATE) -> INTEGER:
        if date is None:
            return None

        return date.timetuple().tm_yday

    def dayOfWeek(self, date: DATE) -> STRING:
        if date is None:
            return None

        dow: int = date.isocalendar()[2]
        return DAY_NAMES[dow]

    def weekOfYear(self, date: DATE) -> INTEGER:
        if (date is None):
            return None

        return date.isocalendar()[1]

    def monthOfYear(self, date: DATE) -> STRING:
        if date is None:
            return None

        moy: int = date.month
        return MONTH_NAMES[moy - 1]

    #
    # Extra conversion functions
    #
    def toDate(self, from_: Any) -> DATE:
        if isinstance(from_, datetime):
            return from_.date()
        elif isinstance(from_, date):
            return from_
        else:
            return None

    def toTime(self, from_: Any) -> TIME:
        if isinstance(from_, time):
            return from_
        elif isinstance(from_, datetime):
            return from_.timetz()
        elif isinstance(from_, date):
            dateTime = self.toDateTime(from_)
            return dateTime.timetz()
        else:
            return None

    def toDateTime(self, from_: Any) -> DATE_TIME:
        if isinstance(from_, datetime):
            return from_
        elif isinstance(from_, date):
            return datetime.combine(from_, time(0, 0, 0, tzinfo=tzinfo.UTC))
        else:
            return None

    def toDuration(self, info: tzinfo) -> DURATION:
        if info is None:
            return None

        delta = info.utcoffset(None)
        seconds = int(delta.total_seconds())
        return Duration(seconds=seconds)

    def toTzinfo(self, duration: DURATION) -> tzinfo:
        if duration is None:
            return None

        seconds = duration.total_seconds()
        mm, ss = divmod(seconds, 60)
        hh, mm = divmod(mm, 60)
        if -24 <= hh <= 24:
            return FixedOffset(offset_hours=int(hh), offset_minutes=int(mm))
        else:
            raise DMNRuntimeException("Incorrect offset {}:{}:{}".format(hh, mm, ss))

    def isValidDateValue(self, value: DATE) -> bool:
        return self.isValidDate(value.year, value.month, value.day)

    def isValidTimeValue(self, value: TIME) -> bool:
        secondsOffset = None if value.tzinfo is None or value.utcoffset() is None else value.tzinfo.utcoffset(BaseType.EP).total_seconds()
        return self.isValidTime(value.hour, value.minute, value.second, secondsOffset)

    def isValidDateTimeValue(self, value: DATE_TIME) -> bool:
        secondsOffset = None if value.tzinfo is None or value.utcoffset() is None else value.utcoffset().total_seconds()
        return self.isValidDate(value.year, value.month, value.day) and self.isValidTime(value.hour, value.minute, value.second, secondsOffset)

    def isValidDate(self, year: int, month: int, day: int) -> bool:
        return self.isValidYear(year) and self.isValidMonth(month) and self.isValidDay(day)

    def isValidTime(self, hour: int, minute: int, second: int, secondsOffset: INTEGER) -> bool:
        return self.isValidHour(hour) and self.isValidMinute(minute) and self.isValidSecond(second) and self.isValidOffset(secondsOffset)

    def isValidDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, secondsOffset: INTEGER) -> bool:
        return self.isValidDate(year, month, day) and self.isValidTime(hour, minute, second, secondsOffset)

    @staticmethod
    def isValidYear(year: int) -> bool:
        return -999999999 <= year <= 999999999

    @staticmethod
    def isValidMonth(month: int) -> bool:
        return 1 <= month <= 12

    @staticmethod
    def isValidDay(day: int) -> bool:
        return 1 <= day <= 31

    @staticmethod
    def isValidHour(hour: int) -> bool:
        return 0 <= hour <= 23

    @staticmethod
    def isValidMinute(minute: int) -> bool:
        return 0 <= minute <= 59

    @staticmethod
    def isValidSecond(second: int) -> bool:
        return 0 <= second <= 59

    @staticmethod
    def isValidOffset(secondsOffset: INTEGER) -> bool:
        if secondsOffset is None:
            return True
        return -18 * 3600 <= secondsOffset < 18 * 3600
