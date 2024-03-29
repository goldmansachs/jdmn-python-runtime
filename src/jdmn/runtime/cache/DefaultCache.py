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
from typing import Any

from jdmn.runtime.cache.Cache import Cache


class DefaultCache(Cache):
    LOGGER = logging.getLogger(__name__)

    def __init__(self):
        self.bindings = {}

    def contains(self, key: str) -> bool:
        return key in self.bindings.keys()

    def bind(self, key: str, value: Any) -> None:
        self.LOGGER.debug("Bind '%s' to '%s'", key, value)
        self.bindings[key] = value

    def lookup(self, key: str) -> Any:
        value = self.bindings[key]

        self.LOGGER.debug("Retrieve '%s' = '%s'", key, value)

        return value

    def clear(self) -> None:
        self.bindings.clear()
