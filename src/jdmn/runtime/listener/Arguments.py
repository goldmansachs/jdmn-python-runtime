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


class Arguments(dict):
    def __str__(self):
        return ", ".join(["{0}= '{1}'".format(key, value) for key, value in self.items()])

    def get(self, key: str) -> Any:
        return self[key]

    def put(self, key: str, value: Any) -> None:
        self[key] = value
