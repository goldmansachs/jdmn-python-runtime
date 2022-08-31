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
from jdmn.feel.lib.BaseStandardFEELLibTest import BaseStandardFEELLibTest


class DefaultStandardFEELLibTest(BaseStandardFEELLibTest):
    """
    Base test class for DefaultStandardFEELLib
    """
    __test__ = False

    #
    # Time operators
    #
    def testTimeIs(self):
        super().testTimeIs()

        # times with equivalent offset and zone id are not is()
        self.assertFalse(self.getLib().timeIs(self.makeTime("12:00:00"), self.makeTime("12:00:00Z")))
        self.assertFalse(self.getLib().timeIs(self.makeTime("12:00:00"), self.makeTime("12:00:00+00:00")))
        self.assertFalse(self.getLib().timeIs(self.makeTime("00:00:00+00:00"), self.makeTime("00:00:00@Etc/UTC")))
        self.assertTrue(self.getLib().timeIs(self.makeTime("00:00:00Z"), self.makeTime("00:00:00+00:00")))
        self.assertFalse(self.getLib().timeIs(self.makeTime("00:00:00Z"), self.makeTime("00:00:00@Etc/UTC")))

    #
    # Date time operators
    #
    def testDateTimeIs(self):
        super().testDateTimeIs()

        # datetime with equivalent offset and zone id are not is()
        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T12:00:00"), self.makeDateAndTime("2018-12-08T12:00:00+00:00")))
        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00+00:00"), self.makeDateAndTime("2018-12-08T00:00:00@Etc/UTC")))
        self.assertTrue(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T12:00:00Z"), self.makeDateAndTime("2018-12-08T12:00:00+00:00")))
        self.assertFalse(self.getLib().dateTimeIs(self.makeDateAndTime("2018-12-08T00:00:00Z"), self.makeDateAndTime("2018-12-08T00:00:00@Etc/UTC")))

    #
    # Conversion functions
    #
    def testDate(self):
        super().testDate()

        self.assertEqualsDateTime("2016-08-01", self.getLib().date(self.makeDateAndTime("2016-08-01T12:00:00Z")))

    def testTime(self):
        super().testTime()

        #
        # conversion from time, date and date time
        #
        self.assertEqualsDateTime("12:00:00Z", self.getLib().time(self.makeTime("12:00:00Z")))
        self.assertEqualsDateTime("00:00:00Z", self.getLib().time(self.getLib().date("2017-08-10")))
        self.assertEqualsDateTime("11:00:00Z", self.getLib().time(self.makeDateAndTime("2016-08-01T11:00:00Z")))

        #
        # conversion from numbers
        #
        self.assertEqualsDateTime("12:00:00", self.getLib().time(self.makeNumber("12"), self.makeNumber("00"), self.makeNumber("00"), None))

        #
        # conversion from date, time and date time
        #
        self.assertEqualsDateTime("00:00:00Z", self.getLib().time(self.getLib().date("2017-08-10")))
        self.assertEqualsDateTime("12:00:00Z", self.getLib().time(self.makeTime("12:00:00Z")))
        self.assertEqualsDateTime("11:00:00Z", self.getLib().time(self.makeDateAndTime("2016-08-01T11:00:00Z")))

    def testDateTime(self):
        super().testDateTime()

        #
        # conversion from string
        #
        self.assertEqualsDateTime("2016-08-01T00:00:00", self.getLib().dateAndTime("2016-08-01"))

        # missing Z
        self.assertEqualsDateTime("-2016-01-30T09:05:00", self.getLib().dateAndTime("-2016-01-30T09:05:00"))
        self.assertEqualsDateTime("-2017-02-28T02:02:02", self.getLib().dateAndTime("-2017-02-28T02:02:02"))

        # with zone id
        self.assertEqualsDateTime("2011-12-03T10:15:30@Europe/Paris", self.getLib().dateAndTime("2011-12-03T10:15:30@Europe/Paris"))

        # year must be in the range [-999,999,999..999,999,999]
        self.assertEqualsDateTime("-999999999-12-31T11:22:33", self.getLib().dateAndTime("-999999999-12-31T11:22:33"))
        self.assertEqualsDateTime("999999999-12-31T11:22:33", self.getLib().dateAndTime("999999999-12-31T11:22:33"))
        self.assertIsNone(self.getLib().dateAndTime("-9999999991-12-31T11:22:33"))
        self.assertIsNone(self.getLib().dateAndTime("9999999991-12-31T11:22:33"))

    def testYearsAndMonthsDuration(self):
        super().testYearsAndMonthsDuration()

        self.assertEqualsDateTime("P0Y0M", self.getLib().yearsAndMonthsDuration(self.makeDateAndTime("2015-12-24T12:15:00.000+01:00"),
                                                                                self.makeDateAndTime("2015-12-24T12:15:00.000+01:00")))
        self.assertEqualsDateTime("P1Y2M", self.getLib().yearsAndMonthsDuration(self.makeDateAndTime("2016-09-30T23:25:00"), self.makeDateAndTime("2017-12-28T12:12:12")))
        self.assertEqualsDateTime("P7Y6M", self.getLib().yearsAndMonthsDuration(self.makeDateAndTime("2010-05-30T03:55:58"), self.makeDateAndTime("2017-12-15T00:59:59")))
        self.assertEqualsDateTime("-P4033Y2M", self.getLib().yearsAndMonthsDuration(self.makeDateAndTime("2014-12-31T23:59:59"), self.makeDateAndTime("-2019-10-01T12:32:59")))
        self.assertEqualsDateTime("-P4035Y11M",
                                  self.getLib().yearsAndMonthsDuration(self.makeDateAndTime("2017-09-05T10:20:00-01:00"), self.makeDateAndTime("-2019-10-01T12:32:59+02:00")))

        self.assertEqualsDateTime("P0Y0M", self.getLib().yearsAndMonthsDuration(self.getLib().dateAndTime("2015-12-24T12:15:00.000+01:00"),
                                                                                self.getLib().dateAndTime("2015-12-24T12:15:00.000+01:00")))

    def testString(self):
        self.assertEqual("None", self.getLib().string(None))

        # test number
        self.assertEqual("123.45", self.getLib().string(self.makeNumber("123.45")))

        # test string
        self.assertEqual("True", self.getLib().string(True))

        # test date
        self.assertEqual("2016-08-01", self.getLib().string(self.makeDate("2016-08-01")))
#        self.assertEqual("999999999-12-31", self.getLib().string(self.getLib().date("999999999-12-31")))
#        self.assertEqual("-999999999-12-31", self.getLib().string(self.getLib().date("-999999999-12-31")))
#        self.assertEqual("999999999-12-31", self.getLib().string(self.getLib().date(self.makeNumber(999999999), self.makeNumber(12), self.makeNumber(31))))
#        self.assertEqual("-999999999-12-31", self.getLib().string(self.getLib().date(self.makeNumber(-999999999), self.makeNumber(12), self.makeNumber(31))))

        # test time
        self.assertEqual("11:00:01+00:00", self.getLib().string(self.makeTime("11:00:01Z")))
#        self.assertEqual("11:00:01Z", self.getLib().string(self.makeTime("11:00:01Z")))
#        self.assertEqual("00:01:00@Etc/UTC", self.getLib().string(self.getLib().time("00:01:00@Etc/UTC")))
#        self.assertEqual("00:01:00@Europe/Paris", self.getLib().string(self.getLib().time("00:01:00@Europe/Paris")))
#        self.assertEqual("10:20:00@Europe/Paris", self.getLib().string(self.getLib().time(self.getLib().dateAndTime("2017-08-10T10:20:00@Europe/Paris"))))
#        self.assertEqual("11:20:00@Asia/Dhaka", self.getLib().string(self.getLib().time(self.getLib().dateAndTime("2017-09-04T11:20:00@Asia/Dhaka"))))
#        self.assertEqual("11:59:45+02:45:55",
#                         self.getLib().string(self.getLib().time(self.makeNumber(11), self.makeNumber(59), self.makeNumber(45), self.getLib().duration("PT2H45M55S"))))
#        self.assertEqual("11:59:45-02:45:55",
#                         self.getLib().string(self.getLib().time(self.makeNumber(11), self.makeNumber(59), self.makeNumber(45), self.getLib().duration("-PT2H45M55S"))))
#        self.assertEqual("00:00:00Z", self.getLib().string(self.getLib().time(self.getLib().date("2017-08-10"))))

        # test date time
        self.assertEqual("2016-08-01T11:00:01+00:00", self.getLib().string(self.makeDateAndTime("2016-08-01T11:00:01Z")))
#        self.assertEqual("2016-08-01T11:00:01Z", self.getLib().string(self.makeDateAndTime("2016-08-01T11:00:01Z")))
#        self.assertEqual("99999-12-31T11:22:33", self.getLib().string(self.getLib().dateAndTime("99999-12-31T11:22:33")))
#        self.assertEqual("-99999-12-31T11:22:33", self.getLib().string(self.getLib().dateAndTime("-99999-12-31T11:22:33")))
#        self.assertEqual("2011-12-31T10:15:30@Europe/Paris", self.getLib().string(self.getLib().dateAndTime("2011-12-31T10:15:30@Europe/Paris")))
#        self.assertEqual("2011-12-31T10:15:30@Etc/UTC", self.getLib().string(self.getLib().dateAndTime("2011-12-31T10:15:30@Etc/UTC")))
#        self.assertEqual("2011-12-31T10:15:30.987@Europe/Paris", self.getLib().string(self.getLib().dateAndTime("2011-12-31T10:15:30.987@Europe/Paris")))
#        self.assertEqual("2011-12-31T10:15:30.123456789@Europe/Paris", self.getLib().string(self.getLib().dateAndTime("2011-12-31T10:15:30.123456789@Europe/Paris")))
#        self.assertEqual("999999999-12-31T23:59:59.999999999@Europe/Paris", self.getLib().string(self.getLib().dateAndTime("999999999-12-31T23:59:59.999999999@Europe/Paris")))
#        self.assertEqual("-999999999-12-31T23:59:59.999999999+02:00", self.getLib().string(self.getLib().dateAndTime("-999999999-12-31T23:59:59.999999999+02:00")))
#        self.assertEqual("2017-01-01T23:59:01@Europe/Paris",
#                         self.getLib().string(self.getLib().dateAndTime(self.getLib().date("2017-01-01"), self.getLib().time("23:59:01@Europe/Paris"))))
#        self.assertEqual("2017-01-01T23:59:01.123456789@Europe/Paris",
#                         self.getLib().string(self.getLib().dateAndTime(self.getLib().date("2017-01-01"), self.getLib().time("23:59:01.123456789@Europe/Paris"))))
#        self.assertEqual("2017-09-05T09:15:30.987654321@Europe/Paris",
#                         self.getLib().string(self.getLib().dateAndTime(self.getLib().dateAndTime("2017-09-05T10:20:00"), self.getLib().time("09:15:30.987654321@Europe/Paris"))))
#        self.assertEqual("2017-09-05T09:15:30.987654321@Europe/Paris", self.getLib().string(
#            self.getLib().dateAndTime(self.getLib().dateAndTime("2017-09-05T10:20:00-01:00"), self.getLib().time("09:15:30.987654321@Europe/Paris"))))
#        self.assertEqual("2017-09-05T09:15:30.987654321@Europe/Paris", self.getLib().string(
#            self.getLib().dateAndTime(self.getLib().dateAndTime("2017-09-05T10:20:00@Europe/Paris"), self.getLib().time("09:15:30.987654321@Europe/Paris"))))

    #
    # Time properties
    #
    def testTimeProperties(self):
        self.assertIsNone(self.getLib().hour(None))
        self.assertEqualsNumber(self.makeNumber("12"), self.getLib().hour(self.getLib().time("12:01:02Z")))

        self.assertIsNone(self.getLib().minute(None))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().minute(self.getLib().time("12:01:02Z")))

        self.assertIsNone(self.getLib().second(None))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().second(self.getLib().time("12:01:02Z")))

        self.assertIsNone(self.getLib().timeOffset(None))
        self.assertIsNone(self.getLib().timeOffset(self.getLib().time("12:01:02")))
        self.assertEqual(self.getLib().duration("PT1H"), self.getLib().timeOffset(self.getLib().time("12:01:02+01:00")))
        self.assertEqual(self.getLib().duration("P0Y0M0DT0H0M0.000S"), self.getLib().timeOffset(self.getLib().time("12:01:02Z")))
        self.assertIsNone(self.getLib().timeOffset(self.getLib().time("12:01:02Z@Etc/UTC")))

        self.assertIsNone(self.getLib().timezone(None))
        self.assertIsNone(self.getLib().timezone(self.getLib().time("12:01:02")))
        self.assertEqual("+01:00", self.getLib().timezone(self.getLib().time("12:01:02+01:00")))
        self.assertEqual("Z", self.getLib().timezone(self.getLib().time("12:01:02Z")))
        self.assertEqual("Etc/UTC", self.getLib().timezone(self.getLib().time("12:01:02@Etc/UTC")))
        self.assertIsNone(self.getLib().timezone(self.getLib().time("12:01:02Z@Etc/UTC")))

    #
    # Date and time properties
    #
    def testDateAndTimeProperties(self):
        self.assertIsNone(self.getLib().year(None))
        self.assertEqualsNumber(self.makeNumber("2018"), self.getLib().year(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))

        self.assertIsNone(self.getLib().month(None))
        self.assertEqualsNumber(self.makeNumber("12"), self.getLib().month(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))

        self.assertIsNone(self.getLib().day(None))
        self.assertEqualsNumber(self.makeNumber("10"), self.getLib().day(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))

        self.assertIsNone(self.getLib().weekday(None))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().weekday(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))

        self.assertIsNone(self.getLib().hour(None))
        self.assertEqualsNumber(self.makeNumber("12"), self.getLib().hour(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))

        self.assertIsNone(self.getLib().minute(None))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().minute(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))

        self.assertIsNone(self.getLib().second(None))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().second(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))

        self.assertIsNone(self.getLib().timeOffset(None))
        self.assertIsNone(self.getLib().timeOffset(self.getLib().dateAndTime("2018-12-10T12:01:02")))
        self.assertEqual(self.getLib().duration("PT1H"), self.getLib().timeOffset(self.getLib().dateAndTime("2018-12-10T12:01:02+01:00")))
        self.assertEqual(self.getLib().duration("P0Y0M0DT0H0M0.000S"), self.getLib().timeOffset(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))
        self.assertIsNone(self.getLib().timeOffset(self.getLib().dateAndTime("2018-12-10T12:01:02Z@Etc/UTC")))

        self.assertIsNone(self.getLib().timezone(None))
        self.assertIsNone(self.getLib().timezone(self.getLib().dateAndTime("2018-12-10T12:01:02")))
        self.assertEqual("+01:00", self.getLib().timezone(self.getLib().dateAndTime("2018-12-10T12:01:02+01:00")))
        self.assertEqual("Z", self.getLib().timezone(self.getLib().dateAndTime("2018-12-10T12:01:02Z")))
        self.assertEqual("Etc/UTC", self.getLib().timezone(self.getLib().dateAndTime("2018-12-10T12:01:02@Etc/UTC")))
        self.assertIsNone(self.getLib().timezone(self.getLib().dateAndTime("2018-12-10T12:01:02Z@Etc/UTC")))
