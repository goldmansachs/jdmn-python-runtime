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
import datetime
from decimal import Decimal
from typing import Any
from unittest import TestCase

import isodate

from jdmn.runtime import DMNType
from jdmn.runtime.Context import Context
from jdmn.runtime.DMNRuntimeException import DMNRuntimeException


class Assert(TestCase):
    NUMBER_COMPARISON_PRECISION = 0.00000001

    def assertEquals(self, expected: Any, actual: Any, message: str = "") -> None:
        if expected is None:
            self.assertEqual(expected, actual, message)
        elif self.isNumber(expected):
            expectedBD = self.normalizeNumber(expected)
            actualBD = self.normalizeNumber(actual)
            if actual is None:
                self.assertEqual(expected, actual, message)
            else:
                condition = abs(expectedBD - actualBD) < self.NUMBER_COMPARISON_PRECISION
                self.assertTrue(condition, (message + ". Expected '{0}' found '{1}'").format(expectedBD, actualBD))
        elif self.isBoolean(expected):
            self.assertEqual(expected, actual, message)
        elif self.isString(expected):
            self.assertEqual(self.normalizeString(expected), self.normalizeString(actual), message)
        elif self.isDateTimeValue(expected):
            self.assertEqual(self.normalizeDateTime(expected), self.normalizeDateTime(actual), message)
        elif self.isList(expected):
            if actual is None:
                self.assertEqual(expected, actual, message)
            else:
                if message is None:
                    message = ""
                self.assertEqual(len(expected), len(actual), message + str(expected) + " vs " + str(actual))
                for i, exp in enumerate(expected):
                    self.assertEquals(exp, actual[i], message)
        elif self.isContext(expected):
            if actual is None:
                actual = Context()
            keySet = expected.getBindings().keys()
            for key in keySet:
                expectedMember = expected.get(key)
                actualMember = actual.get(key)
                self.assertEquals(expectedMember, actualMember, message + " for member '{0}'".format(key))
        elif self.isComplex(expected):
            for propertyName, expectedProperty in expected.__dict__.items():
                try:
                    actualProperty = getattr(actual, propertyName)
                    self.assertEquals(expectedProperty, actualProperty, message)
                except Exception as e:
                    raise DMNRuntimeException("Error in '{}.{}'".format(type(expected), str(propertyName)), e)
        else:
            self.assertEqual(expected, actual, message)

    def isNumber(self, obj: Any) -> bool:
        return isinstance(obj, Decimal)

    def isString(self, obj: Any) -> bool:
        return isinstance(obj, str)

    def isBoolean(self, obj: Any) -> bool:
        return isinstance(obj, bool)

    def isDate(self, obj: Any) -> bool:
        return isinstance(obj, datetime.date)

    def isTime(self, obj: Any) -> bool:
        return isinstance(obj, datetime.time)

    def isDateTime(self, obj: Any) -> bool:
        return isinstance(obj, datetime.datetime)

    def isDuration(self, obj: Any) -> bool:
        return isinstance(obj, isodate.Duration) or isinstance(obj, datetime.timedelta)

    def isDateTimeValue(self, obj: Any) -> bool:
        return self.isDate(obj) \
               or self.isTime(obj) \
               or self.isDateTime(obj) \
               or self.isDuration(obj)

    def isList(self, obj: Any) -> bool:
        return isinstance(obj, list)

    def isContext(self, obj: Any) -> bool:
        return isinstance(obj, Context)

    def isComplex(self, obj: Any) -> bool:
        return isinstance(obj, DMNType.DMNType)

    def normalizeDateTime(self, obj: Any) -> Any:
        if obj is None:
            return None
        return obj

    def normalizeNumber(self, obj: Any) -> Any:
        if obj is None:
            return None
        if isinstance(obj, str):
            return float(obj)
        else:
            return obj

    @staticmethod
    def normalizeString(string):
        # Replace surrogate pairs with equivalent
        if string is None:
            return None

        # Roundtrip to utf-16 to replace surrogate pairs
        utf16bytes = string.encode('utf-16', 'surrogatepass')
        utf16chars = utf16bytes.decode('utf-16')
        utf8 = utf16chars.encode('utf-8').decode('utf-8')
        return utf8
