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
from jdmn.feel.lib.Types import POINT_RANGE_UNION, BOOLEAN
from jdmn.runtime.Range import Range


class DefaultRangeLib:
    def before(self, arg1: POINT_RANGE_UNION, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        raise Exception("Not supported yet")

    def after(self, arg1: POINT_RANGE_UNION, arg2: POINT_RANGE_UNION):
        raise Exception("Not supported yet")

    def meets(self, range1: Range, range2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def metBy(self, range1: Range, range2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def overlaps(self, range1: Range, range2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def overlapsBefore(self, range1: Range, range2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def overlapsAfter(self, range1: Range, range2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def finishes(self, arg1: POINT_RANGE_UNION, arg2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def finishedBy(self, arg1: Range, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        raise Exception("Not supported yet")

    def includes(self, arg1: Range, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        raise Exception("Not supported yet")

    def during(self, arg1: POINT_RANGE_UNION, arg2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def starts(self, arg1: POINT_RANGE_UNION, arg2: Range) -> BOOLEAN:
        raise Exception("Not supported yet")

    def startedBy(self, arg1: Range, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        raise Exception("Not supported yet")

    def coincides(self, arg1: POINT_RANGE_UNION, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        raise Exception("Not supported yet")
