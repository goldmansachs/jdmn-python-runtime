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


class TernaryBooleanLogicUtil:
    def not_(self, operand: Any) -> Optional[bool]:
        if isinstance(operand, bool):
            return not operand
        else:
            return None

    def and_(self, first: Any, second: Any) -> Optional[bool]:
        if self.isBooleanFalse(first) or self.isBooleanFalse(second):
            return False
        elif self.isBooleanTrue(first) and self.isBooleanTrue(second):
            return True
        else:
            return None

    def or_(self, first: Any, second: Any) -> Optional[bool]:
        if self.isBooleanTrue(first) or self.isBooleanTrue(second):
            return True
        elif self.isBooleanFalse(first) and self.isBooleanFalse(second):
            return False
        else:
            return None

    @staticmethod
    def isBooleanTrue(obj: Any) -> bool:
        return isinstance(obj, bool) and obj is True

    @staticmethod
    def isBooleanFalse(obj: Any) -> bool:
        return isinstance(obj, bool) and obj is False
