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
from typing import Optional

from jdmn.feel.lib.Utils import varArgToList


class DefaultBooleanLib:
    @staticmethod
    def all(*args) -> Optional[bool]:
        operands = varArgToList(*args)

        oneFalse = False
        allTrue = True
        for opd in operands:
            if opd is False:
                oneFalse = True
            if opd is not True:
                allTrue = False
        if oneFalse:
            return False
        elif allTrue:
            return True
        else:
            return None

    @staticmethod
    def any(*args) -> Optional[bool]:
        operands = varArgToList(*args)

        oneTrue = False
        allFalse = True
        for opd in operands:
            if opd is True:
                oneTrue = True
            if opd is not False:
                allFalse = False
        if oneTrue:
            return True
        elif allFalse:
            return False
        else:
            return None
