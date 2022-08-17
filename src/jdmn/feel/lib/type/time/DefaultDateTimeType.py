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
from datetime import datetime
from typing import Optional

from isodate import Duration

from jdmn.feel.lib.type.time.DefaultCalendarType import DefaultCalendarType
from jdmn.feel.lib.type.time.DefaultDateTimeComparator import DefaultDateTimeComparator


class DefaultDateTimeType(DefaultCalendarType):
    def __init__(self):
        super().__init__()
        self.__dateTimeComparator = DefaultDateTimeComparator()

    def dateTimeIs(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[bool]:
        if first is None or second is None:
            return first == second

        return self.sameDateTime(first, second)

    def dateTimeEqual(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[bool]:
        return self.__dateTimeComparator.equalTo(first, second)

    def dateTimeNotEqual(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[bool]:
        return self.booleanType.booleanNot(self.dateTimeEqual(first, second))

    def dateTimeLessThan(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[bool]:
        return self.__dateTimeComparator.lessThan(first, second)

    def dateTimeGreaterThan(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[bool]:
        return self.__dateTimeComparator.greaterThan(first, second)

    def dateTimeLessEqualThan(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[bool]:
        return self.__dateTimeComparator.lessEqualThan(first, second)

    def dateTimeGreaterEqualThan(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[bool]:
        return self.__dateTimeComparator.greaterEqualThan(first, second)

    def dateTimeSubtract(self, first: Optional[datetime], second: Optional[datetime]) -> Optional[Duration]:
        if first is None or second is None:
            return None

        if self.isDate(first):
            first = self.dateToDateTime(first)
        if self.isDate(second):
            second = self.dateToDateTime(second)
        if self.canNotSubtract(first, second):
            return None

        durationInSeconds = self.dateTimeValue(first) - self.dateTimeValue(second)
        return Duration(seconds=durationInSeconds)

    def dateTimeAddDuration(self, datetime_: Optional[datetime], duration_: Optional[Duration]) -> Optional[datetime]:
        if datetime_ is None or duration_ is None:
            return None

        return datetime_ + duration_

    def dateTimeSubtractDuration(self, datetime_: Optional[datetime], duration_: Optional[Duration]):
        if datetime_ is None or duration_ is None:
            return None

        return self.dateTimeAddDuration(datetime_, - duration_)
