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
from typing import Any

from jdmn.runtime.listener.Arguments import Arguments
from jdmn.runtime.listener.DRGElement import DRGElement
from jdmn.runtime.listener.Rule import Rule


class EventListener:
    def startDRGElement(self, element: DRGElement, arguments: Arguments) -> None:
        raise NotImplementedError()

    def endDRGElement(self, element: DRGElement, arguments: Arguments, output: Any, duration: int) -> None:
        raise NotImplementedError()

    def startRule(self, element: DRGElement, rule: Rule) -> None:
        raise NotImplementedError()

    def matchRule(self, element: DRGElement, rule: Rule) -> None:
        raise NotImplementedError()

    def endRule(self, element: DRGElement, rule: Rule, result: Any) -> None:
        raise NotImplementedError()

    def matchColumn(self, rule: Rule, columnIndex: int, result: Any) -> None:
        raise NotImplementedError()
