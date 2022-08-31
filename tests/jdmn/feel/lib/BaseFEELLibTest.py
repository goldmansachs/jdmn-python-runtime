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
from jdmn.feel.lib.FEELOperatorsTest import FEELOperatorsTest
from jdmn.runtime.Context import Context


class BaseFEELLibTest(FEELOperatorsTest):
    """
    Base test class for BaseFEELLib
    """
    __test__ = True

    #
    # Conversion functions
    #
    def testNumber(self):
        self.assertEqual(None, self.getLib().number(None))
        self.assertEqual(None, self.getLib().number("1,200.56"))
        self.assertEqual(None, self.getLib().number("xxx"))

        self.assertEqualsNumber("123.56", self.getLib().number("123.56"))
        self.assertEqualsNumber("-123.56", self.getLib().number("-123.56"))

    def testDate(self):
        #
        # conversion from string
        #
        self.assertEqual(None, self.getLib().date(None))
        self.assertEqual(None, self.getLib().date(""))
        self.assertEqual(None, self.getLib().date("xxx"))
        self.assertEqual(None, self.getLib().date("01211-12-31"))
        self.assertEqual(None, self.getLib().date("2017-08-25T11:00:00"))

        # year must be in the range [-999,999,999..999,999,999].
#        self.assertEqualsDateTime("999999999-10-11", self.getLib().date(self.getLib().date("999999999-10-11")))
#        self.assertEqualsDateTime("-999999999-10-11", self.getLib().date(self.getLib().date("-999999999-10-11")))
#        self.assertEqual(None, self.getLib().date(self.getLib().date("9999999991-10-11")))
#        self.assertEqual(None, self.getLib().date(self.getLib().date("-9999999991-10-11")))

        self.assertEqualsDateTime("2016-08-01", self.getLib().date("2016-08-01"))

        #
        # conversion from date
        #
        self.assertEqual(None, self.getLib().date(None))
        self.assertEqualsDateTime("2016-08-01", self.getLib().date(self.makeDate("2016-08-01")))

        #
        # conversion from numbers
        #
        self.assertEqual(None, self.getLib().date(None, None, None))
        self.assertEqual(None, self.getLib().date(self.makeNumber("2016"), None, None))
        self.assertEqual(None, self.getLib().date(None, self.makeNumber("8"), None))
        self.assertEqual(None, self.getLib().date(None, None, self.makeNumber("1")))
        self.assertEqualsDateTime("2016-08-01", self.getLib().date(self.makeNumber("2016"), self.makeNumber("8"), self.makeNumber("1")))

    def testTime(self):
        #
        # conversion from string
        #
        self.assertEqual(None, self.getLib().time(None))
        self.assertEqual(None, self.getLib().time(""))
        self.assertEqual(None, self.getLib().time("xxx"))
#        self.assertEqual(None, self.getLib().time("13:20:00+01:00@Europe/Paris"))
#        self.assertEqual(None, self.getLib().time("13:20:00+00:00[UTC]"))

        # fix input literal
        self.assertEqualsDateTime("11:00:00Z", self.getLib().time("T11:00:00Z"))
        self.assertEqualsDateTime("11:00:00+01:00", self.getLib().time("11:00:00+0100"))

        self.assertEqualsDateTime("11:00:00Z", self.getLib().time("11:00:00Z"))
        self.assertEqualsDateTime("11:00:00.001Z", self.getLib().time("11:00:00.001Z"))

        self.assertEqualsDateTime("11:00:00.001+01:00", self.getLib().time("11:00:00.001+01:00"))
        self.assertEqualsDateTime("11:00:00+01:00", self.getLib().time("11:00:00+01:00"))

        #
        # conversion from number
        #
        self.assertEqual(None, self.getLib().time(None, None, None, None))

        self.assertEqual(None, self.getLib().time(
            self.makeNumber("12"), self.makeNumber("00"), self.makeNumber("00"),
            self.makeDuration("PT25H10M")))
        self.assertEqualsDateTime("12:00:00+01:10", self.getLib().time(
            self.makeNumber("12"), self.makeNumber("00"), self.makeNumber("00"),
            self.makeDuration("PT1H10M")))

    def testDateTime(self):
        #
        # conversion from string
        #
        self.assertEqual(None, self.getLib().dateAndTime(None))
        self.assertEqual(None, self.getLib().dateAndTime(""))
        self.assertEqual(None, self.getLib().dateAndTime("xxx"))
        self.assertEqual(None, self.getLib().dateAndTime("11:00:00"))
#        self.assertEqual(None, self.getLib().dateAndTime("2011-12-03T10:15:30+01:00@Europe/Paris"))
#        self.assertEqual(None, self.getLib().dateAndTime("2017-12-31T12:20:00+19:00"))

        # fix input literal
        self.assertEqualsDateTime("2016-08-01T11:00:00+01:00", self.getLib().dateAndTime("2016-08-01T11:00:00+0100"))

        self.assertEqualsDateTime("2016-08-01T11:00:00Z", self.getLib().dateAndTime("2016-08-01T11:00:00Z"))
        self.assertEqualsDateTime("2016-08-01T11:00:00.001Z", self.getLib().dateAndTime("2016-08-01T11:00:00.001Z"))
        self.assertEqualsDateTime("2016-08-01T11:00:00.001+01:00", self.getLib().dateAndTime("2016-08-01T11:00:00.001+01:00"))
        self.assertEqualsDateTime("2016-08-01T11:00:00+01:00", self.getLib().dateAndTime("2016-08-01T11:00:00+01:00"))

        #
        # conversion from date and time
        #
        self.assertEqual(None, self.getLib().dateAndTime(None, None))
        self.assertEqual(None, self.getLib().dateAndTime(None, self.makeTime("11:00:00Z")))
        self.assertEqual(None, self.getLib().dateAndTime(self.getLib().date("2016-08-01"), None))

        self.assertEqualsDateTime("2016-08-01T11:00:00Z", self.getLib().dateAndTime(self.makeDate("2016-08-01"), self.makeTime("11:00:00Z")))

    def testDuration(self):
        self.assertEqual(None, self.getLib().duration("XXX"))
        self.assertEqual(None, self.getLib().duration(None))

        self.assertEqualsDateTime("P1Y8M", self.getLib().duration("P1Y8M"))
        self.assertEqualsDateTime("P2DT20H", self.getLib().duration("P2DT20H"))

    #
    # Conversion functions
    #
    def testAsList(self):
        self.assertEqualsList([None], self.getLib().asList(None))
        self.assertEqual([], self.getLib().asList())
        self.assertEqual([None, "a"], self.getLib().asList(None, "a"))

    def testAsElement(self):
        self.assertEqual(None, self.getLib().asElement(None))
        self.assertEqual(None, self.getLib().asElement([]))
        self.assertEqual(None, None, self.getLib().asElement(["1", "2"]))

        self.assertEqual("1", self.getLib().asElement(["1"]))

    def testRangeToList(self):
        self.assertEqual(self.makeNumberList(), self.getLib().rangeToList(False, None, False, None))
        self.assertEqual(self.makeNumberList(), self.getLib().rangeToList(False, None, False, self.makeNumber("3")))
        self.assertEqual(self.makeNumberList(), self.getLib().rangeToList(False, self.makeNumber("1"), False, None))

        self.assertEqual(self.makeNumberList("2"), self.getLib().rangeToList(True, self.makeNumber("1"), True, self.makeNumber("3")))
        self.assertEqual(self.makeNumberList("1", "2"), self.getLib().rangeToList(False, self.makeNumber("1"), True, self.makeNumber("3")))
        self.assertEqual(self.makeNumberList("2", "3"), self.getLib().rangeToList(True, self.makeNumber("1"), False, self.makeNumber("3")))
        self.assertEqual(self.makeNumberList("1", "2", "3"), self.getLib().rangeToList(False, self.makeNumber("1"), False, self.makeNumber("3")))

    def testRangeToListNoFlags(self):
        self.assertEqual([], self.getLib().rangeToList(None, None))
        self.assertEqual([], self.getLib().rangeToList(self.makeNumber("0"), None))
        self.assertEqual([], self.getLib().rangeToList(None, self.makeNumber("1")))

        self.assertEqual(self.makeNumberList(1, 2, 3), self.getLib().rangeToList(self.makeNumber("1"), self.makeNumber("3")))
        self.assertEqual(self.makeNumberList(3, 2, 1), self.getLib().rangeToList(self.makeNumber("3"), self.makeNumber("1")))

    def testToDate(self):
        self.assertEqual(None, self.getLib().toDate(None))
        self.assertEqual(None, self.getLib().toDate("1"))
        self.assertEqual(None, self.getLib().toDate(self.makeNumber("1")))
        self.assertEqual(None, self.getLib().toDate(self.makeTime("12:00:00Z")))

        self.assertEqualsDateTime("2016-08-01", self.getLib().toDate(self.makeDate("2016-08-01")))
        self.assertEqualsDateTime("2016-08-01", self.getLib().toDate(self.makeDateAndTime("2016-08-01T12:00:00Z")))

    def testToTime(self):
        self.assertEqual(None, self.getLib().toTime(None))
        self.assertEqual(None, self.getLib().toTime("1"))
        self.assertEqual(None, self.getLib().toTime(self.makeNumber("1")))

        self.assertEqualsDateTime("00:00:00Z", self.getLib().toTime(self.makeDate("2016-08-01")))
        self.assertEqualsDateTime("12:00:00Z", self.getLib().toTime(self.makeTime("12:00:00Z")))
        self.assertEqualsDateTime("12:00:00Z", self.getLib().toTime(self.makeDateAndTime("2016-08-01T12:00:00Z")))

    #
    # Boolean functions
    #
    def testAnd(self):
        self.assertFalse(self.getLib().and_(True, True, False))
        self.assertFalse(self.getLib().and_(None, False))
        self.assertFalse(self.getLib().and_([True, True, False]))
        self.assertFalse(self.getLib().and_([None, False]))

        self.assertTrue(self.getLib().and_())
        self.assertTrue(self.getLib().and_([]))
        self.assertTrue(self.getLib().and_(True, True))
        self.assertTrue(self.getLib().and_([True, True]))

        self.assertEqual(None, self.getLib().and_(None))
        self.assertEqual(None, self.getLib().and_(None, None))
        self.assertEqual(None, self.getLib().and_(None, True))
        self.assertEqual(None, self.getLib().and_([None, None]))
        self.assertEqual(None, self.getLib().and_([None, True]))

    def testOr(self):
        self.assertTrue(self.getLib().or_(True, True))
        self.assertTrue(self.getLib().or_(False, True))
        self.assertTrue(self.getLib().or_(None, True))
        self.assertTrue(self.getLib().or_([True, True]))
        self.assertTrue(self.getLib().or_([False, True]))
        self.assertTrue(self.getLib().or_([None, True]))

        self.assertFalse(self.getLib().or_())
        self.assertFalse(self.getLib().or_([]))
        self.assertFalse(self.getLib().or_(False, False, False))
        self.assertFalse(self.getLib().or_([False, False, False]))

        self.assertEqual(None, self.getLib().or_(None, None))
        self.assertEqual(None, self.getLib().or_(None, False))
        self.assertEqual(None, self.getLib().or_([None, None]))
        self.assertEqual(None, self.getLib().or_([None, False]))

    #
    # List functions
    #
    def testElementAt(self):
        self.assertEqual(None, self.getLib().elementAt(None, self.makeNumber("1")))
        self.assertEqual(None, self.getLib().elementAt(["1", "2", "3"], self.makeNumber("4")))
        self.assertEqual(None, self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-4")))
        self.assertEqual(None, self.getLib().elementAt(["1", "2", "3"], self.makeNumber("0")))

        self.assertEqual("1", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("1")))
        self.assertEqual("2", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("2")))
        self.assertEqual("3", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("3")))
        self.assertEqual("3", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-1")))
        self.assertEqual("2", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-2")))
        self.assertEqual("1", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-3")))

    def testFlattenFirstLevel(self):
        self.assertEqual(None, self.getLib().flattenFirstLevel(None))

        self.assertEqualsList([], self.getLib().flattenFirstLevel([]))
        self.assertEqualsList(["l11", "l12", "l13"], self.getLib().flattenFirstLevel(["l11", "l12", "l13"]))
        self.assertEqualsList(["l11", "l21", "l22", "l13"], self.getLib().flattenFirstLevel(["l11", ["l21", "l22"], "l13"]))
        self.assertEqualsList(["l11", "l21", ["l31", "l32"], "l13"], self.getLib().flattenFirstLevel(["l11", ["l21", ["l31", "l32"]], "l13"]))

        self.assertEqualsList(["l11", None, [None, "l32"], "l13"], self.getLib().flattenFirstLevel(["l11", [None, [None, "l32"]], "l13"]))

    def testCount(self):
        self.assertEqualsNumber(self.makeNumber("0"), self.getLib().count(None))

        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().count(self.makeNumberList(1, 2, 3)))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().count(self.makeNumberList(1, None, 3)))

    def testMin(self):
        self.assertEqual(None, self.getLib().min())
        self.assertEqual(None, self.getLib().min(None))
        self.assertEqual(None, self.getLib().min(self.makeNumberList()))

        self.assertEqual(None, self.getLib().min(self.makeNumber(1), None, self.makeNumber(3)))
        self.assertEqual(None, self.getLib().min(self.makeNumberList(1, None, 3)))

        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().min(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().min(self.makeNumberList(1, 2, 3)))

    def testMax(self):
        self.assertEqual(None, self.getLib().max())
        self.assertEqual(None, self.getLib().max(None))
        self.assertEqual(None, self.getLib().max(self.makeNumberList()))

        self.assertEqual(None, self.getLib().max(self.makeNumber(1), None))
        self.assertEqual(None, self.getLib().max(self.makeNumberList(1, None, 3)))

        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().max(self.makeNumber(1), self.makeNumber(3)))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().max(self.makeNumberList(1, 2, 3)))

    def testSum(self):
        self.assertEqual(None, self.getLib().sum())
        self.assertEqual(None, self.getLib().sum(None))
        self.assertEqual(None, self.getLib().sum((self.makeNumberList())))

        self.assertEqual(None, self.getLib().sum(self.makeNumber(1), None, self.makeNumber(3)))
        self.assertEqual(None, self.getLib().sum(self.makeNumberList(1, None, 3)))

        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().sum(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().sum(self.makeNumberList(1, 2, 3)))

    #
    # Context functions
    #
    def testGetEntries(self):
        self.assertEqual(None, self.getLib().getEntries(None))
        self.assertEqual(None, self.getLib().getEntries(self.makeNumber("1")))

        self.assertEqual([], self.getLib().getEntries(Context()))
        self.assertEqual([Context().add("key", "a").add("value", self.makeNumber("1"))], self.getLib().getEntries(Context().add("a", self.makeNumber("1"))))

    def testGetValue(self):
        self.assertEqual(None, self.getLib().getValue(None, None))
        self.assertEqual(None, self.getLib().getValue(Context(), None))
        self.assertEqual(None, self.getLib().getValue(Context(), "a"))

        self.assertEqual(self.makeNumber("1"), self.getLib().getValue(Context().add("a", self.makeNumber("1")), "a"))
