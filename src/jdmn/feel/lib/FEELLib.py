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
import logging
from typing import Any

from jdmn.feel.lib.Types import DATE, TIME, DATE_TIME


class FEELLib:
    LOGGER = logging.getLogger(__name__)

    def logError(self, message: str, e: Exception = None) -> None:
        if e is None:
            self.LOGGER.error(message)
        else:
            self.LOGGER.exception(message)

    @staticmethod
    def toDate(from_: Any) -> DATE:
        raise Exception("Not supported yet")

    @staticmethod
    def toTime(from_: Any) -> TIME:
        raise Exception("Not supported yet")

    @staticmethod
    def toDateTime(from_: Any) -> DATE_TIME:
        raise Exception("Not supported yet")

    #
    # Error conversions
    #
    @staticmethod
    def toNull(obj: Any) -> Any:
        return None
