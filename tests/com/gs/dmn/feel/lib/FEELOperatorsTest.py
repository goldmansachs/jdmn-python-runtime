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

from com.gs.dmn.feel.lib.StandardFEELLib import StandardFEELLib


class FEELOperatorsTest(TestCase):

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

    def getLib(self) -> StandardFEELLib:
        return StandardFEELLib()
