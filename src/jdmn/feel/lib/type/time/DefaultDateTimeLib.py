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
from datetime import date, time, datetime
from typing import Any

import isodate
from isodate import Duration, tzinfo

from jdmn.feel.lib.Types import STRING, DATE, TIME, DATE_TIME, DURATION, INT

DAY_NAMES = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


class DefaultDateTimeLib:
    #
    # Conversion functions
    #
    def date(self, *args) -> DATE:
        len_ = len(args)
        if len_ == 1:
            arg = args[0]
            if isinstance(arg, str):
                # From literal
                return date.fromisoformat(arg)
            elif isinstance(arg, datetime):
                # From datetime
                return arg.date()
            elif isinstance(arg, date):
                # From date
                return arg
            else:
                return None
        elif len_ == 3:
            # From year, month, day
            year = int(args[0])
            month = int(args[1])
            day = int(args[2])
            return date(year, month, day)
        else:
            return None

    # TODO ZoneIDs not supported in ISO 8601
    def time(self, *args) -> TIME:
        len_ = len(args)
        if len_ == 1:
            arg = args[0]
            if isinstance(arg, str):
                # From literal
                # return time.fromisoformat(literal)
                return isodate.parse_time(arg.upper())
            elif isinstance(arg, time):
                # From time
                return arg
            else:
                return None
        elif len_ == 4:
            # From hour, minute, second, offset
            hour = int(args[0])
            minute = int(args[1])
            seconds = int(args[2])
            return time(hour=hour, minute=minute, second=seconds, tzinfo=args[3])
        else:
            return None

    # TODO ZoneIDs not supported in ISO 8601
    def dateAndTime(self, *args) -> DATE_TIME:
        len_ = len(args)
        if len_ == 1:
            arg = args[0]
            if isinstance(arg, str):
                # From literal
                if "-" in arg and not ("T" in arg):
                    arg += "T00:00:00"
                return isodate.parse_datetime(arg.upper())
            elif isinstance(arg, time):
                # From time
                return arg
            else:
                return None
        elif len_ == 2:
            # From date, time
            return datetime.combine(args[0], args[1])
        else:
            return None

    #
    # Date properties
    #
    def year(self, date: DATE) -> INT:
        if date is None:
            return None

        return date.year

    def yearDateTime(self, dateTime: DATE_TIME) -> INT:
        return self.year(dateTime)

    def month(self, date: DATE) -> INT:
        if date is None:
            return None

        return date.month

    def monthDateTime(self, dateTime: DATE_TIME) -> INT:
        return self.month(dateTime)

    def day(self, date: DATE) -> INT:
        if date is None:
            return None

        return date.day

    def dayDateTime(self, dateTime: DATE_TIME) -> INT:
        return self.day(dateTime)

    def weekday(self, date: DATE) -> INT:
        if date is None:
            return None

        return date.weekday() + 1

    def weekdayDateTime(self, dateTime: DATE_TIME) -> INT:
        return self.weekday(dateTime)

    #
    # Time properties
    #
    def hour(self, time: TIME) -> INT:
        if time is None:
            return None

        return time.hour

    def hourDateTime(self, dateTime: DATE_TIME) -> INT:
        return self.hourDateTime(dateTime)

    def minute(self, time: TIME) -> INT:
        if time is None:
            return None

        return time.minute

    def minuteDateTime(self, dateTime: DATE_TIME) -> INT:
        return self.minute(dateTime)

    def second(self, time: TIME) -> INT:
        if time is None:
            return None

        return time.second

    def secondDateTime(self, dateTime: DATE_TIME) -> INT:
        return self.second(dateTime)

    def timeOffset(self, time: TIME) -> DURATION:
        if time is None:
            return None

        return self.toDuration(time.tzinfo)

    def timeOffsetDateTime(self, dateTime: DATE_TIME) -> DURATION:
        return self.timeOffset(dateTime)

    def timezone(self, time: TIME) -> STRING:
        if time is None:
            return None

        return self.toTimeZone(time.tzinfo)

    def timezoneDateTime(self, dateTime: DATE_TIME) -> STRING:
        return self.timezone(dateTime)

    #
    # Temporal functions
    #
    def dayOfYear(self, date: DATE) -> INT:
        if date is None:
            return None

        return date.timetuple().tm_yday

    def dayOfWeek(self, date: DATE) -> STRING:
        if date is None:
            return None

        dow: int = date.isocalendar()[2]
        return DAY_NAMES[dow]

    def weekOfYear(self, date: DATE) -> INT:
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
        if isinstance(from_, date):
            return from_
        elif isinstance(from_, datetime):
            return from_.date()
        else:
            return None

    def toTime(self, from_: Any) -> TIME:
        if isinstance(from_, time):
            return from_
        elif isinstance(from_, datetime):
            return from_.time()
        else:
            return None

    def toDateTime(self, from_: Any) -> DATE_TIME:
        if isinstance(from_, date):
            return datetime.combine(from_, time(0, 0, 0))
        elif isinstance(from_, datetime):
            return from_
        else:
            return None

    def toDuration(self, info: tzinfo) -> DURATION:
        if info is None:
            return None

        delta = info.utcoffset(None)
        seconds = int(delta.total_seconds())
        return Duration(seconds=seconds)

    def toTimeZone(self, info: tzinfo) -> STRING:
        if info is None:
            return None

        tzname = info.tzname(None)
        return tzname
