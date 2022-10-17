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
from typing import Any, List, Optional

from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType


class DefaultListType(BaseType):
    def __init__(self):
        BaseType.__init__(self)
        self.booleanType = DefaultBooleanType()

    def isList(self, value: Any) -> bool:
        return isinstance(value, List)

    def listValue(self, value: Optional[List[Any]]) -> Optional[List[Any]]:
        return value

    def listIs(self, list1: Optional[List[Any]], list2: Optional[List[Any]]) -> Optional[bool]:
        return self.listEqual(list1, list2)

    def listEqual(self, list1: Optional[List[Any]], list2: Optional[List[Any]]) -> Optional[bool]:
        if list1 is None and list2 is None:
            return True
        elif list1 is None:
            return False
        elif list2 is None:
            return False
        else:
            return self.isList(list1) and self.isList(list2) and list1 == list2

    def listNotEqual(self, list1: Optional[List[Any]], list2: Optional[List[Any]]) -> Optional[bool]:
        return self.booleanType.booleanNot(self.listEqual(list1, list2))
