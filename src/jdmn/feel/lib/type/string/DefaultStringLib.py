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
from datetime import datetime
from typing import Optional, Any

from lxml import etree
import elementpath

from jdmn.feel.lib.Types import STRING, BOOLEAN, INT, LIST, NUMBER


class DefaultStringLib:
    def string(self, from_: Any) -> STRING:
        if isinstance(from_, datetime):
            return str(from_.isoformat())

        return str(from_)

    def contains(self, string: STRING, match: STRING) -> BOOLEAN:
        if string is None or match is None:
            return None

        return match in string

    def startsWith(self, string: Optional[str], match: Optional[str]) -> Optional[bool]:
        if string is None or match is None:
            return None

        return string.startswith(match)

    def endsWith(self, string: STRING, match: STRING) -> BOOLEAN:
        raise Exception("Not supported yet")

    def stringLength(self, string: STRING) -> INT:
        raise Exception("Not supported yet")

    def substring(self, string: STRING, startPosition: NUMBER, length: NUMBER) -> STRING:
        raise Exception("Not supported yet")

    def upperCase(self, string: STRING) -> STRING:
        raise Exception("Not supported yet")

    def lowerCase(self, string: STRING) -> STRING:
        if string is None:
            return None

        return string.lower()

    def substringBefore(self, string: STRING, match: STRING) -> STRING:
        raise Exception("Not supported yet")

    def substringAfter(self, string: STRING, match: STRING) -> STRING:
        raise Exception("Not supported yet")

    def replace(self, input: STRING, pattern: STRING, replacement: STRING, flags: STRING) -> STRING:
        raise Exception("Not supported yet")

    def matches(self, input: STRING, pattern: STRING, flags: STRING) -> BOOLEAN:
        if input is None or pattern is None:
            return None
        if flags is None:
            flags = ""

        expression = "/root[matches(., '{}', '{}')]".format(pattern, flags)
        value = self.evaluateXPath(input, expression)
        return len(value) != 0

    def split(self, string: STRING, delimiter: STRING) -> LIST:
        raise Exception("Not supported yet")

    def evaluateXPath(self, input, expression):
        # Read document
        xmlStr = "<root>" + input + "</root>"
        root = etree.fromstring(xmlStr)

        # Evaluate xpath
        res1 = elementpath.select(root, expression)
        return res1
