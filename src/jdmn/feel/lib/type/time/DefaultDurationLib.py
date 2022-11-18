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
import datetime

import isodate
from dateutil.relativedelta import relativedelta
from isodate import Duration

from jdmn.feel.lib.Types import STRING, DURATION, INTEGER, DATE_OR_DATE_TIME


class DefaultDurationLib:
    @staticmethod
    def duration(from_: STRING) -> DURATION:
        if from_ is None:
            return None

        return isodate.parse_duration(from_)

    @staticmethod
    def yearsAndMonthsDuration(from_: DATE_OR_DATE_TIME, to: DATE_OR_DATE_TIME) -> DURATION:
        if from_ is None or to is None:
            return None

        from_ = from_.date() if isinstance(from_, datetime.datetime) else from_
        to = to.date() if isinstance(to, datetime.datetime) else to

        delta = relativedelta(to, from_)
        return Duration(years=delta.years, months=delta.months)

    @staticmethod
    def years(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        return duration.years

    @staticmethod
    def months(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        return duration.months

    @staticmethod
    def days(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        return duration.days

    @staticmethod
    def hours(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        seconds = duration.seconds
        mm, _ = divmod(seconds, 60)
        hh, _ = divmod(mm, 60)
        return hh

    @staticmethod
    def minutes(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        seconds = duration.seconds
        mm, _ = divmod(seconds, 60)
        _, mm = divmod(mm, 60)
        return mm

    @staticmethod
    def seconds(duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        seconds = duration.seconds
        _, ss = divmod(seconds, 60)
        return ss

    @staticmethod
    def abs(duration: DURATION) -> DURATION:
        if duration is None:
            return None

        return duration.years
