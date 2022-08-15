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
import decimal
from decimal import Decimal
from typing import Any, Optional

from com.gs.dmn.feel.lib.type.numeric.NumericComparator import NumericComparator


class DefaultNumericType:
    def __init__(self):
        self.numericComparator = NumericComparator()

    @staticmethod
    def decimalNumericDivide(first: Optional[Decimal], second: Optional[Decimal]) -> Optional[Decimal]:
        if first is None or second is None:
            return None
        if second.is_zero():
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_UP
            ctx.prec = 34
            return first / second

    def isNumber(self, value: Any) -> bool:
        return isinstance(value, Decimal)

    def numericValue(self, value: Optional[Decimal]) -> Optional[Decimal]:
        return value

    def numericIs(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[bool]:
        if first is None or second is None:
            return first == second

        return first == second

    def numericEqual(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[bool]:
        return self.numericComparator.equalTo(first, second)

    def numericNotEqual(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[bool]:
        return self.numericComparator.notEqualTo(first, second)

    def numericLessThan(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[bool]:
        return self.numericComparator.lessThan(first, second)

    def numericGreaterThan(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[bool]:
        return self.numericComparator.greaterThan(first, second)

    def numericLessEqualThan(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[bool]:
        return self.numericComparator.lessEqualThan(first, second)

    def numericGreaterEqualThan(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[bool]:
        return self.numericComparator.greaterEqualThan(first, second)

    def numericAdd(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[Optional[Decimal]]:
        if first is None or second is None:
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_UP
            ctx.prec = 34
            return first + second

    def numericSubtract(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[Optional[Decimal]]:
        if first is None or second is None:
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_UP
            ctx.prec = 34
            return first - second

    def numericMultiply(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[Optional[Decimal]]:
        if first is None or second is None:
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_UP
            ctx.prec = 34
            return first * second

    def numericDivide(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[Optional[Decimal]]:
        return self.decimalNumericDivide(first, second)

    def numericUnaryMinus(self, first: Optional[Decimal]) -> Optional[Optional[Decimal]]:
        if first is None:
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_UP
            ctx.prec = 34
            return first.copy_negate()

    def numericExponentiation(self, first: Optional[Decimal], second: Optional[Decimal]) -> Optional[Decimal]:
        if first is None or second is None:
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = decimal.ROUND_HALF_UP
            ctx.prec = 34
            return first ** second
