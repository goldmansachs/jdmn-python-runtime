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
from datetime import date
from typing import Optional

from isodate import Duration

from jdmn.feel.lib.type.time.DefaultCalendarType import DefaultCalendarType
from jdmn.feel.lib.type.time.DefaultDateComparator import DefaultDateComparator


class DefaultDateType(DefaultCalendarType):
    def __init__(self):
        super().__init__()
        self.__dateComparator = DefaultDateComparator()

    def dateIs(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        if first is None or second is None:
            return first == second

        return self.sameDate(first, second)

    def dateEqual(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.__dateComparator.equalTo(first, second)

    def dateNotEqual(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.booleanType.booleanNot(self.dateEqual(first, second))

    def dateLessThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.__dateComparator.lessThan(first, second)

    def dateGreaterThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.__dateComparator.greaterThan(first, second)

    def dateLessEqualThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.__dateComparator.lessEqualThan(first, second)

    def dateGreaterEqualThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.__dateComparator.greaterEqualThan(first, second)

    def dateSubtract(self, first: Optional[date], second: Optional[date]) -> Optional[Duration]:
        if first is None or second is None:
            return None

        # Implicit date time conversion
        if self.isDate(first):
            first = self.dateToDateTime(first)
        if self.isDate(second):
            second = self.dateToDateTime(second)
        if self.canNotSubtract(first, second):
            return None

        durationInSeconds = self.dateTimeValue(first) - self.dateTimeValue(second)
        return Duration(seconds=durationInSeconds)

    def dateAddDuration(self, date_: Optional[date], duration_) -> Optional[date]:
        if date_ is None or duration_ is None:
            return None

        return date_ + duration_

    def dateSubtractDuration(self, date_: Optional[date], duration_: Optional[Duration]) -> Optional[date]:
        if date_ is None or duration_ is None:
            return None

        return self.dateAddDuration(date_, - duration_)
