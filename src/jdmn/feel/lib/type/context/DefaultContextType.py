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
from typing import Any

from jdmn.feel.lib.Types import BOOLEAN, LIST, CONTEXT
from jdmn.feel.lib.type.BaseType import BaseType
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType
from jdmn.runtime.Context import Context


class DefaultContextType(BaseType):
    def __init__(self):
        BaseType.__init__(self)
        self.booleanType = DefaultBooleanType()

    def isContext(self, value: Any) -> bool:
        return isinstance(value, Context)

    def contextValue(self, value: CONTEXT) -> CONTEXT:
        if isinstance(value, Context):
            return value
        else:
            return None

    def contextIs(self, c1: CONTEXT, c2: CONTEXT) -> BOOLEAN:
        return self.contextEqual(c1, c2)

    def contextEqual(self, c1: CONTEXT, c2: CONTEXT) -> BOOLEAN:
        if c1 is None and c2 is None:
            return True
        elif c1 is None:
            return False
        elif c2 is None:
            return False
        else:
            return c1 == c2

    def contextNotEqual(self, c1: CONTEXT, c2: CONTEXT) -> BOOLEAN:
        return self.booleanType.booleanNot(self.contextEqual(c1, c2))

    def getEntries(self, m: CONTEXT) -> LIST:
        if self.isContext(m):
            result = []
            keys = m.getBindings().keys()
            for key in keys:
                result.append(Context().add("key", key).add("value", m.get(key)))
            return result
        else:
            return None

    def getValue(self, context: CONTEXT, key: Any) -> Any:
        if self.isContext(context):
            return context.get(key)
        else:
            return None
