#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from datetime import datetime, date, time
from typing import Union

from com.gs.dmn.feel.lib.type.time.BaseDateTimeComparator import BaseDateTimeComparator
from com.gs.dmn.feel.lib.type.time.DefaultCalendarType import DefaultCalendarType


class DefaultDateTimeComparator(BaseDateTimeComparator):
    def __init__(self):
        super().__init__()
        self.__calendarType = DefaultCalendarType()

    def compareTo(self, first: Union[date | time | datetime], second: Union[date | time | datetime]) -> int:
        firstValue = self.__calendarType.value(first)
        secondValue = self.__calendarType.value(second)
        if firstValue == secondValue:
            return 0
        elif firstValue < secondValue:
            return -1
        else:
            return 1
