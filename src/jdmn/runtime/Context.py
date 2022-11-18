#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use self file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from typing import Any


class Context:
    def __init__(self, name: str = None):
        self.name = name
        self.map = {}

    def getName(self) -> str:
        return self.name

    def getBindings(self) -> dict:
        return self.map

    def get(self, name: str, *args) -> Any:
        o = self.map[name]
        if o is not None:
            return o
        for key in args:
            o = self.map[key]
            if o is not None:
                return o
        return None

    def put(self, key: Any, value: Any) -> Any:
        self.map[key] = value
        return value

    def add(self, key: Any, value: Any):
        self.put(key, value)
        return self

    def isEquivalent(self, other: Any):
        return other is not None and isinstance(other, Context) and self.keySet() == other.keySet()

    def __str__(self):
        return str(self.map)

    def keySet(self):
        return self.map.keys()

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if other is None or self.__class__ != other.__class__:
            return False

        return self.map == other.map

    def __hash__(self):
        result = 0
        result = 31 * result + (0 if self.map is None else hash(self.map))
        return result
