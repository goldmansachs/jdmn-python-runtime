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

from jdmn.feel.lib.type.ComparableComparator import ComparableComparator


class StringComparator(ComparableComparator):
    @staticmethod
    def compareTo(first: str, second: str) -> int:
        if first == second:
            return 0
        elif first < second:
            return -1
        else:
            return 1
