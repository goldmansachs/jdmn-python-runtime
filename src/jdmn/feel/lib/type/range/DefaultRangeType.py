#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from typing import Any

from jdmn.feel.lib.Types import BOOLEAN, RANGE
from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType
from jdmn.runtime.Range import Range


class DefaultRangeType(BaseType):
    def __init__(self):
        BaseType.__init__(self)
        self.booleanType = DefaultBooleanType()

    @staticmethod
    def isRange(value: Any) -> bool:
        return isinstance(value, Range)

    @staticmethod
    def rangeValue(value: RANGE) -> RANGE:
        if isinstance(value, Range):
            return value
        else:
            return None

    def rangeIs(self, r1: RANGE, r2: RANGE) -> BOOLEAN:
        return self.rangeEqual(r1, r2)

    def rangeEqual(self, r1: RANGE, r2: RANGE) -> BOOLEAN:
        if r1 is None and r2 is None:
            return True
        elif r1 is None:
            return False
        elif r2 is None:
            return False
        else:
            return self.isRange(r1) and self.isRange(r2) and r1 == r2

    def rangeNotEqual(self, r1: RANGE, r2: RANGE) -> BOOLEAN:
        return self.booleanType.booleanNot(self.rangeEqual(r1, r2))
