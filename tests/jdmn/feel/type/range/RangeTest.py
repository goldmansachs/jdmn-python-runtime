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

from jdmn.runtime.Range import Range

from jdmn.runtime.DMNRuntimeException import DMNRuntimeException

from src.jdmn.feel.lib.type.numeric.DefaultNumericLib import DefaultNumericLib


class RangeTest(TestCase):
    """
    Base test class for Range
    """

    def testDefaultConstructor(self):
        r = Range()
        self.assertFalse(r.startIncluded)
        self.assertIsNone(r.start)
        self.assertFalse(r.endIncluded)
        self.assertIsNone(r.end)
        self.assertIsNone(r.operator)

    def testConstructorWithEndpoints(self):
        r = Range(True, self.makeNumber(3), False, self.makeNumber(4))
        self.assertTrue(r.startIncluded)
        self.assertEqual(3, r.start)
        self.assertFalse(r.endIncluded)
        self.assertEqual(4, r.end)
        self.assertIsNone(r.operator)

    def testConstructorWithEqualOperator(self):
        r = Range("=", self.makeNumber(4))
        self.assertTrue(r.startIncluded)
        self.assertEqual(4, r.start)
        self.assertTrue(r.endIncluded)
        self.assertEqual(4, r.end)
        self.assertEqual("=", r.operator)

    def testConstructorWithNullOperator(self):
        r = Range(None, self.makeNumber(4))
        self.assertTrue(r.startIncluded)
        self.assertEqual(4, r.start)
        self.assertTrue(r.endIncluded)
        self.assertEqual(4, r.end)
        self.assertEqual("=", r.operator)

    def testConstructorWithEmptyOperator(self):
        r = Range("  ", self.makeNumber(4))
        self.assertTrue(r.startIncluded)
        self.assertEqual(4, r.start)
        self.assertTrue(r.endIncluded)
        self.assertEqual(4, r.end)
        self.assertEqual("=", r.operator)

    def testConstructorWithNotEqualOperator(self):
        r = Range("!=", self.makeNumber(4))
        self.assertFalse(r.startIncluded)
        self.assertIsNone(r.start)
        self.assertFalse(r.endIncluded)
        self.assertIsNone(r.end)
        self.assertEqual("!=", r.operator)

    def testConstructorWithLessOperator(self):
        r = Range("<", self.makeNumber(4))
        self.assertFalse(r.startIncluded)
        self.assertIsNone(r.start)
        self.assertFalse(r.endIncluded)
        self.assertEqual(4, r.end)
        self.assertEqual("<", r.operator)

    def testConstructorWithLessEqualOperator(self):
        r = Range("<=", self.makeNumber(4))
        self.assertFalse(r.startIncluded)
        self.assertIsNone(r.start)
        self.assertTrue(r.endIncluded)
        self.assertEqual(4, r.end)
        self.assertEqual("<=", r.operator)

    def testConstructorWithGreaterOperator(self):
        r = Range(">", self.makeNumber(4))
        self.assertFalse(r.startIncluded)
        self.assertEqual(4, r.start)
        self.assertFalse(r.endIncluded)
        self.assertIsNone(r.end)
        self.assertEqual(">", r.operator)

    def testConstructorWithGreaterEqualOperator(self):
        r = Range(">=", self.makeNumber(4))
        self.assertTrue(r.startIncluded)
        self.assertEqual(4, r.start)
        self.assertFalse(r.endIncluded)
        self.assertIsNone(r.end)
        self.assertEqual(">=", r.operator)

    def testConstructorWithIncorrectEndpoints(self):
        with self.assertRaises(DMNRuntimeException):
            Range(True, self.makeNumber(4), False, self.makeNumber(3))

    def testConstructorWithIncorrectOperator(self):
        with self.assertRaises(DMNRuntimeException):
            Range("abc", 4)

    def testConstructorWithIncorrectEndpointOperator(self):
        with self.assertRaises(DMNRuntimeException):
            Range("=", 4)

    @staticmethod
    def makeNumber(number: int):
        return DefaultNumericLib.number(str(number))
