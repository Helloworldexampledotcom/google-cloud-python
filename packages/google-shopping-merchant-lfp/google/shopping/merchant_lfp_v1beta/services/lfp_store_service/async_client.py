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
from collections import OrderedDict
import functools
import re
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.shopping.merchant_lfp_v1beta import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.shopping.merchant_lfp_v1beta.services.lfp_store_service import pagers
from google.shopping.merchant_lfp_v1beta.types import lfpstore

from .client import LfpStoreServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, LfpStoreServiceTransport
from .transports.grpc_asyncio import LfpStoreServiceGrpcAsyncIOTransport


class LfpStoreServiceAsyncClient:
    """Service for a `LFP
    partner <https://support.google.com/merchants/answer/7676652>`__ to
    submit local stores for a merchant.
    """

    _client: LfpStoreServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = LfpStoreServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = LfpStoreServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = LfpStoreServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = LfpStoreServiceClient._DEFAULT_UNIVERSE

    lfp_store_path = staticmethod(LfpStoreServiceClient.lfp_store_path)
    parse_lfp_store_path = staticmethod(LfpStoreServiceClient.parse_lfp_store_path)
    common_billing_account_path = staticmethod(
        LfpStoreServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        LfpStoreServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(LfpStoreServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        LfpStoreServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        LfpStoreServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        LfpStoreServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(LfpStoreServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        LfpStoreServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(LfpStoreServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        LfpStoreServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LfpStoreServiceAsyncClient: The constructed client.
        """
        return LfpStoreServiceClient.from_service_account_info.__func__(LfpStoreServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LfpStoreServiceAsyncClient: The constructed client.
        """
        return LfpStoreServiceClient.from_service_account_file.__func__(LfpStoreServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return LfpStoreServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> LfpStoreServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            LfpStoreServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = functools.partial(
        type(LfpStoreServiceClient).get_transport_class, type(LfpStoreServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str, LfpStoreServiceTransport, Callable[..., LfpStoreServiceTransport]
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the lfp store service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,LfpStoreServiceTransport,Callable[..., LfpStoreServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the LfpStoreServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = LfpStoreServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_lfp_store(
        self,
        request: Optional[Union[lfpstore.GetLfpStoreRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> lfpstore.LfpStore:
        r"""Retrieves information about a store.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_lfp_v1beta

            async def sample_get_lfp_store():
                # Create a client
                client = merchant_lfp_v1beta.LfpStoreServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_lfp_v1beta.GetLfpStoreRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_lfp_store(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_lfp_v1beta.types.GetLfpStoreRequest, dict]]):
                The request object. Request message for the ``GetLfpStore`` method.
            name (:class:`str`):
                Required. The name of the store to retrieve. Format:
                ``accounts/{account}/lfpStores/{target_merchant}~{store_code}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_lfp_v1beta.types.LfpStore:
                A store for the merchant. This will
                be used to match to a store under the
                Google Business Profile of the target
                merchant. If a matching store can't be
                found, the inventories or sales
                submitted with the store code will not
                be used.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, lfpstore.GetLfpStoreRequest):
            request = lfpstore.GetLfpStoreRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_lfp_store
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def insert_lfp_store(
        self,
        request: Optional[Union[lfpstore.InsertLfpStoreRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        lfp_store: Optional[lfpstore.LfpStore] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> lfpstore.LfpStore:
        r"""Inserts a store for the target merchant. If the store
        with the same store code already exists, it will be
        replaced.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_lfp_v1beta

            async def sample_insert_lfp_store():
                # Create a client
                client = merchant_lfp_v1beta.LfpStoreServiceAsyncClient()

                # Initialize request argument(s)
                lfp_store = merchant_lfp_v1beta.LfpStore()
                lfp_store.target_account = 1491
                lfp_store.store_code = "store_code_value"
                lfp_store.store_address = "store_address_value"

                request = merchant_lfp_v1beta.InsertLfpStoreRequest(
                    parent="parent_value",
                    lfp_store=lfp_store,
                )

                # Make the request
                response = await client.insert_lfp_store(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_lfp_v1beta.types.InsertLfpStoreRequest, dict]]):
                The request object. Request message for the
                InsertLfpStore method.
            parent (:class:`str`):
                Required. The LFP provider account Format:
                ``accounts/{account}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            lfp_store (:class:`google.shopping.merchant_lfp_v1beta.types.LfpStore`):
                Required. The store to insert.
                This corresponds to the ``lfp_store`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_lfp_v1beta.types.LfpStore:
                A store for the merchant. This will
                be used to match to a store under the
                Google Business Profile of the target
                merchant. If a matching store can't be
                found, the inventories or sales
                submitted with the store code will not
                be used.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, lfp_store])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, lfpstore.InsertLfpStoreRequest):
            request = lfpstore.InsertLfpStoreRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if lfp_store is not None:
            request.lfp_store = lfp_store

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.insert_lfp_store
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_lfp_store(
        self,
        request: Optional[Union[lfpstore.DeleteLfpStoreRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a store for a target merchant.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_lfp_v1beta

            async def sample_delete_lfp_store():
                # Create a client
                client = merchant_lfp_v1beta.LfpStoreServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_lfp_v1beta.DeleteLfpStoreRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_lfp_store(request=request)

        Args:
            request (Optional[Union[google.shopping.merchant_lfp_v1beta.types.DeleteLfpStoreRequest, dict]]):
                The request object. Request message for the
                DeleteLfpStore method.
            name (:class:`str`):
                Required. The name of the store to delete for the target
                merchant account. Format:
                ``accounts/{account}/lfpStores/{target_merchant}~{store_code}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, lfpstore.DeleteLfpStoreRequest):
            request = lfpstore.DeleteLfpStoreRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_lfp_store
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_lfp_stores(
        self,
        request: Optional[Union[lfpstore.ListLfpStoresRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLfpStoresAsyncPager:
        r"""Lists the stores of the target merchant, specified by the filter
        in ``ListLfpStoresRequest``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_lfp_v1beta

            async def sample_list_lfp_stores():
                # Create a client
                client = merchant_lfp_v1beta.LfpStoreServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_lfp_v1beta.ListLfpStoresRequest(
                    parent="parent_value",
                    target_account=1491,
                )

                # Make the request
                page_result = client.list_lfp_stores(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_lfp_v1beta.types.ListLfpStoresRequest, dict]]):
                The request object. Request message for the ListLfpStores
                method.
            parent (:class:`str`):
                Required. The LFP partner. Format:
                ``accounts/{account}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_lfp_v1beta.services.lfp_store_service.pagers.ListLfpStoresAsyncPager:
                Response message for the
                ListLfpStores method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, lfpstore.ListLfpStoresRequest):
            request = lfpstore.ListLfpStoresRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_lfp_stores
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListLfpStoresAsyncPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "LfpStoreServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("LfpStoreServiceAsyncClient",)
