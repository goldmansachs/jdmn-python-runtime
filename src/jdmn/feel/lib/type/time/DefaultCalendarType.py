#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use self file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from datetime import date, datetime, time, timezone, timedelta
from typing import Optional, Any

import isodate
from isodate import Duration

from jdmn.feel.lib.Types import DATE, TIME, DATE_TIME, INTEGER, DATE_TIME_UNION, DURATION
from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType


class DefaultCalendarType(BaseType):
    def __init__(self):
        BaseType.__init__(self)
        self.booleanType = DefaultBooleanType()

    @staticmethod
    def isDate(obj: Any) -> bool:
        return isinstance(obj, date) and not isinstance(obj, datetime)

    @staticmethod
    def isTime(obj: Any) -> bool:
        return isinstance(obj, time)

    @staticmethod
    def isDateTime(obj: Any) -> bool:
        return isinstance(obj, datetime)

    @staticmethod
    def isDuration(value: Any):
        return isinstance(value, Duration) or isinstance(value, timedelta)

    @staticmethod
    def isYearsAndMonthsDuration(value):
        if isinstance(value, Duration):
            return not (value.years == 0 and value.months == 0) and value.tdelta.total_seconds() == 0.0
        elif isinstance(value, timedelta):
            return False
        else:
            return False

    @staticmethod
    def isDaysAndTimeDuration(value: Any):
        if isinstance(value, Duration):
            return value.years == 0 and value.months == 0 and value.tdelta.total_seconds() != 0.0
        elif isinstance(value, timedelta):
            return True
        else:
            return False

    @staticmethod
    def dateToDateTime(date_: DATE) -> datetime:
        return datetime(date_.year, date_.month, date_.day, tzinfo=timezone.utc)

    @staticmethod
    def timeToDateTime(time_: TIME) -> datetime:
        # EPOCH
        return datetime(year=BaseType.EP_YEAR, month=BaseType.EP_MONTH, day=BaseType.EP_DAY, hour=time_.hour, minute=time_.minute, second=time_.second, tzinfo=time_.tzinfo)

    @staticmethod
    def sameDate(first: DATE, second: DATE) -> bool:
        return first.year == second.year and first.month == second.month and first.day == second.day

    def sameTime(self, first: TIME, second: TIME) -> bool:
        return first.hour == second.hour and first.minute == second.minute and first.second == second.second and \
               self.sameTzInfo(first.tzinfo, second.tzinfo)

    def sameDateTime(self, first: DATE_TIME, second: DATE_TIME) -> bool:
        return first.year == second.year and first.month == second.month and \
               first.day == second.day and first.hour == second.hour and first.minute == second.minute and first.second == second.second and \
               self.sameTzInfo(first.tzinfo, second.tzinfo)

    def value(self, calendar: DATE_TIME_UNION) -> INTEGER:
        if self.isDate(calendar):
            return self.dateValue(calendar)
        elif self.isTime(calendar):
            return self.timeValue(calendar)
        elif self.isDateTime(calendar):
            return self.dateTimeValue(calendar)
        else:
            return None

    def dateValue(self, date_: DATE) -> INTEGER:
        if date_ is None:
            return None

        return self.dateTimeValue(self.dateToDateTime(date_))

    def timeValue(self, time_: TIME) -> INTEGER:
        if time_ is None:
            return None

        value = time_.hour * 3600 + time_.minute * 60 + time_.second
        if time_.tzinfo is not None:
            value -= time_.tzinfo.utcoffset(self.EP).seconds
        return value

    @staticmethod
    def dateTimeValue(datetime_: DATE_TIME) -> Optional[int]:
        if datetime_ is None:
            return None

        # Seconds from EPOCH
        if datetime_.tzinfo is None:
            # Add UTC
            datetime_ = datetime.combine(datetime_.date(), datetime_.time(), timezone.utc)
        timestamp = datetime_.timestamp()
        return int(timestamp)

    @staticmethod
    def canNotSubtract(first: DATE_TIME, second: DATE_TIME) -> bool:
        return first.tzinfo is None and second.tzinfo is not None or first.tzinfo is not None and second.tzinfo is None

    def durationValue(self, duration: Duration) -> INTEGER:
        if duration is None:
            return None

        if self.isYearsAndMonthsDuration(duration):
            return self.monthsValue(duration)
        elif self.isDaysAndTimeDuration(duration):
            return self.secondsValue(duration)
        else:
            return int((self.EP + duration).timestamp())

    @staticmethod
    def monthsValue(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        years = 0 if duration.years is None else duration.years
        months = 0 if duration.months is None else duration.months
        totalMonths = 12 * years + months
        return totalMonths

    @staticmethod
    def secondsValue(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        return int(duration.total_seconds())

    @staticmethod
    def sameTzInfo(tz1: isodate.tzinfo, tz2: isodate.tzinfo) -> bool:
        if tz1 is tz2 or tz1 == tz2:
            return True
        else:
            if isinstance(tz1, isodate.tzinfo.Utc) and isinstance(tz2, isodate.FixedOffset):
                return tz2.utcoffset(None).total_seconds() == 0
            if isinstance(tz2, isodate.tzinfo.Utc) and isinstance(tz1, isodate.FixedOffset):
                return tz1.utcoffset(None).total_seconds() == 0
            if isinstance(tz1, isodate.FixedOffset) and isinstance(tz2, isodate.FixedOffset):
                return tz1.utcoffset(None).total_seconds() == tz1.utcoffset(None).total_seconds()
            return False
