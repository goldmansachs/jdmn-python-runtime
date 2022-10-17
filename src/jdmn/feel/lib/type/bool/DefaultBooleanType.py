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
from typing import Any, Optional

from jdmn.feel.lib.Utils import varArgToList
from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.feel.lib.type.bool.TernaryBooleanLogicUtil import TernaryBooleanLogicUtil


class DefaultBooleanType(BaseType):
    def __init__(self):
        BaseType.__init__(self)

    def isBoolean(self, value: Any) -> bool:
        return isinstance(value, bool)

    def booleanValue(self, value: Optional[bool]) -> Optional[bool]:
        return value

    def booleanNot(self, operand: Any) -> Optional[bool]:
        return TernaryBooleanLogicUtil().not_(operand)

    def booleanOr(self, *args) -> Optional[bool]:
        operands = varArgToList(*args)

        if len(operands) < 2:
            return None
        result = operands[0]
        for opd in operands[1:]:
            result = self.binaryBooleanOr(result, opd)
        return result

    def binaryBooleanOr(self, first: Any, second: Any) -> Optional[bool]:
        return TernaryBooleanLogicUtil().or_(first, second)

    def booleanAnd(self, *args) -> Optional[bool]:
        operands = varArgToList(*args)

        if len(operands) < 2:
            return None
        result = operands[0]
        for opd in operands[1:]:
            result = self.binaryBooleanAnd(result, opd)
        return result

    def binaryBooleanAnd(self, first: Any, second: Any) -> Optional[bool]:
        return TernaryBooleanLogicUtil().and_(first, second)

    def booleanIs(self, first: Optional[bool], second: Optional[bool]) -> Optional[bool]:
        return self.booleanEqual(first, second)

    def booleanEqual(self, first: Optional[bool], second: Optional[bool]) -> Optional[bool]:
        if (first is None and second is None):
            return True
        elif first is None:
            return False
        elif second is None:
            return False
        else:
            return self.isBoolean(first) and self.isBoolean(second) and first == second

    def booleanNotEqual(self, first: Optional[bool], second: Optional[bool]) -> Optional[bool]:
        return self.booleanNot(self.booleanEqual(first, second))
