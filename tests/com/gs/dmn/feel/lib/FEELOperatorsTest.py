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
from decimal import Decimal
from typing import Any
from unittest import TestCase

from com.gs.dmn.feel.lib.StandardFEELLib import StandardFEELLib


class FEELOperatorsTest(TestCase):
    #
    # Numeric operators
    #
    def testNumericValue(self):
        self.assertEqual(None, self.getLib().numericValue(None))
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
        self.assertEqual(None, self.getLib().numericLessThan(None, None))
        self.assertEqual(None, self.getLib().numericLessThan(None, self.makeNumber("1")))
        self.assertEqual(None, self.getLib().numericLessThan(self.makeNumber("1"), None))

        self.assertFalse(self.getLib().numericLessThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertTrue(self.getLib().numericLessThan(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericGreaterThan(self):
        self.assertEqual(None, self.getLib().numericGreaterThan(None, None))
        self.assertEqual(None, self.getLib().numericGreaterThan(None, self.makeNumber("1")))
        self.assertEqual(None, self.getLib().numericGreaterThan(self.makeNumber("1"), None))

        self.assertFalse(self.getLib().numericGreaterThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertTrue(self.getLib().numericGreaterThan(self.makeNumber("2"), self.makeNumber("1")))

    def testNumericLessEqualThan(self):
        self.assertTrue(self.getLib().numericLessEqualThan(None, None))
        self.assertEqual(None, self.getLib().numericLessEqualThan(None, self.makeNumber("1")))
        self.assertEqual(None, self.getLib().numericLessEqualThan(self.makeNumber("1"), None))

        self.assertTrue(self.getLib().numericLessEqualThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertFalse(self.getLib().numericLessEqualThan(self.makeNumber("2"), self.makeNumber("1")))

    def testNumericGreaterEqualThan(self):
        self.assertTrue(self.getLib().numericGreaterEqualThan(None, None))
        self.assertEqual(None, self.getLib().numericGreaterEqualThan(None, self.makeNumber("1")))
        self.assertEqual(None, self.getLib().numericGreaterEqualThan(self.makeNumber("1"), None))

        self.assertTrue(self.getLib().numericGreaterEqualThan(self.makeNumber("1"), self.makeNumber("1")))
        self.assertFalse(self.getLib().numericGreaterEqualThan(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericAdd(self):
        self.assertEqual(None, self.getLib().numericAdd(None, None))
        self.assertEqual(None, self.getLib().numericAdd(None, self.makeNumber("1")))
        self.assertEqual(None, self.getLib().numericAdd(self.makeNumber("1"), None))

        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().numericAdd(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericSubtract(self):
        self.assertEqual(None, self.getLib().numericSubtract(None, None))
        self.assertEqual(None, self.getLib().numericSubtract(None, self.makeNumber("2")))
        self.assertEqual(None, self.getLib().numericSubtract(self.makeNumber("2"), None))

        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().numericSubtract(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericMultiply(self):
        self.assertEqual(None, self.getLib().numericMultiply(None, None))
        self.assertEqual(None, self.getLib().numericMultiply(None, self.makeNumber("2")))
        self.assertEqual(None, self.getLib().numericMultiply(self.makeNumber("2"), None))

        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().numericMultiply(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericDivide(self):
        self.assertEqual(None, self.getLib().numericDivide(None, None))
        self.assertEqual(None, self.getLib().numericDivide(None, self.makeNumber("2")))
        self.assertEqual(None, self.getLib().numericDivide(self.makeNumber("2"), None))

        self.assertEqualsNumber("0.5", self.getLib().numericDivide(self.makeNumber("1"), self.makeNumber("2")))

    def testNumericUnaryMinus(self):
        self.assertEqual(None, self.getLib().numericUnaryMinus(None))

        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().numericUnaryMinus(self.makeNumber("1")))

    def testNumericExponentiation(self):
        self.assertEqual(None, self.getLib().numericExponentiation(None, None))
        self.assertEqual(None, self.getLib().numericExponentiation(None, self.makeNumber("10")))
        self.assertEqual(None, self.getLib().numericExponentiation(self.makeNumber("10"), None))

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
    # String operators
    #
    def testStringValue(self):
        self.assertEqual(None, self.getLib().stringValue(None))
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
        self.assertEqual(None, self.getLib().stringAdd(None, None))
        self.assertEqual(None, self.getLib().stringAdd("a", None))
        self.assertEqual(None, self.getLib().stringAdd(None, "b"))

        self.assertEqual("ab", self.getLib().stringAdd("a", "b"))
        self.assertEqual("ba", self.getLib().stringAdd("b", "a"))

    #
    # Boolean operators
    #
    def testBooleanValue(self):
        self.assertEqual(None, self.getLib().booleanValue(None))
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
        self.assertEqual(None, self.getLib().booleanNot(None))

        self.assertEqual(None, self.getLib().booleanNot("abc"))
        self.assertEqual(None, self.getLib().booleanNot(self.makeNumber("123")))

    def testBooleanOr(self):
        self.assertFalse(self.getLib().booleanOr(False, False))
        self.assertTrue(self.getLib().booleanOr(False, True))
        self.assertTrue(self.getLib().booleanOr(True, False))
        self.assertTrue(self.getLib().booleanOr(True, True))
        self.assertEqual(None, self.getLib().booleanOr(False, None))
        self.assertEqual(None, self.getLib().booleanOr(None, False))
        self.assertTrue(self.getLib().booleanOr(True, None))
        self.assertTrue(self.getLib().booleanOr(None, True))
        self.assertTrue(self.getLib().booleanOr(True, self.makeNumber("123")))
        self.assertTrue(self.getLib().booleanOr(self.makeNumber("123"), True))
        self.assertTrue(self.getLib().booleanOr(True, "123"))
        self.assertTrue(self.getLib().booleanOr(True, None))
        self.assertTrue(self.getLib().booleanOr(None, True))
        self.assertTrue(self.getLib().booleanOr("123", True))
        self.assertEqual(None, self.getLib().booleanOr(None, None))
        self.assertEqual(None, self.getLib().booleanOr("123", "123"))

        self.assertEqual(None, self.getLib().booleanOr(True))
        self.assertTrue(self.getLib().booleanOr(False, False, True))
        self.assertTrue(self.getLib().booleanOr([False, False, True]))
        self.assertEqual(None, self.getLib().booleanOr([[False, False, True]]))

    def testBinaryBooleanOr(self):
        self.assertFalse(self.getLib().binaryBooleanOr(False, False))
        self.assertTrue(self.getLib().binaryBooleanOr(False, True))
        self.assertTrue(self.getLib().binaryBooleanOr(True, False))
        self.assertTrue(self.getLib().binaryBooleanOr(True, True))
        self.assertEqual(None, self.getLib().binaryBooleanOr(False, None))
        self.assertEqual(None, self.getLib().binaryBooleanOr(None, False))
        self.assertTrue(self.getLib().binaryBooleanOr(True, None))
        self.assertTrue(self.getLib().binaryBooleanOr(None, True))
        self.assertTrue(self.getLib().binaryBooleanOr(True, self.makeNumber("123")))
        self.assertTrue(self.getLib().binaryBooleanOr(self.makeNumber("123"), True))
        self.assertTrue(self.getLib().binaryBooleanOr(True, "123"))
        self.assertTrue(self.getLib().binaryBooleanOr(True, None))
        self.assertTrue(self.getLib().binaryBooleanOr(None, True))
        self.assertTrue(self.getLib().binaryBooleanOr("123", True))
        self.assertEqual(None, self.getLib().binaryBooleanOr(None, None))
        self.assertEqual(None, self.getLib().binaryBooleanOr("123", "123"))

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
        self.assertEqual(None, self.getLib().booleanAnd(True, None))
        self.assertEqual(None, self.getLib().booleanAnd(None, True))
        self.assertEqual(None, self.getLib().booleanAnd(None, None))
        self.assertEqual(None, self.getLib().booleanAnd("123", "123"))

        self.assertEqual(None, self.getLib().booleanAnd(True))
        self.assertFalse(self.getLib().booleanAnd(True, True, False))
        self.assertFalse(self.getLib().booleanAnd([False, False, True]))
        self.assertEqual(None, self.getLib().booleanAnd([[False, False, True]]))

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
        self.assertEqual(None, self.getLib().binaryBooleanAnd(True, None))
        self.assertEqual(None, self.getLib().binaryBooleanAnd(None, True))
        self.assertEqual(None, self.getLib().binaryBooleanAnd(None, None))
        self.assertEqual(None, self.getLib().binaryBooleanAnd("123", "123"))

    def getLib(self) -> StandardFEELLib:
        return StandardFEELLib()

    def makeNumber(self, literal: str):
        return Decimal(literal)

    def assertEqualsNumber(self, expected: Any, actual: Decimal):
        if isinstance(expected, str):
            expected = Decimal(expected)

        return self.assertAlmostEqual(expected, actual)
