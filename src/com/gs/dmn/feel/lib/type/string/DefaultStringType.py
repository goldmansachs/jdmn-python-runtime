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
from typing import Any, Optional

from com.gs.dmn.feel.lib.type.string.StringComparator import StringComparator


class DefaultStringType:
    def __init__(self):
        self.stringComparator = StringComparator()

    def isString(self, value: Any) -> bool:
        return isinstance(value, str)

    def stringValue(self, value: Optional[str]) -> Optional[str]:
        return value

    def stringIs(self, first: Optional[str], second: Optional[str]) -> Optional[bool]:
        return first is second

    def stringEqual(self, first: Optional[str], second: Optional[str]) -> Optional[bool]:
        return self.stringComparator.equalTo(first, second)

    def stringNotEqual(self, first: Optional[str], second: Optional[str]) -> Optional[bool]:
        return self.stringComparator.notEqualTo(first, second)

    def stringLessThan(self, first: Optional[str], second: Optional[str]) -> Optional[bool]:
        return self.stringComparator.lessThan(first, second)

    def stringGreaterThan(self, first: Optional[str], second: Optional[str]) -> Optional[bool]:
        return self.stringComparator.greaterThan(first, second)

    def stringLessEqualThan(self, first: Optional[str], second: Optional[str]) -> Optional[bool]:
        return self.stringComparator.lessEqualThan(first, second)

    def stringGreaterEqualThan(self, first: Optional[str], second: Optional[str]) -> Optional[bool]:
        return self.stringComparator.greaterEqualThan(first, second)

    def stringAdd(self, first: Optional[str], second: Optional[str]) -> Optional[str]:
        if first is None or second is None:
            return None
        else:
            return first + second
