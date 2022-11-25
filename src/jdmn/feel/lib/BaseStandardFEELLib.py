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
from jdmn.feel.lib.Types import DECIMAL, STRING, BOOLEAN, DATE, TIME, DATE_TIME, DURATION, LIST, DATE_OR_DATE_TIME, TIME_OR_DATE_TIME
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
    def number(self, literal: STRING, groupingSeparator: STRING = None, decimalSeparator: STRING = None) -> DECIMAL:
        try:
            return self.numberLib.number(literal, groupingSeparator, decimalSeparator)
        except Exception as e:
            message = f"number({literal}, {groupingSeparator}, {decimalSeparator})"
            self.logError(message, e)
            return None

    def string(self, from_: Any) -> STRING:
        try:
            return self.stringLib.string(from_)
        except Exception as e:
            message: STRING = f"string({from_})"
            self.logError(message, e)
            return None

    def date(self, *args) -> DATE:
        try:
            return self.dateTimeLib.date(*args)
        except Exception as e:
            message: STRING = f"date{args}"
            self.logError(message, e)
            return None

    def time(self, *args) -> TIME:
        try:
            return self.dateTimeLib.time(*args)
        except Exception as e:
            message: STRING = f"time{args}"
            self.logError(message, e)
            return None

    def dateAndTime(self, *args) -> DATE_TIME:
        try:
            return self.dateTimeLib.dateAndTime(*args)
        except Exception as e:
            message: STRING = f"dateAndTime{args}"
            self.logError(message, e)
            return None

    def duration(self, from_: STRING) -> DURATION:
        try:
            return self.durationLib.duration(from_)
        except Exception as e:
            message: STRING = f"duration({from_})"
            self.logError(message, e)
            return None

    def yearsAndMonthsDuration(self, from_: DATE_OR_DATE_TIME, to: DATE_OR_DATE_TIME) -> DURATION:
        try:
            return self.durationLib.yearsAndMonthsDuration(from_, to)
        except Exception as e:
            message: STRING = f"yearsAndMonthsDuration({from_}, {to})"
            self.logError(message, e)
            return None

    #
    # Extra conversion functions
    #
    def toDate(self, from_: Any) -> DATE:
        try:
            return self.dateTimeLib.toDate(from_)
        except Exception as e:
            message: STRING = f"toDate({from_})"
            self.logError(message, e)
            return None

    def toTime(self, from_: Any) -> TIME:
        try:
            return self.dateTimeLib.toTime(from_)
        except Exception as e:
            message: STRING = f"toTime({from_})"
            self.logError(message, e)
            return None

    def toDateTime(self, from_: Any) -> DATE_TIME:
        try:
            return self.dateTimeLib.toDateTime(from_)
        except Exception as e:
            message: STRING = f"toTime({from_})"
            self.logError(message, e)
            return None

    #
    # Numeric functions
    #
    def decimal(self, n: DECIMAL, scale: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.decimal(n, scale)
        except Exception as e:
            message: STRING = f"decimal({n}, {scale})"
            self.logError(message, e)
            return None

    def round(self, n: DECIMAL, scale: DECIMAL, mode: STRING) -> DECIMAL:
        try:
            roundingMode = NumericRoundingMode.fromName(mode)
            if roundingMode is None:
                raise DMNRuntimeException(f"Unknown rounding mode '{mode}'. Expected one of '{NumericRoundingMode.allowedValues()}'")
            else:
                return self.numberLib.round(n, scale, roundingMode)

        except Exception as e:
            message: STRING = f"round({n}, {scale}, {mode})"
            self.logError(message, e)
            return None

    def roundUp(self, n: DECIMAL, scale: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.UP)
        except Exception as e:
            message: STRING = f"roundUp({n}, {scale})"
            self.logError(message, e)
            return None

    def roundDown(self, n: DECIMAL, scale: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.DOWN)
        except Exception as e:
            message: STRING = f"roundDown({n}, {scale})"
            self.logError(message, e)
            return None

    def roundHalfUp(self, n: DECIMAL, scale: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.HALF_UP)
        except Exception as e:
            message: STRING = f"roundHalfUp({n}, {scale})"
            self.logError(message, e)
            return None

    def roundHalfDown(self, n: DECIMAL, scale: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.round(n, scale, NumericRoundingMode.HALF_DOWN)
        except Exception as e:
            message: STRING = f"roundHalfDown({n}, {scale})"
            self.logError(message, e)
            return None

    def floor(self, *args) -> DECIMAL:
        try:
            return self.numberLib.floor(*args)
        except Exception as e:
            message: STRING = f"floor{args}"
            self.logError(message, e)
            return None

    def ceiling(self, *args) -> DECIMAL:
        try:
            return self.numberLib.ceiling(*args)
        except Exception as e:
            message: STRING = f"ceiling{args}"
            self.logError(message, e)
            return None

    def abs(self, n: Any) -> Any:
        try:
            if self.isNumber(n):
                return self.numberLib.abs(n)
            else:
                return self.durationLib.abs(n)
        except Exception as e:
            message: STRING = f"abs({n})"
            self.logError(message, e)
            return None

    def intModulo(self, dividend: DECIMAL, divisor: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.intModulo(dividend, divisor)
        except Exception as e:
            message: STRING = f"modulo({dividend}, {divisor})"
            self.logError(message, e)
            return None

    def modulo(self, dividend: DECIMAL, divisor: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.modulo(dividend, divisor)
        except Exception as e:
            message: STRING = f"modulo({dividend}, {divisor})"
            self.logError(message, e)
            return None

    def sqrt(self, number: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.sqrt(number)
        except Exception as e:
            message: STRING = f"sqrt({number})"
            self.logError(message, e)
            return None

    def log(self, number: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.log(number)
        except Exception as e:
            message: STRING = f"log({number})"
            self.logError(message, e)
            return None

    def exp(self, number: DECIMAL) -> DECIMAL:
        try:
            return self.numberLib.exp(number)
        except Exception as e:
            message: STRING = f"exp({number})"
            self.logError(message, e)
            return None

    def odd(self, number: DECIMAL) -> BOOLEAN:
        try:
            return self.numberLib.odd(number)
        except Exception as e:
            message: STRING = f"odd({number})"
            self.logError(message, e)
            return None

    def even(self, number: DECIMAL) -> BOOLEAN:
        try:
            return self.numberLib.even(number)
        except Exception as e:
            message: STRING = f"even({number})"
            self.logError(message, e)
            return None

    def mean(self, *args) -> DECIMAL:
        try:
            return self.numberLib.mean(*args)
        except Exception as e:
            message: STRING = f"mean{args}"
            self.logError(message, e)
            return None

    #
    # String functions
    #
    def contains(self, string: STRING, match: STRING) -> BOOLEAN:
        try:
            return self.stringLib.contains(string, match)
        except Exception as e:
            message: STRING = f"contains({string}, {match})"
            self.logError(message, e)
            return None

    def startsWith(self, string: STRING, match: STRING) -> BOOLEAN:
        try:
            return self.stringLib.startsWith(string, match)
        except Exception as e:
            message: STRING = f"startsWith({string}, {match})"
            self.logError(message, e)
            return None

    def endsWith(self, string: STRING, match: STRING) -> BOOLEAN:
        try:
            return self.stringLib.endsWith(string, match)
        except Exception as e:
            message: STRING = f"endsWith({string}, {match})"
            self.logError(message, e)
            return None

    def stringLength(self, string: STRING) -> DECIMAL:
        try:
            return None if string is None else self.valueOf(self.stringLib.stringLength(string))
        except Exception as e:
            message: STRING = f"stringLength({string})"
            self.logError(message, e)
            return None

    def substring(self, string: STRING, startPosition: DECIMAL, length: DECIMAL = None) -> STRING:
        try:
            return self.stringLib.substring(string, self.numberLib.toNumber(startPosition), self.numberLib.toNumber(length))
        except Exception as e:
            message: STRING = f"substring({string}, {startPosition}, {length})"
            self.logError(message, e)
            return None

    def upperCase(self, string: STRING) -> STRING:
        try:
            return self.stringLib.upperCase(string)
        except Exception as e:
            message: STRING = f"upperCase({string})"
            self.logError(message, e)
            return None

    def lowerCase(self, string: STRING) -> STRING:
        try:
            return self.stringLib.lowerCase(string)
        except Exception as e:
            message: STRING = f"lowerCase({string})"
            self.logError(message, e)
            return None

    def substringBefore(self, string: STRING, match: STRING) -> STRING:
        try:
            return self.stringLib.substringBefore(string, match)
        except Exception as e:
            message: STRING = f"substringBefore({string}, {match})"
            self.logError(message, e)
            return None

    def substringAfter(self, string: STRING, match: STRING) -> STRING:
        try:
            return self.stringLib.substringAfter(string, match)
        except Exception as e:
            message: STRING = f"substringAfter({string}, {match})"
            self.logError(message, e)
            return None

    def replace(self, input_: STRING, pattern: STRING, replacement: STRING, flags: STRING = "") -> STRING:
        try:
            return self.stringLib.replace(input_, pattern, replacement, flags)
        except Exception as e:
            message: STRING = f"replace({input_}, {pattern}, {replacement}, {flags})"
            self.logError(message, e)
            return None

    def matches(self, input_: STRING, pattern: STRING, flags: STRING = "") -> BOOLEAN:
        try:
            return self.stringLib.matches(input_, pattern, flags)
        except Exception as e:
            message: STRING = f"matches({input_}, {pattern}, {flags})"
            self.logError(message, e)
            return None

    def split(self, string: STRING, delimiter: STRING) -> LIST:
        try:
            return self.stringLib.split(string, delimiter)
        except Exception as e:
            message: STRING = f"split({string}, {delimiter})"
            self.logError(message, e)
            return None

    #
    # Boolean functions
    #
    def and_(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.all(*args)
        except Exception as e:
            message = f"and{args}"
            self.logError(message, e)
            return None

    def all(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.all(*args)
        except Exception as e:
            message = f"and{args}"
            self.logError(message, e)
            return None

    def or_(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.any(*args)
        except Exception as e:
            message = f"or{args}"
            self.logError(message, e)
            return None

    def any(self, *args) -> BOOLEAN:
        try:
            return self.booleanLib.any(*args)
        except Exception as e:
            message = f"or{args}"
            self.logError(message, e)
            return None

    def not_(self, operand: BOOLEAN) -> BOOLEAN:
        try:
            return self.booleanType.booleanNot(operand)
        except Exception as e:
            message: STRING = f"not({operand})"
            self.logError(message, e)
            return None

    #
    # Date properties
    #
    def year(self, date: DATE_OR_DATE_TIME) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.year(date))
        except Exception as e:
            message: STRING = f"year({date})"
            self.logError(message, e)
            return None

    def month(self, date: DATE_OR_DATE_TIME) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.month(date))
        except Exception as e:
            message: STRING = f"month({date})"
            self.logError(message, e)
            return None

    def day(self, date: DATE_OR_DATE_TIME) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.day(date))
        except Exception as e:
            message: STRING = f"day({date})"
            self.logError(message, e)
            return None

    def weekday(self, date: DATE_OR_DATE_TIME) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.weekday(date))
        except Exception as e:
            message: STRING = f"weekday({date})"
            self.logError(message, e)
            return None

    #
    # Time properties
    #
    def hour(self, time: TIME_OR_DATE_TIME) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.hour(time))
        except Exception as e:
            message: STRING = f"hour({time})"
            self.logError(message, e)
            return None

    def minute(self, time: TIME_OR_DATE_TIME) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.minute(time))
        except Exception as e:
            message: STRING = f"minute({time})"
            self.logError(message, e)
            return None

    def second(self, time: TIME_OR_DATE_TIME) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.second(time))
        except Exception as e:
            message: STRING = f"second({time})"
            self.logError(message, e)
            return None

    def timeOffset(self, time: TIME_OR_DATE_TIME) -> DURATION:
        try:
            return self.dateTimeLib.timeOffset(time)
        except Exception as e:
            message: STRING = f"timeOffset({time})"
            self.logError(message, e)
            return None

    def timezone(self, time: TIME_OR_DATE_TIME) -> STRING:
        try:
            return self.dateTimeLib.timezone(time)
        except Exception as e:
            message: STRING = f"timezone({time})"
            self.logError(message, e)
            return None

    #
    # Duration properties
    #

    def years(self, duration: DURATION) -> DECIMAL:
        try:
            return self.valueOf(self.durationLib.years(duration))
        except Exception as e:
            message: STRING = f"years({duration})"
            self.logError(message, e)
            return None

    def months(self, duration: DURATION) -> DECIMAL:
        try:
            return self.valueOf(self.durationLib.months(duration))
        except Exception as e:
            message: STRING = f"months({duration})"
            self.logError(message, e)
            return None

    def days(self, duration: DURATION) -> DECIMAL:
        try:
            return self.valueOf(self.durationLib.days(duration))
        except Exception as e:
            message: STRING = f"days({duration})"
            self.logError(message, e)
            return None

    def hours(self, duration: DURATION) -> DECIMAL:
        try:
            return self.valueOf(self.durationLib.hours(duration))
        except Exception as e:
            message: STRING = f"hours({duration})"
            self.logError(message, e)
            return None

    def minutes(self, duration: DURATION) -> DECIMAL:
        try:
            return self.valueOf(self.durationLib.minutes(duration))
        except Exception as e:
            message: STRING = f"minutes({duration})"
            self.logError(message, e)
            return None

    def seconds(self, duration: DURATION) -> DECIMAL:
        try:
            return self.valueOf(self.durationLib.seconds(duration))
        except Exception as e:
            message: STRING = f"seconds({duration})"
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
                self.logError(f"'{value1.getClass().getSimpleName()}' is not supported yet")
                return False

        except Exception as e:
            message: STRING = f"is({value1}, {value2})"
            self.logError(message, e)
            return False

    #
    # Temporal functions
    #

    def dayOfYear(self, date: DATE) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.dayOfYear(date))
        except Exception as e:
            message: STRING = f"dayOfYear({date})"
            self.logError(message, e)
            return None

    def dayOfWeek(self, date: DATE) -> STRING:
        try:
            return self.dateTimeLib.dayOfWeek(date)
        except Exception as e:
            message: STRING = f"dayOfWeek({date})"
            self.logError(message, e)
            return None

    def weekOfYear(self, date: DATE) -> DECIMAL:
        try:
            return self.valueOf(self.dateTimeLib.weekOfYear(date))
        except Exception as e:
            message: STRING = f"weekOfYear({date})"
            self.logError(message, e)
            return None

    def monthOfYear(self, date: DATE) -> STRING:
        try:
            return self.dateTimeLib.monthOfYear(date)
        except Exception as e:
            message: STRING = f"weekOfYear({date})"
            self.logError(message, e)
            return None

    #
    # List functions
    #

    def listContains(self, list_: LIST, element: Any) -> BOOLEAN:
        try:
            return self.listLib.listContains(list_, element)
        except Exception as e:
            message: STRING = f"listContains({list_}, {element})"
            self.logError(message, e)
            return None

    def append(self, list_: LIST, *items):
        try:
            return self.listLib.append(list_, *items)
        except Exception as e:
            message: STRING = f"append({list_}, {items})"
            self.logError(message, e)
            return None

    def count(self, list_: LIST) -> DECIMAL:
        try:
            return self.numberLib.count(list_)
        except Exception as e:
            message = f"count({list_})"
            self.logError(message, e)
            return None

    def min(self, *args) -> Optional[comparable]:
        try:
            return self.numberLib.min(*args)
        except Exception as e:
            message = f"min{args}"
            self.logError(message, e)
            return None

    def max(self, *args) -> Optional[comparable]:
        try:
            return self.numberLib.max(*args)
        except Exception as e:
            message = f"max{args}"
            self.logError(message, e)
            return None

    def sum(self, *args) -> Optional[comparable]:
        try:
            return self.numberLib.sum(*args)
        except Exception as e:
            message = f"sum{args}"
            self.logError(message, e)
            return None

    def sublist(self, list_: LIST, startPosition: DECIMAL, length: DECIMAL = None) -> LIST:
        try:
            return self.listLib.sublist(list_, self.intValue(startPosition), self.intValue(length))
        except Exception as e:
            message: STRING = f"sublist({list_}, {startPosition}, {length})"
            self.logError(message, e)
            return None

    def concatenate(self, *lists) -> LIST:
        try:
            return self.listLib.concatenate(*lists)
        except Exception as e:
            message: STRING = f"concatenate({str(lists)})"
            self.logError(message, e)
            return None

    def insertBefore(self, list_: LIST, position: DECIMAL, newItem: Any) -> LIST:
        try:
            return self.listLib.insertBefore(list_, self.intValue(position), newItem)
        except Exception as e:
            message: STRING = f"insertBefore({list_}, {position}, {newItem})"
            self.logError(message, e)
            return None

    def remove(self, list_: LIST, position: Any):
        try:
            return self.listLib.remove(list_, self.intValue(position))
        except Exception as e:
            message: STRING = f"remove({list_})"
            self.logError(message, e)
            return None

    def reverse(self, list_: LIST) -> LIST:
        try:
            return self.listLib.reverse(list_)
        except Exception as e:
            message: STRING = f"reverse({list_})"
            self.logError(message, e)
            return None

    def indexOf(self, list_: LIST, match: Any) -> LIST:
        result = []
        if list_ is not None:
            for i, o in enumerate(list_):
                if o is None and match is None or o is not None and o == match:
                    result.append(self.valueOf(i + 1))
        return result

    def union(self, *lists):
        try:
            return self.listLib.union(*lists)
        except Exception as e:
            message: STRING = f"union({str(lists)})"
            self.logError(message, e)
            return None

    def distinctValues(self, list_: LIST) -> LIST:
        try:
            return self.listLib.distinctValues(list_)
        except Exception as e:
            message: STRING = f"distinctValues({list_})"
            self.logError(message, e)
            return None

    def flatten(self, list_: LIST) -> LIST:
        try:
            return self.listLib.flatten(list_)
        except Exception as e:
            message: STRING = f"flatten({list_})"
            self.logError(message, e)
            return None

    def product(self, *args) -> DECIMAL:
        try:
            return self.numberLib.product(*args)
        except Exception as e:
            message: STRING = f"product({args})"
            self.logError(message, e)
            return None

    def median(self, *args) -> DECIMAL:
        try:
            return self.numberLib.median(*args)
        except Exception as e:
            message: STRING = f"median{args}"
            self.logError(message, e)
            return None

    def stddev(self, *args) -> DECIMAL:
        try:
            return self.numberLib.stddev(*args)
        except Exception as e:
            message: STRING = f"stddev{args}"
            self.logError(message, e)
            return None

    def mode(self, *args) -> LIST:
        try:
            return self.numberLib.mode(*args)
        except Exception as e:
            message: STRING = f"mode{args}"
            self.logError(message, e)
            return None

    def collect(self, result: LIST, list_: LIST) -> None:
        try:
            self.listLib.collect(result, list_)
        except Exception as e:
            message: STRING = f"collect({result}, {list_})"
            self.logError(message, e)

    def sort(self, list_: LIST, precedes: LambdaExpression) -> LIST:
        try:
            return self.listLib.sort(list_, precedes)
        except Exception as e:
            message: STRING = f"sort({list_})"
            self.logError(message, e)
            return None

    #
    # Range functions
    #

    def before(self, arg1: Any, arg2: Any) -> BOOLEAN:
        try:
            return self.rangeLib.before(arg1, arg2)
        except Exception as e:
            message: STRING = f"before({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def after(self, arg1: Any, arg2: Any) -> BOOLEAN:
        try:
            return self.rangeLib.after(arg1, arg2)
        except Exception as e:
            message: STRING = f"after({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def meets(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.meets(range1, range2)
        except Exception as e:
            message: STRING = f"meets({range1}, {range2})"
            self.logError(message, e)
            return None

    def metBy(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.metBy(range1, range2)
        except Exception as e:
            message: STRING = f"metBy({range1}, {range2})"
            self.logError(message, e)
            return None

    def overlaps(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.overlaps(range1, range2)
        except Exception as e:
            message: STRING = f"overlaps({range1}, {range2})"
            self.logError(message, e)
            return None

    def overlapsBefore(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.overlapsBefore(range1, range2)
        except Exception as e:
            message: STRING = f"overlapsBefore({range1}, {range2})"
            self.logError(message, e)
            return None

    def overlapsAfter(self, range1: Range, range2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.overlapsAfter(range1, range2)
        except Exception as e:
            message: STRING = f"overlapsAfter({range1}, {range2})"
            self.logError(message, e)
            return None

    def finishes(self, arg1: Any, arg2: Any) -> BOOLEAN:
        try:
            return self.rangeLib.finishes(arg1, arg2)
        except Exception as e:
            message: STRING = f"finishes({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def finishedBy(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.finishedBy(arg1, arg2)
        except Exception as e:
            message: STRING = f"finishedBy({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def includes(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.includes(arg1, arg2)
        except Exception as e:
            message: STRING = f"includes({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def during(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.during(arg1, arg2)
        except Exception as e:
            message: STRING = f"during({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def starts(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.starts(arg1, arg2)
        except Exception as e:
            message: STRING = f"starts({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def startedBy(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.startedBy(arg1, arg2)
        except Exception as e:
            message: STRING = f"startedBy({arg1}, {arg2})"
            self.logError(message, e)
            return None

    def coincides(self, arg1: Range, arg2: Range) -> BOOLEAN:
        try:
            return self.rangeLib.coincides(arg1, arg2)
        except Exception as e:
            message: STRING = f"coincides({arg1}, {arg2})"
            self.logError(message, e)
            return None
