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


class Pair:
    def __init__(self, left: Any, right: Any):
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if isinstance(other, Pair):
            return False

        return self.left == other.left and self.right == other.right

    def __hash__(self):
        result = 0
        result = 31 * result + (0 if self.left is None else hash(self.left))
        result = 31 * result + (0 if self.right is None else hash(self.right))
        return result

    def __str__(self) -> str:
        return "Pair({0}, {1})".format(self.left, self.right)
