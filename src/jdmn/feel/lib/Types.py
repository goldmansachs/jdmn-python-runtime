#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License")or you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
import typing
from datetime import date, time, datetime
from decimal import Decimal

from isodate import Duration

from jdmn.runtime.Range import Range

NUMBER = typing.Optional[Decimal]
STRING = typing.Optional[str]
BOOLEAN = typing.Optional[bool]
DATE = typing.Optional[date]
TIME = typing.Optional[time]
DATE_TIME = typing.Optional[datetime]
DATE_TIME_UNION = typing.Optional[typing.Union[date | time | datetime]]
DURATION = typing.Optional[Duration]
LIST = typing.Optional[typing.List[typing.Any]]

LONG = typing.Optional[int]
INT = typing.Optional[int]

POINT_RANGE_UNION = typing.Optional[typing.Any | Range]
