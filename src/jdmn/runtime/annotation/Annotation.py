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
import typing


class Annotation:
    # Index starts from 1

    def __init__(self, decisionName: str, ruleIndex: int, annotation: str):
        self.decisionName = decisionName
        self.ruleIndex = ruleIndex
        self.annotation = annotation

    def __eq__(self, other: typing.Any) -> bool:
        if self is other:
            return True
        if type(self) is not type(other):
            return False

        if self.decisionName != other.decisionName:
            return False
        if self.ruleIndex != other.ruleIndex:
            return False
        if self.annotation != other.annotation:
            return False

        return True

    def __str__(self) -> str:
        return "Annotation('{0}', {1}, '{2}')".format(self.decisionName, self.ruleIndex, self.annotation)
