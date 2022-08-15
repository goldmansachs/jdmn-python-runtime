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
from datetime import date, datetime
from typing import Optional

from isodate import Duration

from com.gs.dmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType
from com.gs.dmn.feel.lib.type.time.DefaultDateTimeComparator import DefaultDateTimeComparator


class DefaultDateType:
    def __init__(self):
        self.comparator = DefaultDateTimeComparator()
        self.booleanType = DefaultBooleanType()

    def dateIs(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        if (first is None or second is None):
            return first == second

        return self.same(first, second)

    def dateValue(self, date: Optional[date]) -> Optional[int]:
        if date is None:
            return None

        return self.dateTimeValue(date)

    def dateEqual(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.comparator.equalTo(first, second)

    def dateNotEqual(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.booleanType.booleanNot(self.dateEqual(first, second))

    def dateLessThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.comparator.lessThan(first, second)

    def dateGreaterThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.comparator.greaterThan(first, second)

    def dateLessEqualThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.comparator.lessEqualThan(first, second)

    def dateGreaterEqualThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.comparator.greaterEqualThan(first, second)

    def dateSubtract(self, first: Optional[date], second: Optional[date]):
        if first is None or second is None:
            return None

        # Implicit date time conversion
        if self.isDate(first):
            first = self.dateToDateTime(first)
        if self.isDate(second):
            second = self.dateToDateTime(second)

        durationInSeconds = (first - second).total_seconds()
        return Duration(seconds=durationInSeconds)

    def dateAddDuration(self, date: Optional[date], duration) -> Optional[date]:
        if date is None or duration is None:
            return None

        pass

    def dateSubtractDuration(self, date: Optional[date], duration: Optional[Duration]) -> Optional[date]:
        if date is None or duration is None:
            return None

        return self.dateAddDuration(date, - duration)

    def isDate(self, obj):
        return isinstance(obj, date)

    def dateToDateTime(self, date):
        return datetime(date.year, date.month, date.day)

    def same(self, first: date, second: date):
        return first.year == second.year and first.month == second.month and first.day == second.day

    def dateTimeValue(self, date) -> int:
        epoch = datetime.utcfromtimestamp(0)
        return int((self.dateToDateTime(date) - epoch).total_seconds())
