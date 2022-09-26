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

from isodate import Duration

from jdmn.feel.lib.Types import DATE, TIME, DATE_TIME, INT, DATE_TIME_UNION, DURATION, LONG
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

    def isDuration(self, value: Any):
        return isinstance(value, Duration)

    def isYearsAndMonthsDuration(self, value):
        return isinstance(value, Duration) and value.tdelta.total_seconds() == 0.0

    def isDaysAndTimeDuration(self, value: Any):
        if value is None:
            return False
        else:
            return isinstance(value, timedelta)

    @staticmethod
    def dateToDateTime(date_: DATE) -> datetime:
        return datetime(date_.year, date_.month, date_.day, tzinfo=timezone.utc)

    @staticmethod
    def timeToDateTime(time_: TIME) -> datetime:
        # EPOCH
        return datetime(year=1970, month=1, day=1, hour=time_.hour, minute=time_.minute, second=time_.second, tzinfo=time_.tzinfo)

    @staticmethod
    def sameDate(first: DATE, second: DATE) -> bool:
        return first.year == second.year and first.month == second.month and first.day == second.day

    @staticmethod
    def sameTime(first: TIME, second: TIME) -> bool:
        return first.hour == second.hour and first.minute == second.minute and first.second == second.second and first.tzinfo == second.tzinfo

    def sameDateTime(self, first: DATE_TIME, second: DATE_TIME) -> bool:
        return self.sameDate(first.date(), second.date()) and self.sameTime(first.time(), second.time())

    def value(self, calendar: DATE_TIME_UNION) -> INT:
        if self.isDate(calendar):
            return self.dateValue(calendar)
        elif self.isTime(calendar):
            return self.timeValue(calendar)
        elif self.isDateTime(calendar):
            return self.dateTimeValue(calendar)
        else:
            return None

    def dateValue(self, date_: DATE) -> INT:
        if date_ is None:
            return None

        return self.dateTimeValue(self.dateToDateTime(date_))

    def timeValue(self, time_: TIME) -> INT:
        if time_ is None:
            return None

        value = time_.hour * 3600 + time_.minute * 60 + time_.second
        if time_.tzinfo is not None:
            value -= time_.utcoffset().seconds
        return value

    def dateTimeValue(self, datetime_: DATE_TIME) -> Optional[int]:
        if datetime_ is None:
            return None

        # Seconds from EPOCH
        if datetime_.tzinfo is None:
            # Add UTC
            datetime_ = datetime.combine(datetime_.date(), datetime_.time(), timezone.utc)
        timestamp = datetime_.timestamp()
        return int(timestamp)

    def canNotSubtract(self, first: DATE_TIME, second: DATE_TIME) -> bool:
        return first.tzinfo is None and second.tzinfo is not None or first.tzinfo is not None and second.tzinfo is None

    def durationValue(self, duration: Duration) -> LONG:
        if duration is None:
            return None

        if self.isYearsAndMonthsDuration(duration):
            return self.monthsValue(duration)
        elif self.isDaysAndTimeDuration(duration):
            return self.secondsValue(duration)
        else:
            return int((datetime(1970, 1, 1) + duration).timestamp())

    @staticmethod
    def monthsValue(duration: DURATION) -> LONG:
        if duration is None:
            return None

        years = 0 if duration.years is None else duration.years
        months = 0 if duration.months is None else duration.months
        totalMonths = 12 * years + months
        return totalMonths

    @staticmethod
    def secondsValue(duration: DURATION) -> LONG:
        if duration is None:
            return None

        return int(duration.total_seconds())
