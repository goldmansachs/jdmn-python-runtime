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
from datetime import datetime, time
from typing import Optional

from isodate import Duration

from jdmn.feel.lib.type.time.DefaultCalendarType import DefaultCalendarType
from jdmn.feel.lib.type.time.DefaultTimeComparator import DefaultTimeComparator


class DefaultTimeType(DefaultCalendarType):
    def __init__(self):
        super().__init__()
        self.__timeComparator = DefaultTimeComparator()

    @staticmethod
    def hasTimezone(calendar: datetime) -> bool:
        return calendar.tzinfo is None

    def timeIs(self, first: Optional[time], second: Optional[time]) -> Optional[bool]:
        if first is None or second is None:
            return first == second

        return self.sameTime(first, second)

    def timeEqual(self, first: Optional[time], second: Optional[time]) -> Optional[bool]:
        return self.__timeComparator.equalTo(first, second)

    def timeNotEqual(self, first: Optional[time], second: Optional[time]) -> Optional[bool]:
        return self.booleanType.booleanNot(self.timeEqual(first, second))

    def timeLessThan(self, first: Optional[time], second: Optional[time]) -> Optional[bool]:
        return self.__timeComparator.lessThan(first, second)

    def timeGreaterThan(self, first: Optional[time], second: Optional[time]) -> Optional[bool]:
        return self.__timeComparator.greaterThan(first, second)

    def timeLessEqualThan(self, first: Optional[time], second: Optional[time]) -> Optional[bool]:
        return self.__timeComparator.lessEqualThan(first, second)

    def timeGreaterEqualThan(self, first: Optional[time], second: Optional[time]) -> Optional[bool]:
        return self.__timeComparator.greaterEqualThan(first, second)

    def timeSubtract(self, first: Optional[time], second: Optional[time]) -> Optional[Duration]:
        if first is None or second is None:
            return None

        durationInSeconds = self.timeValue(first) - self.timeValue(second)
        return Duration(seconds=durationInSeconds)

    def timeAddDuration(self, time_: Optional[time], duration_: Optional[Duration]) -> Optional[time]:
        if time_ is None or duration_ is None:
            return None

        return (self.timeToDateTime(time_) + duration_).timetz()

    def timeSubtractDuration(self, time_: Optional[time], duration_: Optional[Duration]) -> Optional[time]:
        if time_ is None or duration_ is None:
            return None

        return self.timeAddDuration(time_, - duration_)
