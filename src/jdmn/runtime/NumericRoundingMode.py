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
from enum import Enum


class NumericRoundingMode(Enum):
    UP = "up",
    DOWN = "down",
    HALF_UP = "half up",
    HALF_DOWN = "half down",
    HALF_EVEN = "half even",
    UNKNOWN = ""

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name):
        self.displayName = name

    def fromName(self, name: str) -> 'NumericRoundingMode':
        for policy in NumericRoundingMode:
            if policy.displayName == name:
                return policy
        return self.UNKNOWN

    def allowedValues(self):
        return [x for x in NumericRoundingMode if x != NumericRoundingMode.UNKNOWN]
