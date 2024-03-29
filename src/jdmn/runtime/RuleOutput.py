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
from typing import List


class RuleOutput:
    def __init__(self, matched: bool):
        self.matched = matched

    def isMatched(self) -> bool:
        return self.matched

    def setMatched(self, matched: bool) -> None:
        self.matched = matched

    @staticmethod
    def sort(rules: List['RuleOutput']) -> List['RuleOutput']:
        return rules
