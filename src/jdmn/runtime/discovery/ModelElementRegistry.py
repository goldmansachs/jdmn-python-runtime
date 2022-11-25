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
import logging
from typing import Set

from jdmn.runtime.DMNRuntimeException import DMNRuntimeException


class ModelElementRegistry:
    LOGGER = logging.getLogger(__name__)

    def __init__(self):
        self.map = {}

    def register(self, qName: str, className: str) -> None:
        if qName is None:
            raise DMNRuntimeException("Missing qName")
        if className is None:
            raise DMNRuntimeException("Missing class name")

        value = self.map[qName]
        if value is None:
            self.map[qName] = className
        elif value != className:
            raise DMNRuntimeException(f"Name '{qName}' is not unique")
        else:
            self.LOGGER.warning("Name '%s' and value '%s' were already registered", qName, className)

    def discover(self, qName: str) -> str:
        return self.map[qName]

    def keys(self) -> Set[str]:
        return self.map.keys()
