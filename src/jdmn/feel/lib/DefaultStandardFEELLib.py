#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from decimal import Decimal

from jdmn.feel.lib.BaseStandardFEELLib import BaseStandardFEELLib
from jdmn.feel.lib.Types import INTEGER, DECIMAL


class DefaultStandardFEELLib(BaseStandardFEELLib):
    def __init__(self):
        BaseStandardFEELLib.__init__(self)

    #
    # Extra conversion functions
    #
    def valueOf(self, number: INTEGER) -> DECIMAL:
        if number is None:
            return None
        else:
            return Decimal(number)

    def intValue(self, number: DECIMAL) -> INTEGER:
        if number is None:
            return None
        else:
            return int(number)
