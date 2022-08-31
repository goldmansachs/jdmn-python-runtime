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

from jdmn.feel.lib.Types import STRING, DATE, TIME, DATE_TIME, DURATION, INT


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
                return isodate.parse_time(arg)
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
                return isodate.parse_datetime(arg)
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
        raise Exception("Not supported yet")

    def yearDateTime(self, dateTime: DATE_TIME) -> INT:
        raise Exception("Not supported yet")

    def month(self, date: DATE) -> INT:
        raise Exception("Not supported yet")

    def monthDateTime(self, dateTime: DATE_TIME) -> int:
        raise Exception("Not supported yet")

    def day(self, date: DATE) -> INT:
        raise Exception("Not supported yet")

    def dayDateTime(self, dateTime: DATE_TIME) -> int:
        raise Exception("Not supported yet")

    def weekday(self, date: DATE) -> INT:
        raise Exception("Not supported yet")

    def weekdayDateTime(self, dateTime: DATE_TIME) -> int:
        raise Exception("Not supported yet")

    #
    # Time properties
    #
    def hour(self, time: TIME) -> INT:
        raise Exception("Not supported yet")

    def hourDateTime(self, dateTime: DATE_TIME) -> INT:
        raise Exception("Not supported yet")

    def minute(self, time: TIME) -> INT:
        raise Exception("Not supported yet")

    def minuteDateTime(self, dateTime: DATE_TIME) -> INT:
        raise Exception("Not supported yet")

    def second(self, time: TIME) -> INT:
        raise Exception("Not supported yet")

    def secondDateTime(self, dateTime: DATE_TIME) -> INT:
        raise Exception("Not supported yet")

    def timeOffset(self, time: TIME) -> DURATION:
        raise Exception("Not supported yet")

    def timeOffsetDateTime(self, dateTime: DATE_TIME) -> DURATION:
        raise Exception("Not supported yet")

    def timezone(self, time: TIME) -> STRING:
        raise Exception("Not supported yet")

    def timezoneDateTime(self, dateTime: DATE_TIME) -> STRING:
        raise Exception("Not supported yet")

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
