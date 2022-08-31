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


class DefaultFunctionType(BaseType):
    def __init__(self):
        BaseType.__init__(self)

    def isFunction(self, value: Any) -> bool:
        raise Exception("Not supported yet")

    def functionValue(self, value: Any) -> Any:
        raise Exception("Not supported yet")

    def functionIs(self, function1: Any, function2: Any) -> BOOLEAN:
        raise Exception("Not supported yet")

    def functionEqual(self, function1: Any, function2: Any) -> BOOLEAN:
        raise Exception("Not supported yet")

    def functionNotEqual(self, function1: Any, function2: Any) -> BOOLEAN:
        raise Exception("Not supported yet")
