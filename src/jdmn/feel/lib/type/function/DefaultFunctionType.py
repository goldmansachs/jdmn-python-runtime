#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License")or you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from typing import Any

from jdmn.feel.lib.Types import BOOLEAN
from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType


class DefaultFunctionType(BaseType):
    def __init__(self):
        BaseType.__init__(self)
        self.booleanType = DefaultBooleanType()

    @staticmethod
    def isFunction(value: Any) -> bool:
        if value is None:
            return True

        raise Exception("Not supported yet")

    def functionValue(self, value: Any) -> Any:
        if (self.isFunction(value)):
            return value
        else:
            return None

    def functionIs(self, function1: Any, function2: Any) -> BOOLEAN:
        return self.functionEqual(function1, function2)

    def functionEqual(self, function1: Any, function2: Any) -> BOOLEAN:
        if self.isFunction(function1) and self.isFunction(function2):
            return function1 == function2
        else:
            return None

    def functionNotEqual(self, function1: Any, function2: Any) -> BOOLEAN:
        return self.booleanType.booleanNot(self.functionEqual(function1, function2))
