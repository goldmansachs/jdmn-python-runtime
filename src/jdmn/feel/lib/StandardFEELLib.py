#
# Copyright 2016 Goldman Sachs.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.
#
from jdmn.feel.lib.type.bool.DefaultBooleanType import DefaultBooleanType
from jdmn.feel.lib.type.list.DefaultListType import DefaultListType
from jdmn.feel.lib.type.numeric.DefaultNumericType import DefaultNumericType
from jdmn.feel.lib.type.string.DefaultStringType import DefaultStringType
from jdmn.feel.lib.type.time.DefaultDateTimeType import DefaultDateTimeType
from jdmn.feel.lib.type.time.DefaultDateType import DefaultDateType
from jdmn.feel.lib.type.time.DefaultTimeType import DefaultTimeType


class StandardFEELLib(DefaultNumericType, DefaultStringType, DefaultBooleanType, DefaultDateType, DefaultTimeType, DefaultDateTimeType, DefaultListType):
    def __init__(self):
        DefaultNumericType.__init__(self)
        DefaultStringType.__init__(self)
        DefaultBooleanType.__init__(self)
        DefaultDateType.__init__(self)
        DefaultTimeType.__init__(self)
        DefaultDateTimeType.__init__(self)
        DefaultListType.__init__(self)
