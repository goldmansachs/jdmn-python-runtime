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

#
# Lazily evaluate the supplied operations to reduce unnecessary computation
#
# @param <T> the type of value stored
#
#
import logging
import typing


class LazyEval:
    LOGGER = logging.getLogger(__name__)

    def __init__(self, supplier: typing.Callable):
        self.supplier = supplier
        self.isValueSet = False
        self.value = None

    def getOrCompute(self) -> typing.Any:
        return self.value if self.isValueSet else self.compute()

    def compute(self) -> typing.Any:
        self.LOGGER.info("Trigger lazy evaluation")

        self.isValueSet = True
        self.value = self.supplier()
        return self.value
