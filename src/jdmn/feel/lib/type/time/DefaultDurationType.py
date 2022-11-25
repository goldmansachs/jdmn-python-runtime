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
import decimal
from decimal import Decimal

from isodate import Duration

from jdmn.feel.lib.Types import DURATION, BOOLEAN, DECIMAL
from jdmn.feel.lib.type.time.DefaultCalendarType import DefaultCalendarType
from jdmn.feel.lib.type.time.DefaultDurationComparator import DefaultDurationComparator
from jdmn.runtime.DMNRuntimeException import DMNRuntimeException


class DefaultDurationType(DefaultCalendarType):
    def __init__(self):
        super().__init__()
        self.__durationComparator = DefaultDurationComparator()

    def durationIs(self, first: DURATION, second: DURATION) -> BOOLEAN:
        if first is None or second is None:
            return first == second

        if self.isYearsAndMonthsDuration(first) and self.isYearsAndMonthsDuration(second):
            return first == second
        elif self.isDaysAndTimeDuration(first) and self.isDaysAndTimeDuration(second):
            return first == second
        else:
            return False

    def durationEqual(self, first: DURATION, second: DURATION) -> BOOLEAN:
        return self.__durationComparator.equalTo(first, second)

    def durationNotEqual(self, first: DURATION, second: DURATION) -> BOOLEAN:
        return self.__durationComparator.notEqualTo(first, second)

    def durationLessThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        return self.__durationComparator.lessThan(first, second)

    def durationGreaterThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        return self.__durationComparator.greaterThan(first, second)

    def durationLessEqualThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        return self.__durationComparator.lessEqualThan(first, second)

    def durationGreaterEqualThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        return self.__durationComparator.greaterEqualThan(first, second)

    def durationAdd(self, first: DURATION, second: DURATION) -> DURATION:
        if first is None or second is None:
            return None

        if self.isYearsAndMonthsDuration(first) and self.isYearsAndMonthsDuration(second):
            totalMonths = self.monthsValue(first) + self.monthsValue(second)
            return Duration(months=totalMonths)
        elif self.isDaysAndTimeDuration(first) and self.isDaysAndTimeDuration(second):
            durationInSeconds = self.secondsValue(first) + self.secondsValue(second)
            return Duration(seconds=durationInSeconds)
        else:
            raise DMNRuntimeException(f"Cannot add '{first}' and '{second}'")

    def durationSubtract(self, first: DURATION, second: DURATION) -> DURATION:
        if first is None or second is None:
            return None

        return self.durationAdd(first, second.__neg__())

    def durationDivide(self, first: DURATION, second: DURATION) -> DECIMAL:
        if first is None or second is None:
            return None

        if self.isYearsAndMonthsDuration(first) and self.isYearsAndMonthsDuration(second):
            firstValue = Decimal(self.monthsValue(first))
            secondValue = Decimal(self.monthsValue(second))
            return self.divideNumber(firstValue, secondValue)
        elif self.isDaysAndTimeDuration(first) and self.isDaysAndTimeDuration(second):
            firstValue = Decimal(self.secondsValue(first))
            secondValue = Decimal(self.secondsValue(second))
            return self.divideNumber(firstValue, secondValue)
        else:
            raise DMNRuntimeException(f"Cannot divide '{first}' and '{second}'")

    def durationMultiplyNumber(self, first: DURATION, second: DECIMAL) -> DURATION:
        if first is None or second is None:
            return None

        if self.isYearsAndMonthsDuration(first):
            firstValue = Decimal(self.monthsValue(first))
            totalMonths = self.multiplyNumber(firstValue, second)
            return Duration(months=totalMonths.to_integral())
        elif self.isDaysAndTimeDuration(first):
            firstValue = Decimal(self.secondsValue(first))
            durationInSeconds = int(self.multiplyNumber(firstValue, second))
            return Duration(seconds=durationInSeconds)
        else:
            raise DMNRuntimeException(f"Cannot multiply '{first}' and '{second}'")

    def durationDivideNumber(self, first: DURATION, second: DECIMAL) -> DURATION:
        if first is None or second is None:
            return None

        if self.isYearsAndMonthsDuration(first):
            firstValue = Decimal(self.monthsValue(first))
            totalMonths = self.divideNumber(firstValue, second)
            return Duration(months=totalMonths.to_integral())
        elif self.isDaysAndTimeDuration(first):
            firstValue = Decimal(self.secondsValue(first))
            durationInSeconds = int(self.divideNumber(firstValue, second))
            return Duration(seconds=durationInSeconds)
        else:
            raise DMNRuntimeException(f"Cannot divide '{first}' and '{second}'")

    @staticmethod
    def multiplyNumber(firstValue: DECIMAL, secondValue: DECIMAL) -> DECIMAL:
        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.prec = 34
            return firstValue * secondValue

    @staticmethod
    def divideNumber(firstValue: DECIMAL, secondValue: DECIMAL) -> DECIMAL:
        if secondValue == 0:
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_DOWN
            ctx.prec = 34
            return firstValue / secondValue
