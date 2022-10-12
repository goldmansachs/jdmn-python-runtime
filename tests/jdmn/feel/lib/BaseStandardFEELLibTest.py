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
from jdmn.feel.lib.BaseFEELLibTest import BaseFEELLibTest
from jdmn.feel.lib.Types import STRING
from jdmn.runtime.Context import Context
from jdmn.runtime.LambdaExpression import LambdaExpression
from jdmn.runtime.Range import Range


class BaseStandardFEELLibTest(BaseFEELLibTest):
    """
    Base test class for BaseStandardFEELLib
    """
    __test__ = False

    #
    # Conversion functions
    #
    def testNumberWithSeparators(self):
        self.assertIsNone(self.getLib().number(None, None, None))
        self.assertIsNone(self.getLib().number(None, ".", ","))
        self.assertIsNone(self.getLib().number("1.235.00", ".", "."))
        self.assertIsNone(self.getLib().number("12,356,00", ".", ","))

        self.assertEqualsNumber(self.makeNumber("12356"), self.getLib().number("12.356,00", ".", ","))
        self.assertEqualsNumber(self.makeNumber("12356"), self.getLib().number("12.356", ".", ","))
        self.assertEqualsNumber(self.makeNumber("12356.01"), self.getLib().number("12356,01", ".", ","))

        self.assertEqualsNumber(self.makeNumber("12356"), self.getLib().number("12,356.00", ",", "."))
        self.assertEqualsNumber(self.makeNumber("12356"), self.getLib().number("12,356", ",", "."))
        self.assertEqualsNumber(self.makeNumber("12356.01"), self.getLib().number("12356.01", ",", "."))

        self.assertEqualsNumber(self.makeNumber("1000000.01"), self.getLib().number("1000000.01", None, "."))
        self.assertEqualsNumber(self.makeNumber("1000000.00"), self.getLib().number("1,000,000", ",", None))
        self.assertEqualsNumber(self.makeNumber("1000000.00"), self.getLib().number("1,000,000.00", ",", None))
        self.assertEqualsNumber(self.makeNumber("1000000.01"), self.getLib().number("1.000.000,01", ".", ","))

    def testDuration(self):
        self.assertEqualsDateTime("P1Y8M", self.getLib().duration("P1Y8M"))
        self.assertEqualsDateTime("P2DT20H", self.getLib().duration("P2DT20H"))
        self.assertEqualsDateTime("-PT2H", self.getLib().duration("-PT2H"))

        self.assertEqualsDateTime("P1Y8M", self.getLib().duration("P1Y8M"))
        self.assertEqualsDateTime("P2DT20H", self.getLib().duration("P2DT20H"))

        self.assertEqualsDateTime("P999999999M", self.getLib().duration("P999999999M"))
        self.assertEqualsDateTime("-P999999999M", self.getLib().duration("-P999999999M"))
        self.assertEqualsDateTime("P1Y0M2DT6H58M59.000S", self.getLib().duration("P1Y0M2DT6H58M59.000S"))
        # Overflow in duration(from)
        self.assertEqualsDateTime("P11999999988M", self.getLib().duration("P11999999988M"))
#        self.assertEqualsDateTime("P2129706043D", self.getLib().duration("P2129706043D"))
#        self.assertEqualsDateTime("PT0S", self.getLib().duration("PT0.S"))

    def testYearsAndMonthsDuration(self):
        self.assertIsNone(self.getLib().yearsAndMonthsDuration(None, None))

        self.assertEqualsDateTime("P0Y0M", self.getLib().yearsAndMonthsDuration(self.makeDate("2015-12-24"), self.makeDate("2015-12-24")))
        self.assertEqualsDateTime("P1Y2M", self.getLib().yearsAndMonthsDuration(self.makeDate("2016-09-30"), self.makeDate("2017-12-28")))
        self.assertEqualsDateTime("P7Y6M", self.getLib().yearsAndMonthsDuration(self.makeDate("2010-05-30"), self.makeDate("2017-12-15")))
#        self.assertEqualsDateTime("-P4033Y2M", self.getLib().yearsAndMonthsDuration(self.makeDate("2014-12-31"), self.makeDate("-2019-10-01")))
#        self.assertEqualsDateTime("-P4035Y11M", self.getLib().yearsAndMonthsDuration(self.makeDate("2017-09-05"), self.makeDate("-2019-10-01")))

    #
    # Numeric functions
    #
    def testDecimal(self):
        self.assertIsNone(self.getLib().decimal(None, None))
        self.assertIsNone(self.getLib().decimal(None, self.makeNumber("128")))
        self.assertIsNone(self.getLib().decimal(self.makeNumber("10"), None))

#        self.assertEqualsNumber(self.makeNumber("-10"), self.getLib().decimal(self.makeNumber("-10"), self.makeNumber(Long.MAX_VALUE)))

        self.assertEqualsNumber(self.makeNumber("0.33"), self.getLib().decimal(self.makeNumber("0.333"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().decimal(self.makeNumber("1.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().decimal(self.makeNumber("2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("10.00"), self.getLib().decimal(self.makeNumber("10.001"), self.makeNumber("2")))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("10.00"), self.getLib().decimal(self.makeNumber("12.001"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("0E+2"), self.getLib().decimal(self.makeNumber("12.001"), self.makeNumber("-2")))
        self.assertEqualsNumber(self.makeNumber("0E+3"), self.getLib().decimal(self.makeNumber("12.001"), self.makeNumber("-3")))

    def testRoundWithUpMode(self):
        self.assertIsNone(self.getLib().round(None, None, None))
        self.assertIsNone(self.getLib().round(None, self.makeNumber("128"), None))
        self.assertIsNone(self.getLib().round(self.makeNumber("10"), self.makeNumber("2"), None))
        self.assertIsNone(self.getLib().round(self.makeNumber("10"), self.makeNumber("2"), "abc"))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().round(self.makeNumber("5.5"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().round(self.makeNumber("2.5"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("1.6"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("1.1"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.0"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.0"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-1.1"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-1.6"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("-3"), self.getLib().round(self.makeNumber("-2.5"), self.makeNumber("0"), "up"))
        self.assertEqualsNumber(self.makeNumber("-6"), self.getLib().round(self.makeNumber("-5.5"), self.makeNumber("0"), "up"))

        self.assertEqualsNumber(self.makeNumber("5.13"), self.getLib().round(self.makeNumber("5.125"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("2.13"), self.getLib().round(self.makeNumber("2.125"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().round(self.makeNumber("1.126"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().round(self.makeNumber("1.121"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.120"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.120"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().round(self.makeNumber("-1.121"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().round(self.makeNumber("-1.126"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("-2.13"), self.getLib().round(self.makeNumber("-2.125"), self.makeNumber("2"), "up"))
        self.assertEqualsNumber(self.makeNumber("-5.13"), self.getLib().round(self.makeNumber("-5.125"), self.makeNumber("2"), "up"))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.3E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-1"), "up"))
        self.assertEqualsNumber(self.makeNumber("-1.3E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-1"), "up"))
        self.assertEqualsNumber(self.makeNumber("2E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-2"), "up"))
        self.assertEqualsNumber(self.makeNumber("-2E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-2"), "up"))

    def testRoundWithDownMode(self):
        self.assertIsNone(self.getLib().round(None, None, "down"))
        self.assertIsNone(self.getLib().round(None, self.makeNumber("128"), "down"))
        self.assertIsNone(self.getLib().round(self.makeNumber("10"), None, "down"))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("5"), self.getLib().round(self.makeNumber("5.5"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("2.5"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.6"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.1"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.0"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.0"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.1"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.6"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-2.5"), self.makeNumber("0"), "down"))
        self.assertEqualsNumber(self.makeNumber("-5"), self.getLib().round(self.makeNumber("-5.5"), self.makeNumber("0"), "down"))

        self.assertEqualsNumber(self.makeNumber("5.12"), self.getLib().round(self.makeNumber("5.125"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("2.12"), self.getLib().round(self.makeNumber("2.125"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.126"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.121"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.120"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.120"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.121"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.126"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("-2.12"), self.getLib().round(self.makeNumber("-2.125"), self.makeNumber("2"), "down"))
        self.assertEqualsNumber(self.makeNumber("-5.12"), self.getLib().round(self.makeNumber("-5.125"), self.makeNumber("2"), "down"))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.2E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-1"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1.2E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-1"), "down"))
        self.assertEqualsNumber(self.makeNumber("1E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-2"), "down"))
        self.assertEqualsNumber(self.makeNumber("-1E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-2"), "down"))

    def testRoundWithHalfUpMode(self):
        self.assertIsNone(self.getLib().round(None, None, "half up"))
        self.assertIsNone(self.getLib().round(None, self.makeNumber("128"), "half up"))
        self.assertIsNone(self.getLib().round(self.makeNumber("10"), None, "half up"))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().round(self.makeNumber("5.5"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().round(self.makeNumber("2.5"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("1.6"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.1"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.0"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.0"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.1"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-1.6"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-3"), self.getLib().round(self.makeNumber("-2.5"), self.makeNumber("0"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-6"), self.getLib().round(self.makeNumber("-5.5"), self.makeNumber("0"), "half up"))

        self.assertEqualsNumber(self.makeNumber("5.13"), self.getLib().round(self.makeNumber("5.125"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("2.13"), self.getLib().round(self.makeNumber("2.125"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().round(self.makeNumber("1.126"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.121"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.120"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.120"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.121"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().round(self.makeNumber("-1.126"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-2.13"), self.getLib().round(self.makeNumber("-2.125"), self.makeNumber("2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-5.13"), self.getLib().round(self.makeNumber("-5.125"), self.makeNumber("2"), "half up"))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.3E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-1"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-1.3E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-1"), "half up"))
        self.assertEqualsNumber(self.makeNumber("1E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-2"), "half up"))
        self.assertEqualsNumber(self.makeNumber("-1E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-2"), "half up"))

    def testRoundWithHalfDownMode(self):
        self.assertIsNone(self.getLib().round(None, None, "half down"))
        self.assertIsNone(self.getLib().round(None, self.makeNumber("128"), "half down"))
        self.assertIsNone(self.getLib().round(self.makeNumber("10"), None, "half down"))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("5"), self.getLib().round(self.makeNumber("5.5"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("2.5"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("1.6"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.1"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.0"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.0"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.1"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-1.6"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-2.5"), self.makeNumber("0"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-5"), self.getLib().round(self.makeNumber("-5.5"), self.makeNumber("0"), "half down"))

        self.assertEqualsNumber(self.makeNumber("5.12"), self.getLib().round(self.makeNumber("5.125"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("2.12"), self.getLib().round(self.makeNumber("2.125"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().round(self.makeNumber("1.126"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.121"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.120"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.120"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.121"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().round(self.makeNumber("-1.126"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-2.12"), self.getLib().round(self.makeNumber("-2.125"), self.makeNumber("2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-5.12"), self.getLib().round(self.makeNumber("-5.125"), self.makeNumber("2"), "half down"))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.3E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-1"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-1.3E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-1"), "half down"))
        self.assertEqualsNumber(self.makeNumber("1E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-2"), "half down"))
        self.assertEqualsNumber(self.makeNumber("-1E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-2"), "half down"))

    def testRoundWithHalfEvenMode(self):
        self.assertIsNone(self.getLib().round(None, None, "half down"))
        self.assertIsNone(self.getLib().round(None, self.makeNumber("128"), "half down"))
        self.assertIsNone(self.getLib().round(self.makeNumber("10"), None, "half down"))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().round(self.makeNumber("5.5"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("2.5"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().round(self.makeNumber("1.6"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.1"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().round(self.makeNumber("1.0"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.0"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().round(self.makeNumber("-1.1"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-1.6"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().round(self.makeNumber("-2.5"), self.makeNumber("0"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-6"), self.getLib().round(self.makeNumber("-5.5"), self.makeNumber("0"), "half even"))

        self.assertEqualsNumber(self.makeNumber("5.12"), self.getLib().round(self.makeNumber("5.125"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("2.12"), self.getLib().round(self.makeNumber("2.125"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().round(self.makeNumber("1.126"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.121"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().round(self.makeNumber("1.120"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.120"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().round(self.makeNumber("-1.121"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().round(self.makeNumber("-1.126"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-2.12"), self.getLib().round(self.makeNumber("-2.125"), self.makeNumber("2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-5.12"), self.getLib().round(self.makeNumber("-5.125"), self.makeNumber("2"), "half even"))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.3E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-1"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-1.3E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-1"), "half even"))
        self.assertEqualsNumber(self.makeNumber("1E+2"), self.getLib().round(self.makeNumber("125.125"), self.makeNumber("-2"), "half even"))
        self.assertEqualsNumber(self.makeNumber("-1E+2"), self.getLib().round(self.makeNumber("-125.125"), self.makeNumber("-2"), "half even"))

    def testRoundUp(self):
        self.assertIsNone(self.getLib().roundUp(None, None))
        self.assertIsNone(self.getLib().roundUp(None, self.makeNumber("128")))
        self.assertIsNone(self.getLib().roundUp(self.makeNumber("10"), None))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().roundUp(self.makeNumber("5.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().roundUp(self.makeNumber("2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().roundUp(self.makeNumber("1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().roundUp(self.makeNumber("1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundUp(self.makeNumber("1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundUp(self.makeNumber("-1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().roundUp(self.makeNumber("-1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().roundUp(self.makeNumber("-1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-3"), self.getLib().roundUp(self.makeNumber("-2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-6"), self.getLib().roundUp(self.makeNumber("-5.5"), self.makeNumber("0")))

        self.assertEqualsNumber(self.makeNumber("5.13"), self.getLib().roundUp(self.makeNumber("5.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("2.13"), self.getLib().roundUp(self.makeNumber("2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().roundUp(self.makeNumber("1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().roundUp(self.makeNumber("1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundUp(self.makeNumber("1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundUp(self.makeNumber("-1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().roundUp(self.makeNumber("-1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().roundUp(self.makeNumber("-1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-2.13"), self.getLib().roundUp(self.makeNumber("-2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-5.13"), self.getLib().roundUp(self.makeNumber("-5.125"), self.makeNumber("2")))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.3E+2"), self.getLib().roundUp(self.makeNumber("125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("-1.3E+2"), self.getLib().roundUp(self.makeNumber("-125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("2E+2"), self.getLib().roundUp(self.makeNumber("125.125"), self.makeNumber("-2")))
        self.assertEqualsNumber(self.makeNumber("-2E+2"), self.getLib().roundUp(self.makeNumber("-125.125"), self.makeNumber("-2")))

    def testRoundDown(self):
        self.assertIsNone(self.getLib().roundDown(None, None))
        self.assertIsNone(self.getLib().roundDown(None, self.makeNumber("128")))
        self.assertIsNone(self.getLib().roundDown(self.makeNumber("10"), None))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("5"), self.getLib().roundDown(self.makeNumber("5.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().roundDown(self.makeNumber("2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundDown(self.makeNumber("1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundDown(self.makeNumber("1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundDown(self.makeNumber("1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundDown(self.makeNumber("-1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundDown(self.makeNumber("-1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundDown(self.makeNumber("-1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().roundDown(self.makeNumber("-2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-5"), self.getLib().roundDown(self.makeNumber("-5.5"), self.makeNumber("0")))

        self.assertEqualsNumber(self.makeNumber("5.12"), self.getLib().roundDown(self.makeNumber("5.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("2.12"), self.getLib().roundDown(self.makeNumber("2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundDown(self.makeNumber("1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundDown(self.makeNumber("1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundDown(self.makeNumber("1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundDown(self.makeNumber("-1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundDown(self.makeNumber("-1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundDown(self.makeNumber("-1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-2.12"), self.getLib().roundDown(self.makeNumber("-2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-5.12"), self.getLib().roundDown(self.makeNumber("-5.125"), self.makeNumber("2")))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.2E+2"), self.getLib().roundDown(self.makeNumber("125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("-1.2E+2"), self.getLib().roundDown(self.makeNumber("-125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("1E+2"), self.getLib().roundDown(self.makeNumber("125.125"), self.makeNumber("-2")))
        self.assertEqualsNumber(self.makeNumber("-1E+2"), self.getLib().roundDown(self.makeNumber("-125.125"), self.makeNumber("-2")))

    def testRoundHalfUp(self):
        self.assertIsNone(self.getLib().roundHalfUp(None, None))
        self.assertIsNone(self.getLib().roundHalfUp(None, self.makeNumber("128")))
        self.assertIsNone(self.getLib().roundHalfUp(self.makeNumber("10"), None))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().roundHalfUp(self.makeNumber("5.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().roundHalfUp(self.makeNumber("2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().roundHalfUp(self.makeNumber("1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundHalfUp(self.makeNumber("1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundHalfUp(self.makeNumber("1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundHalfUp(self.makeNumber("-1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundHalfUp(self.makeNumber("-1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().roundHalfUp(self.makeNumber("-1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-3"), self.getLib().roundHalfUp(self.makeNumber("-2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-6"), self.getLib().roundHalfUp(self.makeNumber("-5.5"), self.makeNumber("0")))

        self.assertEqualsNumber(self.makeNumber("5.13"), self.getLib().roundHalfUp(self.makeNumber("5.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("2.13"), self.getLib().roundHalfUp(self.makeNumber("2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().roundHalfUp(self.makeNumber("1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundHalfUp(self.makeNumber("1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundHalfUp(self.makeNumber("1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundHalfUp(self.makeNumber("-1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundHalfUp(self.makeNumber("-1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().roundHalfUp(self.makeNumber("-1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-2.13"), self.getLib().roundHalfUp(self.makeNumber("-2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-5.13"), self.getLib().roundHalfUp(self.makeNumber("-5.125"), self.makeNumber("2")))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.3E+2"), self.getLib().roundHalfUp(self.makeNumber("125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("-1.3E+2"), self.getLib().roundHalfUp(self.makeNumber("-125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("1E+2"), self.getLib().roundHalfUp(self.makeNumber("125.125"), self.makeNumber("-2")))
        self.assertEqualsNumber(self.makeNumber("-1E+2"), self.getLib().roundHalfUp(self.makeNumber("-125.125"), self.makeNumber("-2")))

    def testRoundHalfDown(self):
        self.assertIsNone(self.getLib().roundHalfDown(None, None))
        self.assertIsNone(self.getLib().roundHalfDown(None, self.makeNumber("128")))
        self.assertIsNone(self.getLib().roundHalfDown(self.makeNumber("10"), None))

        # From RoundingMode.java https:#docs.oracle.com/javase/8/docs/api/java/math/RoundingMode.html
        self.assertEqualsNumber(self.makeNumber("5"), self.getLib().roundHalfDown(self.makeNumber("5.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().roundHalfDown(self.makeNumber("2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().roundHalfDown(self.makeNumber("1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundHalfDown(self.makeNumber("1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().roundHalfDown(self.makeNumber("1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundHalfDown(self.makeNumber("-1.0"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().roundHalfDown(self.makeNumber("-1.1"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().roundHalfDown(self.makeNumber("-1.6"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().roundHalfDown(self.makeNumber("-2.5"), self.makeNumber("0")))
        self.assertEqualsNumber(self.makeNumber("-5"), self.getLib().roundHalfDown(self.makeNumber("-5.5"), self.makeNumber("0")))

        self.assertEqualsNumber(self.makeNumber("5.12"), self.getLib().roundHalfDown(self.makeNumber("5.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("2.12"), self.getLib().roundHalfDown(self.makeNumber("2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.13"), self.getLib().roundHalfDown(self.makeNumber("1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundHalfDown(self.makeNumber("1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("1.12"), self.getLib().roundHalfDown(self.makeNumber("1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundHalfDown(self.makeNumber("-1.120"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.12"), self.getLib().roundHalfDown(self.makeNumber("-1.121"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-1.13"), self.getLib().roundHalfDown(self.makeNumber("-1.126"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-2.12"), self.getLib().roundHalfDown(self.makeNumber("-2.125"), self.makeNumber("2")))
        self.assertEqualsNumber(self.makeNumber("-5.12"), self.getLib().roundHalfDown(self.makeNumber("-5.125"), self.makeNumber("2")))

        # Negative scale
        self.assertEqualsNumber(self.makeNumber("1.3E+2"), self.getLib().roundHalfDown(self.makeNumber("125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("-1.3E+2"), self.getLib().roundHalfDown(self.makeNumber("-125.125"), self.makeNumber("-1")))
        self.assertEqualsNumber(self.makeNumber("1E+2"), self.getLib().roundHalfDown(self.makeNumber("125.125"), self.makeNumber("-2")))
        self.assertEqualsNumber(self.makeNumber("-1E+2"), self.getLib().roundHalfDown(self.makeNumber("-125.125"), self.makeNumber("-2")))

    def testFloor(self):
        self.assertIsNone(self.getLib().floor(None))
        self.assertIsNone(self.getLib().floor(None, None))

        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().floor(self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().floor(self.makeNumber(1.23)))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().floor(self.makeNumber(1.5)))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().floor(self.makeNumber(1.56)))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().floor(self.makeNumber(-1.56)))

        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().floor(self.makeNumber(1), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("1.2"), self.getLib().floor(self.makeNumber(1.23), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("1.5"), self.getLib().floor(self.makeNumber(1.5), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("1.5"), self.getLib().floor(self.makeNumber(1.56), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("-1.6"), self.getLib().floor(self.makeNumber(-1.56), self.makeNumber(1)))

    def testCeiling(self):
        self.assertIsNone(self.getLib().ceiling(None))
        self.assertIsNone(self.getLib().ceiling(None, None))
        self.assertIsNone(self.getLib().ceiling(self.makeNumber(1), None))

        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().ceiling(self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().ceiling(self.makeNumber(1.23)))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().ceiling(self.makeNumber(1.5)))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().ceiling(self.makeNumber(1.56)))
        self.assertEqualsNumber(self.makeNumber("-1"), self.getLib().ceiling(self.makeNumber(-1.5)))

        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().ceiling(self.makeNumber(1), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("1.3"), self.getLib().ceiling(self.makeNumber(1.23), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("1.5"), self.getLib().ceiling(self.makeNumber(1.5), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("1.6"), self.getLib().ceiling(self.makeNumber(1.56), self.makeNumber(1)))
        self.assertEqualsNumber(self.makeNumber("-1.5"), self.getLib().ceiling(self.makeNumber(-1.56), self.makeNumber(1)))

    def testAbs(self):
        self.assertIsNone(self.getLib().abs(None))

        self.assertEqualsNumber(self.makeNumber("10"), self.getLib().abs(self.makeNumber(10)))
        self.assertEqualsNumber(self.makeNumber("10"), self.getLib().abs(self.makeNumber(-10)))

    def testModulo(self):
        self.assertIsNone(self.getLib().modulo(None, None))
        self.assertIsNone(self.getLib().modulo(self.makeNumber(10), self.makeNumber(0)))

        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().modulo(self.makeNumber(10), self.makeNumber(4)))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().modulo(self.makeNumber(10), self.makeNumber(-4)))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().modulo(self.makeNumber(-10), self.makeNumber(4)))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().modulo(self.makeNumber(-10), self.makeNumber(-4)))

        self.assertEqualsNumber(self.makeNumber("1.1"), self.getLib().modulo(self.makeNumber(10.1), self.makeNumber(4.5)))
        self.assertEqualsNumber(self.makeNumber("3.4"), self.getLib().modulo(self.makeNumber(-10.1), self.makeNumber(4.5)))
        self.assertEqualsNumber(self.makeNumber("-3.4"), self.getLib().modulo(self.makeNumber(10.1), self.makeNumber(-4.5)))
        self.assertEqualsNumber(self.makeNumber("-1.1"), self.getLib().modulo(self.makeNumber(-10.1), self.makeNumber(-4.5)))

    def testIntModulo(self):
        self.assertIsNone(self.getLib().modulo(None, None))
        self.assertIsNone(self.getLib().intModulo(self.makeNumber(10), self.makeNumber(0)))

        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().intModulo(self.makeNumber(10), self.makeNumber(4)))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().intModulo(self.makeNumber(10), self.makeNumber(-4)))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().intModulo(self.makeNumber(-10), self.makeNumber(4)))
        self.assertEqualsNumber(self.makeNumber("-2"), self.getLib().intModulo(self.makeNumber(-10), self.makeNumber(-4)))

    def testSqrt(self):
        self.assertIsNone(self.getLib().sqrt(None))
        self.assertIsNone(self.getLib().sqrt(self.makeNumber(-3)))

        self.assertEqualsNumber(self.makeNumber("4"), self.getLib().sqrt(self.makeNumber(16)))

    def testLog(self):
        self.assertIsNone(self.getLib().log(None))
        self.assertIsNone(self.getLib().log(self.makeNumber(-3)))

        self.assertEqualsNumber(self.makeNumber("2.30258509299404590109361379290930926799774169921875"), self.getLib().log(self.makeNumber(10)))

    def testExp(self):
        self.assertIsNone(self.getLib().exp(None))

        self.assertEqualsNumber(self.makeNumber("148.413159102576599934764089994132518768310546875"), self.getLib().exp(self.makeNumber(5)))

    def testOdd(self):
        self.assertIsNone(self.getLib().odd(None))

        self.assertFalse(self.getLib().odd(self.makeNumber("0.00")))
        self.assertTrue(self.getLib().odd(self.makeNumber("1.00")))
        self.assertTrue(self.getLib().odd(self.makeNumber(5)))
        self.assertFalse(self.getLib().odd(self.makeNumber(2)))

    def testEven(self):
        self.assertIsNone(self.getLib().even(None))

        self.assertTrue(self.getLib().even(self.makeNumber("0.00")))
        self.assertFalse(self.getLib().even(self.makeNumber("1.00")))
        self.assertFalse(self.getLib().even(self.makeNumber(5)))
        self.assertTrue(self.getLib().even(self.makeNumber(2)))

    #
    # String functions
    #
    def testContains(self):
        self.assertIsNone(self.getLib().contains(None, None))
        self.assertIsNone(self.getLib().contains(None, "bcg"))
        self.assertIsNone(self.getLib().contains("bcg", None))

        self.assertTrue(self.getLib().contains("abc", "a"))
        self.assertFalse(self.getLib().contains("aBc1", "bcg"))

        self.assertEqual(False, self.getLib().contains("foobar", "of"))
        self.assertEqual(True, self.getLib().contains("foobar", "fo"))
        self.assertEqual(True, self.getLib().contains("foobar", "r"))

    def testStartsWith(self):
        self.assertIsNone(self.getLib().startsWith(None, None))
        self.assertIsNone(self.getLib().startsWith(None, "bcg"))
        self.assertIsNone(self.getLib().startsWith("bcg", None))

        self.assertTrue(self.getLib().startsWith("abc", "a"))
        self.assertFalse(self.getLib().startsWith("aBc1", "bcg"))

        self.assertEqual(True, self.getLib().startsWith("foobar", "fo"))

    def testEndsWith(self):
        self.assertIsNone(self.getLib().endsWith(None, None))
        self.assertIsNone(self.getLib().endsWith(None, "bcg"))
        self.assertIsNone(self.getLib().endsWith("bcg", None))

        self.assertTrue(self.getLib().endsWith("abc", "c"))
        self.assertFalse(self.getLib().endsWith("aBc1", "bcg"))

        self.assertEqual(True, self.getLib().endsWith("foobar", "r"))

    def testSubstring(self):
        self.assertIsNone(self.getLib().substring(None, None))
        self.assertIsNone(self.getLib().substring(None, self.makeNumber("0")))
        self.assertIsNone(self.getLib().substring("", None))

        self.assertEqual("obar", self.getLib().substring("foobar", self.makeNumber("3")))
        self.assertEqual("oba", self.getLib().substring("foobar", self.makeNumber("3"), self.makeNumber("3")))
        self.assertEqual("a", self.getLib().substring("foobar", self.makeNumber("-2"), self.makeNumber("1")))

        # horse + grinning face emoji
        self.assertEqualsUnicodeString("\uD83D\uDE00", self.getLib().substring("foo\ud83d\udc0ebar\uD83D\uDE00", self.makeNumber("8")))
        self.assertEqualsUnicodeString("\uD83D\uDC0E", self.getLib().substring("foo\ud83d\udc0ebar\uD83D\uDE00", self.makeNumber("4"), self.makeNumber("1")))
        self.assertEqualsUnicodeString("\uD83D\uDC0Ebar", self.getLib().substring("foo\ud83d\udc0ebar\uD83D\uDE00", self.makeNumber("4"), self.makeNumber("4")))

    def testStringLength(self):
        self.assertIsNone(self.getLib().stringLength(None))

        self.assertEqualsNumber(self.makeNumber(3), self.getLib().stringLength("foo"))
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\n"))
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\r"))
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\t"))
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\""))
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\'"))
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\\"))
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\u0009"))
        self.assertEqualsNumber(self.makeNumber(6), self.getLib().stringLength("\\u0009"))
        # horse emoji
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\uD83D\uDCA9"))
        # horse emoji lowercase
        self.assertEqualsNumber(self.makeNumber(1), self.getLib().stringLength("\ud83d\udca9"))
        # horse + grinning face emoji
        self.assertEqualsNumber(self.makeNumber(2), self.getLib().stringLength("\ud83d\udc0e\uD83D\uDE00"))
        # horse + grinning face emoji
        self.assertEqualsNumber(self.makeNumber(2), self.getLib().stringLength("🐎😀"))

    def testUpperCase(self):
        self.assertIsNone(self.getLib().upperCase(None))

        self.assertEqual("ABC4", self.getLib().upperCase("aBc4"))

    def testLowerCase(self):
        self.assertIsNone(self.getLib().lowerCase(None))

        self.assertEqual("abc4", self.getLib().lowerCase("aBc4"))

    def testSubstringBefore(self):
        self.assertIsNone(self.getLib().substringBefore(None, None))
        self.assertIsNone(self.getLib().substringBefore(None, "bar"))
        self.assertIsNone(self.getLib().substringBefore("foobar", None))

        self.assertEqual("foo", self.getLib().substringBefore("foobar", "bar"))
        self.assertEqual("", self.getLib().substringBefore("foobar", "xyz"))

    def testSubstringAfter(self):
        self.assertIsNone(self.getLib().substringAfter(None, None))
        self.assertIsNone(self.getLib().substringAfter(None, "ob"))
        self.assertIsNone(self.getLib().substringAfter("foobar", None))

        self.assertEqual("ar", self.getLib().substringAfter("foobar", "ob"))
        self.assertEqual("", self.getLib().substringAfter("foobar", "xyz"))

    def testReplace(self):
        self.assertIsNone(self.getLib().replace("", "", ""))
        self.assertIsNone(self.getLib().replace("", "", None))

        self.assertIsNone(self.getLib().replace("abc", "[a-z]*", "#"))
        self.assertEqual("#", self.getLib().replace("abc", "[a-z]+", "#"))

        self.assertIsNone(self.getLib().replace(None, "(ab)|(a)", "[1=$1][2=$2]"))
        self.assertIsNone(self.getLib().replace("abcd", None, "[1=$1][2=$2]"))
        self.assertIsNone(self.getLib().replace("abcd", "(ab)|(a)", None))
        self.assertIsNone(self.getLib().replace("abcd", "(ab)|(a)", "$"))

        self.assertEqual("[1=ab][2=]cd", self.getLib().replace("abcd", "(ab)|(a)", "[1=$1][2=$2]"))

        self.assertEqual("a*cada*", self.getLib().replace("abracadabra", "bra", "*"))
        self.assertEqual("*", self.getLib().replace("abracadabra", "a.*a", "*"))
        self.assertEqual("*c*bra", self.getLib().replace("abracadabra", "a.*?a", "*"))
        self.assertEqual("brcdbr", self.getLib().replace("abracadabra", "a", ""))
        self.assertEqual("abbraccaddabbra", self.getLib().replace("abracadabra", "a(.)", "a$1$1"))
        self.assertIsNone(None, self.getLib().replace("abracadabra", ".*?", "$1"))
        self.assertEqual("b", self.getLib().replace("AAAA", "A+", "b"))
        self.assertEqual("bbbb", self.getLib().replace("AAAA", "A+?", "b"))
        self.assertEqual("carted", self.getLib().replace("darted", "^(.*?)d(.*)$", "$1c$2"))

    def testMatches(self):
        self.assertTrue(self.getLib().matches("", "", ""))
        self.assertTrue(self.getLib().matches("", "", None))

        self.assertTrue(self.getLib().matches("", "[a-z]*", ""))
        self.assertTrue(self.getLib().matches("abc", "[a-z]+", ""))

        self.assertTrue(self.getLib().matches("abracadabra", "bra"))
        self.assertTrue(self.getLib().matches("abracadabra", "^a.*a$"))
        self.assertFalse(self.getLib().matches("abracadabra", "^bra"))

        input: STRING = "Kaum hat dies der Hahn gesehen,\n" \
                        "Fangt er auch schon an zu krahen:\n" \
                        "Kikeriki! Kikikerikih!!\n" \
                        "Tak, tak, tak! - da kommen sie.\n"

        self.assertFalse(self.getLib().matches(input, "Kaum.*krahen"))
        self.assertTrue(self.getLib().matches(input, "Kaum.*krahen", "s"))
        self.assertTrue(self.getLib().matches(input, "^Kaum.*gesehen,$", "m"))
        self.assertFalse(self.getLib().matches(input, "^Kaum.*gesehen,$"))
        self.assertTrue(self.getLib().matches(input, "kiki", "i"))

    def testSplit(self):
        self.assertIsNone(self.getLib().split(None, None))
        self.assertIsNone(self.getLib().split("", ""))

        self.assertEqual(self.getLib().asList("John", "Doe"), self.getLib().split("John Doe", "\\s"))
        self.assertEqual(self.getLib().asList("a", "b", "c", "", ""), self.getLib().split("a;b;c;;", ";"))

    #
    # Boolean functions
    #
    def testNot(self):
        self.assertTrue(self.getLib().not_(False))
        self.assertFalse(self.getLib().not_(True))
        self.assertIsNone(self.getLib().not_(None))

    #
    # Date properties
    #
    def testDateProperties(self):
        self.assertIsNone(self.getLib().year(None))
        self.assertEqualsNumber(self.makeNumber("2018"), self.getLib().year(self.makeDate("2018-12-10")))

        self.assertIsNone(self.getLib().month(None))
        self.assertEqualsNumber(self.makeNumber("12"), self.getLib().month(self.makeDate("2018-12-10")))

        self.assertIsNone(self.getLib().day(None))
        self.assertEqualsNumber(self.makeNumber("10"), self.getLib().day(self.makeDate("2018-12-10")))

        self.assertIsNone(self.getLib().weekday(None))
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().weekday(self.makeDate("2018-12-10")))

    #
    # Time properties
    #
    def testTimeProperties(self):
        # See each implementation
        self.assertTrue(True)

    #
    # Date and time properties
    #
    def testDateAndTimeProperties(self):
        # See each implementation
        self.assertTrue(True)

    #
    # Duration properties
    #
    def testDurationProperties(self):
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().years(self.makeDuration("P1Y2M")))
        self.assertEqualsNumber(self.makeNumber("2"), self.getLib().months(self.makeDuration("P1Y2M")))

        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().days(self.makeDuration("P3DT4H5M6.700S")))
        self.assertEqualsNumber(self.makeNumber("4"), self.getLib().hours(self.makeDuration("P3DT4H5M6.700S")))
        self.assertEqualsNumber(self.makeNumber("5"), self.getLib().minutes(self.makeDuration("P3DT4H5M6.700S")))
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().seconds(self.makeDuration("P3DT4H5M6.700S")))

    #
    # Date and time functions
    #
    def testDateAndTimeFunctions(self):
        self.assertTrue(self.getLib().is_(None, None))
        self.assertFalse(self.getLib().is_(None, self.makeDate("2010-10-10")))
        self.assertFalse(self.getLib().is_(self.makeTime("12:00:00"), None))
        self.assertFalse(self.getLib().is_(self.makeDate("2012-12-25"), self.makeTime("23:00:50")))

        self.assertTrue(self.getLib().is_(self.makeNumber("10"), self.makeNumber("10")))
        self.assertFalse(self.getLib().is_(self.makeNumber("10"), self.makeNumber("11")))

        self.assertTrue(self.getLib().is_(True, True))
        self.assertFalse(self.getLib().is_(True, False))

        self.assertTrue(self.getLib().is_("abc", "abc"))
        self.assertFalse(self.getLib().is_("abc", "abd"))

        self.assertTrue(self.getLib().is_(self.makeDate("2012-12-25"), self.makeDate("2012-12-25")))
        self.assertFalse(self.getLib().is_(self.makeDate("2012-12-25"), self.makeDate("2012-12-26")))

        self.assertTrue(self.getLib().is_(self.makeTime("23:00:50z"), self.makeTime("23:00:50z")))
        self.assertTrue(self.getLib().is_(self.makeTime("23:00:50z"), self.makeTime("23:00:50Z")))
        self.assertTrue(self.getLib().is_(self.makeTime("23:00:50z"), self.makeTime("23:00:50+00:00")))

        self.assertTrue(self.getLib().is_(self.makeDateAndTime("2012-12-25T12:00:00"), self.makeDateAndTime("2012-12-25T12:00:00")))
        self.assertFalse(self.getLib().is_(self.makeDateAndTime("2012-12-25T12:00:00"), self.makeDateAndTime("2012-12-26T12:00:00z")))

        self.assertTrue(self.getLib().is_(self.makeDuration("P1Y"), self.makeDuration("P1Y")))
        self.assertFalse(self.getLib().is_(self.makeDuration("P1Y"), self.makeDuration("-P1Y")))
        self.assertTrue(self.getLib().is_(self.makeDuration("P1Y"), self.makeDuration("P12M")))

        self.assertTrue(self.getLib().is_([], []))
        self.assertTrue(self.getLib().is_([self.makeNumber(1), self.makeNumber(3)], [self.makeNumber(1), self.makeNumber(3)]))
        self.assertFalse(self.getLib().is_([self.makeNumber(1), self.makeNumber(3)], []))

        self.assertTrue(self.getLib().is_(Range(True, self.makeNumber(1), True, self.makeNumber(3)), Range(True, self.makeNumber(1), True, self.makeNumber(3))))
        self.assertFalse(self.getLib().is_(Range(True, self.makeNumber(1), True, self.makeNumber(3)), Range(True, self.makeNumber(2), True, self.makeNumber(3))))
        self.assertFalse(self.getLib().is_(Range(True, self.makeNumber(1), True, self.makeNumber(3)), Range(False, self.makeNumber(1), True, self.makeNumber(3))))

        self.assertTrue(self.getLib().is_(Context(), Context()))
        self.assertTrue(self.getLib().is_(Context().add("a", self.makeNumber(1)), Context().add("a", self.makeNumber(1))))
        self.assertFalse(self.getLib().is_(Context().add("a", self.makeNumber(1)), Context()))

    #
    # Temporal functions
    #
    def testTemporalFunctions(self):
        self.assertIsNone(self.getLib().dayOfYear(None))
        self.assertIsNone(self.getLib().dayOfWeek(None))
        self.assertIsNone(self.getLib().weekOfYear(None))
        self.assertIsNone(self.getLib().monthOfYear(None))

        self.assertEqual(self.makeNumber("260"), self.getLib().dayOfYear(self.makeDate("2019-09-17")))
        self.assertEqual("Tuesday", self.getLib().dayOfWeek(self.makeDate("2019-09-17")))
        self.assertEqual(self.makeNumber("38"), self.getLib().weekOfYear(self.makeDate("2019-09-17")))
        self.assertEqual(self.makeNumber("1"), self.getLib().weekOfYear(self.makeDate("2003-12-29")))
        self.assertEqual(self.makeNumber("1"), self.getLib().weekOfYear(self.makeDate("2004-01-04")))
        self.assertEqual(self.makeNumber("53"), self.getLib().weekOfYear(self.makeDate("2005-01-01")))
        self.assertEqual(self.makeNumber("1"), self.getLib().weekOfYear(self.makeDate("2005-01-03")))
        self.assertEqual(self.makeNumber("1"), self.getLib().weekOfYear(self.makeDate("2005-01-09")))
        self.assertEqual("September", self.getLib().monthOfYear(self.makeDate("2019-09-17")))

    #
    # List functions
    #
    def testAppend(self):
        self.assertEqualsList("[None]", self.getLib().append(None, None))
        self.assertEqual(["3"], self.getLib().append(None, "3"))
        self.assertEqual(self.makeNumberList("1", None, "3", None, "3"), self.getLib().append(self.makeNumberList(1, None, 3), None, self.makeNumber(3)))

        self.assertEqual(self.makeNumberList("1", "2", "3", "4"), self.getLib().append(self.makeNumberList(1, 2, 3), self.makeNumber(4)))
        self.assertEqual(self.makeNumberList("1", None, "3", "4"), self.getLib().append(self.makeNumberList(1, None, 3), self.makeNumber(4)))

    def testMin(self):
        super().testMin()
        self.assertEqualsNumber(self.makeNumber("1"), self.getLib().min(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))
        self.assertIsNone(self.getLib().min(1, None, 3))

    def testMax(self):
        super().testMax()
        self.assertEqualsNumber(self.makeNumber("3"), self.getLib().max(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))
        self.assertIsNone(self.getLib().max(1, None, 3))

    def testSum(self):
        super().testSum()
        self.assertEqualsNumber(self.makeNumber("6"), self.getLib().sum(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))
        self.assertIsNone(self.getLib().sum(1, None, 3))

    def testMean(self):
        self.assertIsNone(self.getLib().mean())
        self.assertIsNone(self.getLib().mean(None))
        self.assertIsNone(self.getLib().mean([]))
        self.assertIsNone(self.getLib().mean(self.makeNumberList()))

        self.assertIsNone(self.getLib().mean(self.makeNumber(1), None, self.makeNumber(3)))
        self.assertIsNone(self.getLib().mean(self.makeNumberList(1, None, 3)))

        self.assertEqualsNumber(2.0, self.getLib().mean(self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)), 0.001)
        self.assertEqualsNumber(2.0, self.getLib().mean(self.makeNumberList(1, 2, 3)), 0.001)

    def testAll(self):
        self.assertFalse(self.getLib().all(True, True, False))
        self.assertFalse(self.getLib().all(None, False))
        self.assertFalse(self.getLib().all([True, True, False]))
        self.assertFalse(self.getLib().all([None, False]))

        self.assertTrue(self.getLib().all())
        self.assertTrue(self.getLib().all([]))
        self.assertTrue(self.getLib().all(True, True))
        self.assertTrue(self.getLib().all([True, True]))

        self.assertIsNone(self.getLib().all(None))
        self.assertIsNone(self.getLib().all(None, None))
        self.assertIsNone(self.getLib().all(None, True))
        self.assertIsNone(self.getLib().all([None, None]))
        self.assertIsNone(self.getLib().all([None, True]))

    def testAny(self):
        self.assertTrue(self.getLib().any(True, True))
        self.assertTrue(self.getLib().any(False, True))
        self.assertTrue(self.getLib().any(None, True))
        self.assertTrue(self.getLib().any([True, True]))
        self.assertTrue(self.getLib().any([False, True]))
        self.assertTrue(self.getLib().any([None, True]))

        self.assertFalse(self.getLib().any())
        self.assertFalse(self.getLib().any([]))
        self.assertFalse(self.getLib().any(False, False, False))
        self.assertFalse(self.getLib().any([False, False, False]))

        self.assertIsNone(self.getLib().any(None))
        self.assertIsNone(self.getLib().any(None, None))
        self.assertIsNone(self.getLib().any(None, False))
        self.assertIsNone(self.getLib().any([None, None]))
        self.assertIsNone(self.getLib().any([None, False]))

    def testSublist(self):
        self.assertIsNone(self.getLib().sublist(None, None))
        self.assertIsNone(self.getLib().sublist(None, None, None))

        self.assertEqual(self.makeNumberList("1", "2", "3"), self.getLib().sublist(self.makeNumberList(1, 2, 3), self.makeNumber("1")))
        self.assertEqual(self.makeNumberList("1", "2"), self.getLib().sublist(self.makeNumberList(1, 2, 3), self.makeNumber("1"), self.makeNumber("2")))
        self.assertEqual(self.makeNumberList("2"), self.getLib().sublist(self.makeNumberList(1, 2, 3), self.makeNumber("2"), self.makeNumber("1")))

    def testConcatenate(self):
        self.assertIsNone(self.getLib().concatenate(None, None))

        self.assertEqual(self.makeNumberList("1", "2", "3", "4", "5", "6"), self.getLib().concatenate(self.makeNumberList(1, 2, 3), self.makeNumberList(4, 5, 6)))

    def testInsertBefore(self):
        self.assertIsNone(self.getLib().insertBefore(None, None, None))

        self.assertEqual(self.makeNumberList("2", "1", "3"), self.getLib().insertBefore(self.makeNumberList(1, 3), self.makeNumber("1"), self.makeNumber("2")))
        self.assertEqual(self.makeNumberList("1", "2", "4", "3"), self.getLib().insertBefore(self.makeNumberList(1, 2, 3), self.makeNumber("-1"), self.makeNumber("4")))
        # Out of bounds
        self.assertEqual(self.makeNumberList("1", "2", "3"), self.getLib().insertBefore(self.makeNumberList(1, 2, 3), self.makeNumber("5"), self.makeNumber("4")))
        self.assertEqual(self.makeNumberList("1", "2", "3"), self.getLib().insertBefore(self.makeNumberList(1, 2, 3), self.makeNumber("-5"), self.makeNumber("4")))

    def testRemove(self):
        self.assertIsNone(self.getLib().remove(None, None))

        self.assertEqual(self.makeNumberList("1", "3"), self.getLib().remove(self.makeNumberList(1, 2, 3), self.makeNumber("2")))

    def testReverse(self):
        self.assertEqual([], self.getLib().reverse(None))

        self.assertEqual(self.makeNumberList("3", "2", "1"), self.getLib().reverse(self.makeNumberList(1, 2, 3)))

    def testIndexOf(self):
        self.assertEqual([], self.getLib().indexOf(None, None))

        self.assertEqual(self.makeNumberList("2", "4"), self.getLib().indexOf(["1", "2", "3", "2"], "2"))

    def testUnion(self):
        self.assertIsNone(self.getLib().union(None, None))

        self.assertEqual(self.makeNumberList("1", "2", "3"), self.getLib().union(self.makeNumberList(1, 2), self.makeNumberList(2, 3)))

    def testDistinctValues(self):
        self.assertEqual([], self.getLib().distinctValues(None))

        self.assertEqual(self.makeNumberList("1", "2", "3"), self.getLib().distinctValues(self.makeNumberList(1, 2, 3, 2, 1)))

    def testFlatten(self):
        self.assertIsNone(self.getLib().flatten(None))

        self.assertEqual(self.makeList("1", "2", "3", "4"), self.getLib().flatten([
            [["1", "2"]],
            [["3"]],
            "4"
        ]))

    def testProduct(self):
        self.assertIsNone(self.getLib().product())
        self.assertIsNone(self.getLib().product(None))
        self.assertIsNone(self.getLib().product([]))
        self.assertIsNone(self.getLib().product((self.makeNumberList())))

        self.assertIsNone(self.getLib().product(self.makeNumber(2), None, self.makeNumber(4)))
        self.assertIsNone(self.getLib().product(self.makeNumberList(2, None, 4)))

        self.assertEqualsNumber(self.makeNumber(24), self.getLib().product(self.makeNumber(2), self.makeNumber(3), self.makeNumber(4)))
        self.assertEqualsNumber(self.makeNumber(24), self.getLib().product(self.makeNumberList(2, 3, 4)))

    def testMedian(self):
        self.assertIsNone(self.getLib().median())
        self.assertIsNone(self.getLib().median(None))
        self.assertIsNone(self.getLib().median([]))
        self.assertIsNone(self.getLib().median(self.makeNumberList()))

        self.assertIsNone(self.getLib().median(self.makeNumber(8), None, self.makeNumber(5)))
        self.assertIsNone(self.getLib().median(self.makeNumberList(8, None, 5)))

        self.assertEqualsNumber(self.makeNumber(4), self.getLib().median(self.makeNumber(8), self.makeNumber(2), self.makeNumber(5), self.makeNumber(3), self.makeNumber(4)))
        self.assertEqualsNumber(self.makeNumber(4), self.getLib().median(self.makeNumberList(8, 2, 5, 3, 4)))
        self.assertEqualsNumber(self.makeNumber(2.5), self.getLib().median(self.makeNumber(6), self.makeNumber(1), self.makeNumber(2), self.makeNumber(3)))
        self.assertEqualsNumber(self.makeNumber(2.5), self.getLib().median(self.makeNumberList(6, 1, 2, 3)))

    def testStddev(self):
        self.assertIsNone(self.getLib().stddev())
        self.assertIsNone(self.getLib().stddev(None))
        self.assertIsNone(self.getLib().stddev([]))
        self.assertIsNone(self.getLib().stddev(self.makeNumberList()))

        self.assertIsNone(self.getLib().stddev(self.makeNumber(2), self.makeNumber(4), None, self.makeNumber(5)))
        self.assertIsNone(self.getLib().stddev(self.makeNumberList(2, 4, None, 5)))

        self.assertEqualsNumber(self.makeNumber("2.0816659994661"), self.getLib().stddev(self.makeNumber(2), self.makeNumber(4), self.makeNumber(7), self.makeNumber(5)))
        self.assertEqualsNumber(self.makeNumber("2.0816659994661"), self.getLib().stddev(self.makeNumberList(2, 4, 7, 5)))

    def testMode(self):
        self.assertIsNone(self.getLib().mode(None))

        self.assertEqual(self.makeNumberList(), self.getLib().mode())
        self.assertEqual(self.makeNumberList(), self.getLib().mode([]))
        self.assertEqual(self.makeNumberList(), self.getLib().mode(self.makeNumberList()))

        self.assertIsNone(self.getLib().mode(self.makeNumber(1), None))
        self.assertIsNone(self.getLib().mode(self.makeNumberList(1, None)))

        self.assertEqual(self.makeNumberList(6), self.getLib().mode(self.makeNumber(6), self.makeNumber(3), self.makeNumber(9), self.makeNumber(6), self.makeNumber(6)))
        self.assertEqual(self.makeNumberList(6), self.getLib().mode(self.makeNumberList(6, 3, 9, 6, 6)))
        self.assertEqual(self.makeNumberList(1, 6), self.getLib().mode(self.makeNumber(6), self.makeNumber(1), self.makeNumber(9), self.makeNumber(6), self.makeNumber(1)))
        self.assertEqual(self.makeNumberList(1, 6), self.getLib().mode(self.makeNumberList(6, 1, 9, 6, 1)))

    def testCollect(self):
        self.getLib().collect(None, None)
        self.getLib().collect([], None)

        result = []
        self.getLib().collect(result, [["1", "2"], "3"])
        self.assertEqual(["1", "2", "3"], result)

    def testSort(self):
        comparator = LambdaExpression(lambda *args: (x := args[0], y := args[1], self.getLib().stringLessThan(x, y)))

        self.assertIsNone(self.getLib().sort(None, None))
        self.assertIsNone(self.getLib().sort(None, comparator))
        self.assertEqual([], self.getLib().sort([], None))

        self.assertEqual(["1", "2", "3"], self.getLib().sort(["3", "1", "2"], comparator))
