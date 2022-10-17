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
import logging

from jdmn.runtime.annotation.AnnotationSet import AnnotationSet
from jdmn.runtime.cache.Cache import Cache
from jdmn.runtime.cache.DefaultCache import DefaultCache
from jdmn.runtime.external.DefaultExternalFunctionExecutor import DefaultExternalFunctionExecutor
from jdmn.runtime.external.ExternalFunctionExecutor import ExternalFunctionExecutor
from jdmn.runtime.listener.EventListener import EventListener
from jdmn.runtime.listener.LoggingEventListener import LoggingEventListener


class ExecutionContext:
    LOGGER = logging.getLogger(__name__)

    def __init__(self, annotations: AnnotationSet = None,
                 eventListener: EventListener = None,
                 externalFunctionExecutor: ExternalFunctionExecutor = None,
                 cache: Cache = None):
        self.annotations = AnnotationSet() if annotations is None else annotations
        self.eventListener = LoggingEventListener(self.LOGGER) if eventListener is None else eventListener
        self.externalFunctionExecutor = DefaultExternalFunctionExecutor() if externalFunctionExecutor is None else externalFunctionExecutor
        self.cache = DefaultCache() if cache is None else cache
