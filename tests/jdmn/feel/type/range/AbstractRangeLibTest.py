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
from unittest import TestCase

from jdmn.feel.lib.DefaultStandardFEELLib import DefaultStandardFEELLib
from jdmn.feel.lib.Types import RANGE, STRING, COMPARABLE
from jdmn.runtime.Range import Range


class AbstractRangeLibTest(TestCase):
    """
    Base test class for RangeLib
    """
    __test__ = False

    feelLib = DefaultStandardFEELLib()

    def testBefore(self):
        self.assertIsNone(self.feelLib.before(None, None))

        self.assertTrue(self.feelLib.before(self.makePoint(1), self.makePoint(10)))
        self.assertFalse(self.feelLib.before(self.makePoint(10), self.makePoint(1)))
        self.assertFalse(self.feelLib.before(self.makePoint(1), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.before(self.makePoint(1), self.makeRange("(", 1, 10, "]")))
        self.assertTrue(self.feelLib.before(self.makePoint(1), self.makeRange("[", 5, 10, "]")))
        self.assertFalse(self.feelLib.before(self.makeRange("[", 1, 10, "]"), self.makePoint(10)))
        self.assertTrue(self.feelLib.before(self.makeRange("[", 1, 10, ")"), self.makePoint(10)))
        self.assertTrue(self.feelLib.before(self.makeRange("[", 1, 10, "]"), self.makePoint(15)))
        self.assertTrue(self.feelLib.before(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 15, 20, "]")))
        self.assertFalse(self.feelLib.before(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 10, 20, "]")))
        self.assertTrue(self.feelLib.before(self.makeRange("[", 1, 10, ")"), self.makeRange("[", 10, 20, "]")))
        self.assertTrue(self.feelLib.before(self.makeRange("[", 1, 10, "]"), self.makeRange("(", 10, 20, "]")))

    def testAfter(self):
        self.assertIsNone(self.feelLib.after(None, None))
        self.assertIsNone(self.feelLib.after(None, None))
        self.assertIsNone(self.feelLib.after(None, None))
        self.assertIsNone(self.feelLib.after(None, None))

        self.assertTrue(self.feelLib.after(self.makePoint(10), self.makePoint(5)))
        self.assertFalse(self.feelLib.after(self.makePoint(5), self.makePoint(10)))
        self.assertTrue(self.feelLib.after(self.makePoint(12), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.after(self.makePoint(10), self.makeRange("[", 1, 10, ")")))
        self.assertFalse(self.feelLib.after(self.makePoint(10), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.after(self.makeRange("[", 11, 20, "]"), self.makePoint(12)))
        self.assertTrue(self.feelLib.after(self.makeRange("[", 11, 20, "]"), self.makePoint(10)))
        self.assertTrue(self.feelLib.after(self.makeRange("(", 11, 20, "]"), self.makePoint(11)))
        self.assertFalse(self.feelLib.after(self.makeRange("[", 11, 20, "]"), self.makePoint(11)))
        self.assertTrue(self.feelLib.after(self.makeRange("[", 11, 20, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.after(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 11, 20, "]")))
        self.assertTrue(self.feelLib.after(self.makeRange("[", 11, 20, "]"), self.makeRange("[", 1, 11, ")")))
        self.assertTrue(self.feelLib.after(self.makeRange("(", 11, 20, "]"), self.makeRange("[", 1, 11, "]")))

    def testMeets(self):
        self.assertIsNone(self.feelLib.meets(None, None))

        self.assertTrue(self.feelLib.meets(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 5, 10, "]")))
        self.assertFalse(self.feelLib.meets(self.makeRange("[", 1, 5, ")"), self.makeRange("[", 5, 10, "]")))
        self.assertFalse(self.feelLib.meets(self.makeRange("[", 1, 5, "]"), self.makeRange("(", 5, 10, "]")))
        self.assertFalse(self.feelLib.meets(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 6, 10, "]")))

    def testMetBy(self):
        self.assertIsNone(self.feelLib.metBy(None, None))

        self.assertTrue(self.feelLib.metBy(self.makeRange("[", 5, 10, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.metBy(self.makeRange("[", 5, 10, "]"), self.makeRange("[", 1, 5, ")")))
        self.assertFalse(self.feelLib.metBy(self.makeRange("(", 5, 10, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.metBy(self.makeRange("[", 6, 10, "]"), self.makeRange("[", 1, 5, "]")))

    def testOverlaps(self):
        self.assertIsNone(self.feelLib.overlaps(None, None))

        self.assertTrue(self.feelLib.overlaps(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 3, 8, "]")))
        self.assertTrue(self.feelLib.overlaps(self.makeRange("[", 3, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertTrue(self.feelLib.overlaps(self.makeRange("[", 1, 8, "]"), self.makeRange("[", 3, 5, "]")))
        self.assertTrue(self.feelLib.overlaps(self.makeRange("[", 3, 5, "]"), self.makeRange("[", 1, 8, "]")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 6, 8, "]")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("[", 6, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertTrue(self.feelLib.overlaps(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 5, 8, "]")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("[", 1, 5, "]"), self.makeRange("(", 5, 8, "]")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("[", 1, 5, ")"), self.makeRange("[", 5, 8, "]")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("[", 1, 5, ")"), self.makeRange("(", 5, 8, "]")))
        self.assertTrue(self.feelLib.overlaps(self.makeRange("[", 5, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("(", 5, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("[", 5, 8, "]"), self.makeRange("[", 1, 5, ")")))
        self.assertFalse(self.feelLib.overlaps(self.makeRange("(", 5, 8, "]"), self.makeRange("[", 1, 5, ")")))

    def testOverlapsBefore(self):
        self.assertIsNone(self.feelLib.overlapsBefore(None, None))

        self.assertTrue(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 3, 8, "]")))
        self.assertFalse(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 6, 8, "]")))
        self.assertTrue(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 5, 8, "]")))
        self.assertFalse(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, "]"), self.makeRange("(", 5, 8, "]")))
        self.assertFalse(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, ")"), self.makeRange("[", 5, 8, "]")))
        self.assertTrue(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, ")"), self.makeRange("(", 1, 5, "]")))
        self.assertTrue(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, "]"), self.makeRange("(", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, ")"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlapsBefore(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 1, 5, "]")))

    def testOverlapsAfter(self):
        self.assertIsNone(self.feelLib.overlapsAfter(None, None))

        self.assertTrue(self.feelLib.overlapsAfter(self.makeRange("[", 3, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlapsAfter(self.makeRange("[", 6, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertTrue(self.feelLib.overlapsAfter(self.makeRange("[", 5, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlapsAfter(self.makeRange("(", 5, 8, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlapsAfter(self.makeRange("[", 5, 8, "]"), self.makeRange("[", 1, 5, ")")))
        self.assertTrue(self.feelLib.overlapsAfter(self.makeRange("(", 1, 5, "]"), self.makeRange("[", 1, 5, ")")))
        self.assertTrue(self.feelLib.overlapsAfter(self.makeRange("(", 1, 5, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.overlapsAfter(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 1, 5, ")")))
        self.assertFalse(self.feelLib.overlapsAfter(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 1, 5, "]")))

    def testFinishes(self):
        self.assertIsNone(self.feelLib.finishes(None, None))
        self.assertIsNone(self.feelLib.finishes(None, None))

        self.assertTrue(self.feelLib.finishes(self.makePoint(10), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.finishes(self.makePoint(10), self.makeRange("[", 1, 10, ")")))
        self.assertTrue(self.feelLib.finishes(self.makeRange("[", 5, 10, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.finishes(self.makeRange("[", 5, 10, ")"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.finishes(self.makeRange("[", 5, 10, ")"), self.makeRange("[", 1, 10, ")")))
        self.assertTrue(self.feelLib.finishes(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.finishes(self.makeRange("(", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))

    def testFinishedBy(self):
        self.assertIsNone(self.feelLib.finishedBy(None, None))
        self.assertIsNone(self.feelLib.finishedBy(None, None))

        self.assertTrue(self.feelLib.finishedBy(self.makeRange("[", 1, 10, "]"), self.makePoint(10)))
        self.assertFalse(self.feelLib.finishedBy(self.makeRange("[", 1, 10, ")"), self.makePoint(10)))
        self.assertTrue(self.feelLib.finishedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 5, 10, "]")))
        self.assertFalse(self.feelLib.finishedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 5, 10, ")")))
        self.assertTrue(self.feelLib.finishedBy(self.makeRange("[", 1, 10, ")"), self.makeRange("[", 5, 10, ")")))
        self.assertTrue(self.feelLib.finishedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.finishedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("(", 1, 10, "]")))

    def testIncludes(self):
        self.assertIsNone(self.feelLib.includes(None, None))
        self.assertIsNone(self.feelLib.includes(None, None))

        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makePoint(5)))
        self.assertFalse(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makePoint(12)))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makePoint(1)))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makePoint(10)))
        self.assertFalse(self.feelLib.includes(self.makeRange("(", 1, 10, "]"), self.makePoint(1)))
        self.assertFalse(self.feelLib.includes(self.makeRange("[", 1, 10, ")"), self.makePoint(10)))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 4, 6, "]")))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertTrue(self.feelLib.includes(self.makeRange("(", 1, 10, "]"), self.makeRange("(", 1, 5, "]")))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makeRange("(", 1, 10, ")")))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, ")"), self.makeRange("[", 5, 10, ")")))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, ")")))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makeRange("(", 1, 10, "]")))
        self.assertTrue(self.feelLib.includes(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))

    def testDuring(self):
        self.assertIsNone(self.feelLib.during(None, None))
        self.assertIsNone(self.feelLib.during(None, None))

        self.assertTrue(self.feelLib.during(self.makePoint(5), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.during(self.makePoint(12), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makePoint(1), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makePoint(10), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.during(self.makePoint(1), self.makeRange("(", 1, 10, "]")))
        self.assertFalse(self.feelLib.during(self.makePoint(10), self.makeRange("[", 1, 10, ")")))
        self.assertTrue(self.feelLib.during(self.makeRange("[", 4, 6, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makeRange("(", 1, 5, "]"), self.makeRange("(", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makeRange("(", 1, 10, ")"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makeRange("[", 5, 10, ")"), self.makeRange("[", 1, 10, ")")))
        self.assertTrue(self.feelLib.during(self.makeRange("[", 1, 10, ")"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makeRange("(", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.during(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))

    def testStarts(self):
        self.assertIsNone(self.feelLib.starts(None, None))
        self.assertIsNone(self.feelLib.starts(None, None))

        self.assertTrue(self.feelLib.starts(self.makePoint(1), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.starts(self.makePoint(1), self.makeRange("(", 1, 10, "]")))
        self.assertFalse(self.feelLib.starts(self.makePoint(2), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.starts(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.starts(self.makeRange("(", 1, 5, "]"), self.makeRange("(", 1, 10, "]")))
        self.assertFalse(self.feelLib.starts(self.makeRange("(", 1, 5, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertFalse(self.feelLib.starts(self.makeRange("[", 1, 5, "]"), self.makeRange("(", 1, 10, "]")))
        self.assertTrue(self.feelLib.starts(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.starts(self.makeRange("[", 1, 10, ")"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.starts(self.makeRange("(", 1, 10, ")"), self.makeRange("(", 1, 10, ")")))

    def testStartedBy(self):
        self.assertIsNone(self.feelLib.startedBy(None, None))
        self.assertIsNone(self.feelLib.startedBy(None, None))

        self.assertTrue(self.feelLib.startedBy(self.makeRange("[", 1, 10, "]"), self.makePoint(1)))
        self.assertFalse(self.feelLib.startedBy(self.makeRange("(", 1, 10, "]"), self.makePoint(1)))
        self.assertFalse(self.feelLib.startedBy(self.makeRange("[", 1, 10, "]"), self.makePoint(2)))
        self.assertTrue(self.feelLib.startedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertTrue(self.feelLib.startedBy(self.makeRange("(", 1, 10, "]"), self.makeRange("(", 1, 5, "]")))
        self.assertFalse(self.feelLib.startedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("(", 1, 5, "]")))
        self.assertFalse(self.feelLib.startedBy(self.makeRange("(", 1, 10, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertTrue(self.feelLib.startedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, "]")))
        self.assertTrue(self.feelLib.startedBy(self.makeRange("[", 1, 10, "]"), self.makeRange("[", 1, 10, ")")))
        self.assertTrue(self.feelLib.startedBy(self.makeRange("(", 1, 10, ")"), self.makeRange("(", 1, 10, ")")))

    def testCoincides(self):
        self.assertIsNone(self.feelLib.coincides(None, None))
        self.assertIsNone(self.feelLib.coincides(None, None))

        self.assertTrue(self.feelLib.coincides(self.makePoint(5), self.makePoint(5)))
        self.assertFalse(self.feelLib.coincides(self.makePoint(3), self.makePoint(4)))
        self.assertTrue(self.feelLib.coincides(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.coincides(self.makeRange("(", 1, 5, ")"), self.makeRange("[", 1, 5, "]")))
        self.assertFalse(self.feelLib.coincides(self.makeRange("[", 1, 5, "]"), self.makeRange("[", 2, 6, "]")))

    def makeRange(self, startIncluded: STRING, start: int, end: int, endIncluded: STRING) -> RANGE:
        return Range(startIncluded == "[", self.makePoint(start), endIncluded == "]", self.makePoint(end))

    def makePoint(self, number: int) -> COMPARABLE:
        raise NotImplementedError()
