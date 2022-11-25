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
                self.assertTrue(condition, (message + f". Expected '{expectedBD}' found '{actualBD}'"))
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
                self.assertEquals(expectedMember, actualMember, message + f" for member '{key}'")
        elif self.isComplex(expected):
            for propertyName, expectedProperty in expected.__dict__.items():
                try:
                    actualProperty = getattr(actual, propertyName)
                    self.assertEquals(expectedProperty, actualProperty, message)
                except Exception as e:
                    raise DMNRuntimeException(f"Error in '{type(expected)}.{str(propertyName)}'", e)
        else:
            self.assertEqual(expected, actual, message)

    @staticmethod
    def isNumber(obj: Any) -> bool:
        return isinstance(obj, Decimal)

    @staticmethod
    def isString(obj: Any) -> bool:
        return isinstance(obj, str)

    @staticmethod
    def isBoolean(obj: Any) -> bool:
        return isinstance(obj, bool)

    @staticmethod
    def isDate(obj: Any) -> bool:
        return isinstance(obj, datetime.date)

    @staticmethod
    def isTime(obj: Any) -> bool:
        return isinstance(obj, datetime.time)

    @staticmethod
    def isDateTime(obj: Any) -> bool:
        return isinstance(obj, datetime.datetime)

    @staticmethod
    def isDuration(obj: Any) -> bool:
        return isinstance(obj, (isodate.Duration, datetime.timedelta))

    def isDateTimeValue(self, obj: Any) -> bool:
        return self.isDate(obj) \
               or self.isTime(obj) \
               or self.isDateTime(obj) \
               or self.isDuration(obj)

    @staticmethod
    def isList(obj: Any) -> bool:
        return isinstance(obj, list)

    @staticmethod
    def isContext(obj: Any) -> bool:
        return isinstance(obj, Context)

    @staticmethod
    def isComplex(obj: Any) -> bool:
        return isinstance(obj, DMNType.DMNType)

    @staticmethod
    def normalizeDateTime(obj: Any) -> Any:
        if obj is None:
            return None
        return obj

    @staticmethod
    def normalizeNumber(obj: Any) -> Any:
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
