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

from jdmn.feel.lib.Types import STRING, BOOLEAN, INTEGER, LIST, DECIMAL, TIME_OR_DATE_TIME


class DefaultStringLib:
    def string(self, from_: Any) -> STRING:
        if isinstance(from_, datetime):
            return self.print(from_)
        elif isinstance(from_, date):
            return from_.isoformat()
        elif isinstance(from_, time):
            return self.print(from_)

        return str(from_)

    @staticmethod
    def print(from_: TIME_OR_DATE_TIME) -> str:
        tz = from_.tzinfo
        if isinstance(tz, ZoneInfo):
            copy = from_
            copy = copy.replace(tzinfo=None)
            isoformat = copy.isoformat()
            return f"{isoformat}@{str(tz)}"
        else:
            return from_.isoformat()

    @staticmethod
    def contains(string: STRING, match: STRING) -> BOOLEAN:
        if string is None or match is None:
            return None

        return match in string

    @staticmethod
    def startsWith(string: Optional[str], match: Optional[str]) -> Optional[bool]:
        if string is None or match is None:
            return None

        return string.startswith(match)

    @staticmethod
    def endsWith(string: STRING, match: STRING) -> BOOLEAN:
        if string is None or match is None:
            return None

        return string.endswith(match)

    @staticmethod
    def stringLength(string: STRING) -> INTEGER:
        if string is None:
            return None

        # The number of Unicode code units in the string
        bytes_ = string.encode('utf-16', 'surrogatepass')
        # The number of characters (Unicode code point)
        transformed = bytes_.decode('utf-16')
        result = len(transformed)
        return result

    def substring(self, string: STRING, startPosition: DECIMAL, length: DECIMAL) -> STRING:
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

    @staticmethod
    def upperCase(string: STRING) -> STRING:
        if string is None:
            return None

        return string.upper()

    @staticmethod
    def lowerCase(string: STRING) -> STRING:
        if string is None:
            return None

        return string.lower()

    @staticmethod
    def substringBefore(string: STRING, match: STRING) -> STRING:
        if string is None or match is None:
            return None

        i = string.find(match)
        return "" if i == -1 else string[0:i]

    @staticmethod
    def substringAfter(string: STRING, match: STRING) -> STRING:
        if string is None or match is None:
            return None

        i = string.find(match)
        return "" if i == -1 else string[i + len(match):]

    def replace(self, input_: STRING, pattern: STRING, replacement: STRING, flags: STRING) -> STRING:
        if input_ is None or pattern is None or replacement is None:
            return None
        if flags is None:
            flags = ""

        return self.evaluateReplace(input_, pattern, replacement, flags)

    def matches(self, input_: STRING, pattern: STRING, flags: STRING) -> BOOLEAN:
        if input_ is None or pattern is None:
            return None
        if flags is None:
            flags = ""

        return self.evaluateMatches(input_, pattern, flags)

    @staticmethod
    def split(string: STRING, delimiter: STRING) -> LIST:
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

    def evaluateReplace(self, input_: str, pattern: str, replacement: str, flags: str) -> str:
        expression = f"replace(/root, '{pattern}', '{replacement}', '{flags}')"
        return self.evaluateXPath(input_, expression)

    def evaluateMatches(self, input_: str, pattern: str, flags: str) -> bool:
        expression = f"/root[matches(., '{pattern}', '{flags}')]"
        value = self.evaluateXPath(input_, expression)
        return len(value) != 0

    @staticmethod
    def evaluateXPath(input_: str, expression: str):
        # Read document
        xmlStr = "<root>" + input_ + "</root>"
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
