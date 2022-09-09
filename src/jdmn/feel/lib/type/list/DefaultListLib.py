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
from functools import cmp_to_key
from typing import Any

from jdmn.feel.lib.Types import BOOLEAN, LIST, INT
from jdmn.runtime.LambdaExpression import LambdaExpression


class DefaultListLib:
    def listContains(self, list_: LIST, element: Any) -> BOOLEAN:
        if list_ is None:
            return None

        return element in list_

    def append(self, list_: LIST, *items) -> LIST:
        raise Exception("Not supported yet")

    def sublist(self, list_: LIST, position: INT, length: INT = None) -> LIST:
        result = []
        if list_ is None or self.isOutOfBounds(list_, position):
            return result
        if position < 0:
            startIndex = len(list_) + position
        else:
            startIndex = position - 1
        endIndex = startIndex + length
        return list_[startIndex: endIndex]

    def concatenate(self, *lists) -> LIST:
        result = []
        if lists is not None:
            for list_ in lists:
                result.extend(list_)
        return result

    def insertBefore(self, list_: LIST, position: INT, newItem: Any) -> LIST:
        raise Exception("Not supported yet")

    def remove(self, list_: LIST, position: INT) -> LIST:
        raise Exception("Not supported yet")

    def reverse(self, list_: LIST) -> LIST:
        raise Exception("Not supported yet")

    def union(self, *lists) -> LIST:
        raise Exception("Not supported yet")

    def distinctValues(self, list1: LIST) -> LIST:
        raise Exception("Not supported yet")

    def flatten(self, list1: LIST) -> LIST:
        if list1 is None:
            return None
        result = []
        self.collect(result, list1)
        return result

    def collect(self, result: LIST, list1: LIST) -> None:
        if list1 is not None:
            for obj in list1:
                if isinstance(obj, list):
                    self.collect(result, obj)
                else:
                    result.append(obj)

    def sort(self, list_: LIST, precedes: LambdaExpression) -> LIST:
        clone = []
        clone.extend(list_)
        clone.sort(key=cmp_to_key(lambda o1, o2: -1 if precedes.apply(o1, o2) else (0 if o1 == o2 else 1)))
        return clone

    def isOutOfBounds(self, list_: LIST, position: int) -> bool:
        length = len(list_)
        if position < 0:
            return not (-length <= position)
        else:
            return not (1 <= position <= length)
