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

from com.gs.dmn.feel.lib.type.EqualityComparator import EqualityComparator
from com.gs.dmn.feel.lib.type.bool.TernaryBooleanLogicUtil import TernaryBooleanLogicUtil


class RelationalComparator(EqualityComparator):
    def compare(self, first: Any, second: Any) -> int:
        pass

    def lessThan(self, first: Any, second: Any) -> Optional[bool]:
        pass

    def greaterThan(self, first: Any, second: Any) -> Optional[bool]:
        return self.lessThan(second, first)

    def lessEqualThan(self, first: Any, second: Any) -> Optional[bool]:
        return TernaryBooleanLogicUtil().or_(self.lessThan(first, second), self.equalTo(first, second))

    def greaterEqualThan(self, first: Any, second: Any) -> Optional[bool]:
        return TernaryBooleanLogicUtil().or_(self.greaterThan(first, second), self.equalTo(first, second))
