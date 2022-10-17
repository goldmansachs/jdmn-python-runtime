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
from collections import defaultdict
from decimal import Decimal
from typing import List, Any, Optional

from jdmn.feel.lib.Types import STRING, DECIMAL, BOOLEAN
from jdmn.feel.lib.Utils import varArgToList
from jdmn.feel.lib.type.numeric.DefaultNumericType import DefaultNumericType
from jdmn.runtime.NumericRoundingMode import NumericRoundingMode


class DefaultNumericLib:
    def number(self, literal: STRING, groupingSeparator: STRING = None, decimalSeparator: STRING = None) -> DECIMAL:
        if not literal:
            return None
        if not (" " == groupingSeparator or "." == groupingSeparator or "," == groupingSeparator or groupingSeparator is None):
            return None
        if not ("." == decimalSeparator or "," == decimalSeparator or decimalSeparator is None):
            return None
        if groupingSeparator is not None and groupingSeparator == decimalSeparator:
            return None

        if groupingSeparator is not None:
            literal = literal.replace(groupingSeparator, "")
        if decimalSeparator is not None and not (decimalSeparator == "."):
            literal = literal.replace(decimalSeparator, ".")
        return Decimal(literal, DefaultNumericType.DECIMAL128)

    def decimal(self, n: DECIMAL, scale: DECIMAL) -> DECIMAL:
        if n is None or scale is None:
            return None

        return self.round(n, scale, NumericRoundingMode.HALF_EVEN)

    # Extension to DMN 1.3
    def round(self, n: DECIMAL, scale: DECIMAL, mode: NumericRoundingMode) -> DECIMAL:
        if n is None or scale is None or mode is None or mode == NumericRoundingMode.UNKNOWN:
            return None

        prec = int(scale)
        if prec < 0:
            fmt = "1E{}".format(- prec)
        elif prec == 0:
            fmt = "1E0"
        else:
            fmt = "1E-{}".format(prec)
        return n.quantize(Decimal(fmt), rounding=mode.pMode)

    def floor(self, *args) -> DECIMAL:
        # Extract n ans scale
        operands = varArgToList(*args)
        size = len(operands)
        if size == 0 or size > 2:
            return None
        elif size == 1:
            n = operands[0]
            scale = Decimal(0)
        else:
            n = operands[0]
            scale = operands[1]

        if n is None or scale is None:
            return None
        return self.round(n, scale, NumericRoundingMode.ROUND_FLOOR)

    def ceiling(self, *args) -> DECIMAL:
        # Extract n ans scale
        operands = varArgToList(*args)
        size = len(operands)
        if size == 0 or size > 2:
            return None
        elif size == 1:
            n = operands[0]
            scale = Decimal(0)
        else:
            n = operands[0]
            scale = operands[1]

        if n is None or scale is None:
            return None
        return self.round(n, scale, NumericRoundingMode.ROUND_CEILING)

    def abs(self, n: DECIMAL) -> DECIMAL:
        if n is None:
            return None

        return n.copy_abs()

    def intModulo(self, dividend: DECIMAL, divisor: DECIMAL) -> DECIMAL:
        if dividend is None or divisor is None:
            return None

        return Decimal(dividend % int(divisor))

    def modulo(self, dividend: DECIMAL, divisor: DECIMAL) -> DECIMAL:
        if dividend is None or divisor is None:
            return None

        # dividend - divisor*floor(dividend/divisor)
        return dividend - (divisor * self.floor(dividend / divisor, Decimal(0)))

    def sqrt(self, number: DECIMAL) -> DECIMAL:
        if number is None:
            return None

        return number.sqrt(context=DefaultNumericType.DECIMAL128)

    def log(self, number: DECIMAL) -> DECIMAL:
        if number is None:
            return None

        return number.ln(context=DefaultNumericType.DECIMAL128)

    def exp(self, number: DECIMAL) -> DECIMAL:
        if number is None:
            return None

        return number.exp(context=DefaultNumericType.DECIMAL128)

    def odd(self, number: DECIMAL) -> BOOLEAN:
        if not self.isIntegerValue(number):
            return None

        return int(number) % 2 != 0

    def even(self, number: DECIMAL) -> BOOLEAN:
        if not self.isIntegerValue(number):
            return None

        return int(number) % 2 == 0

    #
    # List functions
    #
    def count(self, list_: List[Any]) -> DECIMAL:
        if list_ is None:
            return Decimal(0)
        else:
            return Decimal(len(list_))

    def min(self, *operands) -> DECIMAL:
        if len(operands) == 0:
            return None
        if len(operands) == 1:
            if isinstance(operands[0], list):
                operands = operands[0]
            else:
                operands = [operands[0]]

        result = operands[0]
        for opd in operands:
            if result > opd:
                result = opd
        return result

    def max(self, *operands) -> DECIMAL:
        if len(operands) == 0:
            return None
        if len(operands) == 1:
            if isinstance(operands[0], list):
                operands = operands[0]
            else:
                operands = [operands[0]]

        result = operands[0]
        for opd in operands:
            if result < opd:
                result = opd
        return result

    def sum(self, *args) -> DECIMAL:
        operands = varArgToList(*args)
        if len(operands) == 0:
            return None

        result = Decimal(0)
        for opd in operands:
            result += opd
        return result

    def mean(self, *args) -> DECIMAL:
        operands = varArgToList(*args)
        if len(operands) == 0:
            return None

        sum = self.sum(operands)
        return DefaultNumericType.decimalNumericDivide(sum, Decimal(len(operands)))

    def product(self, *args) -> DECIMAL:
        operands = varArgToList(*args)
        if len(operands) == 0:
            return None

        result = Decimal(1)
        for opd in operands:
            result = result * opd
        return result

    def median(self, *args) -> DECIMAL:
        operands = varArgToList(*args)
        if len(operands) == 0:
            return None

        sortedList = sorted(operands, key=float)
        size = len(sortedList)
        if size % 2 == 0:
            first = sortedList[int(size / 2)]
            second = sortedList[int(size / 2 - 1)]
            median = (first + second) / 2
        else:
            median = sortedList[int(size / 2)]
        return median

    def stddev(self, *args) -> DECIMAL:
        operands = varArgToList(*args)
        if len(operands) == 0:
            return None

        mean = self.mean(operands)
        length = Decimal(len(operands) - 1)
        variance = Decimal(0)
        for e in operands:
            number = e
            dm = number - mean
            dv = dm * dm
            variance += dv
        variance = DefaultNumericType.decimalNumericDivide(variance, length)
        stddev = self.sqrt(variance)
        return stddev

    def mode(self, *args) -> Optional[List[Decimal]]:
        if (args is None):
            return None
        operands = varArgToList(*args)
        if len(operands) == 0:
            return []

        max = -1
        modes = []
        countMap = defaultdict(int)
        for n in operands:
            if not isinstance(n, Decimal):
                return None
            countMap[n] += 1
            count = countMap[n]
            if count > max:
                max = count

        for key, value in countMap.items():
            if value == max:
                modes.append(key)

        sortedModes = sorted(modes)
        return sortedModes

    @staticmethod
    def toNumber(number: DECIMAL) -> DECIMAL:
        if isinstance(number, Decimal):
            return number
        else:
            return None

    @staticmethod
    def isIntegerValue(number):
        return number is not None and (number == int(number))
