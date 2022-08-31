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


class Range:
    def __init__(self, startIncluded: bool, start: Any, endIncluded: bool, end: Any):
        self.startIncluded = startIncluded
        self.start = start
        self.endIncluded = endIncluded
        self.end = end

    def isStartIncluded(self) -> bool:
        return self.startIncluded

    def getStart(self) -> Any:
        return self.start

    def isEndIncluded(self) -> bool:
        return self.endIncluded

    def getEnd(self) -> Any:
        return self.end

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if type(self) is not type(other):
            return False

        if self.startIncluded != other.startIncluded:
            return False
        if self.endIncluded != other.endIncluded:
            return False
        if self.start != other.start:
            return False
        if self.end != other.end:
            return False
        return True

    def __hash__(self):
        result = 0
        result = 31 * result + (0 if self.startIncluded is None else hash(self.startIncluded))
        result = 31 * result + (0 if self.start is None else hash(self.start))
        result = 31 * result + (0 if self.endIncluded is None else hash(self.endIncluded))
        result = 31 * result + (0 if self.end is None else hash(self.end))
        return result

    def __str__(self):
        return "Range({},{},{},{})".format(self.startIncluded, self.start.toString(), self.end.toString(), self.endIncluded)
