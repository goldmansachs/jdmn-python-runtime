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
from typing import List, Any

from jdmn.runtime.DMNRuntimeException import DMNRuntimeException
from jdmn.runtime.external.ExternalFunctionExecutor import ExternalFunctionExecutor


class DefaultExternalFunctionExecutor(ExternalFunctionExecutor):
    @staticmethod
    def execute(className: str, methodName: str, args: List[Any]) -> Any:
        raise DMNRuntimeException("External execution is not supported")
