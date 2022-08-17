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
from datetime import date, datetime, time, timezone
from typing import Optional, Any, Union

from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType


class DefaultCalendarType:
    def __init__(self):
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
    def dateToDateTime(date_: date) -> datetime:
        return datetime(date_.year, date_.month, date_.day, tzinfo=timezone.utc)

    @staticmethod
    def timeToDateTime(time_: time) -> datetime:
        # EPOCH
        return datetime(year=1970, month=1, day=1, hour=time_.hour, minute=time_.minute, second=time_.second, tzinfo=time_.tzinfo)

    @staticmethod
    def sameDate(first: date, second: date) -> bool:
        return first.year == second.year and first.month == second.month and first.day == second.day

    @staticmethod
    def sameTime(first: time, second: time) -> bool:
        return first.hour == second.hour and first.minute == second.minute and first.second == second.second and first.tzinfo == second.tzinfo

    def sameDateTime(self, first: datetime, second: datetime) -> bool:
        return self.sameDate(first.date(), second.date()) and self.sameTime(first.time(), second.time())

    def value(self, calendar: Union[date | time | datetime]) -> Optional[int]:
        if self.isDate(calendar):
            return self.dateValue(calendar)
        elif self.isTime(calendar):
            return self.timeValue(calendar)
        elif self.isDateTime(calendar):
            return self.dateTimeValue(calendar)
        else:
            return None

    def dateValue(self, date_: Optional[date]) -> Optional[int]:
        if date_ is None:
            return None

        return self.dateTimeValue(self.dateToDateTime(date_))

    def timeValue(self, time_: Optional[time]) -> Optional[int]:
        if time_ is None:
            return None

        value = time_.hour * 3600 + time_.minute * 60 + time_.second
        if time_.tzinfo is not None:
            value -= time_.tzinfo.utcoffset(time_).seconds
        return value

    def dateTimeValue(self, datetime_: Optional[datetime]) -> Optional[int]:
        if datetime_ is None:
            return None

        # Seconds from EPOCH
        if datetime_.tzinfo is None:
            # Add UTC
            datetime_ = datetime.combine(datetime_.date(), datetime_.time(), timezone.utc)
        timestamp = datetime_.timestamp()
        return int(timestamp)

    def canNotSubtract(self, first: datetime, second: datetime) -> bool:
        return first.tzinfo is None and second.tzinfo is not None or first.tzinfo is not None and second.tzinfo is None
