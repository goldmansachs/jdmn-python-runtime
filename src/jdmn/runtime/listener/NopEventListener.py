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

from jdmn.runtime.listener.EventListener import EventListener
from jdmn.runtime.listener.Arguments import Arguments
from jdmn.runtime.listener.DRGElement import DRGElement
from jdmn.runtime.listener.Rule import Rule


class NopEventListener(EventListener):
    def __init__(self):
        EventListener.__init__(self)

    def startDRGElement(self, element: DRGElement, arguments: Arguments) -> None:
        pass # nothing

    def endDRGElement(self, element: DRGElement, arguments: Arguments, output: Any, duration: int) -> None:
        pass

    def startRule(self, element: DRGElement, rule: Rule) -> None:
        pass

    def matchRule(self, element: DRGElement, rule: Rule) -> None:
        pass

    def endRule(self, element: DRGElement, rule: Rule, result: Any) -> None:
        pass

    def matchColumn(self, rule: Rule, columnIndex: int, result: Any) -> None:
        pass
