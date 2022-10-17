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
    __test__ = False

    #
    # Conversion functions
    #
    def testNumber(self):
        self.assertIsNone(self.getLib().number(None))
        self.assertIsNone(self.getLib().number("1,200.56"))
        self.assertIsNone(self.getLib().number("xxx"))

        self.assertEqualsNumber("123.56", self.getLib().number("123.56"))
        self.assertEqualsNumber("-123.56", self.getLib().number("-123.56"))

    def testDate(self):
        #
        # conversion from string
        #
        self.assertIsNone(self.getLib().date(None))
        self.assertIsNone(self.getLib().date(""))
        self.assertIsNone(self.getLib().date(""))
        self.assertIsNone(self.getLib().date("xxx"))
        self.assertIsNone(self.getLib().date("2012-12-25T"))
        self.assertIsNone(self.getLib().date("2012/12/25"))
        self.assertIsNone(self.getLib().date("0000-12-25T"))
        self.assertIsNone(self.getLib().date("2017-13-10"))
        self.assertIsNone(self.getLib().date("998-12-31"))
        self.assertIsNone(self.getLib().date("01211-12-31"))
        self.assertIsNone(self.getLib().date("+2012-12-02"))
        self.assertIsNone(self.getLib().date("2017-08-25T11:00:00"))

        # year must be in the range [-999,999,999..999,999,999].
#        self.assertEqualsDateTime("999999999-10-11", self.getLib().date(self.getLib().date("999999999-10-11")))
#        self.assertEqualsDateTime("-999999999-10-11", self.getLib().date(self.getLib().date("-999999999-10-11")))
#        self.assertIsNone(self.getLib().date(self.getLib().date("9999999991-10-11")))
#        self.assertIsNone(self.getLib().date(self.getLib().date("-9999999991-10-11")))

        self.assertEqualsDateTime("2016-08-01", self.getLib().date("2016-08-01"))

        #
        # conversion from date
        #
        self.assertIsNone(self.getLib().date(None))
        self.assertEqualsDateTime("2016-08-01", self.getLib().date(self.makeDate("2016-08-01")))

        #
        # conversion from numbers
        #
        self.assertIsNone(self.getLib().date(None, None, None))
        self.assertIsNone(self.getLib().date(self.makeNumber("2016"), None, None))
        self.assertIsNone(self.getLib().date(None, self.makeNumber("8"), None))
        self.assertIsNone(self.getLib().date(None, None, self.makeNumber("1")))
        self.assertEqualsDateTime("2016-08-01", self.getLib().date(self.makeNumber("2016"), self.makeNumber("8"), self.makeNumber("1")))

    def testTime(self):
        #
        # conversion from string
        #
        self.assertIsNone(self.getLib().time(None))
        self.assertIsNone(self.getLib().time(""))
        self.assertIsNone(self.getLib().time("xxx"))
        self.assertIsNone(self.getLib().time("13:20:00+01:00@Europe/Paris"))
        self.assertIsNone(self.getLib().time("13:20:00+00:00@UTC"))
        self.assertIsNone(self.getLib().time("07:1:00"))
        self.assertIsNone(self.getLib().time("13:20:00@xyz/abc"))
        self.assertIsNone(self.getLib().time("13:20:00+5:00"))
        self.assertIsNone(self.getLib().time("13:20:00+5"))
        self.assertIsNone(self.getLib().time("07:2"))
        self.assertIsNone(self.getLib().time("11:30:00T"))
        self.assertIsNone(self.getLib().time("2012T-12-2511:00:00Z"))

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
        self.assertIsNone(self.getLib().time(None, None, None, None))

        self.assertIsNone(self.getLib().time(
            self.makeNumber("12"), self.makeNumber("00"), self.makeNumber("00"),
            self.makeDuration("PT25H10M")))
        self.assertEqualsDateTime("12:00:00+01:10", self.getLib().time(
            self.makeNumber("12"), self.makeNumber("00"), self.makeNumber("00"),
            self.makeDuration("PT1H10M")))

    def testDateAndTime(self):
        #
        # conversion from string
        #
        self.assertIsNone(self.getLib().dateAndTime(None))
        self.assertIsNone(self.getLib().dateAndTime(""))
        self.assertIsNone(self.getLib().dateAndTime("xxx"))
        self.assertIsNone(self.getLib().dateAndTime("11:00:00"))
        self.assertIsNone(self.getLib().dateAndTime("2011-12-03T10:15:30+01:00@Europe/Paris"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T12:20:00+19:00"))
        self.assertIsNone(self.getLib().dateAndTime("2011-12-0310:15:30"))
        self.assertIsNone(self.getLib().dateAndTime("2017-00-10T11:22:33"))
        self.assertIsNone(self.getLib().dateAndTime("998-12-31T11:22:33"))
        self.assertIsNone(self.getLib().dateAndTime("01211-12-31T11:22:33"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T07:1:00"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T07:01:2"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T13:20:00@xyz/abc"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T13:20:00+05:0"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T13:20:00+5:00"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T13:20:00+5"))
        self.assertIsNone(self.getLib().dateAndTime("2017-12-31T07:2"))

        # fix input literal
        self.assertEqualsDateTime("2016-08-01T11:00:00+01:00", self.getLib().dateAndTime("2016-08-01T11:00:00+0100"))

        self.assertEqualsDateTime("2016-08-01T11:00:00Z", self.getLib().dateAndTime("2016-08-01T11:00:00Z"))
        self.assertEqualsDateTime("2016-08-01T11:00:00.001Z", self.getLib().dateAndTime("2016-08-01T11:00:00.001Z"))
        self.assertEqualsDateTime("2016-08-01T11:00:00.001+01:00", self.getLib().dateAndTime("2016-08-01T11:00:00.001+01:00"))
        self.assertEqualsDateTime("2016-08-01T11:00:00+01:00", self.getLib().dateAndTime("2016-08-01T11:00:00+01:00"))

        #
        # conversion from date and time
        #
        self.assertIsNone(self.getLib().dateAndTime(None, None))
        self.assertIsNone(self.getLib().dateAndTime(None, self.makeTime("11:00:00Z")))
        self.assertIsNone(self.getLib().dateAndTime(self.getLib().date("2016-08-01"), None))

        self.assertEqualsDateTime("2016-08-01T11:00:00Z", self.getLib().dateAndTime(self.makeDate("2016-08-01"), self.makeTime("11:00:00Z")))

    def testDuration(self):
        self.assertIsNone(self.getLib().duration("XXX"))
        self.assertIsNone(self.getLib().duration(None))

        self.assertEqualsDateTime("P1Y8M", self.getLib().duration("P1Y8M"))
        self.assertEqualsDateTime("P2DT20H", self.getLib().duration("P2DT20H"))

    #
    # Implicit conversion functions
    #
    def testAsList(self):
        self.assertEqualsList("[None]", self.getLib().asList(None))
        self.assertEqual([], self.getLib().asList())
        self.assertEqual([None, "a"], self.getLib().asList(None, "a"))

    def testAsElement(self):
        self.assertIsNone(self.getLib().asElement(None))
        self.assertIsNone(self.getLib().asElement([]))
        self.assertIsNone(None, self.getLib().asElement(["1", "2"]))

        self.assertEqual("1", self.getLib().asElement(["1"]))

    #
    # Error conversions
    #
    def testToNull(self):
        self.assertIsNone(self.getLib().toNull(None))
        self.assertIsNone(self.getLib().toNull([]))
        self.assertIsNone(self.getLib().toNull(["1", "2"]))

        self.assertIsNone(self.getLib().toNull(["1"]))

    #
    # Extra conversion functions
    #
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
        self.assertIsNone(self.getLib().toDate(None))
        self.assertIsNone(self.getLib().toDate("1"))
        self.assertIsNone(self.getLib().toDate(self.makeNumber("1")))
        self.assertIsNone(self.getLib().toDate(self.makeTime("12:00:00Z")))

        self.assertEqualsDateTime("2016-08-01", self.getLib().toDate(self.makeDate("2016-08-01")))
        self.assertEqualsDateTime("2016-08-01", self.getLib().toDate(self.makeDateAndTime("2016-08-01T12:00:00Z")))

    def testToTime(self):
        self.assertIsNone(self.getLib().toTime(None))
        self.assertIsNone(self.getLib().toTime("1"))
        self.assertIsNone(self.getLib().toTime(self.makeNumber("1")))

        self.assertEqualsDateTime("00:00:00Z", self.getLib().toTime(self.makeDate("2016-08-01")))
        self.assertEqualsDateTime("12:00:00Z", self.getLib().toTime(self.makeTime("12:00:00Z")))
        self.assertEqualsDateTime("12:00:00Z", self.getLib().toTime(self.makeDateAndTime("2016-08-01T12:00:00Z")))

    def testToDateTime(self):
        self.assertIsNone(self.getLib().toDateTime(None))
        self.assertIsNone(self.getLib().toDateTime("1"))
        self.assertIsNone(self.getLib().toDateTime(self.makeNumber("1")))
        self.assertIsNone(self.getLib().toDateTime(self.makeTime("12:00:00Z")))

    #
    # Boolean functions
    #
    def testAnd(self):
        self.assertIsNone(self.getLib().and_(None))
        self.assertTrue(self.getLib().and_([]))
        self.assertIsNone(self.getLib().and_([None, None]))
        self.assertFalse(self.getLib().and_([None, False]))
        self.assertIsNone(self.getLib().and_([None, True]))
        self.assertTrue(self.getLib().and_([True, True]))
        self.assertFalse(self.getLib().and_([True, True, False]))

        self.assertTrue(self.getLib().and_())
        self.assertIsNone(self.getLib().and_(None, None))
        self.assertFalse(self.getLib().and_(None, False))
        self.assertIsNone(self.getLib().and_(None, True))
        self.assertTrue(self.getLib().and_(True, True))
        self.assertFalse(self.getLib().and_(True, True, False))

    def testOr(self):
        self.assertIsNone(self.getLib().or_(None))
        self.assertFalse(self.getLib().or_([]))
        self.assertIsNone(self.getLib().or_([None, None]))
        self.assertIsNone(self.getLib().or_([None, False]))
        self.assertTrue(self.getLib().or_([None, True]))
        self.assertTrue(self.getLib().or_([False, True]))
        self.assertTrue(self.getLib().or_([True, True]))
        self.assertFalse(self.getLib().or_([False, False, False]))

        self.assertFalse(self.getLib().or_())
        self.assertIsNone(self.getLib().or_(None, None))
        self.assertIsNone(self.getLib().or_(None, False))
        self.assertTrue(self.getLib().or_(None, True))
        self.assertTrue(self.getLib().or_(False, True))
        self.assertTrue(self.getLib().or_(True, True))
        self.assertFalse(self.getLib().or_(False, False, False))

    #
    # List functions
    #
    def testElementAt(self):
        self.assertIsNone(self.getLib().elementAt(None, self.makeNumber("1")))
        self.assertIsNone(self.getLib().elementAt(["1", "2", "3"], self.makeNumber("4")))
        self.assertIsNone(self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-4")))
        self.assertIsNone(self.getLib().elementAt(["1", "2", "3"], self.makeNumber("0")))

        self.assertEqual("1", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("1")))
        self.assertEqual("2", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("2")))
        self.assertEqual("3", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("3")))
        self.assertEqual("3", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-1")))
        self.assertEqual("2", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-2")))
        self.assertEqual("1", self.getLib().elementAt(["1", "2", "3"], self.makeNumber("-3")))

    def testListContains(self):
        self.assertIsNone(self.getLib().listContains(None, self.makeNumber(2)))
        self.assertIsNone(self.getLib().listContains(None, self.makeNumber(2)))

        self.assertEqual(False, self.getLib().listContains(self.makeNumberList(1, 2, 3), None))
        self.assertEqual(True, self.getLib().listContains(self.makeNumberList(1, 2, 3), self.makeNumber(2)))

    def testFlattenFirstLevel(self):
        self.assertIsNone(self.getLib().flattenFirstLevel(None))

        self.assertEqual([], self.getLib().flattenFirstLevel([]))
        self.assertEqual(["l11", "l12", "l13"], self.getLib().flattenFirstLevel(["l11", "l12", "l13"]))
        self.assertEqual(["l11", "l21", "l22", "l13"], self.getLib().flattenFirstLevel(["l11", ["l21", "l22"], "l13"]))
        self.assertEqual(["l11", "l21", ["l31", "l32"], "l13"], self.getLib().flattenFirstLevel(["l11", ["l21", ["l31", "l32"]], "l13"]))

        self.assertEqual(["l11", None, [None, "l32"], "l13"], self.getLib().flattenFirstLevel(["l11", [None, [None, "l32"]], "l13"]))

    def testCount(self):
        self.assertEqualsNumber(self.makeNumber("0"), self.getLib().count(None))
        self.assertEqualsNumber(self.makeNumber("0"), self.getLib().count(self.makeNumberList()))

        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().count(self.makeNumberList(1, 2, 3)))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().count(self.makeNumberList(1, None, 3)))

    def testMin(self):
        self.assertIsNone(self.getLib().min(None))
        self.assertIsNone(self.getLib().min(self.makeNumberList()))
        self.assertIsNone(self.getLib().min(self.makeNumberList(1, None, 3)))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().min(self.makeNumberList(1, 2, 3)))

        self.assertIsNone(self.getLib().min())
        self.assertIsNone(self.getLib().min(self.makeNumber(1), None, self.makeNumber(3)))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().min(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))

    def testMax(self):
        self.assertIsNone(self.getLib().max(None))
        self.assertIsNone(self.getLib().max(self.makeNumberList()))
        self.assertIsNone(self.getLib().max(self.makeNumberList(1, None, 3)))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().max(self.makeNumberList(1, 2, 3)))

        self.assertIsNone(self.getLib().max())
        self.assertIsNone(self.getLib().max(self.makeNumber(1), None))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().max(self.makeNumber(1), self.makeNumber(3)))

    def testSum(self):
        self.assertIsNone(self.getLib().sum(None))
        self.assertIsNone(self.getLib().sum((self.makeNumberList())))
        self.assertIsNone(self.getLib().sum(self.makeNumberList(1, None, 3)))
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().sum(self.makeNumberList(1, 2, 3)))

        self.assertIsNone(self.getLib().sum())
        self.assertIsNone(self.getLib().sum(self.makeNumber(1), None, self.makeNumber(3)))
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().sum(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))

    #
    # Context functions
    #
    def testGetEntries(self):
        self.assertIsNone(self.getLib().getEntries(None))
        self.assertIsNone(self.getLib().getEntries(self.makeNumber("1")))

        self.assertEqual([], self.getLib().getEntries(Context()))
        self.assertEqual([Context().add("key", "a").add("value", self.makeNumber("1"))], self.getLib().getEntries(Context().add("a", self.makeNumber("1"))))

    def testGetValue(self):
        self.assertIsNone(self.getLib().getValue(None, None))
        self.assertIsNone(self.getLib().getValue(Context(), None))
        self.assertIsNone(self.getLib().getValue(Context(), "a"))

        self.assertEqual(self.makeNumber("1"), self.getLib().getValue(Context().add("a", self.makeNumber("1")), "a"))
