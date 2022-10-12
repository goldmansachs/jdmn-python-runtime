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
    def duration(self, from_: STRING) -> DURATION:
        if from_ is None:
            return None

        return isodate.parse_duration(from_)

    def yearsAndMonthsDuration(self, from_: DATE_OR_DATE_TIME, to: DATE_OR_DATE_TIME) -> DURATION:
        if from_ is None or to is None:
            return None

        from_ = from_.date() if isinstance(from_, datetime.datetime) else from_
        to = to.date() if isinstance(to, datetime.datetime) else to

        delta = relativedelta(to, from_)
        return Duration(years=delta.years, months=delta.months)

    def years(self, duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        return duration.years

    def months(self, duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        return duration.months

    def days(self, duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        return duration.days

    def hours(self, duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        seconds = duration.seconds
        mm, ss = divmod(seconds, 60)
        hh, mm = divmod(mm, 60)
        return hh

    def minutes(self, duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        seconds = duration.seconds
        mm, ss = divmod(seconds, 60)
        hh, mm = divmod(mm, 60)
        return mm

    def seconds(self, duration: DURATION) -> INTEGER:
        if duration is None:
            return None

        seconds = duration.seconds
        mm, ss = divmod(seconds, 60)
        return ss

    def abs(self, duration: DURATION) -> DURATION:
        if duration is None:
            return None

        return duration.years
