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
from typing import List, Optional

from jdmn.runtime.DMNRuntimeException import DMNRuntimeException
from jdmn.runtime.RuleOutput import RuleOutput
from jdmn.runtime.annotation.HitPolicy import HitPolicy


class RuleOutputList:
    def __init__(self):
        self.matchedRuleResults = []

    def add(self, result: RuleOutput) -> None:
        if result is not None and result.isMatched():
            self.matchedRuleResults.append(result)

    def getMatchedRuleResults(self) -> List[RuleOutput]:
        return self.matchedRuleResults

    def noMatchedRules(self) -> bool:
        return len(self.matchedRuleResults) == 0

    def applySingle(self, hitPolicy: HitPolicy) -> Optional[RuleOutput]:
        if hitPolicy is None:
            hitPolicy = HitPolicy.UNIQUE
        if hitPolicy == HitPolicy.UNIQUE:
            if len(self.matchedRuleResults) == 1:
                return self.matchedRuleResults[0]
            else:
                return None
        elif hitPolicy == HitPolicy.ANY:
            if len(self.matchedRuleResults) > 0:
                distinctResults = set(self.matchedRuleResults)
                if len(distinctResults) == 1:
                    return next(iter(distinctResults))
                else:
                    return None
            else:
                return None
        elif hitPolicy == HitPolicy.FIRST:
            if len(self.matchedRuleResults) > 0:
                return self.matchedRuleResults[0]
            else:
                return None
        elif hitPolicy == HitPolicy.PRIORITY:
            if len(self.matchedRuleResults) > 0:
                sortedRuleOutputs = self.sort(self.matchedRuleResults)
                return sortedRuleOutputs[0]
            else:
                return None
        else:
            raise DMNRuntimeException("Not supported single hit policy %{}.".format(hitPolicy.name))

    def applyMultiple(self, hitPolicy: HitPolicy) -> List[RuleOutput]:
        matchedRuleOutputs = self.getMatchedRuleResults()
        if hitPolicy == HitPolicy.COLLECT:
            return matchedRuleOutputs
        elif (hitPolicy == HitPolicy.RULE_ORDER):
            return matchedRuleOutputs
        elif (hitPolicy == HitPolicy.OUTPUT_ORDER):
            return self.sort(matchedRuleOutputs)
        else:
            raise DMNRuntimeException("Not supported multiple hit policy %{}.".format(hitPolicy.name))

    def sort(self, matchedRuleOutputs: List[RuleOutput]) -> List[RuleOutput]:
        if len(matchedRuleOutputs) == 0:
            return matchedRuleOutputs
        else:
            result = matchedRuleOutputs[0]
            return result.sort(matchedRuleOutputs)
