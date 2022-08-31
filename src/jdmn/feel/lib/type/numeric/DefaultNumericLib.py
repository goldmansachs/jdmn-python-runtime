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
from decimal import Decimal, Context, ROUND_HALF_EVEN
from typing import List, Any

from jdmn.feel.lib.Types import STRING, NUMBER
from jdmn.feel.lib.Utils import varArgToList


class DefaultNumericLib:
    def number(self, literal: STRING, groupingSeparator: STRING = None, decimalSeparator: STRING = None) -> NUMBER:
        if not literal:
            return None
        if not (" " == groupingSeparator or "." == groupingSeparator or "," == groupingSeparator or groupingSeparator is None):
            return None
        if not ("." == decimalSeparator or "," == decimalSeparator or decimalSeparator is None):
            return None
        if groupingSeparator is not None and groupingSeparator == decimalSeparator:
            return None

        if groupingSeparator is not None:
            if groupingSeparator == ".":
                groupingSeparator = "\\" + groupingSeparator
            literal = literal.replace(groupingSeparator, "")
        if decimalSeparator is not None and not (decimalSeparator == "."):
            literal = literal.replace(decimalSeparator, ".")
        return Decimal(literal, Context(prec=34, rounding=ROUND_HALF_EVEN))

    def decimal(self, n: NUMBER, scale: NUMBER) -> NUMBER:
        if n is None or scale is None:
            return None

        prec = int(scale)
        if prec < 0:
            raise Exception("Scale '{}' is not supported yet".format(scale))
        elif prec == 0:
            return n.to_integral(rounding=ROUND_HALF_EVEN)
        else:
            context = Context(prec=prec, rounding=ROUND_HALF_EVEN)
            return context.create_decimal(n)

    # Extension to DMN 1.3
    def round(self, n: NUMBER, scale: NUMBER, mode) -> NUMBER:
        raise Exception("Not supported yet")

    def floor(self, n: NUMBER, scale: NUMBER = None) -> NUMBER:
        # if scale is None:
        #     scale = self.valueOf(0)
        raise Exception("Not supported yet")

    def ceiling(self, n: NUMBER, scale: NUMBER) -> NUMBER:
        raise Exception("Not supported yet")

    def abs(self, n: NUMBER) -> NUMBER:
        if n is None:
            return None

        return n.copy_abs()

    def intModulo(self, dividend: NUMBER, divisor: NUMBER) -> NUMBER:
        raise Exception("Not supported yet")

    def modulo(self, dividend: NUMBER, divisor: NUMBER) -> NUMBER:
        raise Exception("Not supported yet")

    def sqrt(self, number: NUMBER) -> NUMBER:
        raise Exception("Not supported yet")

    def log(self, number: NUMBER) -> NUMBER:
        raise Exception("Not supported yet")

    def exp(self, number: NUMBER) -> NUMBER:
        raise Exception("Not supported yet")

    def odd(self, number: NUMBER) -> bool:
        raise Exception("Not supported yet")

    def even(self, number: NUMBER) -> bool:
        raise Exception("Not supported yet")

    #
    # List functions
    #
    def count(self, list_: List[Any]) -> NUMBER:
        if list_ is None:
            return 0
        else:
            return len(list_)

    def min(self, *operands) -> NUMBER:
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

    def max(self, *operands) -> NUMBER:
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

    def sum(self, *args) -> NUMBER:
        operands = varArgToList(*args)
        if len(operands) == 0:
            return None

        result = Decimal(0)
        for opd in operands:
            result += opd
        return result

    def mean(self, *args) -> NUMBER:
        raise Exception("Not supported yet")

    def product(self, *args) -> NUMBER:
        raise Exception("Not supported yet")

    def median(self, *args) -> NUMBER:
        raise Exception("Not supported yet")

    def stddev(self, *args) -> NUMBER:
        raise Exception("Not supported yet")

    def mode(self, *args) -> List[Decimal]:
        raise Exception("Not supported yet")

    def toNumber(self, number: NUMBER) -> NUMBER:
        raise Exception("Not supported yet")
