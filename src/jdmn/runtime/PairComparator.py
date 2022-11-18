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
import jdmn.runtime.Pair


class PairComparator:
    @staticmethod
    def compare(o1: jdmn.runtime.Pair.Pair, o2: jdmn.runtime.Pair.Pair) -> int:
        priority1 = o1.getRight()
        priority2 = o2.getRight()
        if priority1 is None and priority2 is None:
            return 0
        elif priority1 is None:
            return 1
        elif priority2 is None:
            return -1
        else:
            if isinstance(priority1, int) and isinstance(priority2, int):
                return priority2 - priority1
            else:
                return 1
