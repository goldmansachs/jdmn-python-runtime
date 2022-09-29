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
        result = []
        if list_ is not None:
            result.extend(list_)
        if items is not None:
            for item in items:
                result.append(item)
        else:
            result.append(None)
        return result

    def sublist(self, list_: LIST, position: INT, length: INT = None) -> LIST:
        if position is None:
            return None

        result = []
        if list_ is None or self.isOutOfBounds(list_, position):
            return result
        if position < 0:
            startIndex = len(list_) + position
        else:
            startIndex = position - 1
        endIndex = len(list_) if length is None else startIndex + length
        return list_[startIndex: endIndex]

    def concatenate(self, *lists) -> LIST:
        result = []
        if lists is not None:
            for list_ in lists:
                result.extend(list_)
        return result

    def insertBefore(self, list_: LIST, position: INT, newItem: Any) -> LIST:
        result = []
        if list_ is not None:
            result.extend(list_)
        if self.isOutOfBounds(result, position):
            return result
        if position < 0:
            position = len(result) + position
        else:
            position = position - 1
        result.insert(position, newItem)
        return result

    def remove(self, list_: LIST, position: INT) -> LIST:
        result = []
        if list_ is not None:
            result.extend(list_)
        result.pop(position - 1)
        return result

    def reverse(self, list_: LIST) -> LIST:
        result = []
        if list_ is not None:
            result = list_.copy()
            result.reverse()
        return result

    def union(self, *lists) -> LIST:
        result = []
        if lists is not None:
            for list_ in lists:
                result.extend(list_)
        return self.distinctValues(result)

    def distinctValues(self, list1: LIST) -> LIST:
        result = []
        if list1 is not None:
            for element in list1:
                if element not in result:
                    result.append(element)
        return result

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

    @staticmethod
    def isOutOfBounds(list_: LIST, position: INT) -> bool:
        if position is None:
            return False

        length = len(list_)
        if position < 0:
            return not (-length <= position)
        else:
            return not (1 <= position <= length)
