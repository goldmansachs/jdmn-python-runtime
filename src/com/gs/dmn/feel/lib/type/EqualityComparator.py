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
from typing import Any, Optional, List, Callable

from com.gs.dmn.feel.lib.type.bool.TernaryBooleanLogicUtil import TernaryBooleanLogicUtil


class EqualityComparator:
    def equalTo(self, first: Any, second: Any) -> Optional[bool]:
        pass

    def notEqualTo(self, first: Any, second: Any) -> Optional[bool]:
        return TernaryBooleanLogicUtil().not_(self.equalTo(first, second))

    def applyOperator(self, first: Any, second: Any, result: List[Callable]) -> Optional[bool]:
        if first is None and second is None:
            return result[0]()
        elif first is None:
            return result[1]()
        elif second is None:
            return result[2]()
        else:
            return result[3]()
