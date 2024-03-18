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

from google.apps.chat_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.apps.chat_v1.services.chat_service import pagers
from google.apps.chat_v1.types import (
    annotation,
    attachment,
    contextual_addon,
    deletion_metadata,
    group,
    history_state,
    matched_url,
)
from google.apps.chat_v1.types import membership
from google.apps.chat_v1.types import membership as gc_membership
from google.apps.chat_v1.types import message
from google.apps.chat_v1.types import message as gc_message
from google.apps.chat_v1.types import reaction
from google.apps.chat_v1.types import reaction as gc_reaction
from google.apps.chat_v1.types import slash_command
from google.apps.chat_v1.types import space
from google.apps.chat_v1.types import space as gc_space
from google.apps.chat_v1.types import space_setup, user

from .client import ChatServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, ChatServiceTransport
from .transports.grpc_asyncio import ChatServiceGrpcAsyncIOTransport


class ChatServiceAsyncClient:
    """Enables developers to build Chat apps and
    integrations on Google Chat Platform.
    """

    _client: ChatServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = ChatServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ChatServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = ChatServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = ChatServiceClient._DEFAULT_UNIVERSE

    attachment_path = staticmethod(ChatServiceClient.attachment_path)
    parse_attachment_path = staticmethod(ChatServiceClient.parse_attachment_path)
    membership_path = staticmethod(ChatServiceClient.membership_path)
    parse_membership_path = staticmethod(ChatServiceClient.parse_membership_path)
    message_path = staticmethod(ChatServiceClient.message_path)
    parse_message_path = staticmethod(ChatServiceClient.parse_message_path)
    quoted_message_metadata_path = staticmethod(
        ChatServiceClient.quoted_message_metadata_path
    )
    parse_quoted_message_metadata_path = staticmethod(
        ChatServiceClient.parse_quoted_message_metadata_path
    )
    reaction_path = staticmethod(ChatServiceClient.reaction_path)
    parse_reaction_path = staticmethod(ChatServiceClient.parse_reaction_path)
    space_path = staticmethod(ChatServiceClient.space_path)
    parse_space_path = staticmethod(ChatServiceClient.parse_space_path)
    thread_path = staticmethod(ChatServiceClient.thread_path)
    parse_thread_path = staticmethod(ChatServiceClient.parse_thread_path)
    common_billing_account_path = staticmethod(
        ChatServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ChatServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ChatServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(ChatServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(ChatServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        ChatServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ChatServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ChatServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ChatServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ChatServiceClient.parse_common_location_path
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
            ChatServiceAsyncClient: The constructed client.
        """
        return ChatServiceClient.from_service_account_info.__func__(ChatServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ChatServiceAsyncClient: The constructed client.
        """
        return ChatServiceClient.from_service_account_file.__func__(ChatServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return ChatServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ChatServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ChatServiceTransport: The transport used by the client instance.
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
        type(ChatServiceClient).get_transport_class, type(ChatServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, ChatServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the chat service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ChatServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
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
        self._client = ChatServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_message(
        self,
        request: Optional[Union[gc_message.CreateMessageRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        message: Optional[gc_message.Message] = None,
        message_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gc_message.Message:
        r"""Creates a message in a Google Chat space. For an example, see
        `Create a
        message <https://developers.google.com/chat/api/guides/v1/messages/create>`__.

        Calling this method requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__
        and supports the following authentication types:

        -  For text messages, user authentication or app authentication
           are supported.
        -  For card messages, only app authentication is supported.
           (Only Chat apps can create card messages.)

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_create_message():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.CreateMessageRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.CreateMessageRequest, dict]]):
                The request object. Creates a message.
            parent (:class:`str`):
                Required. The resource name of the space in which to
                create a message.

                Format: ``spaces/{space}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            message (:class:`google.apps.chat_v1.types.Message`):
                Required. Message body.
                This corresponds to the ``message`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            message_id (:class:`str`):
                Optional. A custom ID for a message. Lets Chat apps get,
                update, or delete a message without needing to store the
                system-assigned ID in the message's resource name
                (represented in the message ``name`` field).

                The value for this field must meet the following
                requirements:

                -  Begins with ``client-``. For example,
                   ``client-custom-name`` is a valid custom ID, but
                   ``custom-name`` is not.
                -  Contains up to 63 characters and only lowercase
                   letters, numbers, and hyphens.
                -  Is unique within a space. A Chat app can't use the
                   same custom ID for different messages.

                For details, see `Name a
                message <https://developers.google.com/chat/api/guides/v1/messages/create#name_a_created_message>`__.

                This corresponds to the ``message_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Message:
                A message in a Google Chat space.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, message, message_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gc_message.CreateMessageRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if message is not None:
            request.message = message
        if message_id is not None:
            request.message_id = message_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_message,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def list_messages(
        self,
        request: Optional[Union[message.ListMessagesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMessagesAsyncPager:
        r"""Lists messages in a space that the caller is a member of,
        including messages from blocked members and spaces. For an
        example, see `List
        messages </chat/api/guides/v1/messages/list>`__. Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_list_messages():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.ListMessagesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_messages(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.ListMessagesRequest, dict]]):
                The request object. Lists messages in the specified
                space, that the user is a member of.
            parent (:class:`str`):
                Required. The resource name of the space to list
                messages from.

                Format: ``spaces/{space}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListMessagesAsyncPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = message.ListMessagesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_messages,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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
        response = pagers.ListMessagesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_memberships(
        self,
        request: Optional[Union[membership.ListMembershipsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMembershipsAsyncPager:
        r"""Lists memberships in a space. For an example, see `List
        memberships <https://developers.google.com/chat/api/guides/v1/members/list>`__.
        Listing memberships with `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        lists memberships in spaces that the Chat app has access to, but
        excludes Chat app memberships, including its own. Listing
        memberships with `User
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__
        lists memberships in spaces that the authenticated user has
        access to.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_list_memberships():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.ListMembershipsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_memberships(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.ListMembershipsRequest, dict]]):
                The request object.
            parent (:class:`str`):
                Required. The resource name of the
                space for which to fetch a membership
                list.

                Format: spaces/{space}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListMembershipsAsyncPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = membership.ListMembershipsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_memberships,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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
        response = pagers.ListMembershipsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_membership(
        self,
        request: Optional[Union[membership.GetMembershipRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> membership.Membership:
        r"""Returns details about a membership. For an example, see `Get a
        membership <https://developers.google.com/chat/api/guides/v1/members/get>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_get_membership():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.GetMembershipRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_membership(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.GetMembershipRequest, dict]]):
                The request object.
            name (:class:`str`):
                Required. Resource name of the membership to retrieve.

                To get the app's own membership, you can optionally use
                ``spaces/{space}/members/app``.

                Format: ``spaces/{space}/members/{member}`` or
                ``spaces/{space}/members/app``

                When `authenticated as a
                user <https://developers.google.com/chat/api/guides/auth/users>`__,
                you can use the user's email as an alias for
                ``{member}``. For example,
                ``spaces/{space}/members/example@gmail.com`` where
                ``example@gmail.com`` is the email of the Google Chat
                user.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Membership:
                Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = membership.GetMembershipRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_membership,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def get_message(
        self,
        request: Optional[Union[message.GetMessageRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> message.Message:
        r"""Returns details about a message. For an example, see `Read a
        message <https://developers.google.com/chat/api/guides/v1/messages/get>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Note: Might return a message from a blocked member or space.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_get_message():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.GetMessageRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.GetMessageRequest, dict]]):
                The request object.
            name (:class:`str`):
                Required. Resource name of the message.

                Format: ``spaces/{space}/messages/{message}``

                If you've set a custom ID for your message, you can use
                the value from the ``clientAssignedMessageId`` field for
                ``{message}``. For details, see [Name a message]
                (https://developers.google.com/chat/api/guides/v1/messages/create#name_a_created_message).

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Message:
                A message in a Google Chat space.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = message.GetMessageRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_message,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def update_message(
        self,
        request: Optional[Union[gc_message.UpdateMessageRequest, dict]] = None,
        *,
        message: Optional[gc_message.Message] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gc_message.Message:
        r"""Updates a message. There's a difference between the ``patch``
        and ``update`` methods. The ``patch`` method uses a ``patch``
        request while the ``update`` method uses a ``put`` request. We
        recommend using the ``patch`` method. For an example, see
        `Update a
        message <https://developers.google.com/chat/api/guides/v1/messages/update>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.
        When using app authentication, requests can only update messages
        created by the calling Chat app.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_update_message():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.UpdateMessageRequest(
                )

                # Make the request
                response = await client.update_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.UpdateMessageRequest, dict]]):
                The request object.
            message (:class:`google.apps.chat_v1.types.Message`):
                Required. Message with fields
                updated.

                This corresponds to the ``message`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The field paths to update. Separate multiple
                values with commas or use ``*`` to update all field
                paths.

                Currently supported field paths:

                -  ``text``

                -  ``attachment``

                -  ``cards`` (Requires `app
                   authentication </chat/api/guides/auth/service-accounts>`__.)

                -  ``cards_v2`` (Requires `app
                   authentication </chat/api/guides/auth/service-accounts>`__.)

                -  Developer Preview: ``accessory_widgets`` (Requires
                   `app
                   authentication </chat/api/guides/auth/service-accounts>`__.)

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Message:
                A message in a Google Chat space.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([message, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gc_message.UpdateMessageRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if message is not None:
            request.message = message
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_message,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("message.name", request.message.name),)
            ),
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

    async def delete_message(
        self,
        request: Optional[Union[message.DeleteMessageRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a message. For an example, see `Delete a
        message <https://developers.google.com/chat/api/guides/v1/messages/delete>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.
        When using app authentication, requests can only delete messages
        created by the calling Chat app.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_delete_message():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteMessageRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_message(request=request)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.DeleteMessageRequest, dict]]):
                The request object.
            name (:class:`str`):
                Required. Resource name of the message.

                Format: ``spaces/{space}/messages/{message}``

                If you've set a custom ID for your message, you can use
                the value from the ``clientAssignedMessageId`` field for
                ``{message}``. For details, see [Name a message]
                (https://developers.google.com/chat/api/guides/v1/messages/create#name_a_created_message).

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = message.DeleteMessageRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_message,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def get_attachment(
        self,
        request: Optional[Union[attachment.GetAttachmentRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> attachment.Attachment:
        r"""Gets the metadata of a message attachment. The attachment data
        is fetched using the `media
        API <https://developers.google.com/chat/api/reference/rest/v1/media/download>`__.
        For an example, see `Get a message
        attachment <https://developers.google.com/chat/api/guides/v1/media-and-attachments/get>`__.
        Requires `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_get_attachment():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.GetAttachmentRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_attachment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.GetAttachmentRequest, dict]]):
                The request object.
            name (:class:`str`):
                Required. Resource name of the attachment, in the form
                ``spaces/*/messages/*/attachments/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Attachment:
                An attachment in Google Chat.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = attachment.GetAttachmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_attachment,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def upload_attachment(
        self,
        request: Optional[Union[attachment.UploadAttachmentRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> attachment.UploadAttachmentResponse:
        r"""Uploads an attachment. For an example, see `Upload media as a
        file
        attachment <https://developers.google.com/chat/api/guides/v1/media-and-attachments/upload>`__.
        Requires user
        `authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        You can upload attachments up to 200 MB. Certain file types
        aren't supported. For details, see `File types blocked by Google
        Chat <https://support.google.com/chat/answer/7651457?&co=GENIE.Platform%3DDesktop#File%20types%20blocked%20in%20Google%20Chat>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_upload_attachment():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.UploadAttachmentRequest(
                    parent="parent_value",
                    filename="filename_value",
                )

                # Make the request
                response = await client.upload_attachment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.UploadAttachmentRequest, dict]]):
                The request object.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.UploadAttachmentResponse:

        """
        # Create or coerce a protobuf request object.
        request = attachment.UploadAttachmentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.upload_attachment,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def list_spaces(
        self,
        request: Optional[Union[space.ListSpacesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSpacesAsyncPager:
        r"""Lists spaces the caller is a member of. Group chats and DMs
        aren't listed until the first message is sent. For an example,
        see `List
        spaces <https://developers.google.com/chat/api/guides/v1/spaces/list>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        Lists spaces visible to the caller or authenticated user. Group
        chats and DMs aren't listed until the first message is sent.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_list_spaces():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.ListSpacesRequest(
                )

                # Make the request
                page_result = client.list_spaces(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.ListSpacesRequest, dict]]):
                The request object. A request to list the spaces the
                caller is a member of.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListSpacesAsyncPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = space.ListSpacesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_spaces,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
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
        response = pagers.ListSpacesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_space(
        self,
        request: Optional[Union[space.GetSpaceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> space.Space:
        r"""Returns details about a space. For an example, see `Get a
        space <https://developers.google.com/chat/api/guides/v1/spaces/get>`__.

        Requires
        `authentication <https://developers.google.com/chat/api/guides/auth>`__.
        Supports `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__
        and `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_get_space():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.GetSpaceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.GetSpaceRequest, dict]]):
                The request object. A request to return a single space.
            name (:class:`str`):
                Required. Resource name of the space, in the form
                ``"spaces/*"``.

                Format: ``spaces/{space}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = space.GetSpaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_space,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def create_space(
        self,
        request: Optional[Union[gc_space.CreateSpaceRequest, dict]] = None,
        *,
        space: Optional[gc_space.Space] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gc_space.Space:
        r"""Creates a named space. Spaces grouped by topics aren't
        supported. For an example, see `Create a
        space <https://developers.google.com/chat/api/guides/v1/spaces/create>`__.

        If you receive the error message ``ALREADY_EXISTS`` when
        creating a space, try a different ``displayName``. An existing
        space within the Google Workspace organization might already use
        this display name.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_create_space():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.CreateSpaceRequest(
                )

                # Make the request
                response = await client.create_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.CreateSpaceRequest, dict]]):
                The request object.
            space (:class:`google.apps.chat_v1.types.Space`):
                Required. The ``displayName`` and ``spaceType`` fields
                must be populated. Only ``SpaceType.SPACE`` is
                supported.

                If you receive the error message ``ALREADY_EXISTS`` when
                creating a space, try a different ``displayName``. An
                existing space within the Google Workspace organization
                might already use this display name.

                The space ``name`` is assigned on the server so anything
                specified in this field will be ignored.

                This corresponds to the ``space`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([space])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gc_space.CreateSpaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if space is not None:
            request.space = space

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_space,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
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

    async def set_up_space(
        self,
        request: Optional[Union[space_setup.SetUpSpaceRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> space.Space:
        r"""Creates a space and adds specified users to it. The calling user
        is automatically added to the space, and shouldn't be specified
        as a membership in the request. For an example, see `Set up a
        space <https://developers.google.com/chat/api/guides/v1/spaces/set-up>`__.

        To specify the human members to add, add memberships with the
        appropriate ``member.name`` in the ``SetUpSpaceRequest``. To add
        a human user, use ``users/{user}``, where ``{user}`` can be the
        email address for the user. For users in the same Workspace
        organization ``{user}`` can also be the ``id`` for the person
        from the People API, or the ``id`` for the user in the Directory
        API. For example, if the People API Person profile ID for
        ``user@example.com`` is ``123456789``, you can add the user to
        the space by setting the ``membership.member.name`` to
        ``users/user@example.com`` or ``users/123456789``.

        For a space or group chat, if the caller blocks or is blocked by
        some members, then those members aren't added to the created
        space.

        To create a direct message (DM) between the calling user and
        another human user, specify exactly one membership to represent
        the human user. If one user blocks the other, the request fails
        and the DM isn't created.

        To create a DM between the calling user and the calling app, set
        ``Space.singleUserBotDm`` to ``true`` and don't specify any
        memberships. You can only use this method to set up a DM with
        the calling app. To add the calling app as a member of a space
        or an existing DM between two human users, see `create a
        membership <https://developers.google.com/chat/api/guides/v1/members/create>`__.

        If a DM already exists between two users, even when one user
        blocks the other at the time a request is made, then the
        existing DM is returned.

        Spaces with threaded replies aren't supported. If you receive
        the error message ``ALREADY_EXISTS`` when setting up a space,
        try a different ``displayName``. An existing space within the
        Google Workspace organization might already use this display
        name.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_set_up_space():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.SetUpSpaceRequest(
                )

                # Make the request
                response = await client.set_up_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.SetUpSpaceRequest, dict]]):
                The request object.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        request = space_setup.SetUpSpaceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_up_space,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
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

    async def update_space(
        self,
        request: Optional[Union[gc_space.UpdateSpaceRequest, dict]] = None,
        *,
        space: Optional[gc_space.Space] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gc_space.Space:
        r"""Updates a space. For an example, see `Update a
        space <https://developers.google.com/chat/api/guides/v1/spaces/update>`__.

        If you're updating the ``displayName`` field and receive the
        error message ``ALREADY_EXISTS``, try a different display name..
        An existing space within the Google Workspace organization might
        already use this display name.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_update_space():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.UpdateSpaceRequest(
                )

                # Make the request
                response = await client.update_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.UpdateSpaceRequest, dict]]):
                The request object. A request to update a single space.
            space (:class:`google.apps.chat_v1.types.Space`):
                Required. Space with fields to be updated.
                ``Space.name`` must be populated in the form of
                ``spaces/{space}``. Only fields specified by
                ``update_mask`` are updated.

                This corresponds to the ``space`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The updated field paths, comma separated if
                there are multiple.

                Currently supported field paths:

                -  ``display_name`` (Only supports changing the display
                   name of a space with the ``SPACE`` type, or when also
                   including the ``space_type`` mask to change a
                   ``GROUP_CHAT`` space type to ``SPACE``. Trying to
                   update the display name of a ``GROUP_CHAT`` or a
                   ``DIRECT_MESSAGE`` space results in an invalid
                   argument error. If you receive the error message
                   ``ALREADY_EXISTS`` when updating the ``displayName``,
                   try a different ``displayName``. An existing space
                   within the Google Workspace organization might
                   already use this display name.)

                -  ``space_type`` (Only supports changing a
                   ``GROUP_CHAT`` space type to ``SPACE``. Include
                   ``display_name`` together with ``space_type`` in the
                   update mask and ensure that the specified space has a
                   non-empty display name and the ``SPACE`` space type.
                   Including the ``space_type`` mask and the ``SPACE``
                   type in the specified space when updating the display
                   name is optional if the existing space already has
                   the ``SPACE`` type. Trying to update the space type
                   in other ways results in an invalid argument error).

                -  ``space_details``

                -  ``space_history_state`` (Supports `turning history on
                   or off for the
                   space <https://support.google.com/chat/answer/7664687>`__
                   if `the organization allows users to change their
                   history
                   setting <https://support.google.com/a/answer/7664184>`__.
                   Warning: mutually exclusive with all other field
                   paths.)

                -  Developer Preview: ``access_settings.audience``
                   (Supports changing the `access
                   setting <https://support.google.com/chat/answer/11971020>`__
                   of a space. If no audience is specified in the access
                   setting, the space's access setting is updated to
                   restricted. Warning: mutually exclusive with all
                   other field paths.)

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([space, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gc_space.UpdateSpaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if space is not None:
            request.space = space
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_space,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("space.name", request.space.name),)
            ),
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

    async def delete_space(
        self,
        request: Optional[Union[space.DeleteSpaceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a named space. Always performs a cascading delete, which
        means that the space's child resources—like messages posted in
        the space and memberships in the space—are also deleted. For an
        example, see `Delete a
        space <https://developers.google.com/chat/api/guides/v1/spaces/delete>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__
        from a user who has permission to delete the space.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_delete_space():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteSpaceRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_space(request=request)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.DeleteSpaceRequest, dict]]):
                The request object. Request for deleting a space.
            name (:class:`str`):
                Required. Resource name of the space to delete.

                Format: ``spaces/{space}``

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = space.DeleteSpaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_space,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def complete_import_space(
        self,
        request: Optional[Union[space.CompleteImportSpaceRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> space.CompleteImportSpaceResponse:
        r"""Completes the `import
        process <https://developers.google.com/chat/api/guides/import-data>`__
        for the specified space and makes it visible to users. Requires
        app authentication and domain-wide delegation. For more
        information, see `Authorize Google Chat apps to import
        data <https://developers.google.com/chat/api/guides/authorize-import>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_complete_import_space():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.CompleteImportSpaceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.complete_import_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.CompleteImportSpaceRequest, dict]]):
                The request object. Request message for completing the
                import process for a space.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.CompleteImportSpaceResponse:

        """
        # Create or coerce a protobuf request object.
        request = space.CompleteImportSpaceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.complete_import_space,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def find_direct_message(
        self,
        request: Optional[Union[space.FindDirectMessageRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> space.Space:
        r"""Returns the existing direct message with the specified user. If
        no direct message space is found, returns a ``404 NOT_FOUND``
        error. For an example, see `Find a direct
        message </chat/api/guides/v1/spaces/find-direct-message>`__.

        With `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__,
        returns the direct message space between the specified user and
        the authenticated user.

        With `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__,
        returns the direct message space between the specified user and
        the calling Chat app.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__
        or `app
        authentication <https://developers.google.com/chat/api/guides/auth/service-accounts>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_find_direct_message():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.FindDirectMessageRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.find_direct_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.FindDirectMessageRequest, dict]]):
                The request object. A request to get direct message space
                based on the user resource.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        request = space.FindDirectMessageRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.find_direct_message,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
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

    async def create_membership(
        self,
        request: Optional[Union[gc_membership.CreateMembershipRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        membership: Optional[gc_membership.Membership] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gc_membership.Membership:
        r"""Creates a human membership or app membership for the calling
        app. Creating memberships for other apps isn't supported. For an
        example, see `Create a
        membership <https://developers.google.com/chat/api/guides/v1/members/create>`__.
        When creating a membership, if the specified member has their
        auto-accept policy turned off, then they're invited, and must
        accept the space invitation before joining. Otherwise, creating
        a membership adds the member directly to the specified space.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        To specify the member to add, set the ``membership.member.name``
        in the ``CreateMembershipRequest``:

        -  To add the calling app to a space or a direct message between
           two human users, use ``users/app``. Unable to add other apps
           to the space.

        -  To add a human user, use ``users/{user}``, where ``{user}``
           can be the email address for the user. For users in the same
           Workspace organization ``{user}`` can also be the ``id`` for
           the person from the People API, or the ``id`` for the user in
           the Directory API. For example, if the People API Person
           profile ID for ``user@example.com`` is ``123456789``, you can
           add the user to the space by setting the
           ``membership.member.name`` to ``users/user@example.com`` or
           ``users/123456789``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_create_membership():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.CreateMembershipRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_membership(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.CreateMembershipRequest, dict]]):
                The request object.
            parent (:class:`str`):
                Required. The resource name of the
                space for which to create the
                membership.

                Format: spaces/{space}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            membership (:class:`google.apps.chat_v1.types.Membership`):
                Required. The membership relation to create. The
                ``memberType`` field must contain a user with the
                ``user.name`` and ``user.type`` fields populated. The
                server will assign a resource name and overwrite
                anything specified. When a Chat app creates a membership
                relation for a human user, it must use the
                ``chat.memberships`` scope, set ``user.type`` to
                ``HUMAN``, and set ``user.name`` with format
                ``users/{user}``, where ``{user}`` can be the email
                address for the user. For users in the same Workspace
                organization ``{user}`` can also be the ``id`` of the
                `person <https://developers.google.com/people/api/rest/v1/people>`__
                from the People API, or the ``id`` for the user in the
                Directory API. For example, if the People API Person
                profile ID for ``user@example.com`` is ``123456789``,
                you can add the user to the space by setting the
                ``membership.member.name`` to ``users/user@example.com``
                or ``users/123456789``. When a Chat app creates a
                membership relation for itself, it must use the
                ``chat.memberships.app`` scope, set ``user.type`` to
                ``BOT``, and set ``user.name`` to ``users/app``.

                This corresponds to the ``membership`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Membership:
                Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, membership])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gc_membership.CreateMembershipRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if membership is not None:
            request.membership = membership

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_membership,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def delete_membership(
        self,
        request: Optional[Union[membership.DeleteMembershipRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> membership.Membership:
        r"""Deletes a membership. For an example, see `Delete a
        membership <https://developers.google.com/chat/api/guides/v1/members/delete>`__.

        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_delete_membership():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteMembershipRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.delete_membership(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.DeleteMembershipRequest, dict]]):
                The request object.
            name (:class:`str`):
                Required. Resource name of the membership to delete.
                Chat apps can delete human users' or their own
                memberships. Chat apps can't delete other apps'
                memberships.

                When deleting a human membership, requires the
                ``chat.memberships`` scope and
                ``spaces/{space}/members/{member}`` format. You can use
                the email as an alias for ``{member}``. For example,
                ``spaces/{space}/members/example@gmail.com`` where
                ``example@gmail.com`` is the email of the Google Chat
                user.

                When deleting an app membership, requires the
                ``chat.memberships.app`` scope and
                ``spaces/{space}/members/app`` format.

                Format: ``spaces/{space}/members/{member}`` or
                ``spaces/{space}/members/app``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Membership:
                Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = membership.DeleteMembershipRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_membership,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def create_reaction(
        self,
        request: Optional[Union[gc_reaction.CreateReactionRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        reaction: Optional[gc_reaction.Reaction] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gc_reaction.Reaction:
        r"""Creates a reaction and adds it to a message. For an example, see
        `Create a
        reaction <https://developers.google.com/chat/api/guides/v1/reactions/create>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.
        Only unicode emoji are supported.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_create_reaction():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.CreateReactionRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_reaction(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.CreateReactionRequest, dict]]):
                The request object. Creates a reaction to a message.
            parent (:class:`str`):
                Required. The message where the reaction is created.

                Format: ``spaces/{space}/messages/{message}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            reaction (:class:`google.apps.chat_v1.types.Reaction`):
                Required. The reaction to create.
                This corresponds to the ``reaction`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.types.Reaction:
                A reaction to a message.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, reaction])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gc_reaction.CreateReactionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if reaction is not None:
            request.reaction = reaction

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_reaction,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def list_reactions(
        self,
        request: Optional[Union[reaction.ListReactionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReactionsAsyncPager:
        r"""Lists reactions to a message. For an example, see `List
        reactions <https://developers.google.com/chat/api/guides/v1/reactions/list>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_list_reactions():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.ListReactionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_reactions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.ListReactionsRequest, dict]]):
                The request object. Lists reactions to a message.
            parent (:class:`str`):
                Required. The message users reacted to.

                Format: ``spaces/{space}/messages/{message}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListReactionsAsyncPager:
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reaction.ListReactionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_reactions,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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
        response = pagers.ListReactionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_reaction(
        self,
        request: Optional[Union[reaction.DeleteReactionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a reaction to a message. For an example, see `Delete a
        reaction <https://developers.google.com/chat/api/guides/v1/reactions/delete>`__.
        Requires `user
        authentication <https://developers.google.com/chat/api/guides/auth/users>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            async def sample_delete_reaction():
                # Create a client
                client = chat_v1.ChatServiceAsyncClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteReactionRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_reaction(request=request)

        Args:
            request (Optional[Union[google.apps.chat_v1.types.DeleteReactionRequest, dict]]):
                The request object. Deletes a reaction to a message.
            name (:class:`str`):
                Required. Name of the reaction to delete.

                Format:
                ``spaces/{space}/messages/{message}/reactions/{reaction}``

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reaction.DeleteReactionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_reaction,
            default_retry=retries.AsyncRetry(
                initial=1.0,
                maximum=10.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

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

    async def __aenter__(self) -> "ChatServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ChatServiceAsyncClient",)
