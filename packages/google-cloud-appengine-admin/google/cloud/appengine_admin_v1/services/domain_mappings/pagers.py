# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import retry_async as retries_async

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
    OptionalAsyncRetry = Union[
        retries_async.AsyncRetry, gapic_v1.method._MethodDefault, None
    ]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore
    OptionalAsyncRetry = Union[retries_async.AsyncRetry, object, None]  # type: ignore

from google.cloud.appengine_admin_v1.types import appengine, domain_mapping


class ListDomainMappingsPager:
    """A pager for iterating through ``list_domain_mappings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.appengine_admin_v1.types.ListDomainMappingsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``domain_mappings`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListDomainMappings`` requests and continue to iterate
    through the ``domain_mappings`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.appengine_admin_v1.types.ListDomainMappingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., appengine.ListDomainMappingsResponse],
        request: appengine.ListDomainMappingsRequest,
        response: appengine.ListDomainMappingsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.appengine_admin_v1.types.ListDomainMappingsRequest):
                The initial request object.
            response (google.cloud.appengine_admin_v1.types.ListDomainMappingsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = appengine.ListDomainMappingsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[appengine.ListDomainMappingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __iter__(self) -> Iterator[domain_mapping.DomainMapping]:
        for page in self.pages:
            yield from page.domain_mappings

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListDomainMappingsAsyncPager:
    """A pager for iterating through ``list_domain_mappings`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.appengine_admin_v1.types.ListDomainMappingsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``domain_mappings`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListDomainMappings`` requests and continue to iterate
    through the ``domain_mappings`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.appengine_admin_v1.types.ListDomainMappingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[appengine.ListDomainMappingsResponse]],
        request: appengine.ListDomainMappingsRequest,
        response: appengine.ListDomainMappingsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.appengine_admin_v1.types.ListDomainMappingsRequest):
                The initial request object.
            response (google.cloud.appengine_admin_v1.types.ListDomainMappingsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = appengine.ListDomainMappingsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[appengine.ListDomainMappingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(
                self._request,
                retry=self._retry,
                timeout=self._timeout,
                metadata=self._metadata,
            )
            yield self._response

    def __aiter__(self) -> AsyncIterator[domain_mapping.DomainMapping]:
        async def async_generator():
            async for page in self.pages:
                for response in page.domain_mappings:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
