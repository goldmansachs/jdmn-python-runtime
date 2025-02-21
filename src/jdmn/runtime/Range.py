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
import datetime
import decimal
import typing
from typing import Any

import isodate
from jdmn.runtime.DMNRuntimeException import DMNRuntimeException

comparable = typing.Optional[typing.Union[decimal.Decimal, str, datetime.date, datetime.time, datetime.datetime, datetime.timedelta, isodate.Duration]]


class Range:
    def __init__(self, *args):
        if len(args) == 0:
            self.startIncluded = False
            self.start = None
            self.endIncluded = False
            self.end = None
            self.operator = None
        elif len(args) == 4:
            self.startIncluded = args[0]
            self.start = args[1]
            self.endIncluded = args[2]
            self.end = args[3]
            self.operator = None
            # Check if both ends are comparable types
            if not isinstance(self.start, comparable) or not isinstance(self.end, comparable):
                raise DMNRuntimeException("Invalid range: start type {} and type {} must be comparable.".format(type(self.start), type(self.end)))
            if self.start is not None and self.end is not None:
                # Check if endpoints have same type
                if type(self.start) is not type(self.end):
                    raise DMNRuntimeException("Invalid range: start type {} and type {} must be the same.".format(type(self.start), type(self.end)))
                # Check if start <= end; Duration does not support relational operators
                if not isinstance(self.start, isodate.Duration) and self.start > self.end:
                    raise DMNRuntimeException("Invalid range: start {} cannot be greater than end {}.".format(self.start, self.end))

        elif len(args) == 2:
            self.operator = args[0]
            if self.operator is None:
                self.operator = "="
            if len(self.operator.strip()) == 0:
                self.operator = "="
            endpoint = args[1]
            match self.operator:
                case "=":
                    self.startIncluded = True
                    self.start = endpoint
                    self.end = endpoint
                    self.endIncluded = True
                case "!=":
                    self.startIncluded = False
                    self.start = None
                    self.end = None
                    self.endIncluded = False
                case "<":
                    self.startIncluded = False
                    self.start = None
                    self.end = endpoint
                    self.endIncluded = False
                case "<=":
                    self.startIncluded = False
                    self.start = None
                    self.end = endpoint
                    self.endIncluded = True
                case ">":
                    self.startIncluded = False
                    self.start = endpoint
                    self.end = None
                    self.endIncluded = False
                case ">=":
                    self.startIncluded = True
                    self.start = endpoint
                    self.end = None
                    self.endIncluded = False
                case _:
                    raise DMNRuntimeException("Illegal operator '{}'".format(self.operator))
            if not isinstance(self.start, comparable):
                raise DMNRuntimeException("Invalid range: endpoint most be comparable {}.".format(type(endpoint)))
        else:
            raise DMNRuntimeException("Illegal Range constructor '{}'".format(*args))

    def isStartIncluded(self) -> bool:
        return self.startIncluded

    def getStart(self) -> Any:
        return self.start

    def isEndIncluded(self) -> bool:
        return self.endIncluded

    def getEnd(self) -> Any:
        return self.end

    def getOperator(self) -> str:
        return self.end

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if type(self) is not type(other):
            return False

        if self.startIncluded != other.startIncluded:
            return False
        if self.endIncluded != other.endIncluded:
            return False
        if self.start != other.start:
            return False
        if self.end != other.end:
            return False
        if self.operator != other.operator:
            return False
        return True

    def __hash__(self):
        result = 0
        result = 31 * result + (0 if self.startIncluded is None else hash(self.startIncluded))
        result = 31 * result + (0 if self.start is None else hash(self.start))
        result = 31 * result + (0 if self.endIncluded is None else hash(self.endIncluded))
        result = 31 * result + (0 if self.end is None else hash(self.end))
        result = 31 * result + (0 if self.operator is None else hash(self.operator))
        return result

    def __str__(self):
        return "Range({},{},{},{},{})".format(self.startIncluded, self.start, self.end, self.endIncluded, self.operator)
