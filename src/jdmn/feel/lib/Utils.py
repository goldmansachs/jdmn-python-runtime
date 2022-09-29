#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License")or you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from typing import List, Any


def varArgToList(*operands) -> List[Any]:
    if len(operands) == 0:
        return []
    if len(operands) == 1:
        if isinstance(operands[0], list):
            operands = operands[0]
        else:
            operands = [operands[0]]
    return list(operands)
