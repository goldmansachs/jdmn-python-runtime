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
from datetime import date, time, datetime, timedelta
from decimal import Decimal
from typing import Any, Optional, List
from unittest import TestCase

from isodate import Duration

from jdmn.feel.lib.BaseStandardFEELLib import BaseStandardFEELLib
from jdmn.feel.lib.DefaultStandardFEELLib import DefaultStandardFEELLib
from jdmn.runtime.Assert import Assert
from jdmn.runtime.Context import Context
from jdmn.runtime.Range import Range


class FEELOperatorsTest(TestCase):
    """
    Base test class for operators
    """
    __test__ = False

    #
    # Numeric operators
    #
    def testIsNumeric(self):
        self.assertFalse(self.getLib().isNumber(None))
        self.assertTrue(self.getLib().isNumber(self.getLib().number("1")))
        self.assertFalse(self.getLib().isNumber("abc"))
        self.assertFalse(self.getLib().isNumber(True))
        self.assertFalse(self.getLib().isNumber(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isNumber(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isNumber(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isNumber(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isNumber(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isNumber(Context()))
        self.assertFalse(self.getLib().isNumber(Range(True, 0, True, 1)))

    def testNumericValue(self):
        self.assertIsNone(self.getLib().numericValue(None))
        self.assertEqual(self.makeNumber("1"), self.getLib().numericValue(self.makeNumber("1")))

    def testNumericIs(self):
        self.assertTrue(self.getLib().numericIs(None, None))
        self.assertFalse(self.getLib().numericIs(None, self.makeNumber("1")))
        self.assertFalse(self.getLib().numericIs(self.makeNumber("1"), None))

        self.assertTrue(self.getLib().numericIs(self.makeNumber("1"), self.makeNumber("1")))
        self.assertFalse(self.getLib().numericIs(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericEqual(self):
        self.assertTrue(self.getLib().numericEqual(None, None))
        self.assertFalse(self.getLib().numericEqual(None, self.makeNumber("1")))
        self.assertFalse(self.getLib().numericEqual(self.makeNumber("1"), None))

        self.assertTrue(self.getLib().numericEqual(self.makeNumber("1"), self.makeNumber("1")))
        self.assertFalse(self.getLib().numericEqual(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericNotEqual(self):
        self.assertFalse(self.getLib().numericNotEqual(None, None))
        self.assertTrue(self.getLib().numericNotEqual(None, self.makeNumber("1")))
        self.assertTrue(self.getLib().numericNotEqual(self.makeNumber("1"), None))

        self.assertFalse(self.getLib().numericNotEqual(self.makeNumber("1"), self.makeNumber("1")))
        self.assertTrue(self.getLib().numericNotEqual(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericLessThan(self):
        self.assertIsNone(self.getLib().numericLessThan(None, None))
        self.assertIsNone(self.getLib().numericLessThan(None, self.makeNumber("1")))
        self.assertIsNone(self.getLib().numericLessThan(self.makeNumber("1"), None))

        self.assertFalse(self.getLib().numericLessThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertTrue(self.getLib().numericLessThan(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericGreaterThan(self):
        self.assertIsNone(self.getLib().numericGreaterThan(None, None))
        self.assertIsNone(self.getLib().numericGreaterThan(None, self.makeNumber("1")))
        self.assertIsNone(self.getLib().numericGreaterThan(self.makeNumber("1"), None))

        self.assertFalse(self.getLib().numericGreaterThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertTrue(self.getLib().numericGreaterThan(self.makeNumber("2"), self.makeNumber("1")))

    def testNumericLessEqualThan(self):
        self.assertTrue(self.getLib().numericLessEqualThan(None, None))
        self.assertIsNone(self.getLib().numericLessEqualThan(None, self.makeNumber("1")))
        self.assertIsNone(self.getLib().numericLessEqualThan(self.makeNumber("1"), None))

        self.assertTrue(self.getLib().numericLessEqualThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertFalse(self.getLib().numericLessEqualThan(self.makeNumber("2"), self.makeNumber("1")))

    def testNumericGreaterEqualThan(self):
        self.assertTrue(self.getLib().numericGreaterEqualThan(None, None))
        self.assertIsNone(self.getLib().numericGreaterEqualThan(None, self.makeNumber("1")))
        self.assertIsNone(self.getLib().numericGreaterEqualThan(self.makeNumber("1"), None))

        self.assertTrue(self.getLib().numericGreaterEqualThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertFalse(self.getLib().numericGreaterEqualThan(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericAdd(self):
        self.assertIsNone(self.getLib().numericAdd(None, None))
        self.assertIsNone(self.getLib().numericAdd(None, self.makeNumber("1")))
        self.assertIsNone(self.getLib().numericAdd(self.makeNumber("1"), None))

        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().numericAdd(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericSubtract(self):
        self.assertIsNone(self.getLib().numericSubtract(None, None))
        self.assertIsNone(self.getLib().numericSubtract(None, self.makeNumber("2")))
        self.assertIsNone(self.getLib().numericSubtract(self.makeNumber("2"), None))

        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().numericSubtract(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericMultiply(self):
        self.assertIsNone(self.getLib().numericMultiply(None, None))
        self.assertIsNone(self.getLib().numericMultiply(None, self.makeNumber("2")))
        self.assertIsNone(self.getLib().numericMultiply(self.makeNumber("2"), None))

        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().numericMultiply(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericDivide(self):
        self.assertIsNone(self.getLib().numericDivide(None, None))
        self.assertIsNone(self.getLib().numericDivide(None, self.makeNumber("2")))
        self.assertIsNone(self.getLib().numericDivide(self.makeNumber("2"), None))

        self.assertEqualsNumber("0.5", self.getLib().numericDivide(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericUnaryMinus(self):
        self.assertIsNone(self.getLib().numericUnaryMinus(None))

        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().numericUnaryMinus(self.makeNumber("1")))

    def testNumericExponentiation(self):
        self.assertIsNone(self.getLib().numericExponentiation(None, None))
        self.assertIsNone(self.getLib().numericExponentiation(None, self.makeNumber("10")))
        self.assertIsNone(self.getLib().numericExponentiation(self.makeNumber("10"), None))

        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().numericExponentiation(self.makeNumber("2"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("0.5"), self.getLib().numericExponentiation(self.makeNumber("2"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("1024"), self.getLib().numericExponentiation(self.makeNumber("2"), self.makeNumber("10")))

        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().numericExponentiation(self.makeNumber("3"), self.makeNumber("0")))

        self.assertEqualsNumber(self.makeNumber("1.41421356"), self.getLib().numericExponentiation(self.makeNumber("2"), self.makeNumber("0.5")))
        self.assertEqualsNumber(self.makeNumber("8"), self.getLib().numericExponentiation(self.makeNumber("2"), self.makeNumber("3")))
        self.assertEqualsNumber(self.makeNumber("11.31370849"), self.getLib().numericExponentiation(self.makeNumber("2"), self.makeNumber("3.5")))
        self.assertEqualsNumber(self.makeNumber("11.84466611"), self.getLib().numericExponentiation(self.makeNumber("3"), self.makeNumber("2.25")))
        self.assertEqualsNumber(self.makeNumber("15.58845726"), self.getLib().numericExponentiation(self.makeNumber("3"), self.makeNumber("2.5")))
        self.assertEqualsNumber(self.makeNumber("20.51556351"), self.getLib().numericExponentiation(self.makeNumber("3"), self.makeNumber("2.75")))
        self.assertEqualsNumber(self.makeNumber("1.73205080"), self.getLib().numericExponentiation(self.makeNumber("3"), self.makeNumber("0.5")))
        self.assertEqualsNumber(self.makeNumber("0.11111111"), self.getLib().numericExponentiation(self.makeNumber("3"), self.makeNumber("-2")))
        self.assertEqualsNumber(self.makeNumber("0.04874348"), self.getLib().numericExponentiation(self.makeNumber("3"), self.makeNumber("-2.75")))

    #
    # Boolean operators
    #
    def testIsBoolean(self):
        self.assertFalse(self.getLib().isBoolean(None))
        self.assertFalse(self.getLib().isBoolean(self.getLib().number("1")))
        self.assertFalse(self.getLib().isBoolean("abc"))
        self.assertTrue(self.getLib().isBoolean(True))
        self.assertFalse(self.getLib().isBoolean(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isBoolean(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isBoolean(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isBoolean(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isBoolean(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isBoolean(Context()))
        self.assertFalse(self.getLib().isBoolean(Range(True, 0, True, 1)))

    def testBooleanValue(self):
        self.assertIsNone(self.getLib().booleanValue(None))
        self.assertTrue(self.getLib().booleanValue(True))
        self.assertFalse(self.getLib().booleanValue(False))

    def testBooleanIs(self):
        self.assertTrue(self.getLib().booleanIs(None, None))
        self.assertFalse(self.getLib().booleanIs(True, None))
        self.assertFalse(self.getLib().booleanIs(None, True))

        self.assertFalse(self.getLib().booleanIs(False, True))
        self.assertTrue(self.getLib().booleanIs(True, True))

    def testBooleanEqual(self):
        self.assertTrue(self.getLib().booleanEqual(None, None))
        self.assertFalse(self.getLib().booleanEqual(True, None))
        self.assertFalse(self.getLib().booleanEqual(None, True))

        self.assertFalse(self.getLib().booleanEqual(False, True))
        self.assertTrue(self.getLib().booleanEqual(True, True))

    def testBooleanNotEqual(self):
        self.assertFalse(self.getLib().booleanNotEqual(None, None))
        self.assertTrue(self.getLib().booleanNotEqual(True, None))
        self.assertTrue(self.getLib().booleanNotEqual(None, True))

        self.assertTrue(self.getLib().booleanNotEqual(False, True))
        self.assertFalse(self.getLib().booleanNotEqual(True, True))

    def testBooleanNot(self):
        self.assertTrue(self.getLib().booleanNot(False))
        self.assertFalse(self.getLib().booleanNot(True))
        self.assertIsNone(self.getLib().booleanNot(None))

        self.assertIsNone(self.getLib().booleanNot("abc"))
        self.assertIsNone(self.getLib().booleanNot(self.makeNumber("123")))

    def testBooleanOr(self):
        self.assertFalse(self.getLib().booleanOr(False, False))
        self.assertTrue(self.getLib().booleanOr(False, True))
        self.assertTrue(self.getLib().booleanOr(True, False))
        self.assertTrue(self.getLib().booleanOr(True, True))
        self.assertIsNone(self.getLib().booleanOr(False, None))
        self.assertIsNone(self.getLib().booleanOr(None, False))
        self.assertTrue(self.getLib().booleanOr(True, None))
        self.assertTrue(self.getLib().booleanOr(None, True))
        self.assertTrue(self.getLib().booleanOr(True, self.makeNumber("123")))
        self.assertTrue(self.getLib().booleanOr(self.makeNumber("123"), True))
        self.assertTrue(self.getLib().booleanOr(True, "123"))
        self.assertTrue(self.getLib().booleanOr(True, None))
        self.assertTrue(self.getLib().booleanOr(None, True))
        self.assertTrue(self.getLib().booleanOr("123", True))
        self.assertIsNone(self.getLib().booleanOr(None, None))
        self.assertIsNone(self.getLib().booleanOr("123", "123"))

        self.assertIsNone(self.getLib().booleanOr(True))
        self.assertTrue(self.getLib().booleanOr(False, False, True))
        self.assertTrue(self.getLib().booleanOr([False, False, True]))
        self.assertIsNone(self.getLib().booleanOr([[False, False, True]]))

    def testBinaryBooleanOr(self):
        self.assertFalse(self.getLib().binaryBooleanOr(False, False))
        self.assertTrue(self.getLib().binaryBooleanOr(False, True))
        self.assertTrue(self.getLib().binaryBooleanOr(True, False))
        self.assertTrue(self.getLib().binaryBooleanOr(True, True))
        self.assertIsNone(self.getLib().binaryBooleanOr(False, None))
        self.assertIsNone(self.getLib().binaryBooleanOr(None, False))
        self.assertTrue(self.getLib().binaryBooleanOr(True, None))
        self.assertTrue(self.getLib().binaryBooleanOr(None, True))
        self.assertTrue(self.getLib().binaryBooleanOr(True, self.makeNumber("123")))
        self.assertTrue(self.getLib().binaryBooleanOr(self.makeNumber("123"), True))
        self.assertTrue(self.getLib().binaryBooleanOr(True, "123"))
        self.assertTrue(self.getLib().binaryBooleanOr(True, None))
        self.assertTrue(self.getLib().binaryBooleanOr(None, True))
        self.assertTrue(self.getLib().binaryBooleanOr("123", True))
        self.assertIsNone(self.getLib().binaryBooleanOr(None, None))
        self.assertIsNone(self.getLib().binaryBooleanOr("123", "123"))

    def testBooleanAnd(self):
        self.assertFalse(self.getLib().booleanAnd(False, False))
        self.assertFalse(self.getLib().booleanAnd(False, True))
        self.assertFalse(self.getLib().booleanAnd(True, False))
        self.assertTrue(self.getLib().booleanAnd(True, True))
        self.assertFalse(self.getLib().booleanAnd(False, None))
        self.assertFalse(self.getLib().booleanAnd(None, False))
        self.assertFalse(self.getLib().booleanAnd(False, self.makeNumber("123")))
        self.assertFalse(self.getLib().booleanAnd(self.makeNumber("123"), False))
        self.assertFalse(self.getLib().booleanAnd(False, "123"))
        self.assertFalse(self.getLib().booleanAnd(False, None))
        self.assertFalse(self.getLib().booleanAnd(None, False))
        self.assertFalse(self.getLib().booleanAnd("123", False))
        self.assertIsNone(self.getLib().booleanAnd(True, None))
        self.assertIsNone(self.getLib().booleanAnd(None, True))
        self.assertIsNone(self.getLib().booleanAnd(None, None))
        self.assertIsNone(self.getLib().booleanAnd("123", "123"))

        self.assertIsNone(self.getLib().booleanAnd(True))
        self.assertFalse(self.getLib().booleanAnd(True, True, False))
        self.assertFalse(self.getLib().booleanAnd([False, False, True]))
        self.assertIsNone(self.getLib().booleanAnd([[False, False, True]]))

    def testBinaryBooleanAnd(self):
        self.assertFalse(self.getLib().binaryBooleanAnd(False, False))
        self.assertFalse(self.getLib().binaryBooleanAnd(False, True))
        self.assertFalse(self.getLib().binaryBooleanAnd(True, False))
        self.assertTrue(self.getLib().binaryBooleanAnd(True, True))
        self.assertFalse(self.getLib().binaryBooleanAnd(False, None))
        self.assertFalse(self.getLib().binaryBooleanAnd(None, False))
        self.assertFalse(self.getLib().binaryBooleanAnd(False, self.makeNumber("123")))
        self.assertFalse(self.getLib().binaryBooleanAnd(self.makeNumber("123"), False))
        self.assertFalse(self.getLib().binaryBooleanAnd(False, "123"))
        self.assertFalse(self.getLib().binaryBooleanAnd(False, None))
        self.assertFalse(self.getLib().binaryBooleanAnd(None, False))
        self.assertFalse(self.getLib().binaryBooleanAnd("123", False))
        self.assertIsNone(self.getLib().binaryBooleanAnd(True, None))
        self.assertIsNone(self.getLib().binaryBooleanAnd(None, True))
        self.assertIsNone(self.getLib().binaryBooleanAnd(None, None))
        self.assertIsNone(self.getLib().binaryBooleanAnd("123", "123"))

    #
    # String operators
    #
    def testIsString(self):
        self.assertFalse(self.getLib().isString(None))
        self.assertFalse(self.getLib().isString(self.getLib().number("1")))
        self.assertTrue(self.getLib().isString("abc"))
        self.assertFalse(self.getLib().isString(True))
        self.assertFalse(self.getLib().isString(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isString(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isString(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isString(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isString(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isString(Context()))
        self.assertFalse(self.getLib().isString(Range(True, 0, True, 1)))

    def testStringValue(self):
        self.assertIsNone(self.getLib().stringValue(None))
        self.assertEqual("a", self.getLib().stringValue("a"))

    def testStringIs(self):
        self.assertTrue(self.getLib().stringIs(None, None))
        self.assertFalse(self.getLib().stringIs("a", None))
        self.assertFalse(self.getLib().stringIs(None, "b"))

        self.assertFalse(self.getLib().stringIs("a", "b"))
        self.assertTrue(self.getLib().stringIs("b", "b"))

    def testStringEqual(self):
        self.assertTrue(self.getLib().stringEqual(None, None))
        self.assertFalse(self.getLib().stringEqual("a", None))
        self.assertFalse(self.getLib().stringEqual(None, "b"))

        self.assertFalse(self.getLib().stringEqual("a", "b"))
        self.assertTrue(self.getLib().stringEqual("b", "b"))

    def testStringNotEqual(self):
        self.assertFalse(self.getLib().stringNotEqual(None, None))
        self.assertTrue(self.getLib().stringNotEqual("a", None))
        self.assertTrue(self.getLib().stringNotEqual(None, "b"))

        self.assertTrue(self.getLib().stringNotEqual("a", "b"))
        self.assertFalse(self.getLib().stringNotEqual("b", "b"))

    def testStringAdd(self):
        self.assertIsNone(self.getLib().stringAdd(None, None))
        self.assertIsNone(self.getLib().stringAdd("a", None))
        self.assertIsNone(self.getLib().stringAdd(None, "b"))

        self.assertEqual("ab", self.getLib().stringAdd("a", "b"))
        self.assertEqual("ba", self.getLib().stringAdd("b", "a"))

    #
    # Date operators
    #
    def testIsDate(self):
        self.assertFalse(self.getLib().isDate(None))
        self.assertFalse(self.getLib().isDate(self.getLib().number("1")))
        self.assertFalse(self.getLib().isDate("abc"))
        self.assertFalse(self.getLib().isDate(True))
        self.assertTrue(self.getLib().isDate(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isDate(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isDate(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isDate(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isDate(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isDate(Context()))
        self.assertFalse(self.getLib().isDate(Range(True, 0, True, 1)))

    def testDateValue(self):
        self.assertIsNone(self.getLib().dateValue(None))

        self.assertEqual(0, self.getLib().dateValue(self.makeDate("1970-01-01")))
        self.assertEqual(86400, self.getLib().dateValue(self.makeDate("1970-01-02")))
        self.assertEqual(2678400, self.getLib().dateValue(self.makeDate("1970-02-01")))
        self.assertEqual(946684800, self.getLib().dateValue(self.makeDate("2000-01-01")))

        # Negative dates are not supported in datetime object
        # self.assertEqual(-124334265600, self.getLib().dateValue(self.makeDate("-1970-01-02")))
        # self.assertEqual(-124331673600, self.getLib().dateValue(self.makeDate("-1970-02-01")))
        # self.assertEqual(-125281123200, self.getLib().dateValue(self.makeDate("-2000-01-01")))

    def testDateIs(self):
        self.assertTrue(self.getLib().dateIs(None, None))
        self.assertFalse(self.getLib().dateIs(None, self.makeDate("2016-08-01")))
        self.assertFalse(self.getLib().dateIs(self.makeDate("2016-08-01"), None))

        self.assertTrue(self.getLib().dateIs(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertFalse(self.getLib().dateIs(self.makeDate("2016-08-01"), self.makeDate("2016-08-02")))

    def testDateEqual(self):
        self.assertTrue(self.getLib().dateEqual(None, None))
        self.assertFalse(self.getLib().dateEqual(None, self.makeDate("2016-08-01")))
        self.assertFalse(self.getLib().dateEqual(self.makeDate("2016-08-01"), None))

        self.assertTrue(self.getLib().dateEqual(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertFalse(self.getLib().dateEqual(self.makeDate("2016-08-01"), self.makeDate("2016-08-02")))

    def testDateNotEqual(self):
        self.assertFalse(self.getLib().dateNotEqual(None, None))
        self.assertTrue(self.getLib().dateNotEqual(None, self.makeDate("2016-08-01")))
        self.assertTrue(self.getLib().dateNotEqual(self.makeDate("2016-08-01"), None))

        self.assertFalse(self.getLib().dateNotEqual(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertTrue(self.getLib().dateEqual(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))

    def testDateLessThan(self):
        self.assertIsNone(self.getLib().dateLessThan(None, None))
        self.assertIsNone(self.getLib().dateLessThan(None, self.makeDate("2016-08-01")))
        self.assertIsNone(self.getLib().dateLessThan(self.makeDate("2016-08-01"), None))

        self.assertFalse(self.getLib().dateLessThan(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertTrue(self.getLib().dateLessThan(self.makeDate("2016-08-01"), self.makeDate("2016-08-02")))

    def testDateGreaterThan(self):
        self.assertIsNone(self.getLib().dateGreaterThan(None, None))
        self.assertIsNone(self.getLib().dateGreaterThan(None, self.makeDate("2016-08-01")))
        self.assertIsNone(self.getLib().dateGreaterThan(self.makeDate("2016-08-01"), None))

        self.assertFalse(self.getLib().dateGreaterThan(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertTrue(self.getLib().dateGreaterThan(self.makeDate("2016-08-02"), self.makeDate("2016-08-01")))

    def testDateLessEqualThan(self):
        self.assertTrue(self.getLib().dateLessEqualThan(None, None))
        self.assertIsNone(self.getLib().dateLessEqualThan(None, self.makeDate("2016-08-01")))
        self.assertIsNone(self.getLib().dateLessEqualThan(self.makeDate("2016-08-01"), None))

        self.assertTrue(self.getLib().dateLessEqualThan(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertFalse(self.getLib().dateLessEqualThan(self.makeDate("2016-08-03"), self.makeDate("2016-08-02")))

    def testDateGreaterEqualThan(self):
        self.assertTrue(self.getLib().dateGreaterEqualThan(None, None))
        self.assertIsNone(self.getLib().dateGreaterEqualThan(None, self.makeDate("2016-08-01")))
        self.assertIsNone(self.getLib().dateGreaterEqualThan(self.makeDate("2016-08-01"), None))

        self.assertTrue(self.getLib().dateGreaterEqualThan(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertFalse(self.getLib().dateGreaterEqualThan(self.makeDate("2016-08-01"), self.makeDate("2016-08-03")))

    def testDateSubtract(self):
        self.assertIsNone(self.getLib().dateSubtract(None, None))
        self.assertIsNone(self.getLib().dateSubtract(None, self.makeDate("2016-08-01")))
        self.assertIsNone(self.getLib().dateSubtract(self.makeDate("2016-08-01"), None))

        self.assertEqual(self.makeDuration("PT0S"), self.getLib().dateSubtract(self.makeDate("2016-08-01"), self.makeDate("2016-08-01")))
        self.assertEqual(self.makeDuration("-P2D"), self.getLib().dateSubtract(self.makeDate("2016-08-01"), self.makeDate("2016-08-03")))

    def testDateAddDuration(self):
        self.assertIsNone(self.getLib().dateAddDuration(None, None))
        self.assertIsNone(self.getLib().dateAddDuration(None, self.makeDuration("P0Y2M")))
        self.assertIsNone(self.getLib().dateAddDuration(self.makeDate("2016-08-01"), None))

        self.assertEqualsDate("2016-10-01", self.getLib().dateAddDuration(self.makeDate("2016-08-01"), self.makeDuration("P0Y2M")))
        self.assertEqualsDate("2016-06-01", self.getLib().dateAddDuration(self.makeDate("2016-08-01"), self.makeDuration("-P0Y2M")))

    def testDateSubtractDuration(self):
        self.assertIsNone(self.getLib().dateSubtractDuration(None, None))
        self.assertIsNone(self.getLib().dateSubtractDuration(None, self.makeDuration("P0Y2M")))
        self.assertIsNone(self.getLib().dateSubtractDuration(self.makeDate("2016-08-01"), None))

        self.assertEqualsDate("2016-06-01", self.getLib().dateSubtractDuration(self.makeDate("2016-08-01"), self.makeDuration("P0Y2M")))
        self.assertEqualsDate("2016-10-01", self.getLib().dateSubtractDuration(self.makeDate("2016-08-01"), self.makeDuration("-P0Y2M")))

    #
    # Time operators
    #
    def testIsTime(self):
        self.assertFalse(self.getLib().isTime(None))
        self.assertFalse(self.getLib().isTime(self.getLib().number("1")))
        self.assertFalse(self.getLib().isTime("abc"))
        self.assertFalse(self.getLib().isTime(True))
        self.assertFalse(self.getLib().isTime(self.getLib().date("2020-01-01")))
        self.assertTrue(self.getLib().isTime(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isTime(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isTime(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isTime(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isTime(Context()))
        self.assertFalse(self.getLib().isTime(Range(True, 0, True, 1)))

    def testTimeValue(self):
        self.assertIsNone(self.getLib().timeValue(None))

        # local time
        self.assertEqual(3723, self.getLib().timeValue(self.makeTime("01:02:03")))
        self.assertEqual(3723, self.getLib().timeValue(self.makeTime("01:02:03.0004")))

        # offset time
        self.assertEqual(3723, self.getLib().timeValue(self.makeTime("01:02:03Z")))
        self.assertEqual(3723, self.getLib().timeValue(self.makeTime("01:02:03Z")))
        self.assertEqual(3723, self.getLib().timeValue(self.makeTime("01:02:03+00:00")))
        self.assertEqual(63, self.getLib().timeValue(self.makeTime("01:02:03+01:01")))

        # zoneid time
#        self.assertEqual(123, self.getLib().timeValue(self.makeTime("01:02:03@Europe/Paris")))
#        self.assertEqual(3723, self.getLib().timeValue(self.makeTime("01:02:03@Etc/UTC")))

    def testTimeIs(self):
        self.assertTrue(self.getLib().timeIs(None, None))
        self.assertFalse(self.getLib().timeIs(None, self.makeTime("12:00:00Z")))
        self.assertFalse(self.getLib().timeIs(self.makeTime("12:00:00Z"), None))

        # same times are is()
        self.assertTrue(self.getLib().timeIs(self.makeTime("10:30:00"), self.makeTime("10:30:00")))
        # different times are not is()
        self.assertFalse(self.getLib().timeIs(self.makeTime("10:30:00"), self.makeTime("10:30:01")))
        # different times with zero milliseconds are is()
        self.assertTrue(self.getLib().timeIs(self.makeTime("10:30:00.0000"), self.makeTime("10:30:00")))
        # different times with same milliseconds are is()
        self.assertTrue(self.getLib().timeIs(self.makeTime("10:30:00.0001"), self.makeTime("10:30:00.0001")))
        # different times with different milliseconds are is()
        self.assertTrue(self.getLib().timeIs(self.makeTime("10:30:00.0001"), self.makeTime("10:30:00.0002")))
        # same times in same zone are is()
#        self.assertTrue(self.getLib().timeIs(self.makeTime("10:30:00@Europe/Paris"), self.makeTime("10:30:00@Europe/Paris")))
        # same times - one with zone one without are not is()
#        self.assertFalse(self.getLib().timeIs(self.makeTime("10:30:00@Europe/Paris"), self.makeTime("10:30:00")))
        # same times with different zones are not is()
#        self.assertFalse(self.getLib().timeIs(self.makeTime("10:30:00@Europe/Paris"), self.makeTime("10:30:00@Asia/Dhaka")))
        # same times = one with offset, the other with zone are not equal
#        self.assertFalse(self.getLib().timeIs(self.makeTime("10:30:00+02:00"), self.makeTime("10:30:00@Europe/Paris")))
        # same times = one with Z zone, the other with UTC are is()
#        self.assertTrue(self.getLib().timeIs(self.makeTime("10:30:00Z"), self.makeTime("10:30:00+00:00")))

    def testTimeEqual(self):
        self.assertTrue(self.getLib().timeEqual(None, None))
        self.assertFalse(self.getLib().timeEqual(None, self.makeTime("12:00:00Z")))
        self.assertFalse(self.getLib().timeEqual(self.makeTime("12:00:00Z"), None))

        # same times are equal
        self.assertTrue(self.getLib().timeEqual(self.makeTime("10:30:00"), self.makeTime("10:30:00")))
        # different times are not equal
        self.assertFalse(self.getLib().timeEqual(self.makeTime("10:30:00"), self.makeTime("10:30:01")))
        # same times with zero milliseconds are equal
        self.assertTrue(self.getLib().timeEqual(self.makeTime("10:30:00.0000"), self.makeTime("10:30:00")))
        # same times with same milliseconds are equal
        self.assertTrue(self.getLib().timeEqual(self.makeTime("10:30:00.0001"), self.makeTime("10:30:00.0001")))
        # same times with different milliseconds are equal
        self.assertTrue(self.getLib().timeEqual(self.makeTime("10:30:00.0001"), self.makeTime("10:30:00.0002")))
        # same times in same zone are equal
#        self.assertTrue(self.getLib().timeEqual(self.makeTime("10:30:00@Europe/Paris"), self.makeTime("10:30:00@Europe/Paris")))
        # same times - one with zone one without are not equal
#        self.assertFalse(self.getLib().timeEqual(self.makeTime("10:30:00@Europe/Paris"), self.makeTime("10:30:00")))
        # same times with different zones are not equal
#        self.assertFalse(self.getLib().timeEqual(self.makeTime("10:30:00@Europe/Paris"), self.makeTime("10:30:00@Asia/Dhaka")))
        # same times = one with offset, the other with zone are not equal
#        self.assertFalse(self.getLib().timeEqual(self.makeTime("10:30:00+02:00"), self.makeTime("10:30:00@Europe/Paris")))
        # same times = one with Z zone, the other with UTC are equal
        self.assertTrue(self.getLib().timeEqual(self.makeTime("10:30:00Z"), self.makeTime("10:30:00+00:00")))

        # times with equivalent offset and zone id are equal
        self.assertTrue(self.getLib().timeEqual(self.makeTime("12:00:00"), self.makeTime("12:00:00+00:00")))
#        self.assertTrue(self.getLib().timeEqual(self.makeTime("00:00:00+00:00"), self.makeTime("00:00:00@Etc/UTC")))
        self.assertTrue(self.getLib().timeEqual(self.makeTime("00:00:00Z"), self.makeTime("00:00:00+00:00")))
#        self.assertTrue(self.getLib().timeEqual(self.makeTime("00:00:00Z"), self.makeTime("00:00:00@Etc/UTC")))

    def testTimeNotEqual(self):
        self.assertFalse(self.getLib().timeNotEqual(None, None))
        self.assertTrue(self.getLib().timeNotEqual(None, self.makeTime("12:00:00Z")))
        self.assertTrue(self.getLib().timeNotEqual(self.makeTime("12:00:00Z"), None))

        self.assertFalse(self.getLib().timeNotEqual(self.makeTime("12:00:00Z"), self.makeTime("12:00:00Z")))
        self.assertTrue(self.getLib().timeNotEqual(self.makeTime("12:00:00Z"), self.makeTime("12:00:01Z")))

    def testTimeLessThan(self):
        self.assertIsNone(self.getLib().timeLessThan(None, None))
        self.assertIsNone(self.getLib().timeLessThan(None, self.makeTime("12:00:00Z")))
        self.assertIsNone(self.getLib().timeLessThan(self.makeTime("12:00:00Z"), None))

        self.assertFalse(self.getLib().timeLessThan(self.makeTime("12:00:00Z"), self.makeTime("12:00:00Z")))
        self.assertTrue(self.getLib().timeLessThan(self.makeTime("11:00:00Z"), self.makeTime("12:00:01Z")))

    def testTimeGreaterThan(self):
        self.assertIsNone(self.getLib().timeGreaterThan(None, None))
        self.assertIsNone(self.getLib().timeGreaterThan(None, self.makeTime("12:00:00Z")))
        self.assertIsNone(self.getLib().timeGreaterThan(self.makeTime("12:00:00Z"), None))

        self.assertFalse(self.getLib().timeGreaterThan(self.makeTime("12:00:00Z"), self.makeTime("12:00:00Z")))
        self.assertTrue(self.getLib().timeGreaterThan(self.makeTime("13:00:00Z"), self.makeTime("12:00:01Z")))

    def testTimeLessEqualThan(self):
        self.assertTrue(self.getLib().timeLessEqualThan(None, None))
        self.assertIsNone(self.getLib().timeLessEqualThan(None, self.makeTime("12:00:00Z")))
        self.assertIsNone(self.getLib().timeLessEqualThan(self.makeTime("12:00:00Z"), None))

        self.assertTrue(self.getLib().timeLessEqualThan(self.makeTime("12:00:00Z"), self.makeTime("12:00:00Z")))
        self.assertFalse(self.getLib().timeLessEqualThan(self.makeTime("13:00:00Z"), self.makeTime("12:00:01Z")))

    def testTimeGreaterEqualThan(self):
        self.assertTrue(self.getLib().timeGreaterEqualThan(None, None))
        self.assertIsNone(self.getLib().timeGreaterEqualThan(None, self.makeTime("12:00:00Z")))
        self.assertIsNone(self.getLib().timeGreaterEqualThan(self.makeTime("12:00:00Z"), None))

        self.assertTrue(self.getLib().timeGreaterEqualThan(self.makeTime("12:00:00Z"), self.makeTime("12:00:00Z")))
        self.assertFalse(self.getLib().timeGreaterEqualThan(self.makeTime("11:00:00Z"), self.makeTime("12:00:01Z")))

    def testTimeSubtract(self):
        self.assertIsNone(self.getLib().timeSubtract(None, None))
        self.assertIsNone(self.getLib().timeSubtract(None, self.makeTime("12:00:00Z")))
        self.assertIsNone(self.getLib().timeSubtract(self.makeTime("12:00:00Z"), None))

        self.assertEqual(self.makeDuration("PT1H"), self.getLib().timeSubtract(self.makeTime("13:00:00Z"), self.makeTime("12:00:00Z")))
        self.assertEqual(self.makeDuration("P0D"), self.getLib().timeSubtract(self.makeTime("12:00:00Z"), self.makeTime("12:00:00Z")))
        self.assertEqual(self.makeDuration("-PT1H"), self.getLib().timeSubtract(self.makeTime("12:00:00Z"), self.makeTime("13:00:00Z")))

    def testTimeAddDuration(self):
        self.assertIsNone(self.getLib().timeAddDuration(None, None))
        self.assertIsNone(self.getLib().timeAddDuration(None, self.makeDuration("P0DT1H")))
        self.assertIsNone(self.getLib().timeAddDuration(self.makeTime("12:00:00Z"), None))

        self.assertEqualsTime("13:00:01Z", self.getLib().timeAddDuration(self.makeTime("12:00:01Z"), self.makeDuration("P0DT1H")))
        self.assertEqualsTime("12:00:01Z", self.getLib().timeAddDuration(self.makeTime("12:00:01Z"), self.makeDuration("P1DT0H")))

    def testTimeSubtractDuration(self):
        self.assertIsNone(self.getLib().timeSubtractDuration(None, None))
        self.assertIsNone(self.getLib().timeSubtractDuration(None, self.makeDuration("P0DT1H")))
        self.assertIsNone(self.getLib().timeSubtractDuration(self.makeTime("12:00:01Z"), None))

        self.assertEqualsTime("11:00:01Z", self.getLib().timeSubtractDuration(self.makeTime("12:00:01Z"), self.makeDuration("P0DT1H")))
        self.assertEqualsTime("12:00:01Z", self.getLib().timeSubtractDuration(self.makeTime("12:00:01Z"), self.makeDuration("P1DT0H")))

    #
    # Date and time operators
    #
    def testIsDateTime(self):
        self.assertFalse(self.getLib().isDateTime(None))
        self.assertFalse(self.getLib().isDateTime(self.getLib().number("1")))
        self.assertFalse(self.getLib().isDateTime("abc"))
        self.assertFalse(self.getLib().isDateTime(True))
        self.assertFalse(self.getLib().isDateTime(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isDateTime(self.getLib().time("12:00:00")))
        self.assertTrue(self.getLib().isDateTime(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isDateTime(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isDateTime(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isDateTime(Context()))
        self.assertFalse(self.getLib().isDateTime(Range(True, 0, True, 1)))

    def testDateTimeValue(self):
        self.assertIsNone(self.getLib().dateTimeValue(None))

        # local date time
        self.assertEqual(3723, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03")))
        self.assertEqual(3723, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03.0004")))
        self.assertEqual(315536523, self.getLib().dateTimeValue(self.makeDateAndTime("1980-01-01T01:02:03.0004")))
#        self.assertEqual(-124649967477, self.getLib().dateTimeValue(self.makeDateAndTime("-1980-01-01T01:02:03.0004")))

        # offset date time
        self.assertEqual(3723, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03Z")))
        self.assertEqual(3723, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03Z")))
        self.assertEqual(3723, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03+00:00")))
        self.assertEqual(63, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03+01:01")))
        self.assertEqual(315532863, self.getLib().dateTimeValue(self.makeDateAndTime("1980-01-01T01:02:03+01:01")))
#        self.assertEqual(-124649971137, self.getLib().dateTimeValue(self.makeDateAndTime("-1980-01-01T01:02:03+01:01")))

        # zoneid date time
#        self.assertEqual(123, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03@Europe/Paris")))
#        self.assertEqual(3723, self.getLib().dateTimeValue(self.makeDateAndTime("1970-01-01T01:02:03@Etc/UTC")))
#        self.assertEqual(315536523, self.getLib().dateTimeValue(self.makeDateAndTime("1980-01-01T01:02:03@Etc/UTC")))
#        self.assertEqual(-124649967477, self.getLib().dateTimeValue(self.makeDateAndTime("-1980-01-01T01:02:03@Etc/UTC")))

    def testDateTimeIs(self):
        # datetime equals None
        self.assertTrue(self.getLib().dateTimeIs(None, None))
        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00"), None))
        self.assertFalse(self.getLib().dateTimeIs(None, self.makeDateAndTime("2018-12-08T00:00:00")))

        self.assertTrue(self.getLib().dateTimeIs(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:01Z")))

        # same datetimes are is ()
        self.assertTrue(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T10:30:00"), self.makeDateAndTime("2018-12-08T10:30:00")))
        # datetimes with no time is is () to datetime with zero time
        self.assertTrue(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08"), self.makeDateAndTime("2018-12-08T00:00:00")))
        # datetimes with same milliseconds are is ()
        self.assertTrue(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00.0001"), self.makeDateAndTime("2018-12-08T00:00:00.0001")))
        # datetimes with different milliseconds are is ()
        self.assertTrue(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00.0001"), self.makeDateAndTime("2018-12-08T00:00:00.0002")))
        # different datetimes are not is ()
        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00"), self.makeDateAndTime("2018-12-07T00:00:00")))
        # same datetimes in same zone are is ()
#        self.assertTrue(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris"), self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris")))
        # same datetimes in different zones are not is ()
#        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris"), self.makeDateAndTime("2018-12-08T00:00:00@Asia/Dhaka")))
        # same datetimes, one with zone one without are not is ()
#        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00"), self.makeDateAndTime("2018-12-08T00:00:00@Asia/Dhaka")))
        # same datetimes, one with offset and the other with zone are not is ()
#        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00+02:00"), self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris")))

    def testDateTimeEqual(self):
        # datetime equals None
        self.assertTrue(self.getLib().dateTimeEqual(None, None))
        self.assertFalse(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00"), None))
        self.assertFalse(self.getLib().dateTimeEqual(None, self.makeDateAndTime("2018-12-08T00:00:00")))

        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertFalse(self.getLib().dateTimeEqual(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:01Z")))

        # same datetimes are equal
        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T10:30:00"), self.makeDateAndTime("2018-12-08T10:30:00")))
        # datetimes with no time is equal to datetime with zero time
        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08"), self.makeDateAndTime("2018-12-08T00:00:00")))
        # datetimes with same milliseconds are equal
        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00.0001"), self.makeDateAndTime("2018-12-08T00:00:00.0001")))
        # datetimes with different milliseconds are equal
        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00.0001"), self.makeDateAndTime("2018-12-08T00:00:00.0002")))
        # different datetimes are not equal
        self.assertFalse(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00"), self.makeDateAndTime("2018-12-07T00:00:00")))
        # same datetimes in same zone are equal
#        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris"), self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris")))
        # same datetimes in different zones are not equal
#        self.assertFalse(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris"), self.makeDateAndTime("2018-12-08T00:00:00@Asia/Dhaka")))
        # same datetimes, one with zone one without are not equal
#        self.assertFalse(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00"), self.makeDateAndTime("2018-12-08T00:00:00@Asia/Dhaka")))
        # same datetimes, one with offset and the other with zone are not equal
#        self.assertFalse(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00+02:00"), self.makeDateAndTime("2018-12-08T00:00:00@Europe/Paris")))

        # datetime with equivalent offset and zone id are equal
#        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00+00:00"), self.makeDateAndTime("2018-12-08T00:00:00@Etc/UTC")))
        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T12:00:00Z"), self.makeDateAndTime("2018-12-08T12:00:00+00:00")))
#        self.assertTrue(self.getLib().dateTimeEqual(self.makeDateAndTime("2018-12-08T00:00:00Z"), self.makeDateAndTime("2018-12-08T00:00:00@Etc/UTC")))

    def testDateTimeNotEqual(self):
        self.assertFalse(self.getLib().dateTimeNotEqual(None, None))
        self.assertTrue(self.getLib().dateTimeNotEqual(None, self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertTrue(self.getLib().dateTimeNotEqual(self.makeDateAndTime("2016-08-01T11:00:00Z"), None))

        self.assertFalse(self.getLib().dateTimeNotEqual(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertTrue(self.getLib().dateTimeNotEqual(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:01Z")))

    def testDateTimeLessThan(self):
        self.assertIsNone(self.getLib().dateTimeLessThan(None, None))
        self.assertIsNone(self.getLib().dateTimeLessThan(None, self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertIsNone(self.getLib().dateTimeLessThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), None))

        self.assertFalse(self.getLib().dateTimeLessThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertTrue(self.getLib().dateTimeLessThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2017-08-01T11:00:01Z")))

    def testDateTimeGreaterThan(self):
        self.assertIsNone(self.getLib().dateTimeGreaterThan(None, None))
        self.assertIsNone(self.getLib().dateTimeGreaterThan(None, self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertIsNone(self.getLib().dateTimeGreaterThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), None))

        self.assertTrue(self.getLib().dateTimeGreaterThan(self.makeDateAndTime("2017-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertFalse(self.getLib().dateTimeGreaterThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:01Z")))

    def testDateTimeLessEqualThan(self):
        self.assertTrue(self.getLib().dateTimeLessEqualThan(None, None))
        self.assertIsNone(self.getLib().dateTimeLessEqualThan(None, self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertIsNone(self.getLib().dateTimeLessEqualThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), None))

        self.assertTrue(self.getLib().dateTimeLessEqualThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertFalse(self.getLib().dateTimeLessEqualThan(self.makeDateAndTime("2016-08-01T11:00:01Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))

    def testDateTimeGreaterEqualThan(self):
        self.assertTrue(self.getLib().dateTimeGreaterEqualThan(None, None))
        self.assertIsNone(self.getLib().dateTimeGreaterEqualThan(None, self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertIsNone(self.getLib().dateTimeGreaterEqualThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), None))

        self.assertTrue(self.getLib().dateTimeGreaterEqualThan(self.makeDateAndTime("2016-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:00Z")))
        self.assertFalse(self.getLib().dateTimeGreaterEqualThan(self.makeDateAndTime("2015-08-01T11:00:00Z"), self.makeDateAndTime("2016-08-01T11:00:01Z")))

    def testDateTimeSubtract(self):
        self.assertIsNone(self.getLib().dateTimeSubtract(None, None))
        self.assertIsNone(self.getLib().dateTimeSubtract(None, self.makeDateAndTime("2016-08-01T12:00:00Z")))
        self.assertIsNone(self.getLib().dateTimeSubtract(self.makeDateAndTime("2016-08-01T12:00:00Z"), None))

        self.assertEqual(self.makeDuration("PT1H"), self.getLib().dateTimeSubtract(self.makeDateAndTime("2016-08-01T13:00:00Z"), self.makeDateAndTime("2016-08-01T12:00:00Z")))
        self.assertEqual(self.makeDuration("PT0S"), self.getLib().dateTimeSubtract(self.makeDateAndTime("2016-08-01T12:00:00Z"), self.makeDateAndTime("2016-08-01T12:00:00Z")))
        self.assertEqual(self.makeDuration("-P2DT1H"), self.getLib().dateTimeSubtract(self.makeDateAndTime("2016-08-01T12:00:00Z"), self.makeDateAndTime("2016-08-03T13:00:00Z")))

    def testDateTimeAddDuration(self):
        self.assertIsNone(self.getLib().dateTimeAddDuration(None, None))
        self.assertIsNone(self.getLib().dateTimeAddDuration(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().dateTimeAddDuration(self.makeDateAndTime("2016-08-01T12:00:00Z"), None))

        self.assertEqualsDateTime("2017-03-01T12:00:01Z", self.getLib().dateTimeAddDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("P1Y1M")))
        self.assertEqualsDateTime("2015-01-01T12:00:01Z", self.getLib().dateTimeAddDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("-P1Y1M")))

        self.assertEqualsDateTime("2016-02-02T13:00:01Z", self.getLib().dateTimeAddDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("P1DT1H")))
        self.assertEqualsDateTime("2016-01-31T11:00:01Z", self.getLib().dateTimeAddDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("-P1DT1H")))

    def testDateTimeSubtractDuration(self):
        self.assertIsNone(self.getLib().dateTimeSubtractDuration(None, None))
        self.assertIsNone(self.getLib().dateTimeSubtractDuration(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().dateTimeSubtractDuration(self.makeDateAndTime("2016-08-01T12:00:00Z"), None))

        self.assertEqualsDateTime("2015-01-01T12:00:01Z", self.getLib().dateTimeSubtractDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("P1Y1M")))
        self.assertEqualsDateTime("2017-03-01T12:00:01Z", self.getLib().dateTimeSubtractDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("-P1Y1M")))

        self.assertEqualsDateTime("2016-01-31T11:00:01Z", self.getLib().dateTimeSubtractDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("P1DT1H")))
        self.assertEqualsDateTime("2016-02-02T13:00:01Z", self.getLib().dateTimeSubtractDuration(self.makeDateAndTime("2016-02-01T12:00:01Z"), self.makeDuration("-P1DT1H")))

    #
    # Duration operators
    #
    def testIsDuration(self):
        self.assertFalse(self.getLib().isDuration(None))

        # years and months
        self.assertTrue(self.getLib().isYearsAndMonthsDuration(self.makeDuration("P1Y2M")))
        self.assertTrue(self.getLib().isYearsAndMonthsDuration(self.makeDuration("-P1Y2M")))

        # days and time
        self.assertTrue(self.getLib().isDaysAndTimeDuration(self.makeDuration("P1DT2H3M4S")))
        self.assertTrue(self.getLib().isDaysAndTimeDuration(self.makeDuration("-P1DT2H3M4S")))

        # mixture
        self.assertTrue(self.getLib().isDuration(self.makeDuration("P1Y2M1DT2H3M4S")))
        self.assertTrue(self.getLib().isDuration(self.makeDuration("-P1Y2M1DT2H3M4S")))

    def testDurationValue(self):
        self.assertIsNone(self.getLib().durationValue(None))

        # years and months
        self.assertEqual(12 + 2, self.getLib().durationValue(self.makeDuration("P1Y2M")))
        self.assertEqual(-(12 + 2), self.getLib().durationValue(self.makeDuration("-P1Y2M")))

        # days and time
        self.assertEqual((24 + 2) * 3600 + 3 * 60 + 4, self.getLib().durationValue(self.makeDuration("P1DT2H3M4S")))
        self.assertEqual(- ((24 + 2) * 3600 + 3 * 60 + 4), self.getLib().durationValue(self.makeDuration("-P1DT2H3M4S")))

        # mixture
        self.assertEqual(36727384, self.getLib().durationValue(self.makeDuration("P1Y2M1DT2H3M4S")))
#        self.assertEqual(-36727384, self.getLib().durationValue(self.makeDuration("-P1Y2M1DT2H3M4S")))

    def testDurationIs(self):
        self.assertTrue(self.getLib().durationIs(None, None))
        self.assertFalse(self.getLib().durationIs(None, self.makeDuration("P1Y1M")))
        self.assertFalse(self.getLib().durationIs(self.makeDuration("P1Y1M"), None))

        self.assertTrue(self.getLib().durationIs(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertTrue(self.getLib().durationIs(self.makeDuration("P1Y1M"), self.makeDuration("P0Y13M")))
        self.assertFalse(self.getLib().durationIs(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertTrue(self.getLib().durationIs(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertTrue(self.getLib().durationIs(self.makeDuration("P1DT1H"), self.makeDuration("P0DT25H")))
        self.assertFalse(self.getLib().durationIs(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

        # different semantic domains
        # both are timedelta
#        self.assertFalse(self.getLib().durationIs(self.makeDuration("P0Y"), self.makeDuration("P0D")))

    def testDurationEqual(self):
        self.assertTrue(self.getLib().durationEqual(None, None))
        self.assertFalse(self.getLib().durationEqual(None, self.makeDuration("P1Y1M")))
        self.assertFalse(self.getLib().durationEqual(self.makeDuration("P1Y1M"), None))

        self.assertTrue(self.getLib().durationEqual(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertTrue(self.getLib().durationEqual(self.makeDuration("P1Y1M"), self.makeDuration("P0Y13M")))
        self.assertFalse(self.getLib().durationEqual(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertTrue(self.getLib().durationEqual(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertTrue(self.getLib().durationEqual(self.makeDuration("P1DT1H"), self.makeDuration("P0DT25H")))
        self.assertFalse(self.getLib().durationEqual(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationNotEqual(self):
        self.assertFalse(self.getLib().durationNotEqual(None, None))
        self.assertTrue(self.getLib().durationNotEqual(None, self.makeDuration("P1Y1M")))
        self.assertTrue(self.getLib().durationNotEqual(self.makeDuration("P1Y1M"), None))

        self.assertFalse(self.getLib().durationNotEqual(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertFalse(self.getLib().durationNotEqual(self.makeDuration("P1Y1M"), self.makeDuration("P0Y13M")))
        self.assertTrue(self.getLib().durationNotEqual(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertFalse(self.getLib().durationNotEqual(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertFalse(self.getLib().durationNotEqual(self.makeDuration("P1DT1H"), self.makeDuration("P0DT25H")))
        self.assertTrue(self.getLib().durationNotEqual(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationLessThan(self):
        self.assertIsNone(self.getLib().durationLessThan(None, None))
        self.assertIsNone(self.getLib().durationLessThan(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().durationLessThan(self.makeDuration("P1Y1M"), None))

        self.assertFalse(self.getLib().durationLessThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertFalse(self.getLib().durationLessThan(self.makeDuration("P1Y1M"), self.makeDuration("P0Y13M")))
        self.assertTrue(self.getLib().durationLessThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertFalse(self.getLib().durationLessThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertFalse(self.getLib().durationLessThan(self.makeDuration("P1DT1H"), self.makeDuration("P0DT25H")))
        self.assertTrue(self.getLib().durationLessThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationGreaterThan(self):
        self.assertIsNone(self.getLib().durationGreaterThan(None, None))
        self.assertIsNone(self.getLib().durationGreaterThan(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().durationGreaterThan(self.makeDuration("P1Y1M"), None))

        self.assertFalse(self.getLib().durationGreaterThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertFalse(self.getLib().durationGreaterThan(self.makeDuration("P1Y1M"), self.makeDuration("P0Y13M")))
        self.assertFalse(self.getLib().durationGreaterThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertFalse(self.getLib().durationGreaterThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertFalse(self.getLib().durationGreaterThan(self.makeDuration("P1DT1H"), self.makeDuration("P0DT25H")))
        self.assertFalse(self.getLib().durationGreaterThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationLessEqualThan(self):
        self.assertTrue(self.getLib().durationLessEqualThan(None, None))
        self.assertIsNone(self.getLib().durationLessEqualThan(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().durationLessEqualThan(self.makeDuration("P1Y1M"), None))

        self.assertTrue(self.getLib().durationLessEqualThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertTrue(self.getLib().durationLessEqualThan(self.makeDuration("P1Y1M"), self.makeDuration("P0Y13M")))
        self.assertTrue(self.getLib().durationLessEqualThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertTrue(self.getLib().durationLessEqualThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertTrue(self.getLib().durationLessEqualThan(self.makeDuration("P1DT1H"), self.makeDuration("P0DT25H")))
        self.assertTrue(self.getLib().durationLessEqualThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationGreaterEqualThan(self):
        self.assertTrue(self.getLib().durationGreaterEqualThan(None, None))
        self.assertIsNone(self.getLib().durationGreaterEqualThan(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().durationGreaterEqualThan(self.makeDuration("P1Y1M"), None))

        self.assertTrue(self.getLib().durationGreaterEqualThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertTrue(self.getLib().durationGreaterEqualThan(self.makeDuration("P1Y1M"), self.makeDuration("P0Y13M")))
        self.assertFalse(self.getLib().durationGreaterEqualThan(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertTrue(self.getLib().durationGreaterEqualThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertTrue(self.getLib().durationGreaterEqualThan(self.makeDuration("P1DT1H"), self.makeDuration("P0DT25H")))
        self.assertFalse(self.getLib().durationGreaterEqualThan(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationAdd(self):
        self.assertIsNone(self.getLib().durationAdd(None, None))
        self.assertIsNone(self.getLib().durationAdd(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().durationAdd(self.makeDuration("P1Y1M"), None))

        self.assertEqual(self.makeDuration("P2Y2M"), self.getLib().durationAdd(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertEqual(self.makeDuration("P2Y3M"), self.getLib().durationAdd(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertEqual(self.makeDuration("P2DT2H"), self.getLib().durationAdd(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertEqual(self.makeDuration("P2DT3H"), self.getLib().durationAdd(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationSubtract(self):
        self.assertIsNone(self.getLib().durationSubtract(None, None))
        self.assertIsNone(self.getLib().durationSubtract(None, self.makeDuration("P1Y1M")))
        self.assertIsNone(self.getLib().durationSubtract(self.makeDuration("P1Y1M"), None))

        self.assertEqual(self.makeDuration("P0Y0M"), self.getLib().durationSubtract(self.makeDuration("P1Y1M"), self.makeDuration("P1Y1M")))
        self.assertEqual(self.makeDuration("-P0Y1M"), self.getLib().durationSubtract(self.makeDuration("P1Y1M"), self.makeDuration("P1Y2M")))

        self.assertEqual(self.makeDuration("P0DT0H"), self.getLib().durationSubtract(self.makeDuration("P1DT1H"), self.makeDuration("P1DT1H")))
        self.assertEqual(self.makeDuration("-P0DT1H"), self.getLib().durationSubtract(self.makeDuration("P1DT1H"), self.makeDuration("P1DT2H")))

    def testDurationMultiply(self):
        self.assertIsNone(self.getLib().durationMultiplyNumber(None, None))
        self.assertIsNone(self.getLib().durationMultiplyNumber(None, self.makeNumber("2")))
        self.assertIsNone(self.getLib().durationMultiplyNumber(self.makeDuration("P1Y1M"), None))

        self.assertEqual(self.makeDuration("P2Y2M"), self.getLib().durationMultiplyNumber(self.makeDuration("P1Y1M"), self.makeNumber("2")))
        self.assertEqual(self.makeDuration("-P2Y2M"), self.getLib().durationMultiplyNumber(self.makeDuration("P1Y1M"), self.makeNumber("-2")))

        self.assertEqual(self.makeDuration("P2DT2H"), self.getLib().durationMultiplyNumber(self.makeDuration("P1DT1H"), self.makeNumber("2")))
        self.assertEqual(self.makeDuration("-P2DT2H"), self.getLib().durationMultiplyNumber(self.makeDuration("P1DT1H"), self.makeNumber("-2")))

    def testDurationDivide(self):
        self.assertIsNone(self.getLib().durationDivideNumber(None, None))
        self.assertIsNone(self.getLib().durationDivideNumber(None, self.makeNumber("2")))
        self.assertIsNone(self.getLib().durationDivideNumber(self.makeDuration("P1Y1M"), None))

        self.assertEqual(self.makeDuration("P0Y6M"), self.getLib().durationDivideNumber(self.makeDuration("P1Y1M"), self.makeNumber("2")))
        self.assertEqual(self.makeDuration("P1Y1M"), self.getLib().durationDivideNumber(self.makeDuration("P2Y2M"), self.makeNumber("2")))

        self.assertEqual(self.makeDuration("P0DT12H30M"), self.getLib().durationDivideNumber(self.makeDuration("P1DT1H"), self.makeNumber("2")))
        self.assertEqual(self.makeDuration("P1DT1H"), self.getLib().durationDivideNumber(self.makeDuration("P2DT2H"), self.makeNumber("2")))

    #
    # List operators
    #
    def testIsList(self):
        self.assertFalse(self.getLib().isList(None))
        self.assertFalse(self.getLib().isList(self.getLib().number("1")))
        self.assertFalse(self.getLib().isList("abc"))
        self.assertFalse(self.getLib().isList(True))
        self.assertFalse(self.getLib().isList(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isList(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isList(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isList(self.getLib().duration("P1Y1M")))
        self.assertTrue(self.getLib().isList(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isList(Context()))
        self.assertFalse(self.getLib().isList(Range(True, 0, True, 1)))

    def testListIs(self):
        self.assertTrue(self.getLib().listIs(None, None))
        self.assertFalse(self.getLib().listIs(self.makeList("a"), None))
        self.assertFalse(self.getLib().listIs(None, self.makeList("a")))

        self.assertFalse(self.getLib().listIs(self.makeList("a"), self.makeList("b")))
        self.assertTrue(self.getLib().listIs(self.makeList("a"), self.makeList("a")))

    def testListEqual(self):
        self.assertTrue(self.getLib().listEqual(None, None))
        self.assertFalse(self.getLib().listEqual(self.makeList("a"), None))
        self.assertFalse(self.getLib().listEqual(None, self.makeList("a")))

        self.assertFalse(self.getLib().listEqual(self.makeList("a"), self.makeList("b")))
        self.assertTrue(self.getLib().listEqual(self.makeList("a"), self.makeList("a")))

    def testListNotEqual(self):
        self.assertFalse(self.getLib().listNotEqual(None, None))
        self.assertTrue(self.getLib().listNotEqual(self.makeList("a"), None))
        self.assertTrue(self.getLib().listNotEqual(None, self.makeList("a")))

        self.assertTrue(self.getLib().listNotEqual(self.makeList("a"), self.makeList("b")))
        self.assertFalse(self.getLib().listNotEqual(self.makeList("a"), self.makeList("a")))

    #
    # Context operators
    #
    def testIsContext(self):
        self.assertFalse(self.getLib().isContext(None))
        self.assertFalse(self.getLib().isContext(self.getLib().number("1")))
        self.assertFalse(self.getLib().isContext("abc"))
        self.assertFalse(self.getLib().isContext(True))
        self.assertFalse(self.getLib().isContext(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isContext(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isContext(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isContext(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isContext(self.getLib().asList("a")))
        self.assertTrue(self.getLib().isContext(Context()))
        self.assertFalse(self.getLib().isContext(Range(True, 0, True, 1)))

    def testContextValue(self):
        c1 = Context()

        self.assertIsNone(self.getLib().contextValue(None))
        self.assertIsNone(self.getLib().contextValue(self.getLib().number("123")))
        self.assertEqual(c1, self.getLib().contextValue(c1))

    def testContextIs(self):
        c1 = Context().add("m", "a")
        c2 = Context().add("m", "b")
        c3 = Context().add("m", "a")

        self.assertTrue(self.getLib().contextIs(None, None))
        self.assertFalse(self.getLib().contextIs(c1, None))
        self.assertFalse(self.getLib().contextIs(None, c1))

        self.assertTrue(self.getLib().contextIs(c1, c1))
        self.assertFalse(self.getLib().contextIs(c1, c2))
        self.assertTrue(self.getLib().contextIs(c1, c3))

    def testContextEqual(self):
        c1 = Context().add("m", "a")
        c2 = Context().add("m", "b")
        c3 = Context().add("m", "a")

        self.assertTrue(self.getLib().contextEqual(None, None))
        self.assertFalse(self.getLib().contextEqual(c1, None))
        self.assertFalse(self.getLib().contextEqual(None, c1))

        self.assertFalse(self.getLib().contextEqual(c1, c2))
        self.assertTrue(self.getLib().contextEqual(c1, c3))

    def testContextNotEqual(self):
        c1 = Context().add("m", "a")
        c2 = Context().add("m", "b")
        c3 = Context().add("m", "a")

        self.assertFalse(self.getLib().contextNotEqual(None, None))
        self.assertTrue(self.getLib().contextNotEqual(c1, None))
        self.assertTrue(self.getLib().contextNotEqual(None, c1))

        self.assertTrue(self.getLib().contextNotEqual(c1, c2))
        self.assertFalse(self.getLib().contextNotEqual(c1, c3))

    #
    # Range operators
    #
    def testIsRange(self):
        self.assertFalse(self.getLib().isRange(None))
        self.assertFalse(self.getLib().isRange(self.getLib().number("1")))
        self.assertFalse(self.getLib().isRange("abc"))
        self.assertFalse(self.getLib().isRange(True))
        self.assertFalse(self.getLib().isRange(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isRange(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isRange(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isRange(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isRange(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isRange(Context()))
        self.assertTrue(self.getLib().isRange(Range(True, 0, True, 1)))

    def testRangeValue(self):
        r1 = Range(True, self.getLib().number("1"), True, self.getLib().number("2"))

        self.assertIsNone(self.getLib().rangeValue(None))
        self.assertEqual(r1, self.getLib().rangeValue(r1))

    def testRangeIs(self):
        r1 = Range(True, self.getLib().number("1"), True, self.getLib().number("2"))
        r2 = Range(True, self.getLib().number("1"), True, self.getLib().number("3"))
        r3 = Range(True, self.getLib().number("1"), True, self.getLib().number("2"))

        self.assertTrue(self.getLib().rangeIs(None, None))
        self.assertFalse(self.getLib().rangeIs(r1, None))
        self.assertFalse(self.getLib().rangeIs(None, r1))

        self.assertTrue(self.getLib().rangeIs(r1, r1))
        self.assertFalse(self.getLib().rangeIs(r1, r2))
        self.assertTrue(self.getLib().rangeIs(r1, r3))

    def testRangeEqual(self):
        r1 = Range(True, self.getLib().number("1"), True, self.getLib().number("2"))
        r2 = Range(True, self.getLib().number("1"), True, self.getLib().number("3"))
        r3 = Range(True, self.getLib().number("1"), True, self.getLib().number("2"))

        self.assertTrue(self.getLib().rangeEqual(None, None))
        self.assertFalse(self.getLib().rangeEqual(r1, None))
        self.assertFalse(self.getLib().rangeEqual(None, r1))

        self.assertFalse(self.getLib().rangeEqual(r1, r2))
        self.assertTrue(self.getLib().rangeEqual(r1, r3))

    def testRangeNotEqual(self):
        r1 = Range(True, self.getLib().number("1"), True, self.getLib().number("2"))
        r2 = Range(True, self.getLib().number("1"), True, self.getLib().number("3"))
        r3 = Range(True, self.getLib().number("1"), True, self.getLib().number("2"))

        self.assertFalse(self.getLib().rangeNotEqual(None, None))
        self.assertTrue(self.getLib().rangeNotEqual(r1, None))
        self.assertTrue(self.getLib().rangeNotEqual(None, r1))

        self.assertTrue(self.getLib().rangeNotEqual(r1, r2))
        self.assertFalse(self.getLib().rangeNotEqual(r1, r3))

    #
    # Function operators
    #
    def testIsFunction(self):
        self.assertTrue(self.getLib().isFunction(None))
        self.assertFalse(self.getLib().isFunction(self.getLib().number("1")))
        self.assertFalse(self.getLib().isFunction("abc"))
        self.assertFalse(self.getLib().isFunction(True))
        self.assertFalse(self.getLib().isFunction(self.getLib().date("2020-01-01")))
        self.assertFalse(self.getLib().isFunction(self.getLib().time("12:00:00")))
        self.assertFalse(self.getLib().isFunction(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isFunction(self.getLib().dateAndTime("2020-01-01T12:00:00")))
        self.assertFalse(self.getLib().isFunction(self.getLib().duration("P1Y1M")))
        self.assertFalse(self.getLib().isFunction(self.getLib().asList("a")))
        self.assertFalse(self.getLib().isFunction(Context()))
        self.assertFalse(self.getLib().isFunction(Range(True, 0, True, 1)))

    def testFunctionValue(self):
        self.assertIsNone(self.getLib().functionValue(None))
        self.assertIsNone(self.getLib().functionValue("a"))

    def testFunctionIs(self):
        self.assertTrue(self.getLib().functionIs(None, None))
        self.assertIsNone(self.getLib().functionIs("a", None))
        self.assertIsNone(self.getLib().functionIs(None, "b"))

        self.assertIsNone(self.getLib().functionIs("a", "b"))
        self.assertIsNone(self.getLib().functionIs("b", "b"))

    def testFunctionEqual(self):
        self.assertTrue(self.getLib().functionEqual(None, None))
        self.assertIsNone(self.getLib().functionEqual("a", None))
        self.assertIsNone(self.getLib().functionEqual(None, "b"))

        self.assertIsNone(self.getLib().functionEqual("a", "b"))
        self.assertIsNone(self.getLib().functionEqual("b", "b"))

    def testFunctionNotEqual(self):
        self.assertFalse(self.getLib().functionNotEqual(None, None))
        self.assertIsNone(self.getLib().functionNotEqual("a", None))
        self.assertIsNone(self.getLib().functionNotEqual(None, "b"))

        self.assertIsNone(self.getLib().functionNotEqual("a", "b"))
        self.assertIsNone(self.getLib().functionNotEqual("b", "b"))

    #
    # Common
    #
    def getLib(self) -> BaseStandardFEELLib:
        return DefaultStandardFEELLib()

    def makeNumber(self, literal: Any) -> Decimal:
        return self.getLib().number(literal)

    def makeNumberList(self, *numbers):
        return [self.makeNumber(str(n)) for n in numbers]

    def makeDate(self, literal: str) -> date:
        return self.getLib().date(literal)

    def makeTime(self, literal: str) -> time:
        return self.getLib().time(literal)

    def makeDateAndTime(self, literal: str) -> datetime:
        return self.getLib().dateAndTime(literal)

    def makeDuration(self, literal: str) -> Duration:
        return self.getLib().duration(literal)

    @staticmethod
    def makeList(*args) -> List[Any]:
        return [x for x in args]

    def assertEqualsNumber(self, expected: Any, actual: Any, delta: float = None):
        if isinstance(expected, str):
            expected = self.makeNumber(expected)

        return self.assertAlmostEqual(expected, actual, delta=delta)

    def assertEqualsDate(self, expected: Any, actual: Optional[date]):
        if isinstance(expected, str):
            expected = self.makeDate(expected)

        return expected == actual

    def assertEqualsTime(self, expected: Any, actual: Optional[time]):
        if isinstance(expected, str):
            expected = self.makeTime(expected)

        return expected == actual

    def assertEqualsDateTime(self, expected: Any, actual: Optional[datetime]):
        if isinstance(actual, date):
            expected = self.makeDateAndTime(expected)
        elif isinstance(actual, Duration):
            expected = self.makeDuration(expected)
        elif isinstance(actual, timedelta):
            expected = self.makeDuration(expected)

        return expected == actual

    def assertEqualsList(self, expected: Any, actual: Any):
        Assert().assertEquals(expected, str(actual))
