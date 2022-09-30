#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from typing import Any, Optional

from jdmn.feel.lib.BaseFEELLib import BaseFEELLib
from jdmn.feel.lib.Types import NUMBER, STRING, BOOLEAN, DATE, TIME, DATE_TIME, DURATION, LIST
from jdmn.feel.lib.type.ComparableComparator import comparable
from jdmn.feel.lib.type.bool.DefaultBooleanLib import DefaultBooleanLib
from jdmn.feel.lib.type.list.DefaultListLib import DefaultListLib
from jdmn.feel.lib.type.numeric.DefaultNumericLib import DefaultNumericLib
from jdmn.feel.lib.type.range.DefaultRangeLib import DefaultRangeLib
from jdmn.feel.lib.type.string.DefaultStringLib import DefaultStringLib
from jdmn.feel.lib.type.time.DefaultDateTimeLib import DefaultDateTimeLib
from jdmn.feel.lib.type.time.DefaultDurationLib import DefaultDurationLib
from jdmn.runtime.DMNRuntimeException import DMNRuntimeException
from jdmn.runtime.LambdaExpression import LambdaExpression
from jdmn.runtime.NumericRoundingMode import NumericRoundingMode
from jdmn.runtime.Range import Range


class BaseStandardFEELLib(BaseFEELLib):
    # Libs
    numberLib = DefaultNumericLib()
    stringLib = DefaultStringLib()
    booleanLib = DefaultBooleanLib()
    dateTimeLib = DefaultDateTimeLib()
    durationLib = DefaultDurationLib()
    listLib = DefaultListLib()
    rangeLib = DefaultRangeLib()

    def __init__(self):
        BaseFEELLib.__init__(self)

    #
    # Conversion functions
    #
    def number(self, literal: STRING, groupingSeparator: STRING = None, decimalSeparator: STRING = None) -> NUMBER:
        try:
            return self.numberLib.number(literal, groupingSeparator, decimalSeparator)
        except Exception as e:
            message = "number({}, {}, {})".format(literal, groupingSeparator, decimalSeparator)
            self.logError(message, e)
            return None

    def string(self, from_: Any) -> STRING:
        try:
            return self.stringLib.string(from_)
        except Exception as e:
            message: STRING = "string({})".format(from_)
            self.logError(message, e)
            return None

    def date(self, *args) -> DATE:
        try:
            return self.dateTimeLib.date(*args)
        except Exception as e:
            message: STRING = "date({})".format(*args)
            self.logError(message, e)
            return None

    # TODO ZoneIDs not supported in ISO 8601
    def time(self, *args) -> TIME:
        try:
            return self.dateTimeLib.time(*args)
        except Exception as e:
            message: STRING = "time({})".format(*args)
            self.logError(message, e)
            return None

    def dateAndTime(self, *args) -> DATE_TIME:
        try:
            return self.dateTimeLib.dateAndTime(*args)
        except Exception as e:
            message: STRING = "dateAndTime({})".format(*args)
            self.logError(message, e)
            return None

    def duration(self, from_: STRING) -> DURATION:
        try:
            return self.durationLib.duration(from_)
        except Exception as e:
            message: STRING = "duration({})".format(from_)
            self.logError(message, e)
            return None

    def yearsAndMonthsDuration(self, from_: DATE, to: DATE) -> DURATION:
        try:
            return self.durationLib.yearsAndMonthsDuration(from_, to)
        except Exception as e:
            message: STRING = "yearsAndMonthsDURATION({}, {})".format(from_, to)
            self.logError(message, e)
            return None

    #
    # Extra conversion functions
    #
    def toDate(self, from_: Any) -> DATE:
        try:
            return self.dateTimeLib.toDate(from_)
        except Exception as e:
            message: STRING = "toDate({})".format(from_)
            self.logError(message, e)
            return None

    def toTime(self, from_: Any) -> TIME:
        try:
            return self.dateTimeLib.toTime(from_)
        except Exception as e:
            message: STRING = "toTime({})".format(from_)
            self.logError(message, e)
            return None

    def toDateTime(self, from_: Any) -> DATE_TIME:
        try:
            return self.dateTimeLib.toDateTime(from_)
        except Exception as e:
            message: STRING = "toTime({})".format(from_)
            self.logError(message, e)
            return None

    #
    # Numeric functions
    #
    def decimal(self, n: NUMBER, scale: NUMBER) -> NUMBER:
        try:
            return self.numberLib.decimal(n, scale)
        except Exception as e:
            message: STRING = "decimal({}, {})".format(n, scale)
            self.logError(message, e)
            return None

    def round(self, n: NUMBER, scale: NUMBER, mode: STRING) -> NUMBER:
        try:
            roundingMode = NumericRoundingMode.fromName(mode)
            if roundingMode is None:
                raise DMNRuntimeException("Unknown rounding mode '{}'. Expected one of '{}'".format(mode, NumericRoundingMode.allowedValues()))
            else:
                return self.numberLib.round(n, scale, roundingMode)

        except Exception as e:
            message: STRING = "round({}, {}, {})".format(n, scale, mode)
            self.logError(message, e)
            return None

    def roundUp(self, n: NUMBER, scale: NUMBER) -> NUMBER:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.UP)
        except Exception as e:
            message: STRING = "roundUp({}, {})".format(n, scale)
            self.logError(message, e)
            return None

    def roundDown(self, n: NUMBER, scale: NUMBER) -> NUMBER:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.DOWN)
        except Exception as e:
            message: STRING = "roundDown({}, {})".format(n, scale)
            self.logError(message, e)
            return None

    def roundHalfUp(self, n: NUMBER, scale: NUMBER) -> NUMBER:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.HALF_UP)
        except Exception as e:
            message: STRING = "roundHalfUp({}, {})".format(n, scale)
            self.logError(message, e)
            return None

    def roundHalfDown(self, n: NUMBER, scale: NUMBER) -> NUMBER:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.HALF_DOWN)
        except Exception as e:
            message: STRING = "roundHalfDown({}, {})".format(n, scale)
            self.logError(message, e)
            return None

    def floor(self, *args) -> NUMBER:
        try:
            return self.numberLib.floor(*args)
        except Exception as e:
            message: STRING = "floor({})".format(*args)
            self.logError(message, e)
            return None

    def ceiling(self, *args) -> NUMBER:
        try:
            return self.numberLib.ceiling(*args)
        except Exception as e:
            message: STRING = "ceiling({})".format(*args)
            self.logError(message, e)
            return None

    def abs(self, n: Any) -> Any:
        try:
            if self.isNumber(n):
                return self.numberLib.abs(n)
            else:
                return self.durationLib.abs(n)
        except Exception as e:
            message: STRING = "abs({})".format(n)
            self.logError(message, e)
            return None

    def intModulo(self, dividend: NUMBER, divisor: NUMBER) -> NUMBER:
        try:
            return self.numberLib.intModulo(dividend, divisor)
        except Exception as e:
            message: STRING = "modulo({}, {})".format(dividend, divisor)
            self.logError(message, e)
            return None

    def modulo(self, dividend: NUMBER, divisor: NUMBER) -> NUMBER:
        try:
            return self.numberLib.modulo(dividend, divisor)
        except Exception as e:
            message: STRING = "modulo({}, {})".format(dividend, divisor)
            self.logError(message, e)
            return None

    def sqrt(self, number: NUMBER) -> NUMBER:
        try:
            return self.numberLib.sqrt(number)
        except Exception as e:
            message: STRING = "sqrt({})".format(number)
            self.logError(message, e)
            return None

    def log(self, number: NUMBER) -> NUMBER:
        try:
            return self.numberLib.log(number)
        except Exception as e:
            message: STRING = "log({})".format(number)
            self.logError(message, e)
            return None

    def exp(self, number: NUMBER) -> NUMBER:
        try:
            return self.numberLib.exp(number)
        except Exception as e:
            message: STRING = "exp({})".format(number)
            self.logError(message, e)
            return None

    def odd(self, number: NUMBER) -> BOOLEAN:
        try:
            return self.numberLib.odd(number)
        except Exception as e:
            message: STRING = "odd({})".format(number)
            self.logError(message, e)
            return None

    def even(self, number: NUMBER) -> BOOLEAN:
        try:
            return self.numberLib.even(number)
        except Exception as e:
            message: STRING = "even({})".format(number)
            self.logError(message, e)
            return None

    def mean(self, *args) -> NUMBER:
        try:
            return self.numberLib.mean(*args)
        except Exception as e:
            message: STRING = "mean({})".format(str(args))
            self.logError(message, e)
            return None

    #
    # String functions
    #
    def contains(self, string: STRING, match: STRING) -> BOOLEAN:
        try:
            return self.stringLib.contains(string, match)
        except Exception as e:
            message: STRING = "contains({}, {})".format(string, match)
            self.logError(message, e)
            return None

    def startsWith(self, string: STRING, match: STRING) -> BOOLEAN:
        try:
            return self.stringLib.startsWith(string, match)
        except Exception as e:
            message: STRING = "startsWith({}, {})".format(string, match)
            self.logError(message, e)
            return None

    def endsWith(self, string: STRING, match: STRING) -> BOOLEAN:
        try:
            return self.stringLib.endsWith(string, match)
        except Exception as e:
            message: STRING = "endsWith({}, {})".format(string, match)
            self.logError(message, e)
            return None

    def stringLength(self, string: STRING) -> NUMBER:
        try:
            return None if string is None else self.valueOf(self.stringLib.stringLength(string))
        except Exception as e:
            message: STRING = "stringLength({})".format(string)
            self.logError(message, e)
            return None

    def substring(self, string: STRING, startPosition: NUMBER, length: NUMBER = None) -> STRING:
        try:
            return self.stringLib.substring(string, self.numberLib.toNumber(startPosition), self.numberLib.toNumber(length))
        except Exception as e:
            message: STRING = "substring({}, {}, {})".format(string, startPosition, length)
            self.logError(message, e)
            return None

    def upperCase(self, string: STRING) -> STRING:
        try:
            return self.stringLib.upperCase(string)
        except Exception as e:
            message: STRING = "upperCase({})".format(string)
            self.logError(message, e)
            return None

    def lowerCase(self, string: STRING) -> STRING:
        try:
            return self.stringLib.lowerCase(string)
        except Exception as e:
            message: STRING = "lowerCase({})".format(string)
            self.logError(message, e)
            return None

    def substringBefore(self, string: STRING, match: STRING) -> STRING:
        try:
            return self.stringLib.substringBefore(string, match)
        except Exception as e:
            message: STRING = "substringBefore({}, {})".format(string, match)
            self.logError(message, e)
            return None

    def substringAfter(self, string: STRING, match: STRING) -> STRING:
        try:
            return self.stringLib.substringAfter(string, match)
        except Exception as e:
            message: STRING = "substringAfter({}, {})".format(string, match)
            self.logError(message, e)
            return None

    def replace(self, input: STRING, pattern: STRING, replacement: STRING, flags: STRING = "") -> STRING:
        try:
            return self.stringLib.replace(input, pattern, replacement, flags)
        except Exception as e:
            message: STRING = "replace({}, {}, {}, {})".format(input, pattern, replacement, flags)
            self.logError(message, e)
            return None

    def matches(self, input: STRING, pattern: STRING, flags: STRING = "") -> BOOLEAN:
        try:
            return self.stringLib.matches(input, pattern, flags)
        except Exception as e:
            message: STRING = "matches({}, {}, {})".format(input, pattern, flags)
            self.logError(message, e)
            return None

    def split(self, string: STRING, delimiter: STRING) -> LIST:
        try:
            return self.stringLib.split(string, delimiter)
        except Exception as e:
            message: STRING = "split({}, {})".format(string, delimiter)
            self.logError(message, e)
            return None

    #
    # Boolean functions
    #
    def and_(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.all(*args)
        except Exception as e:
            message = "and({})".format(*args)
            self.logError(message, e)
            return None

    def all(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.all(*args)
        except Exception as e:
            message = "and({})".format(*args)
            self.logError(message, e)
            return None

    def or_(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.any(*args)
        except Exception as e:
            message = "or({})".format(*args)
            self.logError(message, e)
            return None

    def any(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.any(*args)
        except Exception as e:
            message = "or({})".format(*args)
            self.logError(message, e)
            return None

    def not_(self, operand: BOOLEAN) -> BOOLEAN:
        try:
            return self.booleanType.booleanNot(operand)
        except Exception as e:
            message: STRING = "not({})".format(operand)
            self.logError(message, e)
            return None

    #
    # Date properties
    #
    def year(self, date: DATE) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.year(date))
        except Exception as e:
            message: STRING = "year({})".format(date)
            self.logError(message, e)
            return None

    def month(self, date: DATE) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.month(date))
        except Exception as e:
            message: STRING = "month({})".format(date)
            self.logError(message, e)
            return None

    def day(self, date: DATE) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.day(date))
        except Exception as e:
            message: STRING = "day({})".format(date)
            self.logError(message, e)
            return None

    def weekday(self, date: DATE) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.weekday(date))
        except Exception as e:
            message: STRING = "weekday({})".format(date)
            self.logError(message, e)
            return None

    #
    # Time properties
    #
    def hour(self, time: TIME) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.hour(time))
        except Exception as e:
            message: STRING = "hour({})".format(time)
            self.logError(message, e)
            return None

    def minute(self, time: TIME) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.minute(time))
        except Exception as e:
            message: STRING = "minute({})".format(time)
            self.logError(message, e)
            return None

    def second(self, time: TIME) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.second(time))
        except Exception as e:
            message: STRING = "second({})".format(time)
            self.logError(message, e)
            return None

    def timeOffset(self, time: TIME) -> DURATION:
        try:
            return self.dateTimeLib.timeOffset(time)
        except Exception as e:
            message: STRING = "timeOffset({})".format(time)
            self.logError(message, e)
            return None

    def timezone(self, time: TIME) -> STRING:
        try:
            return self.dateTimeLib.timezone(time)
        except Exception as e:
            message: STRING = "timezone({})".format(time)
            self.logError(message, e)
            return None

    #
    # Duration properties
    #

    def years(self, duration: DURATION) -> NUMBER:
        try:
            return self.valueOf(self.durationLib.years(duration))
        except Exception as e:
            message: STRING = "years({})".format(duration)
            self.logError(message, e)
            return None

    def months(self, duration: DURATION) -> NUMBER:
        try:
            return self.valueOf(self.durationLib.months(duration))
        except Exception as e:
            message: STRING = "months({})".format(duration)
            self.logError(message, e)
            return None

    def days(self, duration: DURATION) -> NUMBER:
        try:
            return self.valueOf(self.durationLib.days(duration))
        except Exception as e:
            message: STRING = "days({})".format(duration)
            self.logError(message, e)
            return None

    def hours(self, duration: DURATION) -> NUMBER:
        try:
            return self.valueOf(self.durationLib.hours(duration))
        except Exception as e:
            message: STRING = "hours({})".format(duration)
            self.logError(message, e)
            return None

    def minutes(self, duration: DURATION) -> NUMBER:
        try:
            return self.valueOf(self.durationLib.minutes(duration))
        except Exception as e:
            message: STRING = "minutes({})".format(duration)
            self.logError(message, e)
            return None

    def seconds(self, duration: DURATION) -> NUMBER:
        try:
            return self.valueOf(self.durationLib.seconds(duration))
        except Exception as e:
            message: STRING = "seconds({})".format(duration)
            self.logError(message, e)
            return None

    #
    # Date and time functions
    #

    def is_(self, value1: Any, value2: Any) -> BOOLEAN:
        try:
            if value1 is None or value2 is None:
                return value1 == value2
            elif type(value1) != type(value2):
                # Different kind
                return False
            elif self.isNumber(value1):
                return self.numericType.numericIs(value1, value2)
            elif self.isBoolean(value1):
                return self.booleanType.booleanIs(value1, value2)
            elif self.isString(value1):
                return self.stringType.stringIs(value1, value2)
            elif self.isDate(value1):
                return self.dateType.dateIs(value1, value2)
            elif self.isTime(value1):
                return self.timeType.timeIs(value1, value2)
            elif self.isDateTime(value1):
                return self.dateTimeType.dateTimeIs(value1, value2)
            elif self.isDuration(value1):
                return self.durationType.durationIs(value1, value2)
            elif self.isList(value1):
                return self.listType.listIs(value1, value2)
            elif self.isRange(value1):
                return self.rangeType.rangeIs(value1, value2)
            elif self.isContext(value1):
                return self.contextType.contextIs(value1, value2)
            else:
                self.logError("'{}' is not supported yet".format(value1.getClass().getSimpleName()))
                return False

        except Exception as e:
            message: STRING = "is({}, {})".format(value1, value2)
            self.logError(message, e)
            return False

    #
    # Temporal functions
    #

    def dayOfYear(self, date: DATE) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.dayOfYear(date))
        except Exception as e:
            message: STRING = "dayOfYear({})".format(date)
            self.logError(message, e)
            return None

    def dayOfWeek(self, date: DATE) -> STRING:
        try:
            return self.dateTimeLib.dayOfWeek(date)
        except Exception as e:
            message: STRING = "dayOfWeek({})".format(date)
            self.logError(message, e)
            return None

    def weekOfYear(self, date: DATE) -> NUMBER:
        try:
            return self.valueOf(self.dateTimeLib.weekOfYear(date))
        except Exception as e:
            message: STRING = "weekOfYear({})".format(date)
            self.logError(message, e)
            return None

    def monthOfYear(self, date: DATE) -> STRING:
        try:
            return self.dateTimeLib.monthOfYear(date)
        except Exception as e:
            message: STRING = "weekOfYear({})".format(date)
            self.logError(message, e)
            return None

    #
    # List functions
    #

    def listContains(self, list: LIST, element: Any) -> BOOLEAN:
        try:
            return self.listLib.listContains(list, element)
        except Exception as e:
            message: STRING = "listContains({}, {})".format(list, element)
            self.logError(message, e)
            return None

    def append(self, list: LIST, *items):
        try:
            return self.listLib.append(list, *items)
        except Exception as e:
            message: STRING = "append({}, {})".format(list, *items)
            self.logError(message, e)
            return None

    def count(self, list: LIST) -> NUMBER:
        try:
            return self.numberLib.count(list)
        except Exception as e:
            message = "count({})".format(list)
            self.logError(message, e)
            return None

    def min(self, *args) -> Optional[comparable]:
        try:
            return self.numberLib.min(*args)
        except Exception as e:
            message = "min({})".format(*args)
            self.logError(message, e)
            return None

    def max(self, *args) -> Optional[comparable]:
        try:
            return self.numberLib.max(*args)
        except Exception as e:
            message = "max({})".format(*args)
            self.logError(message, e)
            return None

    def sum(self, *args) -> Optional[comparable]:
        try:
            return self.numberLib.sum(*args)
        except Exception as e:
            message = "sum({})".format(*args)
            self.logError(message, e)
            return None

    def sublist(self, list: LIST, startPosition: NUMBER, length: NUMBER = None) -> LIST:
        try:
            return self.listLib.sublist(list, self.intValue(startPosition), self.intValue(length))
        except Exception as e:
            message: STRING = "sublist({}, {}, {})".format(list, startPosition, length)
            self.logError(message, e)
            return None

    def concatenate(self, *lists) -> LIST:
        try:
            return self.listLib.concatenate(*lists)
        except Exception as e:
            message: STRING = "concatenate({})".format(str(lists))
            self.logError(message, e)
            return None

    def insertBefore(self, list: LIST, position: NUMBER, newItem: Any) -> LIST:
        try:
            return self.listLib.insertBefore(list, self.intValue(position), newItem)
        except Exception as e:
            message: STRING = "insertBefore({}, {}, {})".format(list, position, newItem)
            self.logError(message, e)
            return None

    def remove(self, list: LIST, position: Any):
        try:
            return self.listLib.remove(list, self.intValue(position))
        except Exception as e:
            message: STRING = "remove({})".format(list)
            self.logError(message, e)
            return None

    def reverse(self, list: LIST) -> LIST:
        try:
            return self.listLib.reverse(list)
        except Exception as e:
            message: STRING = "reverse({})".format(list)
            self.logError(message, e)
            return None

    def indexOf(self, list: LIST, match: Any) -> LIST:
        result = []
        if list is not None:
            for i, o in enumerate(list):
                if o is None and match is None or o is not None and o == match:
                    result.append(self.valueOf(i + 1))
        return result

    def union(self, *lists):
        try:
            return self.listLib.union(*lists)
        except Exception as e:
            message: STRING = "union({})".format(str(lists))
            self.logError(message, e)
            return None

    def distinctValues(self, list: LIST) -> LIST:
        try:
            return self.listLib.distinctValues(list)
        except Exception as e:
            message: STRING = "distinctValues({})".format(list)
            self.logError(message, e)
            return None

    def flatten(self, list: LIST) -> LIST:
        try:
            return self.listLib.flatten(list)
        except Exception as e:
            message: STRING = "flatten({})".format(list)
            self.logError(message, e)
            return None

    def product(self, *args) -> NUMBER:
        try:
            return self.numberLib.product(*args)
        except Exception as e:
            message: STRING = "product({})".format(args)
            self.logError(message, e)
            return None

    def median(self, *args) -> NUMBER:
        try:
            return self.numberLib.median(*args)
        except Exception as e:
            message: STRING = "median({})".format(*args)
            self.logError(message, e)
            return None

    def stddev(self, *args) -> NUMBER:
        try:
            return self.numberLib.stddev(*args)
        except Exception as e:
            message: STRING = "stddev({})".format(*args)
            self.logError(message, e)
            return None

    def mode(self, *args) -> LIST:
        try:
            return self.numberLib.mode(*args)
        except Exception as e:
            message: STRING = "mode({})".format(*args)
            self.logError(message, e)
            return None

    def collect(self, result: LIST, list: LIST) -> None:
        try:
            self.listLib.collect(result, list)
        except Exception as e:
            message: STRING = "collect({}, {})".format(result, list)
            self.logError(message, e)

    def sort(self, list: LIST, precedes: LambdaExpression) -> LIST:
        try:
            return self.listLib.sort(list, precedes)
        except Exception as e:
            message: STRING = "sort({})".format(list)
            self.logError(message, e)
            return None

    #
    # Range functions
    #

    def before(self, arg1: Any, arg2: Any) -> BOOLEAN:
        try:
            return self.rangeLib.before(arg1, arg2)
        except Exception as e:
            message: STRING = "before({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def after(self, arg1: Any, arg2: Any) -> BOOLEAN:
        try:
            return self.rangeLib.after(arg1, arg2)
        except Exception as e:
            message: STRING = "after({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def meets(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.meets(range1, range2)
        except Exception as e:
            message: STRING = "meets({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    def metBy(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.metBy(range1, range2)
        except Exception as e:
            message: STRING = "metBy({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    def overlaps(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.overlaps(range1, range2)
        except Exception as e:
            message: STRING = "overlaps({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    def overlapsBefore(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.overlapsBefore(range1, range2)
        except Exception as e:
            message: STRING = "overlapsBefore({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    def overlapsAfter(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.overlapsAfter(range1, range2)
        except Exception as e:
            message: STRING = "overlapsAfter({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    def finishes(self, arg1: Any, arg2: Any) -> BOOLEAN:
        try:
            return self.rangeLib.finishes(arg1, arg2)
        except Exception as e:
            message: STRING = "finishes({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def finishedBy(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.finishedBy(arg1, arg2)
        except Exception as e:
            message: STRING = "finishedBy({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def includes(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.includes(arg1, arg2)
        except Exception as e:
            message: STRING = "includes({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def during(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.during(arg1, arg2)
        except Exception as e:
            message: STRING = "during({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def starts(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.starts(arg1, arg2)
        except Exception as e:
            message: STRING = "starts({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def startedBy(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.startedBy(arg1, arg2)
        except Exception as e:
            message: STRING = "startedBy({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None

    def coincides(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.coincides(arg1, arg2)
        except Exception as e:
            message: STRING = "coincides({}, {})".format(arg1, arg2)
            self.logError(message, e)
            return None
