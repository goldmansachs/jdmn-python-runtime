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
from typing import Any, Optional, Callable

from jdmn.feel.lib.Types import DECIMAL
from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.feel.lib.type.numeric.NumericComparator import NumericComparator


class DefaultNumericType(BaseType):
    DECIMAL128 = decimal.Context(prec=34, rounding=decimal.ROUND_HALF_EVEN)

    def __init__(self):
        BaseType.__init__(self)
        self.numericComparator = NumericComparator()

    @staticmethod
    def isNumber(value: Any) -> bool:
        return isinstance(value, Decimal)

    @staticmethod
    def numericValue(value: DECIMAL) -> DECIMAL:
        return value

    @staticmethod
    def numericIs(first: DECIMAL, second: DECIMAL) -> Optional[bool]:
        if first is None or second is None:
            return first == second

        return first == second

    def numericEqual(self, first: DECIMAL, second: DECIMAL) -> Optional[bool]:
        return self.numericComparator.equalTo(first, second)

    def numericNotEqual(self, first: DECIMAL, second: DECIMAL) -> Optional[bool]:
        return self.numericComparator.notEqualTo(first, second)

    def numericLessThan(self, first: DECIMAL, second: DECIMAL) -> Optional[bool]:
        return self.numericComparator.lessThan(first, second)

    def numericGreaterThan(self, first: DECIMAL, second: DECIMAL) -> Optional[bool]:
        return self.numericComparator.greaterThan(first, second)

    def numericLessEqualThan(self, first: DECIMAL, second: DECIMAL) -> Optional[bool]:
        return self.numericComparator.lessEqualThan(first, second)

    def numericGreaterEqualThan(self, first: DECIMAL, second: DECIMAL) -> Optional[bool]:
        return self.numericComparator.greaterEqualThan(first, second)

    def numericAdd(self, first: DECIMAL, second: DECIMAL) -> Optional[Optional[Decimal]]:
        if first is None or second is None:
            return None

        return self.decimalOperation(first, second, lambda x, y: x + y)

    def numericSubtract(self, first: DECIMAL, second: DECIMAL) -> Optional[Optional[Decimal]]:
        if first is None or second is None:
            return None

        return self.decimalOperation(first, second, lambda x, y: x - y)

    def numericMultiply(self, first: DECIMAL, second: DECIMAL) -> Optional[Optional[Decimal]]:
        if first is None or second is None:
            return None

        return self.decimalOperation(first, second, lambda x, y: x * y)

    def numericDivide(self, first: DECIMAL, second: DECIMAL) -> Optional[Optional[Decimal]]:
        return self.decimalNumericDivide(first, second)

    @staticmethod
    def numericUnaryMinus(first: DECIMAL) -> Optional[Optional[Decimal]]:
        if first is None:
            return None

        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = DefaultNumericType.DECIMAL128.rounding
            ctx.prec = DefaultNumericType.DECIMAL128.prec
            return first.copy_negate()

    def numericExponentiation(self, first: DECIMAL, second: DECIMAL) -> DECIMAL:
        if first is None or second is None:
            return None

        return self.decimalOperation(first, second, lambda x, y: x ** y)

    @staticmethod
    def decimalNumericDivide(first: DECIMAL, second: DECIMAL) -> DECIMAL:
        if first is None or second is None:
            return None
        if second.is_zero():
            return None

        return DefaultNumericType.decimalOperation(first, second, lambda x, y: x / y)

    @staticmethod
    def decimalOperation(first: DECIMAL, second: DECIMAL, funct: Callable[[DECIMAL, DECIMAL], DECIMAL]):
        # DECIMAL 128
        with decimal.localcontext() as ctx:
            ctx.rounding = DefaultNumericType.DECIMAL128.rounding
            ctx.prec = DefaultNumericType.DECIMAL128.prec
            return funct(first, second)
