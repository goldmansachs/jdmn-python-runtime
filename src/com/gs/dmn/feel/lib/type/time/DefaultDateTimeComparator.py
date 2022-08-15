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
from datetime import date
from typing import Optional

from com.gs.dmn.feel.lib.type.RelationalComparator import RelationalComparator


class DefaultDateTimeComparator(RelationalComparator):
    def compare(self, first: Optional[date], second: Optional[date]) -> Optional[int]:
        if first is None or second is None:
            return None
        else:
            return self.compareTo(first, second)

    def equalTo(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.applyOperator(first, second, [
                lambda: True,
                lambda: False,
                lambda:False,
                lambda: self.compareTo(first, second) == 0
        ])

    def lessThan(self, first: Optional[date], second: Optional[date]) -> Optional[bool]:
        return self.applyOperator(first, second, [
                lambda: None,
                lambda: None,
                lambda: None,
                lambda: self.compareTo(first, second) == -1
            ])

    def compareTo(self, first: date, second: date) -> int:
        if first == second:
            return 0
        elif first < second:
            return -1
        else:
            return 1
