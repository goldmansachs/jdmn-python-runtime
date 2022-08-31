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


class DefaultDurationType(DefaultCalendarType):
    def __init__(self):
        super().__init__()
        self.__timeComparator = DefaultDateTimeComparator()

    def isYearsAndMonthsDuration(self, value):
        raise Exception("Not supported yet")

    def isDaysAndTimeDuration(self, value):
        raise Exception("Not supported yet")

    @staticmethod
    def hasTimezone(calendar: datetime) -> bool:
        return calendar.tzinfo is None

    def durationIs(self, first: Duration, second: Duration) -> Optional[bool]:
        if first is None or second is None:
            return first == second

        return self.sameTime(first, second)

    def durationValue(self, duration):
        raise Exception("Not supported yet")

    def durationEqual(self, first: Duration, second: Duration) -> Optional[bool]:
        return self.__timeComparator.equalTo(first, second)

    def durationNotEqual(self, first: Duration, second: Duration) -> Optional[bool]:
        return self.booleanType.booleanNot(self.timeEqual(first, second))

    def durationLessThan(self, first: Duration, second: Duration) -> Optional[bool]:
        return self.__timeComparator.lessThan(first, second)

    def durationGreaterThan(self, first: Duration, second: Duration) -> Optional[bool]:
        return self.__timeComparator.greaterThan(first, second)

    def durationLessEqualThan(self, first: Duration, second: Duration) -> Optional[bool]:
        return self.__timeComparator.lessEqualThan(first, second)

    def durationGreaterEqualThan(self, first: Duration, second: Duration) -> Optional[bool]:
        return self.__timeComparator.greaterEqualThan(first, second)

    def durationAdd(self, first: Duration, second: Duration) -> Optional[Duration]:
        if first is None or second is None:
            return None

        durationInSeconds = self.durationValue(first) + self.durationValue(second)
        return Duration(seconds=durationInSeconds)

    def durationSubtract(self, first: Duration, second: Duration) -> Optional[Duration]:
        if first is None or second is None:
            return None

        durationInSeconds = self.durationValue(first) - self.durationValue(second)
        return Duration(seconds=durationInSeconds)

    def durationDivide(self, first, second):
        raise Exception("Not supported yet")

    def durationMultiplyNumber(self, first, second):
        raise Exception("Not supported yet")

    def durationDivideNumber(self, first, second):
        raise Exception("Not supported yet")
