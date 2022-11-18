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
from datetime import datetime, date, time, timedelta
from decimal import Decimal

from isodate import Duration

from jdmn.feel.lib.Types import POINT_RANGE_UNION, BOOLEAN, RANGE, COMPARABLE
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType
from jdmn.feel.lib.type.numeric.NumericComparator import NumericComparator
from jdmn.feel.lib.type.string.StringComparator import StringComparator
from jdmn.feel.lib.type.time.DefaultDateComparator import DefaultDateComparator
from jdmn.feel.lib.type.time.DefaultDateTimeComparator import DefaultDateTimeComparator
from jdmn.feel.lib.type.time.DefaultDurationComparator import DefaultDurationComparator
from jdmn.feel.lib.type.time.DefaultTimeComparator import DefaultTimeComparator
from jdmn.runtime.Range import Range

COMPARATOR_MAP = {}
COMPARATOR_MAP[Decimal] = NumericComparator()
COMPARATOR_MAP[str] = StringComparator()
COMPARATOR_MAP[date] = DefaultDateComparator()
COMPARATOR_MAP[time] = DefaultTimeComparator()
COMPARATOR_MAP[datetime] = DefaultDateTimeComparator()
COMPARATOR_MAP[Duration] = DefaultDurationComparator()
COMPARATOR_MAP[timedelta] = DefaultDurationComparator()


class DefaultRangeLib:
    BOOLEAN_TYPE = DefaultBooleanType()

    def before(self, arg1: POINT_RANGE_UNION, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isPoint(arg1) and self.isPoint(arg2):
            # point1 < point2
            rc = self.resolveComparator(arg1)
            return None if rc is None else rc.lessThan(arg1, arg2)
        elif self.isPoint(arg1) and self.isRange(arg2):
            # point < range.start
            # or (point = range.start and not(range.start included) )
            point: COMPARABLE = arg1
            range_: RANGE = arg2
            start = range_.getStart()
            rc = self.resolveComparator(point)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                rc.lessThan(point, start),
                self.BOOLEAN_TYPE.booleanAnd(rc.equalTo(point, start), not range_.isStartIncluded())
            )
        elif self.isRange(arg1) and self.isPoint(arg2):
            # range.end < point
            # or (range.end = point and not (range.end included) )
            range_ = arg1
            point = arg2
            end = range_.getEnd()
            rc = self.resolveComparator(point)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                rc.lessThan(end, point),
                self.BOOLEAN_TYPE.booleanAnd(rc.equalTo(end, point), not range_.isEndIncluded())
            )
        else:
            # range1.end < range2.start
            # or ((not (range1.end included) or not (range2.start included)) and range1.end = range2.start)
            range1 = arg1
            range2 = arg2
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                rc.lessThan(end1, start2),
                self.BOOLEAN_TYPE.booleanAnd(
                    self.BOOLEAN_TYPE.booleanOr(not range1.isEndIncluded(), not range2.isStartIncluded()),
                    rc.equalTo(end1, start2)
                )
            )

    def after(self, arg1: POINT_RANGE_UNION, arg2: POINT_RANGE_UNION):
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isPoint(arg1) and self.isPoint(arg2):
            # point1 > point2
            rc = self.resolveComparator(arg1)
            return None if rc is None else rc.greaterThan(arg1, arg2)
        elif self.isPoint(arg1) and self.isRange(arg2):
            # point > range.end
            # or (point = range.end and not(range.end included) )
            point = arg1
            range_ = arg2
            end = range_.getEnd()
            rc = self.resolveComparator(point)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                    rc.greaterThan(point, end),
                    self.BOOLEAN_TYPE.booleanAnd(
                         rc.equalTo(point, end),
                         not range_.isEndIncluded()
                    )
            )
        elif self.isRange(arg1) and self.isPoint(arg2):
            # range.start > point
            # or (range.start = point and not(range.start included) )
            range_ = arg1
            point = arg2
            start = range_.getStart()
            rc = self.resolveComparator(start)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                    rc.greaterThan(start, point),
                    self.BOOLEAN_TYPE.booleanAnd(
                            rc.equalTo(start, point),
                            not range_.isStartIncluded()
                    )
            )
        else:
            # range1.start > range2.end
            # or ((not (range1.start included) or not (range2.end included)) and range1.start = range2.end)
            range1 = arg1
            range2 = arg2
            start1 = range1.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                rc.greaterThan(start1, end2),
                self.BOOLEAN_TYPE.booleanAnd(
                    self.BOOLEAN_TYPE.booleanOr(not range1.isStartIncluded(), not range2.isEndIncluded()),
                    rc.equalTo(start1, end2)
                )
            )

    def meets(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        if self.checkArguments(range1, range2):
            return None
        if not self.isRange(range1) or not self.isRange(range2):
            return None

        #
        # DMN 1.3 spec
        # range1.end included
        # and range2.start included
        # and range1.end = range2.start
        #
        start1 = range1.getStart()
        end1 = range1.getEnd()
        start2 = range2.getStart()
        rc = self.resolveComparator(start1)
        return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                range1.isEndIncluded(),
                range2.isStartIncluded(),
                rc.equalTo(end1, start2)
        )

    def metBy(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        if self.checkArguments(range1, range2):
            return None
        if not self.isRange(range1) or not self.isRange(range2):
            return None

        #
        # DMN 1.3 spec
        # range1.start included
        # and range2.end included
        # and range1.start = range2.end
        #
        start1 = range1.getStart()
        end2 = range2.getEnd()
        rc = self.resolveComparator(start1)
        return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                range1.isStartIncluded(),
                range2.isEndIncluded(),
                rc.equalTo(start1, end2)
        )

    def overlaps(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        if self.checkArguments(range1, range2):
            return None
        if not self.isRange(range1) or not self.isRange(range2):
            return None

        #
        # CQL spec
        #
        # The overlaps operator returns true if the first interval overlaps the second.
        # More precisely,
        #      if the starting or ending point of either interval is in the other,
        #      or if the ending point of the first interval is greater than or equal to the starting point of the second interval,
        #      and the starting point of the first interval is less than or equal to the ending point of the second interval.
        #
        # DMN 1.3 spec
        # (range1.end > range2.start or (range1.end = range2.start and (range1.end included or range2.end included)))
        # and (range1.start < range2.end or (range1.start = range2.end and range1.start included and range2.end included))
        #
        # Corrected:
        # overlaps before(range1, range2)
        # or overlaps after(range1, range2)
        # or includes(range1, range2)
        # or includes(range2, range1)
        #
        return self.BOOLEAN_TYPE.booleanOr(
            self.overlapsBefore(range1, range2),
            self.overlapsAfter(range1, range2),
            self.includes(range1, range2),
            self.includes(range2, range1)
        )

    def overlapsBefore(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        if self.checkArguments(range1, range2):
            return None
        if not self.isRange(range1) or not self.isRange(range2):
            return None

        #
        # CQL spec:
        # The operator overlaps before returns true if the first interval overlaps the second and starts before it,
        # while the overlaps after operator returns true if the first interval overlaps the second and ends after it.
        #

        #
        # DMN 1.3 spec
        # range1 starts before range2
        # and range1.end is in range2
        #
        # (range1.start < range2.start or (range1.start = range2.start and range1.start included and range2.start included))
        # and (range1.end > range2.start or (range1.end = range2.start and range1.end included and range2.start included))
        # and (range1.end < range2.end  or (range1.end = range2.end and (not(range1.end included) or range2.end included )))
        #

        # Corrected to
        # (range1.start < range2.start or (range1.start = range2.start and (range1.start included and not(range2.start included))))
        # and (range1.end > range2.start or (range1.end = range2.start and range1.end included and range2.start included))
        # and (range1.end < range2.end  or (range1.end = range2.end and (not(range1.end included) or range2.end included )))
        start1 = range1.getStart()
        end1 = range1.getEnd()
        start2 = range2.getStart()
        end2 = range2.getEnd()
        rc = self.resolveComparator(start1)
        if rc is None:
            return None

        range1StartsBeforeRange2 = self.BOOLEAN_TYPE.booleanOr(
                rc.lessThan(start1, start2),
                self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(start1, start2),
                        range1.isStartIncluded(),
                        not range2.isStartIncluded()
                )
        )
        range1EndIsInRange2 = self.BOOLEAN_TYPE.booleanAnd(
                self.BOOLEAN_TYPE.booleanOr(
                    rc.greaterThan(end1, start2),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(end1, start2),
                        range1.isEndIncluded(),
                        range2.isStartIncluded()
                    )
                ),
                self.BOOLEAN_TYPE.booleanOr(
                        rc.lessThan(end1, end2),
                        self.BOOLEAN_TYPE.booleanAnd(
                                rc.equalTo(end1, end2),
                                self.BOOLEAN_TYPE.booleanOr(
                                        not range1.isEndIncluded(),
                                        range2.isEndIncluded()
                                )
                        )
                )
        )
        return self.BOOLEAN_TYPE.booleanAnd(
                range1StartsBeforeRange2,
                range1EndIsInRange2
        )

    def overlapsAfter(self, range1: RANGE, range2: RANGE) -> BOOLEAN:
        if self.checkArguments(range1, range2):
            return None
        if not self.isRange(range1) or not self.isRange(range2):
            return None

        #
        # DMN 1.3 spec
        # range2 starts before range1
        # range2.end is in range1
        #
        # (range2.start < range1.start or (range2.start = range1.start and range2.start included and not( range1.start included)))
        # and (range2.end > range1.start or (range2.end = range1.start and range2.end included and range1.start included ))
        # and (range2.end < range1.end or (range2.end = range1.end and (not(range2.end included) or range1.end included)))
        #
        start1 = range1.getStart()
        end1 = range1.getEnd()
        start2 = range2.getStart()
        end2 = range2.getEnd()
        rc = self.resolveComparator(start1)
        if rc is None:
            return None

        range2StartsBeforeRange1 = self.BOOLEAN_TYPE.booleanOr(
                rc.lessThan(start2, start1),
                self.BOOLEAN_TYPE.booleanAnd(rc.equalTo(start2, start1), range2.isStartIncluded(), not range1.isStartIncluded())
        )
        range2EndIsInRange1 = self.BOOLEAN_TYPE.booleanAnd(
                self.BOOLEAN_TYPE.booleanOr(
                    rc.greaterThan(end2, start1),
                    self.BOOLEAN_TYPE.booleanAnd(
                            rc.equalTo(end2, start1),
                            range2.isEndIncluded(),
                            range1.isStartIncluded()
                    )
                ),
                self.BOOLEAN_TYPE.booleanOr(
                        rc.lessThan(end2, end1),
                        self.BOOLEAN_TYPE.booleanAnd(
                                rc.equalTo(end2, end1),
                                self.BOOLEAN_TYPE.booleanOr(
                                        not range2.isEndIncluded(),
                                        range1.isEndIncluded()
                                )
                        )
                )
        )
        return self.BOOLEAN_TYPE.booleanAnd(
                range2StartsBeforeRange1,
                range2EndIsInRange1
        )

    def finishes(self, arg1: POINT_RANGE_UNION, arg2: RANGE) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isPoint(arg1) and self.isRange(arg2):
            point = arg1
            range_ = arg2
            # range.end included
            # and range.end = point
            end = range_.getEnd()
            rc = self.resolveComparator(point)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                range_.isEndIncluded(),
                rc.equalTo(end, point)
            )
        elif self.isRange(arg1) and self.isRange(arg2):
            range1 = arg1
            range2 = arg2
            # range1.end
            included = range2.end
            included
            # and range1.end = range2.end
            # and (range1.start > range2.start or (range1.start = range2.start and ( not (range1.start included) or range2.start included)))
            #
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                range1.isEndIncluded() == range2.isEndIncluded(),
                rc.equalTo(end1, end2),
                self.BOOLEAN_TYPE.booleanOr(
                    rc.greaterThan(start1, start2),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(start1, start2),
                        self.BOOLEAN_TYPE.booleanOr(not range1.isStartIncluded(), range2.isStartIncluded())
                    )
                )
            )
        else:
            return None

    def finishedBy(self, arg1: RANGE, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isRange(arg1) and self.isPoint(arg2):
            range_ = arg1
            point = arg2
            # range.end included
            # and range.end = point
            start = range_.getStart()
            end = range_.getEnd()
            rc = self.resolveComparator(start)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                range_.isEndIncluded(),
                rc.equalTo(end, point)
            )
        elif self.isRange(arg1) and self.isRange(arg2):
            range1 = arg1
            range2 = arg2
            # range1.end included = range2.end included
            # and range1.end = range2.end
            # and (range1.start < range2.start or (range1.start = range2.start and (range1.start included or not (range2.start included))))
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                range1.isEndIncluded() == range2.isEndIncluded(),
                rc.equalTo(end1, end2),
                self.BOOLEAN_TYPE.booleanOr(
                    rc.lessThan(start1, start2),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(start1, start2),
                        self.BOOLEAN_TYPE.booleanOr(range1.isStartIncluded(), not range2.isStartIncluded())
                    )
                )
            )
        else:
            return None

    def includes(self, arg1: RANGE, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isRange(arg1) and self.isPoint(arg2):
            range_ = arg1
            point = arg2
            # (range.start < point and range.end > point)
            # or (range.start = point and range.start included)
            # or (range.end = point and range.end included)
            start = range_.getStart()
            end = range_.getEnd()
            rc = self.resolveComparator(start)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                self.BOOLEAN_TYPE.booleanAnd(rc.lessThan(start, point), rc.greaterThan(end, point)),
                self.BOOLEAN_TYPE.booleanAnd(rc.equalTo(start, point), range_.isStartIncluded()),
                self.BOOLEAN_TYPE.booleanAnd(rc.equalTo(end, point), range_.isEndIncluded())
            )
        elif self.isRange(arg1) and self.isRange(arg2):
            range1 = arg1
            range2 = arg2
            # (range1.start < range2.start or (range1.start = range2.start and (range1.start included or not (range2.start included))))
            # and (range1.end > range2.end or (range1.end = range2.end and (range1.end included or not (range2.end included))))
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                self.BOOLEAN_TYPE.booleanOr(
                    rc.lessThan(start1, start2),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(start1, start2),
                        self.BOOLEAN_TYPE.booleanOr(
                            range1.isStartIncluded(),
                            not range2.isStartIncluded()
                        )
                    )
                ),
                self.BOOLEAN_TYPE.booleanOr(
                    rc.greaterThan(end1, end2),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(end1, end2),
                        self.BOOLEAN_TYPE.booleanOr(
                            range1.isEndIncluded(),
                            not range2.isEndIncluded()
                        )
                    )
                )
            )
        else:
            return None

    def during(self, arg1: POINT_RANGE_UNION, arg2: RANGE) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isPoint(arg1) and self.isRange(arg2):
            point = arg1
            range_ = arg2
            # (range.start < point and range.end > point)
            # or (range.start = point and range.start included)
            # or (range.end = point and range.end included)
            start = range_.getStart()
            end = range_.getEnd()
            rc = self.resolveComparator(point)
            return None if rc is None else self.BOOLEAN_TYPE.booleanOr(
                self.BOOLEAN_TYPE.booleanAnd(rc.lessThan(start, point), rc.greaterThan(end, point)),
                self.BOOLEAN_TYPE.booleanAnd(rc.equalTo(start, point), range_.isStartIncluded()),
                self.BOOLEAN_TYPE.booleanAnd(rc.equalTo(end, point), range_.isEndIncluded())
            )
        elif self.isRange(arg1) and self.isRange(arg2):
            range1 = arg1
            range2 = arg2
            # (range2.start < range1.start or (range2.start = range1.start and (range2.start included or not (range1.start included))))
            # and (range2.end > range1.end or (range2.end = range1.end and (range2.end included or not (range1.end included))))
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                self.BOOLEAN_TYPE.booleanOr(
                    rc.lessThan(start2, start1),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(start2, start1),
                        self.BOOLEAN_TYPE.booleanOr(range2.isStartIncluded(), not range1.isStartIncluded())
                    )
                ),
                self.BOOLEAN_TYPE.booleanOr(
                    rc.greaterThan(end2, end1),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(end2, end1),
                        self.BOOLEAN_TYPE.booleanOr(range2.isEndIncluded(), not range1.isEndIncluded())
                    )
                )
            )
        else:
            return None

    def starts(self, arg1: POINT_RANGE_UNION, arg2: RANGE) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isPoint(arg1) and self.isRange(arg2):
            point = arg1
            range_ = arg2
            # range.start = point
            # and range.start included
            start = range_.getStart()
            rc = self.resolveComparator(point)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                rc.equalTo(start, point),
                range_.isStartIncluded()
            )
        elif self.isRange(arg1) and self.isRange(arg2):
            range1 = arg1
            range2 = arg2
            # range1.start = range2.start
            # and range1.start included = range2.start included
            # and (range1.end < range2.end or (range1.end = range2.end and ( not (range1.end included) or range2.end included)))
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                rc.equalTo(start1, start2),
                range1.isStartIncluded() == range2.isStartIncluded(),
                self.BOOLEAN_TYPE.booleanOr(
                    rc.lessThan(end1, end2),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(end1, end2),
                        self.BOOLEAN_TYPE.booleanOr(
                            not range1.isEndIncluded(),
                            range2.isEndIncluded()
                        )
                    )
                )
            )
        else:
            return None

    def startedBy(self, arg1: RANGE, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isRange(arg1) and self.isPoint(arg2):
            range_ = arg1
            point = arg2
            # range.start = point
            # and range.start included
            start = range_.getStart()
            rc = self.resolveComparator(point)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                rc.equalTo(start, point),
                range_.isStartIncluded()
            )
        elif self.isRange(arg1) and self.isRange(arg2):
            range1 = arg1
            range2 = arg2
            # range1.start = range2.start
            # and range1.start included = range2.start included
            # and (range2.end < range1.end or (range2.end = range1.end and ( not (range2.end included) or range1.end included)))
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                rc.equalTo(start1, start2),
                range1.isStartIncluded() == range2.isStartIncluded(),
                self.BOOLEAN_TYPE.booleanOr(
                    rc.lessThan(end2, end1),
                    self.BOOLEAN_TYPE.booleanAnd(
                        rc.equalTo(end2, end1),
                        self.BOOLEAN_TYPE.booleanOr(
                            not range2.isEndIncluded(),
                            range1.isEndIncluded()
                        )
                    )
                )
            )
        else:
            return None

    def coincides(self, arg1: POINT_RANGE_UNION, arg2: POINT_RANGE_UNION) -> BOOLEAN:
        if self.checkArguments(arg1, arg2):
            return None

        #
        # DMN 1.3 spec
        #
        if self.isPoint(arg1) and self.isPoint(arg2):
            point1 = arg1
            point2 = arg2
            # point1 = point2
            rc = self.resolveComparator(point1)
            return None if rc is None else rc.equalTo(point1, point2)
        elif self.isRange(arg1) and self.isRange(arg2):
            range1 = arg1
            range2 = arg2
            # range1.start = range2.start
            # and range1.start included = range2.start included
            # and range1.end = range2.end
            # and range1.end included = range2.end included
            start1 = range1.getStart()
            end1 = range1.getEnd()
            start2 = range2.getStart()
            end2 = range2.getEnd()
            rc = self.resolveComparator(start1)
            return None if rc is None else self.BOOLEAN_TYPE.booleanAnd(
                rc.equalTo(start1, start2),
                range1.isStartIncluded() == range2.isStartIncluded(),
                rc.equalTo(end1, end2),
                range1.isEndIncluded() == range2.isEndIncluded()
            )
        else:
            return None

    @staticmethod
    def checkArguments(arg1: POINT_RANGE_UNION, arg2: POINT_RANGE_UNION) -> bool:
        return arg1 is None or arg2 is None

    @staticmethod
    def isPoint(arg1):
        return not isinstance(arg1, Range)

    @staticmethod
    def isRange(arg1):
        return isinstance(arg1, Range)

    @staticmethod
    def resolveComparator(arg):
        key = type(arg)
        cmp = COMPARATOR_MAP.get(key)
        return cmp
