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
from typing import Optional

from jdmn.feel.lib.Types import DATE_TIME_UNION
from jdmn.feel.lib.type.RelationalComparator import RelationalComparator


class BaseDateTimeComparator(RelationalComparator):
    def __init__(self):
        super().__init__()

    def compare(self, first: DATE_TIME_UNION, second: DATE_TIME_UNION) -> Optional[int]:
        if first is None or second is None:
            return None
        else:
            return self.compareTo(first, second)

    def equalTo(self, first: DATE_TIME_UNION, second: DATE_TIME_UNION) -> Optional[bool]:
        return self.applyOperator(first, second, [
                lambda: True,
                lambda: False,
                lambda:False,
                lambda: self.compareTo(first, second) == 0
        ])

    def lessThan(self, first: DATE_TIME_UNION, second: DATE_TIME_UNION) -> Optional[bool]:
        return self.applyOperator(first, second, [
                lambda: None,
                lambda: None,
                lambda: None,
                lambda: self.compareTo(first, second) == -1
            ])

    @staticmethod
    def compareTo(first: DATE_TIME_UNION, second: DATE_TIME_UNION) -> int:
        pass
