#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
import re
from zoneinfo import ZoneInfo

from datetime import datetime, date, time
from typing import Optional, Any

from lxml import etree
import elementpath

from jdmn.feel.lib.Types import STRING, BOOLEAN, INT, LIST, NUMBER, TIME_OR_DATE_TIME


class DefaultStringLib:
    def string(self, from_: Any) -> STRING:
        if isinstance(from_, datetime):
            return self.print(from_)
        elif isinstance(from_, date):
            return from_.isoformat()
        elif isinstance(from_, time):
            return self.print(from_)

        return str(from_)

    def print(self, from_: TIME_OR_DATE_TIME) -> str:
        tz = from_.tzinfo
        if isinstance(tz, ZoneInfo):
            copy = from_
            copy = copy.replace(tzinfo=None)
            isoformat = copy.isoformat()
            return "{}@{}".format(isoformat, str(tz))
        else:
            return from_.isoformat()

    def contains(self, string: STRING, match: STRING) -> BOOLEAN:
        if string is None or match is None:
            return None

        return match in string

    def startsWith(self, string: Optional[str], match: Optional[str]) -> Optional[bool]:
        if string is None or match is None:
            return None

        return string.startswith(match)

    def endsWith(self, string: STRING, match: STRING) -> BOOLEAN:
        if string is None or match is None:
            return None

        return string.endswith(match)

    def stringLength(self, string: STRING) -> INT:
        if string is None:
            return None

        # The number of Unicode code units in the string
        bytes = string.encode('utf-16', 'surrogatepass')
        # The number of characters (Unicode code point)
        transformed = bytes.decode('utf-16')
        result = len(transformed)
        return result

    def substring(self, string: STRING, startPosition: NUMBER, length: NUMBER) -> STRING:
        if string is None or startPosition is None:
            return None

        start = int(startPosition)
        if start < 0:
            start = len(string) + start
        else:
            start -= 1

        normal = self.normalizeSurrogatePairs(string)
        end = len(normal) if length is None else start + int(length)
        result = self.substringCodePoints(normal, start, end)
        return result

    def upperCase(self, string: STRING) -> STRING:
        if string is None:
            return None

        return string.upper()

    def lowerCase(self, string: STRING) -> STRING:
        if string is None:
            return None

        return string.lower()

    def substringBefore(self, string: STRING, match: STRING) -> STRING:
        if string is None or match is None:
            return None

        i = string.find(match)
        return "" if i == -1 else string[0:i]

    def substringAfter(self, string: STRING, match: STRING) -> STRING:
        if string is None or match is None:
            return None

        i = string.find(match)
        return "" if i == -1 else string[i + len(match):]

    def replace(self, input: STRING, pattern: STRING, replacement: STRING, flags: STRING) -> STRING:
        if input is None or pattern is None or replacement is None:
            return None
        if flags is None:
            flags = ""

        expression = "replace(/root, '{}', '{}', '{}')".format(pattern, replacement, flags)
        return self.evaluateXPath(input, expression)

    def matches(self, input: STRING, pattern: STRING, flags: STRING) -> BOOLEAN:
        if input is None or pattern is None:
            return None
        if flags is None:
            flags = ""

        expression = "/root[matches(., '{}', '{}')]".format(pattern, flags)
        value = self.evaluateXPath(input, expression)
        return len(value) != 0

    def split(self, string: STRING, delimiter: STRING) -> LIST:
        if string is None or delimiter is None:
            return None
        if string.strip() == "" or delimiter.strip() == "":
            return None

        result = []
        pattern = re.compile(delimiter)
        start = 0
        for match in re.finditer(pattern, string):
            delimiterStart = match.start()
            delimiterEnd = match.end()
            token = string[start:delimiterStart]
            result.append(token)
            start = delimiterEnd
        if start <= len(string):
            token = string[start:]
            result.append(token)
        return result

    @staticmethod
    def evaluateXPath(input, expression):
        # Read document
        xmlStr = "<root>" + input + "</root>"
        root = etree.fromstring(xmlStr)

        # Evaluate xpath
        res1 = elementpath.select(root, expression)
        return res1

    @staticmethod
    def normalizeSurrogatePairs(string):
        if string is None:
            return None

        # Roundtrip to utf-16 to replace surrogate pairs
        utf16bytes = string.encode('utf-16', 'surrogatepass')
        utf16chars = utf16bytes.decode('utf-16')
        utf8 = utf16chars.encode('utf-8').decode('utf-8')
        return utf8

    @staticmethod
    def substringCodePoints(string, start: int, end: int) -> str:
        result = ""
        cps = [ord(c) for c in string]
        for i, v in enumerate(cps):
            if start <= i < end:
                result += chr(v)
        return result
