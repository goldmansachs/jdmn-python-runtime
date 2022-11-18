#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License")or you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from typing import Any

from jdmn.feel.lib.FEELLib import FEELLib
from jdmn.feel.lib.Types import DECIMAL, BOOLEAN, DATE, TIME, DATE_TIME, DURATION, LIST, INTEGER, STRING, CONTEXT, RANGE
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType
from jdmn.feel.lib.type.context.DefaultContextType import DefaultContextType
from jdmn.feel.lib.type.function.DefaultFunctionType import DefaultFunctionType
from jdmn.feel.lib.type.list.DefaultListType import DefaultListType
from jdmn.feel.lib.type.numeric.DefaultNumericType import DefaultNumericType
from jdmn.feel.lib.type.range.DefaultRangeType import DefaultRangeType
from jdmn.feel.lib.type.string.DefaultStringType import DefaultStringType
from jdmn.feel.lib.type.time.DefaultDateTimeType import DefaultDateTimeType
from jdmn.feel.lib.type.time.DefaultDateType import DefaultDateType
from jdmn.feel.lib.type.time.DefaultDurationType import DefaultDurationType
from jdmn.feel.lib.type.time.DefaultTimeType import DefaultTimeType
from jdmn.runtime.LazyEval import LazyEval
from jdmn.runtime.listener.EventListener import EventListener
from jdmn.runtime.listener.Rule import Rule


class BaseFEELLib(FEELLib):
    # Types
    numericType = DefaultNumericType()
    booleanType = DefaultBooleanType()
    stringType = DefaultStringType()
    dateType = DefaultDateType()
    timeType = DefaultTimeType()
    dateTimeType = DefaultDateTimeType()
    durationType = DefaultDurationType()
    listType = DefaultListType()
    contextType = DefaultContextType()
    rangeType = DefaultRangeType()
    functionType = DefaultFunctionType()

    def __init__(self):
        FEELLib.__init__(self)

    #
    # Numeric operators
    #
    def isNumber(self, value: Any) -> bool:
        try:
            return self.numericType.isNumber(value)
        except Exception as e:
            message = "isNumber({})".format(value)
            self.logError(message, e)
            return False

    def numericValue(self, value: DECIMAL) -> DECIMAL:
        try:
            return self.numericType.numericValue(value)
        except Exception as e:
            message = "numericValue({})".format(value)
            self.logError(message, e)
            return None

    def numericIs(self, first: DECIMAL, second: DECIMAL) -> BOOLEAN:
        try:
            return self.numericType.numericIs(first, second)
        except Exception as e:
            message = "numericIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericEqual(self, first: DECIMAL, second: DECIMAL) -> BOOLEAN:
        try:
            return self.numericType.numericEqual(first, second)
        except Exception as e:
            message = "numericEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericNotEqual(self, first: DECIMAL, second: DECIMAL) -> BOOLEAN:
        try:
            return self.numericType.numericNotEqual(first, second)
        except Exception as e:
            message = "numericNotEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericLessThan(self, first: DECIMAL, second: DECIMAL) -> BOOLEAN:
        try:
            return self.numericType.numericLessThan(first, second)
        except Exception as e:
            message = "numericLessThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericGreaterThan(self, first: DECIMAL, second: DECIMAL) -> BOOLEAN:
        try:
            return self.numericType.numericGreaterThan(first, second)
        except Exception as e:
            message = "numericGreaterThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericLessEqualThan(self, first: DECIMAL, second: DECIMAL) -> BOOLEAN:
        try:
            return self.numericType.numericLessEqualThan(first, second)
        except Exception as e:
            message = "numericLessEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericGreaterEqualThan(self, first: DECIMAL, second: DECIMAL) -> BOOLEAN:
        try:
            return self.numericType.numericGreaterEqualThan(first, second)
        except Exception as e:
            message = "numericGreaterEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericAdd(self, first: DECIMAL, second: DECIMAL) -> DECIMAL:
        try:
            return self.numericType.numericAdd(first, second)
        except Exception as e:
            message = "numericAdd({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericSubtract(self, first: DECIMAL, second: DECIMAL) -> DECIMAL:
        try:
            return self.numericType.numericSubtract(first, second)
        except Exception as e:
            message = "numericSubtract({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericMultiply(self, first: DECIMAL, second: DECIMAL) -> DECIMAL:
        try:
            return self.numericType.numericMultiply(first, second)
        except Exception as e:
            message = "numericMultiply({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericDivide(self, first: DECIMAL, second: DECIMAL) -> DECIMAL:
        try:
            return self.numericType.numericDivide(first, second)
        except Exception as e:
            message = "numericDivide({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def numericUnaryMinus(self, first: DECIMAL) -> DECIMAL:
        try:
            return self.numericType.numericUnaryMinus(first)
        except Exception as e:
            message = "numericUnaryMinus({}".format(first)
            self.logError(message, e)
            return None

    def numericExponentiation(self, first: DECIMAL, second: DECIMAL) -> DECIMAL:
        try:
            return self.numericType.numericExponentiation(first, second)
        except Exception as e:
            message = "numericExponentiation({}, {})".format(first, second)
            self.logError(message, e)
            return None

    #
    # Boolean operators
    #
    def isBoolean(self, value: Any) -> BOOLEAN:
        try:
            return self.booleanType.isBoolean(value)
        except Exception as e:
            message = "isBoolean({})".format(value)
            self.logError(message, e)
            return False

    def booleanValue(self, value: BOOLEAN) -> BOOLEAN:
        try:
            return self.booleanType.booleanValue(value)
        except Exception as e:
            message = "booleanValue({})".format(value)
            self.logError(message, e)
            return None

    def booleanIs(self, first: BOOLEAN, second: BOOLEAN) -> BOOLEAN:
        try:
            return self.booleanType.booleanIs(first, second)
        except Exception as e:
            message = "booleanIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def booleanEqual(self, first: BOOLEAN, second: BOOLEAN) -> BOOLEAN:
        try:
            return self.booleanType.booleanEqual(first, second)
        except Exception as e:
            message = "booleanEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def booleanNotEqual(self, first: BOOLEAN, second: BOOLEAN) -> BOOLEAN:
        try:
            return self.booleanType.booleanNotEqual(first, second)
        except Exception as e:
            message = "booleanNotEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def booleanNot(self, operand: Any) -> BOOLEAN:
        try:
            return self.booleanType.booleanNot(operand)
        except Exception as e:
            message = "booleanNot({})".format(operand)
            self.logError(message, e)
            return None

    def booleanOr(self, *operands) -> BOOLEAN:
        try:
            return self.booleanType.booleanOr(*operands)
        except Exception as e:
            message = "booleanOr({})".format(operands)
            self.logError(message, e)
            return None

    def binaryBooleanOr(self, first: Any, second: Any) -> BOOLEAN:
        try:
            return self.booleanType.binaryBooleanOr(first, second)
        except Exception as e:
            message = "binaryBooleanOr({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def booleanAnd(self, *operands) -> BOOLEAN:
        try:
            return self.booleanType.booleanAnd(*operands)
        except Exception as e:
            message = "booleanAnd({})".format(operands)
            self.logError(message, e)
            return None

    def binaryBooleanAnd(self, first: Any, second: Any) -> BOOLEAN:
        try:
            return self.booleanType.binaryBooleanAnd(first, second)
        except Exception as e:
            message = "binaryBooleanAnd({}, {})".format(first, second)
            self.logError(message, e)
            return None

    #
    # String operators
    #
    def isString(self, value: Any) -> BOOLEAN:
        try:
            return self.stringType.isString(value)
        except Exception as e:
            message = "isString({})".format(value)
            self.logError(message, e)
            return False

    def stringValue(self, value: STRING) -> STRING:
        try:
            return self.stringType.stringValue(value)
        except Exception as e:
            message = "stringValue({})".format(value)
            self.logError(message, e)
            return None

    def stringIs(self, first: STRING, second: STRING) -> BOOLEAN:
        try:
            return self.stringType.stringIs(first, second)
        except Exception as e:
            message = "stringIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def stringEqual(self, first: STRING, second: STRING) -> BOOLEAN:
        try:
            return self.stringType.stringEqual(first, second)
        except Exception as e:
            message = "stringEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def stringNotEqual(self, first: STRING, second: STRING) -> BOOLEAN:
        try:
            return self.stringType.stringNotEqual(first, second)
        except Exception as e:
            message = "stringNotEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def stringLessThan(self, first: STRING, second: STRING) -> BOOLEAN:
        try:
            return self.stringType.stringLessThan(first, second)
        except Exception as e:
            message = "stringLessThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def stringGreaterThan(self, first: STRING, second: STRING) -> BOOLEAN:
        try:
            return self.stringType.stringGreaterThan(first, second)
        except Exception as e:
            message = "stringGreaterThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def stringLessEqualThan(self, first: STRING, second: STRING) -> BOOLEAN:
        try:
            return self.stringType.stringLessEqualThan(first, second)
        except Exception as e:
            message = "stringLessEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def stringGreaterEqualThan(self, first: STRING, second: STRING) -> BOOLEAN:
        try:
            return self.stringType.stringGreaterEqualThan(first, second)
        except Exception as e:
            message = "({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def stringAdd(self, first: STRING, second: STRING) -> STRING:
        try:
            return self.stringType.stringAdd(first, second)
        except Exception as e:
            message = "stringAdd({}, {})".format(first, second)
            self.logError(message, e)
            return None

    #
    # Date operators
    #
    def isDate(self, value: Any) -> BOOLEAN:
        try:
            return self.dateType.isDate(value)
        except Exception as e:
            message = "isDate({})".format(value)
            self.logError(message, e)
            return False

    def dateValue(self, date: DATE) -> INTEGER:
        try:
            return self.dateType.dateValue(date)
        except Exception as e:
            message = "dateValue({})".format(date)
            self.logError(message, e)
            return None

    def dateIs(self, first: DATE, second: DATE) -> BOOLEAN:
        try:
            return self.dateType.dateIs(first, second)
        except Exception as e:
            message = "dateIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateEqual(self, first: DATE, second: DATE) -> BOOLEAN:
        try:
            return self.dateType.dateEqual(first, second)
        except Exception as e:
            message = "dateEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateNotEqual(self, first: DATE, second: DATE) -> BOOLEAN:
        try:
            return self.dateType.dateNotEqual(first, second)
        except Exception as e:
            message = "dateNotEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateLessThan(self, first: DATE, second: DATE) -> BOOLEAN:
        try:
            return self.dateType.dateLessThan(first, second)
        except Exception as e:
            message = "dateLessThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateGreaterThan(self, first: DATE, second: DATE) -> BOOLEAN:
        try:
            return self.dateType.dateGreaterThan(first, second)
        except Exception as e:
            message = "dateGreaterThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateLessEqualThan(self, first: DATE, second: DATE) -> BOOLEAN:
        try:
            return self.dateType.dateLessEqualThan(first, second)
        except Exception as e:
            message = "dateLessEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateGreaterEqualThan(self, first: DATE, second: DATE) -> BOOLEAN:
        try:
            return self.dateType.dateGreaterEqualThan(first, second)
        except Exception as e:
            message = "dateGreaterEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateSubtract(self, first: DATE, second: DATE) -> DURATION:
        try:
            dateTime1: DATE_TIME = self.toDateTime(first)
            dateTime2: DATE_TIME = self.toDateTime(second)
            return self.dateTimeType.dateTimeSubtract(dateTime1, dateTime2)
        except Exception as e:
            message = "dateSubtract({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateAddDuration(self, date: DATE, duration: DURATION) -> DATE:
        try:
            return self.dateType.dateAddDuration(date, duration)
        except Exception as e:
            message = "dateAddDuration({}, {})".format(date, duration)
            self.logError(message, e)
            return None

    def dateSubtractDuration(self, date: DATE, duration: DURATION) -> DATE:
        try:
            return self.dateType.dateSubtractDuration(date, duration)
        except Exception as e:
            message = "dateSubtractDuration({}, {})".format(date, duration)
            self.logError(message, e)
            return None

    #
    # Time operators
    #
    def isTime(self, value: Any) -> BOOLEAN:
        try:
            return self.timeType.isTime(value)
        except Exception as e:
            message = "isTime({})".format(value)
            self.logError(message, e)
            return False

    def timeValue(self, time: TIME) -> INTEGER:
        try:
            return self.timeType.timeValue(time)
        except Exception as e:
            message = "timeValue({})".format(time)
            self.logError(message, e)
            return None

    def timeIs(self, first: TIME, second: TIME) -> BOOLEAN:
        try:
            return self.timeType.timeIs(first, second)
        except Exception as e:
            message = "timeIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeEqual(self, first: TIME, second: TIME) -> BOOLEAN:
        try:
            return self.timeType.timeEqual(first, second)
        except Exception as e:
            message = "timeEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeNotEqual(self, first: TIME, second: TIME) -> BOOLEAN:
        try:
            return self.timeType.timeNotEqual(first, second)
        except Exception as e:
            message = "timeNotEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeLessThan(self, first: TIME, second: TIME) -> BOOLEAN:
        try:
            return self.timeType.timeLessThan(first, second)
        except Exception as e:
            message = "timeLessThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeGreaterThan(self, first: TIME, second: TIME) -> BOOLEAN:
        try:
            return self.timeType.timeGreaterThan(first, second)
        except Exception as e:
            message = "timeGreaterThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeLessEqualThan(self, first: TIME, second: TIME) -> BOOLEAN:
        try:
            return self.timeType.timeLessEqualThan(first, second)
        except Exception as e:
            message = "timeLessEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeGreaterEqualThan(self, first: TIME, second: TIME) -> BOOLEAN:
        try:
            return self.timeType.timeGreaterEqualThan(first, second)
        except Exception as e:
            message = "timeGreaterEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeSubtract(self, first: TIME, second: TIME) -> DURATION:
        try:
            return self.timeType.timeSubtract(first, second)
        except Exception as e:
            message = "timeSubtract({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def timeAddDuration(self, time: TIME, duration: DURATION) -> TIME:
        try:
            return self.timeType.timeAddDuration(time, duration)
        except Exception as e:
            message = "timeAddDuration({}, {})".format(time, duration)
            self.logError(message, e)
            return None

    def timeSubtractDuration(self, time: TIME, duration: DURATION) -> TIME:
        try:
            return self.timeType.timeSubtractDuration(time, duration)
        except Exception as e:
            message = "timeSubtractDuration({}, {})".format(time, duration)
            self.logError(message, e)
            return None

    #
    # Date and Time operators
    #
    def isDateTime(self, value: Any) -> BOOLEAN:
        try:
            return self.dateTimeType.isDateTime(value)
        except Exception as e:
            message = "isDateTime({})".format(value)
            self.logError(message, e)
            return False

    def dateTimeValue(self, dateTime: DATE_TIME) -> INTEGER:
        try:
            return self.dateTimeType.dateTimeValue(dateTime)
        except Exception as e:
            message = "dateTimeValue({})".format(dateTime)
            self.logError(message, e)
            return None

    def dateTimeIs(self, first: DATE_TIME, second: DATE_TIME) -> BOOLEAN:
        try:
            return self.dateTimeType.dateTimeIs(first, second)
        except Exception as e:
            message = "dateTimeIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeEqual(self, first: DATE_TIME, second: DATE_TIME) -> BOOLEAN:
        try:
            return self.dateTimeType.dateTimeEqual(first, second)
        except Exception as e:
            message = "dateTimeEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeNotEqual(self, first: DATE_TIME, second: DATE_TIME) -> BOOLEAN:
        try:
            return self.dateTimeType.dateTimeNotEqual(first, second)
        except Exception as e:
            message = "dateTimeNotEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeLessThan(self, first: DATE_TIME, second: DATE_TIME) -> BOOLEAN:
        try:
            return self.dateTimeType.dateTimeLessThan(first, second)
        except Exception as e:
            message = "dateTimeLessThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeGreaterThan(self, first: DATE_TIME, second: DATE_TIME) -> BOOLEAN:
        try:
            return self.dateTimeType.dateTimeGreaterThan(first, second)
        except Exception as e:
            message = "dateTimeGreaterThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeLessEqualThan(self, first: DATE_TIME, second: DATE_TIME) -> BOOLEAN:
        try:
            return self.dateTimeType.dateTimeLessEqualThan(first, second)
        except Exception as e:
            message = "dateTimeLessEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeGreaterEqualThan(self, first: DATE_TIME, second: DATE_TIME) -> BOOLEAN:
        try:
            return self.dateTimeType.dateTimeGreaterEqualThan(first, second)
        except Exception as e:
            message = "dateTimeGreaterEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeSubtract(self, first: DATE_TIME, second: DATE_TIME) -> DURATION:
        try:
            if self.isDate(first):
                first = self.toDateTime(first)
            if self.isDate(second):
                second = self.toDateTime(second)

            return self.dateTimeType.dateTimeSubtract(first, second)
        except Exception as e:
            message = "dateTimeSubtract({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def dateTimeAddDuration(self, dateTime: DATE_TIME, duration: DURATION) -> DATE_TIME:
        try:
            return self.dateTimeType.dateTimeAddDuration(dateTime, duration)
        except Exception as e:
            message = "dateTimeAddDuration({}, {})".format(dateTime, duration)
            self.logError(message, e)
            return None

    def dateTimeSubtractDuration(self, dateTime: DATE_TIME, duration: DURATION) -> DATE_TIME:
        try:
            return self.dateTimeType.dateTimeSubtractDuration(dateTime, duration)
        except Exception as e:
            message = "dateTimeSubtractDuration({}, {})".format(dateTime, duration)
            self.logError(message, e)
            return None

    #
    # Duration operators
    #
    def isDuration(self, value: Any) -> BOOLEAN:
        try:
            return self.durationType.isDuration(value)
        except Exception as e:
            message = "isDuration({})".format(value)
            self.logError(message, e)
            return False

    def isYearsAndMonthsDuration(self, value: Any) -> BOOLEAN:
        try:
            return self.durationType.isYearsAndMonthsDuration(value)
        except Exception as e:
            message = "isYearsAndMonthsDuration({})".format(value)
            self.logError(message, e)
            return False

    def isDaysAndTimeDuration(self, value: Any) -> BOOLEAN:
        try:
            return self.durationType.isDaysAndTimeDuration(value)
        except Exception as e:
            message = "isDaysAndTimeDuration({})".format(value)
            self.logError(message, e)
            return False

    def durationIs(self, first: DURATION, second: DURATION) -> BOOLEAN:
        try:
            return self.durationType.durationIs(first, second)
        except Exception as e:
            message = "durationIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationValue(self, duration: DURATION) -> INTEGER:
        try:
            return self.durationType.durationValue(duration)
        except Exception as e:
            message = "durationValue({})".format(duration)
            self.logError(message, e)
            return None

    def durationEqual(self, first: DURATION, second: DURATION) -> BOOLEAN:
        try:
            return self.durationType.durationEqual(first, second)
        except Exception as e:
            message = "durationEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationNotEqual(self, first: DURATION, second: DURATION) -> BOOLEAN:
        try:
            return self.durationType.durationNotEqual(first, second)
        except Exception as e:
            message = "durationNotEqual({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationLessThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        try:
            return self.durationType.durationLessThan(first, second)
        except Exception as e:
            message = "durationLessThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationGreaterThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        try:
            return self.durationType.durationGreaterThan(first, second)
        except Exception as e:
            message = "durationGreaterThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationLessEqualThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        try:
            return self.durationType.durationLessEqualThan(first, second)
        except Exception as e:
            message = "durationLessEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationGreaterEqualThan(self, first: DURATION, second: DURATION) -> BOOLEAN:
        try:
            return self.durationType.durationGreaterEqualThan(first, second)
        except Exception as e:
            message = "durationGreaterEqualThan({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationAdd(self, first: DURATION, second: DURATION) -> DURATION:
        try:
            return self.durationType.durationAdd(first, second)
        except Exception as e:
            message = "durationAdd({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationSubtract(self, first: DURATION, second: DURATION) -> DURATION:
        try:
            return self.durationType.durationSubtract(first, second)
        except Exception as e:
            message = "durationSubtract({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationDivide(self, first: DURATION, second: DURATION) -> DECIMAL:
        try:
            return self.durationType.durationDivide(first, second)
        except Exception as e:
            message = "durationMultiply({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationMultiplyNumber(self, first: DURATION, second: DECIMAL) -> DURATION:
        try:
            return self.durationType.durationMultiplyNumber(first, second)
        except Exception as e:
            message = "durationMultiply({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def durationDivideNumber(self, first: DURATION, second: DECIMAL) -> DURATION:
        try:
            return self.durationType.durationDivideNumber(first, second)
        except Exception as e:
            message = "durationDivide({}, {})".format(first, second)
            self.logError(message, e)
            return None

    #
    # List operators
    #
    def isList(self, value: Any) -> BOOLEAN:
        try:
            return self.listType.isList(value)
        except Exception as e:
            message = "isList({})".format(value)
            self.logError(message, e)
            return False

    def listValue(self, value: LIST) -> LIST:
        try:
            return self.listType.listValue(value)
        except Exception as e:
            message = "listValue({})".format(value)
            self.logError(message, e)
            return None

    def listIs(self, first: LIST, second: LIST) -> BOOLEAN:
        try:
            return self.listType.listIs(first, second)
        except Exception as e:
            message = "listIs({}, {})".format(first, second)
            self.logError(message, e)
            return None

    def listEqual(self, list1: LIST, list2: LIST) -> BOOLEAN:
        try:
            return self.listType.listEqual(list1, list2)
        except Exception as e:
            message = "listEqual({}, {})".format(list1, list2)
            self.logError(message, e)
            return None

    def listNotEqual(self, list1: LIST, list2: LIST) -> BOOLEAN:
        try:
            return self.listType.listNotEqual(list1, list2)
        except Exception as e:
            message = "listNotEqual({}, {})".format(list1, list2)
            self.logError(message, e)
            return None

    #
    # Context operators
    #
    def isContext(self, value: Any) -> BOOLEAN:
        try:
            return self.contextType.isContext(value)
        except Exception as e:
            message = "isContext({})".format(value)
            self.logError(message, e)
            return False

    def contextValue(self, value: CONTEXT) -> CONTEXT:
        try:
            return self.contextType.contextValue(value)
        except Exception as e:
            message = "contextValue({})".format(value)
            self.logError(message, e)
            return None

    def contextIs(self, c1: CONTEXT, c2: CONTEXT) -> BOOLEAN:
        try:
            return self.contextType.contextIs(c1, c2)
        except Exception as e:
            message = "contextIs({}, {})".format(c1, c2)
            self.logError(message, e)
            return None

    def contextEqual(self, c1: CONTEXT, c2: CONTEXT) -> BOOLEAN:
        try:
            return self.contextType.contextEqual(c1, c2)
        except Exception as e:
            message = "contextEqual({}, {})".format(c1, c2)
            self.logError(message, e)
            return None

    def contextNotEqual(self, c1: CONTEXT, c2: CONTEXT) -> BOOLEAN:
        try:
            return self.contextType.contextNotEqual(c1, c2)
        except Exception as e:
            message = "contextNotEqual({}, {})".format(c1, c2)
            self.logError(message, e)
            return None

    #
    # Context functions
    #
    def getEntries(self, m: CONTEXT) -> LIST:
        try:
            return self.contextType.getEntries(m)
        except Exception as e:
            message = "getEntries({})".format(m)
            self.logError(message, e)
            return None

    def getValue(self, m: CONTEXT, key: Any) -> Any:
        try:
            return self.contextType.getValue(m, key)
        except Exception as e:
            message = "getValue({}, {})".format(m, key)
            self.logError(message, e)
            return None

    #
    # Range operators
    #
    def isRange(self, value: Any) -> BOOLEAN:
        try:
            return self.rangeType.isRange(value)
        except Exception as e:
            message = "isRange({})".format(value)
            self.logError(message, e)
            return False

    def rangeValue(self, value: RANGE) -> RANGE:
        try:
            return self.rangeType.rangeValue(value)
        except Exception as e:
            message = "rangeValue({})".format(value)
            self.logError(message, e)
            return None

    def rangeIs(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        try:
            return self.rangeType.rangeIs(range1, range2)
        except Exception as e:
            message = "rangeIs({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    def rangeEqual(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        try:
            return self.rangeType.rangeEqual(range1, range2)
        except Exception as e:
            message = "rangeEqual({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    def rangeNotEqual(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        try:
            return self.rangeType.rangeNotEqual(range1, range2)
        except Exception as e:
            message = "rangeNotEqual({}, {})".format(range1, range2)
            self.logError(message, e)
            return None

    #
    # Function operators
    #
    def isFunction(self, value: Any) -> BOOLEAN:
        try:
            return self.functionType.isFunction(value)
        except Exception as e:
            message = "isFunction({})".format(value)
            self.logError(message, e)
            return False

    def functionValue(self, value: Any) -> Any:
        try:
            return self.functionType.functionValue(value)
        except Exception as e:
            message = "functionValue({})".format(value)
            self.logError(message, e)
            return None

    def functionIs(self, function1: Any, function2: Any) -> BOOLEAN:
        try:
            return self.functionType.functionIs(function1, function2)
        except Exception as e:
            message = "functionIs({}, {})".format(function1, function2)
            self.logError(message, e)
            return None

    def functionEqual(self, function1: Any, function2: Any) -> BOOLEAN:
        try:
            return self.functionType.functionEqual(function1, function2)
        except Exception as e:
            message = "functionEqual({}, {})".format(function1, function2)
            self.logError(message, e)
            return None

    def functionNotEqual(self, function1: Any, function2: Any) -> BOOLEAN:
        try:
            return self.functionType.functionNotEqual(function1, function2)
        except Exception as e:
            message = "functionNotEqual({}, {})".format(function1, function2)
            self.logError(message, e)
            return None

    #
    # Conversion functions
    #
    @staticmethod
    def asList(*args) -> LIST:
        if len(args) == 0:
            return []
        else:
            return list(args)

    @staticmethod
    def asElement(list_: LIST) -> Any:
        if list_ is None:
            return None
        elif len(list_) == 1:
            return list_[0]
        else:
            return None

    #
    # Other functions
    #
    def rangeToList(self, *args) -> LIST:
        len_ = len(args)
        if len_ == 2:
            arg1 = args[0]
            arg2 = args[1]
            return self.rangeToListWithArgs(False, arg1, False, arg2)
        elif len_ == 4:
            return self.rangeToListWithArgs(args[0], args[1], args[2], args[3])
        else:
            return None

    def rangeToListWithArgs(self, isOpenStart: bool, start: DECIMAL, isOpenEnd: bool, end: DECIMAL) -> LIST:
        if start is None or end is None:
            return []
        else:
            range_ = self.intRange(isOpenStart, start, isOpenEnd, end)
            return list(range_)

    @staticmethod
    def intRange(isOpenStart: bool, start: DECIMAL, isOpenEnd: bool, end: DECIMAL):
        if start is None or end is None:
            return None

        startValue: int = int(start) + 1 if isOpenStart else int(start)
        endValue: int = int(end) - 1 if isOpenEnd else int(end)
        if startValue <= endValue:
            return range(startValue, endValue + 1)
        else:
            return range(startValue, endValue - 1, -1)

    @staticmethod
    def flattenFirstLevel(list_: LIST) -> LIST:
        if list_ is None:
            return None

        result = []
        for obj in list_:
            if isinstance(obj, list):
                result.extend(obj)
            else:
                result.append(obj)

        return result

    @staticmethod
    def elementAt(list_: LIST, number: DECIMAL) -> Any:
        if list_ is None:
            return None

        index = int(number)

        listSize = len(list_)
        if 1 <= index <= listSize:
            return list_[index - 1]
        elif -listSize <= index <= -1:
            return list_[listSize + index]
        else:
            return None

    @staticmethod
    def ruleMatches(eventListener: EventListener, rule: Rule, *operands) -> bool:
        if (operands is None or len(operands) == 0):
            return False
        else:
            for i, operand in enumerate(operands):
                if isinstance(operand, LazyEval):
                    operand = operand.getOrCompute()

                # Column index starts first 1
                eventListener.matchColumn(rule, i + 1, operand)

                if operand is None or operand is False:
                    return False
            return True

    def valueOf(self, number: int) -> DECIMAL:
        raise NotImplementedError()

    def intValue(self, number: DECIMAL) -> int:
        raise NotImplementedError()
