#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from jdmn.feel.lib.DefaultStandardFEELLib import DefaultStandardFEELLib
from jdmn.feel.lib.Types import COMPARABLE
from jdmn.feel.type.range.AbstractRangeLibTest import AbstractRangeLibTest


class DefaultTimeRangeLibTest(AbstractRangeLibTest):
    """
    Base test class for DefaultRangeLib
    """
    __test__ = True

    feelLib = DefaultStandardFEELLib()

    def makePoint(self, number: int) -> COMPARABLE:
        if number < 0 or number > 60:
            raise Exception("Illegal second field")
        return self.feelLib.time(f"12:00:{number:02d}")
