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

from google.cloud.iam_admin_v1.types import iam


class ListServiceAccountsPager:
    """A pager for iterating through ``list_service_accounts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.ListServiceAccountsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``accounts`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListServiceAccounts`` requests and continue to iterate
    through the ``accounts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.ListServiceAccountsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., iam.ListServiceAccountsResponse],
        request: iam.ListServiceAccountsRequest,
        response: iam.ListServiceAccountsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.ListServiceAccountsRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.ListServiceAccountsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.ListServiceAccountsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[iam.ListServiceAccountsResponse]:
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

    def __iter__(self) -> Iterator[iam.ServiceAccount]:
        for page in self.pages:
            yield from page.accounts

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServiceAccountsAsyncPager:
    """A pager for iterating through ``list_service_accounts`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.ListServiceAccountsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``accounts`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListServiceAccounts`` requests and continue to iterate
    through the ``accounts`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.ListServiceAccountsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[iam.ListServiceAccountsResponse]],
        request: iam.ListServiceAccountsRequest,
        response: iam.ListServiceAccountsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.ListServiceAccountsRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.ListServiceAccountsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.ListServiceAccountsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[iam.ListServiceAccountsResponse]:
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

    def __aiter__(self) -> AsyncIterator[iam.ServiceAccount]:
        async def async_generator():
            async for page in self.pages:
                for response in page.accounts:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class QueryGrantableRolesPager:
    """A pager for iterating through ``query_grantable_roles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.QueryGrantableRolesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``roles`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``QueryGrantableRoles`` requests and continue to iterate
    through the ``roles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.QueryGrantableRolesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., iam.QueryGrantableRolesResponse],
        request: iam.QueryGrantableRolesRequest,
        response: iam.QueryGrantableRolesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.QueryGrantableRolesRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.QueryGrantableRolesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.QueryGrantableRolesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[iam.QueryGrantableRolesResponse]:
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

    def __iter__(self) -> Iterator[iam.Role]:
        for page in self.pages:
            yield from page.roles

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class QueryGrantableRolesAsyncPager:
    """A pager for iterating through ``query_grantable_roles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.QueryGrantableRolesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``roles`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``QueryGrantableRoles`` requests and continue to iterate
    through the ``roles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.QueryGrantableRolesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[iam.QueryGrantableRolesResponse]],
        request: iam.QueryGrantableRolesRequest,
        response: iam.QueryGrantableRolesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.QueryGrantableRolesRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.QueryGrantableRolesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.QueryGrantableRolesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[iam.QueryGrantableRolesResponse]:
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

    def __aiter__(self) -> AsyncIterator[iam.Role]:
        async def async_generator():
            async for page in self.pages:
                for response in page.roles:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRolesPager:
    """A pager for iterating through ``list_roles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.ListRolesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``roles`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListRoles`` requests and continue to iterate
    through the ``roles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.ListRolesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., iam.ListRolesResponse],
        request: iam.ListRolesRequest,
        response: iam.ListRolesResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.ListRolesRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.ListRolesResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.ListRolesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[iam.ListRolesResponse]:
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

    def __iter__(self) -> Iterator[iam.Role]:
        for page in self.pages:
            yield from page.roles

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListRolesAsyncPager:
    """A pager for iterating through ``list_roles`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.ListRolesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``roles`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListRoles`` requests and continue to iterate
    through the ``roles`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.ListRolesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[iam.ListRolesResponse]],
        request: iam.ListRolesRequest,
        response: iam.ListRolesResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.ListRolesRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.ListRolesResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.ListRolesRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[iam.ListRolesResponse]:
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

    def __aiter__(self) -> AsyncIterator[iam.Role]:
        async def async_generator():
            async for page in self.pages:
                for response in page.roles:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class QueryTestablePermissionsPager:
    """A pager for iterating through ``query_testable_permissions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.QueryTestablePermissionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``permissions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``QueryTestablePermissions`` requests and continue to iterate
    through the ``permissions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.QueryTestablePermissionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., iam.QueryTestablePermissionsResponse],
        request: iam.QueryTestablePermissionsRequest,
        response: iam.QueryTestablePermissionsResponse,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.QueryTestablePermissionsRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.QueryTestablePermissionsResponse):
                The initial response object.
            retry (google.api_core.retry.Retry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.QueryTestablePermissionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[iam.QueryTestablePermissionsResponse]:
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

    def __iter__(self) -> Iterator[iam.Permission]:
        for page in self.pages:
            yield from page.permissions

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class QueryTestablePermissionsAsyncPager:
    """A pager for iterating through ``query_testable_permissions`` requests.

    This class thinly wraps an initial
    :class:`google.cloud.iam_admin_v1.types.QueryTestablePermissionsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``permissions`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``QueryTestablePermissions`` requests and continue to iterate
    through the ``permissions`` field on the
    corresponding responses.

    All the usual :class:`google.cloud.iam_admin_v1.types.QueryTestablePermissionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[iam.QueryTestablePermissionsResponse]],
        request: iam.QueryTestablePermissionsRequest,
        response: iam.QueryTestablePermissionsResponse,
        *,
        retry: OptionalAsyncRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiates the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.cloud.iam_admin_v1.types.QueryTestablePermissionsRequest):
                The initial request object.
            response (google.cloud.iam_admin_v1.types.QueryTestablePermissionsResponse):
                The initial response object.
            retry (google.api_core.retry.AsyncRetry): Designation of what errors,
                if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = iam.QueryTestablePermissionsRequest(request)
        self._response = response
        self._retry = retry
        self._timeout = timeout
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterator[iam.QueryTestablePermissionsResponse]:
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

    def __aiter__(self) -> AsyncIterator[iam.Permission]:
        async def async_generator():
            async for page in self.pages:
                for response in page.permissions:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
