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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
import math

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.edgecontainer_v1.services.edge_container import (
    EdgeContainerAsyncClient,
    EdgeContainerClient,
    pagers,
    transports,
)
from google.cloud.edgecontainer_v1.types import resources, service


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert EdgeContainerClient._get_default_mtls_endpoint(None) is None
    assert (
        EdgeContainerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        EdgeContainerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        EdgeContainerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        EdgeContainerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        EdgeContainerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


def test__read_environment_variables():
    assert EdgeContainerClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert EdgeContainerClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert EdgeContainerClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            EdgeContainerClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert EdgeContainerClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert EdgeContainerClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert EdgeContainerClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            EdgeContainerClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert EdgeContainerClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert EdgeContainerClient._get_client_cert_source(None, False) is None
    assert (
        EdgeContainerClient._get_client_cert_source(mock_provided_cert_source, False)
        is None
    )
    assert (
        EdgeContainerClient._get_client_cert_source(mock_provided_cert_source, True)
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                EdgeContainerClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                EdgeContainerClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    EdgeContainerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerClient),
)
@mock.patch.object(
    EdgeContainerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = EdgeContainerClient._DEFAULT_UNIVERSE
    default_endpoint = EdgeContainerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = EdgeContainerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        EdgeContainerClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        EdgeContainerClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == EdgeContainerClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        EdgeContainerClient._get_api_endpoint(None, None, default_universe, "auto")
        == default_endpoint
    )
    assert (
        EdgeContainerClient._get_api_endpoint(None, None, default_universe, "always")
        == EdgeContainerClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        EdgeContainerClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == EdgeContainerClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        EdgeContainerClient._get_api_endpoint(None, None, mock_universe, "never")
        == mock_endpoint
    )
    assert (
        EdgeContainerClient._get_api_endpoint(None, None, default_universe, "never")
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        EdgeContainerClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        EdgeContainerClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        EdgeContainerClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        EdgeContainerClient._get_universe_domain(None, None)
        == EdgeContainerClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        EdgeContainerClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (EdgeContainerClient, transports.EdgeContainerGrpcTransport, "grpc"),
        (EdgeContainerClient, transports.EdgeContainerRestTransport, "rest"),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=ga_credentials.AnonymousCredentials())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # TODO: This is needed to cater for older versions of google-auth
    # Make this test unconditional once the minimum supported version of
    # google-auth becomes 2.23.0 or higher.
    google_auth_major, google_auth_minor = [
        int(part) for part in google.auth.__version__.split(".")[0:2]
    ]
    if google_auth_major > 2 or (google_auth_major == 2 and google_auth_minor >= 23):
        credentials = ga_credentials.AnonymousCredentials()
        credentials._universe_domain = "foo.com"
        # Test the case when there is a universe mismatch from the credentials.
        client = client_class(transport=transport_class(credentials=credentials))
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )

        # Test the case when there is a universe mismatch from the client.
        #
        # TODO: Make this test unconditional once the minimum supported version of
        # google-api-core becomes 2.15.0 or higher.
        api_core_major, api_core_minor = [
            int(part) for part in api_core_version.__version__.split(".")[0:2]
        ]
        if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
            client = client_class(
                client_options={"universe_domain": "bar.com"},
                transport=transport_class(
                    credentials=ga_credentials.AnonymousCredentials(),
                ),
            )
            with pytest.raises(ValueError) as excinfo:
                client._validate_universe_domain()
            assert (
                str(excinfo.value)
                == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
            )

    # Test that ValueError is raised if universe_domain is provided via client options and credentials is None
    with pytest.raises(ValueError):
        client._compare_universes("foo.bar", None)


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (EdgeContainerClient, "grpc"),
        (EdgeContainerAsyncClient, "grpc_asyncio"),
        (EdgeContainerClient, "rest"),
    ],
)
def test_edge_container_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "edgecontainer.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://edgecontainer.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.EdgeContainerGrpcTransport, "grpc"),
        (transports.EdgeContainerGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.EdgeContainerRestTransport, "rest"),
    ],
)
def test_edge_container_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (EdgeContainerClient, "grpc"),
        (EdgeContainerAsyncClient, "grpc_asyncio"),
        (EdgeContainerClient, "rest"),
    ],
)
def test_edge_container_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "edgecontainer.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://edgecontainer.googleapis.com"
        )


def test_edge_container_client_get_transport_class():
    transport = EdgeContainerClient.get_transport_class()
    available_transports = [
        transports.EdgeContainerGrpcTransport,
        transports.EdgeContainerRestTransport,
    ]
    assert transport in available_transports

    transport = EdgeContainerClient.get_transport_class("grpc")
    assert transport == transports.EdgeContainerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (EdgeContainerClient, transports.EdgeContainerGrpcTransport, "grpc"),
        (
            EdgeContainerAsyncClient,
            transports.EdgeContainerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (EdgeContainerClient, transports.EdgeContainerRestTransport, "rest"),
    ],
)
@mock.patch.object(
    EdgeContainerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerClient),
)
@mock.patch.object(
    EdgeContainerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerAsyncClient),
)
def test_edge_container_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(EdgeContainerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(EdgeContainerClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (EdgeContainerClient, transports.EdgeContainerGrpcTransport, "grpc", "true"),
        (
            EdgeContainerAsyncClient,
            transports.EdgeContainerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (EdgeContainerClient, transports.EdgeContainerGrpcTransport, "grpc", "false"),
        (
            EdgeContainerAsyncClient,
            transports.EdgeContainerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (EdgeContainerClient, transports.EdgeContainerRestTransport, "rest", "true"),
        (EdgeContainerClient, transports.EdgeContainerRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    EdgeContainerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerClient),
)
@mock.patch.object(
    EdgeContainerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_edge_container_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [EdgeContainerClient, EdgeContainerAsyncClient]
)
@mock.patch.object(
    EdgeContainerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(EdgeContainerClient),
)
@mock.patch.object(
    EdgeContainerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(EdgeContainerAsyncClient),
)
def test_edge_container_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize(
    "client_class", [EdgeContainerClient, EdgeContainerAsyncClient]
)
@mock.patch.object(
    EdgeContainerClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerClient),
)
@mock.patch.object(
    EdgeContainerAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(EdgeContainerAsyncClient),
)
def test_edge_container_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = EdgeContainerClient._DEFAULT_UNIVERSE
    default_endpoint = EdgeContainerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = EdgeContainerClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (EdgeContainerClient, transports.EdgeContainerGrpcTransport, "grpc"),
        (
            EdgeContainerAsyncClient,
            transports.EdgeContainerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (EdgeContainerClient, transports.EdgeContainerRestTransport, "rest"),
    ],
)
def test_edge_container_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            EdgeContainerClient,
            transports.EdgeContainerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            EdgeContainerAsyncClient,
            transports.EdgeContainerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (EdgeContainerClient, transports.EdgeContainerRestTransport, "rest", None),
    ],
)
def test_edge_container_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_edge_container_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.edgecontainer_v1.services.edge_container.transports.EdgeContainerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = EdgeContainerClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            EdgeContainerClient,
            transports.EdgeContainerGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            EdgeContainerAsyncClient,
            transports.EdgeContainerGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_edge_container_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "edgecontainer.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="edgecontainer.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListClustersRequest,
        dict,
    ],
)
def test_list_clusters(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListClustersResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListClustersPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_clusters_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_clusters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListClustersRequest()


def test_list_clusters_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListClustersRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_clusters(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListClustersRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_clusters_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_clusters in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_clusters] = mock_rpc
        request = {}
        client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_clusters_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListClustersResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_clusters()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListClustersRequest()


@pytest.mark.asyncio
async def test_list_clusters_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_clusters
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_clusters
        ] = mock_object

        request = {}
        await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_clusters_async(
    transport: str = "grpc_asyncio", request_type=service.ListClustersRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListClustersResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListClustersRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListClustersAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_clusters_async_from_dict():
    await test_list_clusters_async(request_type=dict)


def test_list_clusters_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value = service.ListClustersResponse()
        client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_clusters_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListClustersRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListClustersResponse()
        )
        await client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_clusters_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListClustersResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_clusters(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_clusters_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_clusters(
            service.ListClustersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_clusters_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListClustersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListClustersResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_clusters(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_clusters_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_clusters(
            service.ListClustersRequest(),
            parent="parent_value",
        )


def test_list_clusters_pager(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                    resources.Cluster(),
                ],
                next_page_token="abc",
            ),
            service.ListClustersResponse(
                clusters=[],
                next_page_token="def",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                ],
                next_page_token="ghi",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_clusters(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Cluster) for i in results)


def test_list_clusters_pages(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_clusters), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                    resources.Cluster(),
                ],
                next_page_token="abc",
            ),
            service.ListClustersResponse(
                clusters=[],
                next_page_token="def",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                ],
                next_page_token="ghi",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_clusters(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_clusters_async_pager():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_clusters), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                    resources.Cluster(),
                ],
                next_page_token="abc",
            ),
            service.ListClustersResponse(
                clusters=[],
                next_page_token="def",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                ],
                next_page_token="ghi",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_clusters(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Cluster) for i in responses)


@pytest.mark.asyncio
async def test_list_clusters_async_pages():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_clusters), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                    resources.Cluster(),
                ],
                next_page_token="abc",
            ),
            service.ListClustersResponse(
                clusters=[],
                next_page_token="def",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                ],
                next_page_token="ghi",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_clusters(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetClusterRequest,
        dict,
    ],
)
def test_get_cluster(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Cluster(
            name="name_value",
            default_max_pods_per_node=2634,
            endpoint="endpoint_value",
            port=453,
            cluster_ca_certificate="cluster_ca_certificate_value",
            control_plane_version="control_plane_version_value",
            node_version="node_version_value",
            external_load_balancer_ipv4_address_pools=[
                "external_load_balancer_ipv4_address_pools_value"
            ],
            status=resources.Cluster.Status.PROVISIONING,
            target_version="target_version_value",
            release_channel=resources.Cluster.ReleaseChannel.NONE,
            external_load_balancer_ipv6_address_pools=[
                "external_load_balancer_ipv6_address_pools_value"
            ],
        )
        response = client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Cluster)
    assert response.name == "name_value"
    assert response.default_max_pods_per_node == 2634
    assert response.endpoint == "endpoint_value"
    assert response.port == 453
    assert response.cluster_ca_certificate == "cluster_ca_certificate_value"
    assert response.control_plane_version == "control_plane_version_value"
    assert response.node_version == "node_version_value"
    assert response.external_load_balancer_ipv4_address_pools == [
        "external_load_balancer_ipv4_address_pools_value"
    ]
    assert response.status == resources.Cluster.Status.PROVISIONING
    assert response.target_version == "target_version_value"
    assert response.release_channel == resources.Cluster.ReleaseChannel.NONE
    assert response.external_load_balancer_ipv6_address_pools == [
        "external_load_balancer_ipv6_address_pools_value"
    ]


def test_get_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetClusterRequest()


def test_get_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetClusterRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetClusterRequest(
            name="name_value",
        )


def test_get_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_cluster] = mock_rpc
        request = {}
        client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Cluster(
                name="name_value",
                default_max_pods_per_node=2634,
                endpoint="endpoint_value",
                port=453,
                cluster_ca_certificate="cluster_ca_certificate_value",
                control_plane_version="control_plane_version_value",
                node_version="node_version_value",
                external_load_balancer_ipv4_address_pools=[
                    "external_load_balancer_ipv4_address_pools_value"
                ],
                status=resources.Cluster.Status.PROVISIONING,
                target_version="target_version_value",
                release_channel=resources.Cluster.ReleaseChannel.NONE,
                external_load_balancer_ipv6_address_pools=[
                    "external_load_balancer_ipv6_address_pools_value"
                ],
            )
        )
        response = await client.get_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetClusterRequest()


@pytest.mark.asyncio
async def test_get_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_cluster
        ] = mock_object

        request = {}
        await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_cluster_async(
    transport: str = "grpc_asyncio", request_type=service.GetClusterRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Cluster(
                name="name_value",
                default_max_pods_per_node=2634,
                endpoint="endpoint_value",
                port=453,
                cluster_ca_certificate="cluster_ca_certificate_value",
                control_plane_version="control_plane_version_value",
                node_version="node_version_value",
                external_load_balancer_ipv4_address_pools=[
                    "external_load_balancer_ipv4_address_pools_value"
                ],
                status=resources.Cluster.Status.PROVISIONING,
                target_version="target_version_value",
                release_channel=resources.Cluster.ReleaseChannel.NONE,
                external_load_balancer_ipv6_address_pools=[
                    "external_load_balancer_ipv6_address_pools_value"
                ],
            )
        )
        response = await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Cluster)
    assert response.name == "name_value"
    assert response.default_max_pods_per_node == 2634
    assert response.endpoint == "endpoint_value"
    assert response.port == 453
    assert response.cluster_ca_certificate == "cluster_ca_certificate_value"
    assert response.control_plane_version == "control_plane_version_value"
    assert response.node_version == "node_version_value"
    assert response.external_load_balancer_ipv4_address_pools == [
        "external_load_balancer_ipv4_address_pools_value"
    ]
    assert response.status == resources.Cluster.Status.PROVISIONING
    assert response.target_version == "target_version_value"
    assert response.release_channel == resources.Cluster.ReleaseChannel.NONE
    assert response.external_load_balancer_ipv6_address_pools == [
        "external_load_balancer_ipv6_address_pools_value"
    ]


@pytest.mark.asyncio
async def test_get_cluster_async_from_dict():
    await test_get_cluster_async(request_type=dict)


def test_get_cluster_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value = resources.Cluster()
        client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_cluster_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Cluster())
        await client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_cluster_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Cluster()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_cluster_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cluster(
            service.GetClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_cluster_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Cluster()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Cluster())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_cluster_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_cluster(
            service.GetClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateClusterRequest,
        dict,
    ],
)
def test_create_cluster(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.CreateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateClusterRequest()


def test_create_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.CreateClusterRequest(
        parent="parent_value",
        cluster_id="cluster_id_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateClusterRequest(
            parent="parent_value",
            cluster_id="cluster_id_value",
            request_id="request_id_value",
        )


def test_create_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_cluster] = mock_rpc
        request = {}
        client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateClusterRequest()


@pytest.mark.asyncio
async def test_create_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_cluster
        ] = mock_object

        request = {}
        await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_cluster_async(
    transport: str = "grpc_asyncio", request_type=service.CreateClusterRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.CreateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_cluster_async_from_dict():
    await test_create_cluster_async(request_type=dict)


def test_create_cluster_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_cluster_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateClusterRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_cluster_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_cluster(
            parent="parent_value",
            cluster=resources.Cluster(name="name_value"),
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cluster
        mock_val = resources.Cluster(name="name_value")
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


def test_create_cluster_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cluster(
            service.CreateClusterRequest(),
            parent="parent_value",
            cluster=resources.Cluster(name="name_value"),
            cluster_id="cluster_id_value",
        )


@pytest.mark.asyncio
async def test_create_cluster_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_cluster(
            parent="parent_value",
            cluster=resources.Cluster(name="name_value"),
            cluster_id="cluster_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].cluster
        mock_val = resources.Cluster(name="name_value")
        assert arg == mock_val
        arg = args[0].cluster_id
        mock_val = "cluster_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_cluster_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_cluster(
            service.CreateClusterRequest(),
            parent="parent_value",
            cluster=resources.Cluster(name="name_value"),
            cluster_id="cluster_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateClusterRequest,
        dict,
    ],
)
def test_update_cluster(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.UpdateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateClusterRequest()


def test_update_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.UpdateClusterRequest(
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateClusterRequest(
            request_id="request_id_value",
        )


def test_update_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_cluster] = mock_rpc
        request = {}
        client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateClusterRequest()


@pytest.mark.asyncio
async def test_update_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_cluster
        ] = mock_object

        request = {}
        await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.update_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_cluster_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateClusterRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.UpdateClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_cluster_async_from_dict():
    await test_update_cluster_async(request_type=dict)


def test_update_cluster_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateClusterRequest()

    request.cluster.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cluster.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_cluster_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateClusterRequest()

    request.cluster.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cluster.name=name_value",
    ) in kw["metadata"]


def test_update_cluster_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_cluster(
            cluster=resources.Cluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].cluster
        mock_val = resources.Cluster(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_cluster_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cluster(
            service.UpdateClusterRequest(),
            cluster=resources.Cluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_cluster_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_cluster(
            cluster=resources.Cluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].cluster
        mock_val = resources.Cluster(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_cluster_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_cluster(
            service.UpdateClusterRequest(),
            cluster=resources.Cluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpgradeClusterRequest,
        dict,
    ],
)
def test_upgrade_cluster(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.upgrade_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.UpgradeClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_upgrade_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.upgrade_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpgradeClusterRequest()


def test_upgrade_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.UpgradeClusterRequest(
        name="name_value",
        target_version="target_version_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.upgrade_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpgradeClusterRequest(
            name="name_value",
            target_version="target_version_value",
            request_id="request_id_value",
        )


def test_upgrade_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.upgrade_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.upgrade_cluster] = mock_rpc
        request = {}
        client.upgrade_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.upgrade_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_upgrade_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.upgrade_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpgradeClusterRequest()


@pytest.mark.asyncio
async def test_upgrade_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.upgrade_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.upgrade_cluster
        ] = mock_object

        request = {}
        await client.upgrade_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.upgrade_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_upgrade_cluster_async(
    transport: str = "grpc_asyncio", request_type=service.UpgradeClusterRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.upgrade_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.UpgradeClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_upgrade_cluster_async_from_dict():
    await test_upgrade_cluster_async(request_type=dict)


def test_upgrade_cluster_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpgradeClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.upgrade_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_upgrade_cluster_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpgradeClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.upgrade_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_upgrade_cluster_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.upgrade_cluster(
            name="name_value",
            target_version="target_version_value",
            schedule=service.UpgradeClusterRequest.Schedule.IMMEDIATELY,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].target_version
        mock_val = "target_version_value"
        assert arg == mock_val
        arg = args[0].schedule
        mock_val = service.UpgradeClusterRequest.Schedule.IMMEDIATELY
        assert arg == mock_val


def test_upgrade_cluster_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.upgrade_cluster(
            service.UpgradeClusterRequest(),
            name="name_value",
            target_version="target_version_value",
            schedule=service.UpgradeClusterRequest.Schedule.IMMEDIATELY,
        )


@pytest.mark.asyncio
async def test_upgrade_cluster_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.upgrade_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.upgrade_cluster(
            name="name_value",
            target_version="target_version_value",
            schedule=service.UpgradeClusterRequest.Schedule.IMMEDIATELY,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].target_version
        mock_val = "target_version_value"
        assert arg == mock_val
        arg = args[0].schedule
        mock_val = service.UpgradeClusterRequest.Schedule.IMMEDIATELY
        assert arg == mock_val


@pytest.mark.asyncio
async def test_upgrade_cluster_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.upgrade_cluster(
            service.UpgradeClusterRequest(),
            name="name_value",
            target_version="target_version_value",
            schedule=service.UpgradeClusterRequest.Schedule.IMMEDIATELY,
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteClusterRequest,
        dict,
    ],
)
def test_delete_cluster(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.DeleteClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_cluster_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteClusterRequest()


def test_delete_cluster_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.DeleteClusterRequest(
        name="name_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_cluster(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteClusterRequest(
            name="name_value",
            request_id="request_id_value",
        )


def test_delete_cluster_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_cluster] = mock_rpc
        request = {}
        client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_cluster_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_cluster()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteClusterRequest()


@pytest.mark.asyncio
async def test_delete_cluster_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_cluster
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_cluster
        ] = mock_object

        request = {}
        await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_cluster_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteClusterRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.DeleteClusterRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_cluster_async_from_dict():
    await test_delete_cluster_async(request_type=dict)


def test_delete_cluster_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_cluster_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteClusterRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_cluster_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_cluster_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cluster(
            service.DeleteClusterRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_cluster_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_cluster), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_cluster(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_cluster_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_cluster(
            service.DeleteClusterRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GenerateAccessTokenRequest,
        dict,
    ],
)
def test_generate_access_token(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateAccessTokenResponse(
            access_token="access_token_value",
        )
        response = client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GenerateAccessTokenRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateAccessTokenResponse)
    assert response.access_token == "access_token_value"


def test_generate_access_token_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_access_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GenerateAccessTokenRequest()


def test_generate_access_token_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GenerateAccessTokenRequest(
        cluster="cluster_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_access_token(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GenerateAccessTokenRequest(
            cluster="cluster_value",
        )


def test_generate_access_token_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_access_token
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_access_token
        ] = mock_rpc
        request = {}
        client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_access_token(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_access_token_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateAccessTokenResponse(
                access_token="access_token_value",
            )
        )
        response = await client.generate_access_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GenerateAccessTokenRequest()


@pytest.mark.asyncio
async def test_generate_access_token_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.generate_access_token
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.generate_access_token
        ] = mock_object

        request = {}
        await client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.generate_access_token(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_generate_access_token_async(
    transport: str = "grpc_asyncio", request_type=service.GenerateAccessTokenRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateAccessTokenResponse(
                access_token="access_token_value",
            )
        )
        response = await client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GenerateAccessTokenRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateAccessTokenResponse)
    assert response.access_token == "access_token_value"


@pytest.mark.asyncio
async def test_generate_access_token_async_from_dict():
    await test_generate_access_token_async(request_type=dict)


def test_generate_access_token_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GenerateAccessTokenRequest()

    request.cluster = "cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        call.return_value = service.GenerateAccessTokenResponse()
        client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cluster=cluster_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_generate_access_token_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GenerateAccessTokenRequest()

    request.cluster = "cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateAccessTokenResponse()
        )
        await client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cluster=cluster_value",
    ) in kw["metadata"]


def test_generate_access_token_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateAccessTokenResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_access_token(
            cluster="cluster_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].cluster
        mock_val = "cluster_value"
        assert arg == mock_val


def test_generate_access_token_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_access_token(
            service.GenerateAccessTokenRequest(),
            cluster="cluster_value",
        )


@pytest.mark.asyncio
async def test_generate_access_token_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_access_token), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateAccessTokenResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateAccessTokenResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_access_token(
            cluster="cluster_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].cluster
        mock_val = "cluster_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_generate_access_token_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_access_token(
            service.GenerateAccessTokenRequest(),
            cluster="cluster_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GenerateOfflineCredentialRequest,
        dict,
    ],
)
def test_generate_offline_credential(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateOfflineCredentialResponse(
            client_certificate="client_certificate_value",
            client_key="client_key_value",
            user_id="user_id_value",
        )
        response = client.generate_offline_credential(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GenerateOfflineCredentialRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateOfflineCredentialResponse)
    assert response.client_certificate == "client_certificate_value"
    assert response.client_key == "client_key_value"
    assert response.user_id == "user_id_value"


def test_generate_offline_credential_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_offline_credential()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GenerateOfflineCredentialRequest()


def test_generate_offline_credential_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GenerateOfflineCredentialRequest(
        cluster="cluster_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.generate_offline_credential(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GenerateOfflineCredentialRequest(
            cluster="cluster_value",
        )


def test_generate_offline_credential_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_offline_credential
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_offline_credential
        ] = mock_rpc
        request = {}
        client.generate_offline_credential(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_offline_credential(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_generate_offline_credential_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateOfflineCredentialResponse(
                client_certificate="client_certificate_value",
                client_key="client_key_value",
                user_id="user_id_value",
            )
        )
        response = await client.generate_offline_credential()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GenerateOfflineCredentialRequest()


@pytest.mark.asyncio
async def test_generate_offline_credential_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.generate_offline_credential
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.generate_offline_credential
        ] = mock_object

        request = {}
        await client.generate_offline_credential(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.generate_offline_credential(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_generate_offline_credential_async(
    transport: str = "grpc_asyncio",
    request_type=service.GenerateOfflineCredentialRequest,
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateOfflineCredentialResponse(
                client_certificate="client_certificate_value",
                client_key="client_key_value",
                user_id="user_id_value",
            )
        )
        response = await client.generate_offline_credential(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GenerateOfflineCredentialRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateOfflineCredentialResponse)
    assert response.client_certificate == "client_certificate_value"
    assert response.client_key == "client_key_value"
    assert response.user_id == "user_id_value"


@pytest.mark.asyncio
async def test_generate_offline_credential_async_from_dict():
    await test_generate_offline_credential_async(request_type=dict)


def test_generate_offline_credential_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GenerateOfflineCredentialRequest()

    request.cluster = "cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        call.return_value = service.GenerateOfflineCredentialResponse()
        client.generate_offline_credential(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cluster=cluster_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_generate_offline_credential_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GenerateOfflineCredentialRequest()

    request.cluster = "cluster_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateOfflineCredentialResponse()
        )
        await client.generate_offline_credential(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "cluster=cluster_value",
    ) in kw["metadata"]


def test_generate_offline_credential_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateOfflineCredentialResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_offline_credential(
            cluster="cluster_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].cluster
        mock_val = "cluster_value"
        assert arg == mock_val


def test_generate_offline_credential_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_offline_credential(
            service.GenerateOfflineCredentialRequest(),
            cluster="cluster_value",
        )


@pytest.mark.asyncio
async def test_generate_offline_credential_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.generate_offline_credential), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.GenerateOfflineCredentialResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.GenerateOfflineCredentialResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_offline_credential(
            cluster="cluster_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].cluster
        mock_val = "cluster_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_generate_offline_credential_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_offline_credential(
            service.GenerateOfflineCredentialRequest(),
            cluster="cluster_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListNodePoolsRequest,
        dict,
    ],
)
def test_list_node_pools(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListNodePoolsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListNodePoolsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNodePoolsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_node_pools_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_node_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListNodePoolsRequest()


def test_list_node_pools_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListNodePoolsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_node_pools(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListNodePoolsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_node_pools_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_node_pools in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_node_pools] = mock_rpc
        request = {}
        client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_node_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_node_pools_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListNodePoolsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_node_pools()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListNodePoolsRequest()


@pytest.mark.asyncio
async def test_list_node_pools_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_node_pools
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_node_pools
        ] = mock_object

        request = {}
        await client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_node_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_node_pools_async(
    transport: str = "grpc_asyncio", request_type=service.ListNodePoolsRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListNodePoolsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListNodePoolsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNodePoolsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_node_pools_async_from_dict():
    await test_list_node_pools_async(request_type=dict)


def test_list_node_pools_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListNodePoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value = service.ListNodePoolsResponse()
        client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_node_pools_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListNodePoolsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListNodePoolsResponse()
        )
        await client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_node_pools_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListNodePoolsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_node_pools(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_node_pools_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_node_pools(
            service.ListNodePoolsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_node_pools_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListNodePoolsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListNodePoolsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_node_pools(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_node_pools_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_node_pools(
            service.ListNodePoolsRequest(),
            parent="parent_value",
        )


def test_list_node_pools_pager(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                    resources.NodePool(),
                ],
                next_page_token="abc",
            ),
            service.ListNodePoolsResponse(
                node_pools=[],
                next_page_token="def",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                ],
                next_page_token="ghi",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_node_pools(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.NodePool) for i in results)


def test_list_node_pools_pages(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_node_pools), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                    resources.NodePool(),
                ],
                next_page_token="abc",
            ),
            service.ListNodePoolsResponse(
                node_pools=[],
                next_page_token="def",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                ],
                next_page_token="ghi",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_node_pools(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_node_pools_async_pager():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_node_pools), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                    resources.NodePool(),
                ],
                next_page_token="abc",
            ),
            service.ListNodePoolsResponse(
                node_pools=[],
                next_page_token="def",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                ],
                next_page_token="ghi",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_node_pools(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.NodePool) for i in responses)


@pytest.mark.asyncio
async def test_list_node_pools_async_pages():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_node_pools), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                    resources.NodePool(),
                ],
                next_page_token="abc",
            ),
            service.ListNodePoolsResponse(
                node_pools=[],
                next_page_token="def",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                ],
                next_page_token="ghi",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_node_pools(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetNodePoolRequest,
        dict,
    ],
)
def test_get_node_pool(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.NodePool(
            name="name_value",
            node_location="node_location_value",
            node_count=1070,
            machine_filter="machine_filter_value",
            node_version="node_version_value",
        )
        response = client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.NodePool)
    assert response.name == "name_value"
    assert response.node_location == "node_location_value"
    assert response.node_count == 1070
    assert response.machine_filter == "machine_filter_value"
    assert response.node_version == "node_version_value"


def test_get_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetNodePoolRequest()


def test_get_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetNodePoolRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetNodePoolRequest(
            name="name_value",
        )


def test_get_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_node_pool] = mock_rpc
        request = {}
        client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_node_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.NodePool(
                name="name_value",
                node_location="node_location_value",
                node_count=1070,
                machine_filter="machine_filter_value",
                node_version="node_version_value",
            )
        )
        response = await client.get_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetNodePoolRequest()


@pytest.mark.asyncio
async def test_get_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_node_pool
        ] = mock_object

        request = {}
        await client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_node_pool_async(
    transport: str = "grpc_asyncio", request_type=service.GetNodePoolRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.NodePool(
                name="name_value",
                node_location="node_location_value",
                node_count=1070,
                machine_filter="machine_filter_value",
                node_version="node_version_value",
            )
        )
        response = await client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.NodePool)
    assert response.name == "name_value"
    assert response.node_location == "node_location_value"
    assert response.node_count == 1070
    assert response.machine_filter == "machine_filter_value"
    assert response.node_version == "node_version_value"


@pytest.mark.asyncio
async def test_get_node_pool_async_from_dict():
    await test_get_node_pool_async(request_type=dict)


def test_get_node_pool_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value = resources.NodePool()
        client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_node_pool_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.NodePool())
        await client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_node_pool_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.NodePool()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_node_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_node_pool_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_node_pool(
            service.GetNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_node_pool_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.NodePool()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.NodePool())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_node_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_node_pool_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_node_pool(
            service.GetNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateNodePoolRequest,
        dict,
    ],
)
def test_create_node_pool(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.CreateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateNodePoolRequest()


def test_create_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.CreateNodePoolRequest(
        parent="parent_value",
        node_pool_id="node_pool_id_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateNodePoolRequest(
            parent="parent_value",
            node_pool_id="node_pool_id_value",
            request_id="request_id_value",
        )


def test_create_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_node_pool
        ] = mock_rpc
        request = {}
        client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_node_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateNodePoolRequest()


@pytest.mark.asyncio
async def test_create_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_node_pool
        ] = mock_object

        request = {}
        await client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_node_pool_async(
    transport: str = "grpc_asyncio", request_type=service.CreateNodePoolRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.CreateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_node_pool_async_from_dict():
    await test_create_node_pool_async(request_type=dict)


def test_create_node_pool_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateNodePoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_node_pool_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateNodePoolRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_node_pool_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_node_pool(
            parent="parent_value",
            node_pool=resources.NodePool(name="name_value"),
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].node_pool
        mock_val = resources.NodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


def test_create_node_pool_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_node_pool(
            service.CreateNodePoolRequest(),
            parent="parent_value",
            node_pool=resources.NodePool(name="name_value"),
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.asyncio
async def test_create_node_pool_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_node_pool(
            parent="parent_value",
            node_pool=resources.NodePool(name="name_value"),
            node_pool_id="node_pool_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].node_pool
        mock_val = resources.NodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].node_pool_id
        mock_val = "node_pool_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_node_pool_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_node_pool(
            service.CreateNodePoolRequest(),
            parent="parent_value",
            node_pool=resources.NodePool(name="name_value"),
            node_pool_id="node_pool_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateNodePoolRequest,
        dict,
    ],
)
def test_update_node_pool(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.UpdateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateNodePoolRequest()


def test_update_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.UpdateNodePoolRequest(
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateNodePoolRequest(
            request_id="request_id_value",
        )


def test_update_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_node_pool
        ] = mock_rpc
        request = {}
        client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_node_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateNodePoolRequest()


@pytest.mark.asyncio
async def test_update_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_node_pool
        ] = mock_object

        request = {}
        await client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.update_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_node_pool_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateNodePoolRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.UpdateNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_node_pool_async_from_dict():
    await test_update_node_pool_async(request_type=dict)


def test_update_node_pool_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateNodePoolRequest()

    request.node_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "node_pool.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_node_pool_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateNodePoolRequest()

    request.node_pool.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "node_pool.name=name_value",
    ) in kw["metadata"]


def test_update_node_pool_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_node_pool(
            node_pool=resources.NodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].node_pool
        mock_val = resources.NodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_node_pool_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_node_pool(
            service.UpdateNodePoolRequest(),
            node_pool=resources.NodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_node_pool_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_node_pool(
            node_pool=resources.NodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].node_pool
        mock_val = resources.NodePool(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_node_pool_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_node_pool(
            service.UpdateNodePoolRequest(),
            node_pool=resources.NodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteNodePoolRequest,
        dict,
    ],
)
def test_delete_node_pool(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.DeleteNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_node_pool_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteNodePoolRequest()


def test_delete_node_pool_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.DeleteNodePoolRequest(
        name="name_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_node_pool(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteNodePoolRequest(
            name="name_value",
            request_id="request_id_value",
        )


def test_delete_node_pool_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_node_pool
        ] = mock_rpc
        request = {}
        client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_node_pool_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_node_pool()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteNodePoolRequest()


@pytest.mark.asyncio
async def test_delete_node_pool_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_node_pool
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_node_pool
        ] = mock_object

        request = {}
        await client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_node_pool_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteNodePoolRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.DeleteNodePoolRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_node_pool_async_from_dict():
    await test_delete_node_pool_async(request_type=dict)


def test_delete_node_pool_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_node_pool_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteNodePoolRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_node_pool_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_node_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_node_pool_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_node_pool(
            service.DeleteNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_node_pool_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node_pool), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_node_pool(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_node_pool_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_node_pool(
            service.DeleteNodePoolRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListMachinesRequest,
        dict,
    ],
)
def test_list_machines(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListMachinesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_machines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListMachinesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMachinesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_machines_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_machines()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListMachinesRequest()


def test_list_machines_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListMachinesRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_machines(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListMachinesRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_machines_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_machines in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_machines] = mock_rpc
        request = {}
        client.list_machines(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_machines(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_machines_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListMachinesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_machines()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListMachinesRequest()


@pytest.mark.asyncio
async def test_list_machines_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_machines
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_machines
        ] = mock_object

        request = {}
        await client.list_machines(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_machines(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_machines_async(
    transport: str = "grpc_asyncio", request_type=service.ListMachinesRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListMachinesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_machines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListMachinesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMachinesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_machines_async_from_dict():
    await test_list_machines_async(request_type=dict)


def test_list_machines_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListMachinesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        call.return_value = service.ListMachinesResponse()
        client.list_machines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_machines_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListMachinesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListMachinesResponse()
        )
        await client.list_machines(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_machines_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListMachinesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_machines(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_machines_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_machines(
            service.ListMachinesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_machines_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListMachinesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListMachinesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_machines(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_machines_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_machines(
            service.ListMachinesRequest(),
            parent="parent_value",
        )


def test_list_machines_pager(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                    resources.Machine(),
                ],
                next_page_token="abc",
            ),
            service.ListMachinesResponse(
                machines=[],
                next_page_token="def",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                ],
                next_page_token="ghi",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_machines(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Machine) for i in results)


def test_list_machines_pages(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_machines), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                    resources.Machine(),
                ],
                next_page_token="abc",
            ),
            service.ListMachinesResponse(
                machines=[],
                next_page_token="def",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                ],
                next_page_token="ghi",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_machines(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_machines_async_pager():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_machines), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                    resources.Machine(),
                ],
                next_page_token="abc",
            ),
            service.ListMachinesResponse(
                machines=[],
                next_page_token="def",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                ],
                next_page_token="ghi",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_machines(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.Machine) for i in responses)


@pytest.mark.asyncio
async def test_list_machines_async_pages():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_machines), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                    resources.Machine(),
                ],
                next_page_token="abc",
            ),
            service.ListMachinesResponse(
                machines=[],
                next_page_token="def",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                ],
                next_page_token="ghi",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_machines(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetMachineRequest,
        dict,
    ],
)
def test_get_machine(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Machine(
            name="name_value",
            hosted_node="hosted_node_value",
            zone="zone_value",
            version="version_value",
            disabled=True,
        )
        response = client.get_machine(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetMachineRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Machine)
    assert response.name == "name_value"
    assert response.hosted_node == "hosted_node_value"
    assert response.zone == "zone_value"
    assert response.version == "version_value"
    assert response.disabled is True


def test_get_machine_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_machine()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetMachineRequest()


def test_get_machine_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetMachineRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_machine(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetMachineRequest(
            name="name_value",
        )


def test_get_machine_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_machine in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_machine] = mock_rpc
        request = {}
        client.get_machine(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_machine(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_machine_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Machine(
                name="name_value",
                hosted_node="hosted_node_value",
                zone="zone_value",
                version="version_value",
                disabled=True,
            )
        )
        response = await client.get_machine()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetMachineRequest()


@pytest.mark.asyncio
async def test_get_machine_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_machine
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_machine
        ] = mock_object

        request = {}
        await client.get_machine(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_machine(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_machine_async(
    transport: str = "grpc_asyncio", request_type=service.GetMachineRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.Machine(
                name="name_value",
                hosted_node="hosted_node_value",
                zone="zone_value",
                version="version_value",
                disabled=True,
            )
        )
        response = await client.get_machine(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetMachineRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Machine)
    assert response.name == "name_value"
    assert response.hosted_node == "hosted_node_value"
    assert response.zone == "zone_value"
    assert response.version == "version_value"
    assert response.disabled is True


@pytest.mark.asyncio
async def test_get_machine_async_from_dict():
    await test_get_machine_async(request_type=dict)


def test_get_machine_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetMachineRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        call.return_value = resources.Machine()
        client.get_machine(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_machine_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetMachineRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Machine())
        await client.get_machine(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_machine_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Machine()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_machine(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_machine_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_machine(
            service.GetMachineRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_machine_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_machine), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.Machine()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(resources.Machine())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_machine(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_machine_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_machine(
            service.GetMachineRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListVpnConnectionsRequest,
        dict,
    ],
)
def test_list_vpn_connections(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListVpnConnectionsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )
        response = client.list_vpn_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.ListVpnConnectionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVpnConnectionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_vpn_connections_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_vpn_connections()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListVpnConnectionsRequest()


def test_list_vpn_connections_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.ListVpnConnectionsRequest(
        parent="parent_value",
        page_token="page_token_value",
        filter="filter_value",
        order_by="order_by_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_vpn_connections(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListVpnConnectionsRequest(
            parent="parent_value",
            page_token="page_token_value",
            filter="filter_value",
            order_by="order_by_value",
        )


def test_list_vpn_connections_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_vpn_connections in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_vpn_connections
        ] = mock_rpc
        request = {}
        client.list_vpn_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_vpn_connections(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_vpn_connections_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListVpnConnectionsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_vpn_connections()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListVpnConnectionsRequest()


@pytest.mark.asyncio
async def test_list_vpn_connections_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_vpn_connections
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_vpn_connections
        ] = mock_object

        request = {}
        await client.list_vpn_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_vpn_connections(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_vpn_connections_async(
    transport: str = "grpc_asyncio", request_type=service.ListVpnConnectionsRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListVpnConnectionsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_vpn_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.ListVpnConnectionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVpnConnectionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_vpn_connections_async_from_dict():
    await test_list_vpn_connections_async(request_type=dict)


def test_list_vpn_connections_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListVpnConnectionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        call.return_value = service.ListVpnConnectionsResponse()
        client.list_vpn_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_vpn_connections_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListVpnConnectionsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListVpnConnectionsResponse()
        )
        await client.list_vpn_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_vpn_connections_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListVpnConnectionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_vpn_connections(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_vpn_connections_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_vpn_connections(
            service.ListVpnConnectionsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_vpn_connections_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListVpnConnectionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListVpnConnectionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_vpn_connections(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_vpn_connections_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_vpn_connections(
            service.ListVpnConnectionsRequest(),
            parent="parent_value",
        )


def test_list_vpn_connections_pager(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
                next_page_token="abc",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[],
                next_page_token="def",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                ],
                next_page_token="ghi",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_vpn_connections(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.VpnConnection) for i in results)


def test_list_vpn_connections_pages(transport_name: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
                next_page_token="abc",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[],
                next_page_token="def",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                ],
                next_page_token="ghi",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_vpn_connections(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_vpn_connections_async_pager():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
                next_page_token="abc",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[],
                next_page_token="def",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                ],
                next_page_token="ghi",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_vpn_connections(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, resources.VpnConnection) for i in responses)


@pytest.mark.asyncio
async def test_list_vpn_connections_async_pages():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_vpn_connections),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
                next_page_token="abc",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[],
                next_page_token="def",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                ],
                next_page_token="ghi",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_vpn_connections(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetVpnConnectionRequest,
        dict,
    ],
)
def test_get_vpn_connection(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.VpnConnection(
            name="name_value",
            nat_gateway_ip="nat_gateway_ip_value",
            bgp_routing_mode=resources.VpnConnection.BgpRoutingMode.REGIONAL,
            cluster="cluster_value",
            vpc="vpc_value",
            enable_high_availability=True,
            router="router_value",
        )
        response = client.get_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetVpnConnectionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.VpnConnection)
    assert response.name == "name_value"
    assert response.nat_gateway_ip == "nat_gateway_ip_value"
    assert response.bgp_routing_mode == resources.VpnConnection.BgpRoutingMode.REGIONAL
    assert response.cluster == "cluster_value"
    assert response.vpc == "vpc_value"
    assert response.enable_high_availability is True
    assert response.router == "router_value"


def test_get_vpn_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_vpn_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetVpnConnectionRequest()


def test_get_vpn_connection_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetVpnConnectionRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_vpn_connection(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetVpnConnectionRequest(
            name="name_value",
        )


def test_get_vpn_connection_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_vpn_connection in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_vpn_connection
        ] = mock_rpc
        request = {}
        client.get_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_vpn_connection_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.VpnConnection(
                name="name_value",
                nat_gateway_ip="nat_gateway_ip_value",
                bgp_routing_mode=resources.VpnConnection.BgpRoutingMode.REGIONAL,
                cluster="cluster_value",
                vpc="vpc_value",
                enable_high_availability=True,
                router="router_value",
            )
        )
        response = await client.get_vpn_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetVpnConnectionRequest()


@pytest.mark.asyncio
async def test_get_vpn_connection_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_vpn_connection
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_vpn_connection
        ] = mock_object

        request = {}
        await client.get_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_vpn_connection_async(
    transport: str = "grpc_asyncio", request_type=service.GetVpnConnectionRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.VpnConnection(
                name="name_value",
                nat_gateway_ip="nat_gateway_ip_value",
                bgp_routing_mode=resources.VpnConnection.BgpRoutingMode.REGIONAL,
                cluster="cluster_value",
                vpc="vpc_value",
                enable_high_availability=True,
                router="router_value",
            )
        )
        response = await client.get_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetVpnConnectionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.VpnConnection)
    assert response.name == "name_value"
    assert response.nat_gateway_ip == "nat_gateway_ip_value"
    assert response.bgp_routing_mode == resources.VpnConnection.BgpRoutingMode.REGIONAL
    assert response.cluster == "cluster_value"
    assert response.vpc == "vpc_value"
    assert response.enable_high_availability is True
    assert response.router == "router_value"


@pytest.mark.asyncio
async def test_get_vpn_connection_async_from_dict():
    await test_get_vpn_connection_async(request_type=dict)


def test_get_vpn_connection_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetVpnConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        call.return_value = resources.VpnConnection()
        client.get_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_vpn_connection_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetVpnConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.VpnConnection()
        )
        await client.get_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_vpn_connection_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.VpnConnection()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_vpn_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_vpn_connection_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vpn_connection(
            service.GetVpnConnectionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_vpn_connection_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.VpnConnection()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.VpnConnection()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_vpn_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_vpn_connection_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_vpn_connection(
            service.GetVpnConnectionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateVpnConnectionRequest,
        dict,
    ],
)
def test_create_vpn_connection(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.CreateVpnConnectionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_vpn_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_vpn_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateVpnConnectionRequest()


def test_create_vpn_connection_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.CreateVpnConnectionRequest(
        parent="parent_value",
        vpn_connection_id="vpn_connection_id_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_vpn_connection(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateVpnConnectionRequest(
            parent="parent_value",
            vpn_connection_id="vpn_connection_id_value",
            request_id="request_id_value",
        )


def test_create_vpn_connection_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_vpn_connection
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_vpn_connection
        ] = mock_rpc
        request = {}
        client.create_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_vpn_connection_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_vpn_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateVpnConnectionRequest()


@pytest.mark.asyncio
async def test_create_vpn_connection_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_vpn_connection
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_vpn_connection
        ] = mock_object

        request = {}
        await client.create_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.create_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_vpn_connection_async(
    transport: str = "grpc_asyncio", request_type=service.CreateVpnConnectionRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.CreateVpnConnectionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_vpn_connection_async_from_dict():
    await test_create_vpn_connection_async(request_type=dict)


def test_create_vpn_connection_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateVpnConnectionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_vpn_connection_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateVpnConnectionRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_vpn_connection_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_vpn_connection(
            parent="parent_value",
            vpn_connection=resources.VpnConnection(name="name_value"),
            vpn_connection_id="vpn_connection_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].vpn_connection
        mock_val = resources.VpnConnection(name="name_value")
        assert arg == mock_val
        arg = args[0].vpn_connection_id
        mock_val = "vpn_connection_id_value"
        assert arg == mock_val


def test_create_vpn_connection_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_vpn_connection(
            service.CreateVpnConnectionRequest(),
            parent="parent_value",
            vpn_connection=resources.VpnConnection(name="name_value"),
            vpn_connection_id="vpn_connection_id_value",
        )


@pytest.mark.asyncio
async def test_create_vpn_connection_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_vpn_connection(
            parent="parent_value",
            vpn_connection=resources.VpnConnection(name="name_value"),
            vpn_connection_id="vpn_connection_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].vpn_connection
        mock_val = resources.VpnConnection(name="name_value")
        assert arg == mock_val
        arg = args[0].vpn_connection_id
        mock_val = "vpn_connection_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_vpn_connection_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_vpn_connection(
            service.CreateVpnConnectionRequest(),
            parent="parent_value",
            vpn_connection=resources.VpnConnection(name="name_value"),
            vpn_connection_id="vpn_connection_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteVpnConnectionRequest,
        dict,
    ],
)
def test_delete_vpn_connection(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.DeleteVpnConnectionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_vpn_connection_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_vpn_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteVpnConnectionRequest()


def test_delete_vpn_connection_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.DeleteVpnConnectionRequest(
        name="name_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_vpn_connection(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteVpnConnectionRequest(
            name="name_value",
            request_id="request_id_value",
        )


def test_delete_vpn_connection_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_vpn_connection
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_vpn_connection
        ] = mock_rpc
        request = {}
        client.delete_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_vpn_connection_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_vpn_connection()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteVpnConnectionRequest()


@pytest.mark.asyncio
async def test_delete_vpn_connection_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_vpn_connection
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_vpn_connection
        ] = mock_object

        request = {}
        await client.delete_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.delete_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_vpn_connection_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteVpnConnectionRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.DeleteVpnConnectionRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_vpn_connection_async_from_dict():
    await test_delete_vpn_connection_async(request_type=dict)


def test_delete_vpn_connection_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteVpnConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_vpn_connection_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteVpnConnectionRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_vpn_connection_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_vpn_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_vpn_connection_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_vpn_connection(
            service.DeleteVpnConnectionRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_vpn_connection_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_vpn_connection), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_vpn_connection(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_vpn_connection_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_vpn_connection(
            service.DeleteVpnConnectionRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetServerConfigRequest,
        dict,
    ],
)
def test_get_server_config(request_type, transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ServerConfig(
            default_version="default_version_value",
        )
        response = client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = service.GetServerConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ServerConfig)
    assert response.default_version == "default_version_value"


def test_get_server_config_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_server_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetServerConfigRequest()


def test_get_server_config_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = service.GetServerConfigRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_server_config(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetServerConfigRequest(
            name="name_value",
        )


def test_get_server_config_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_server_config in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_server_config
        ] = mock_rpc
        request = {}
        client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_server_config_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ServerConfig(
                default_version="default_version_value",
            )
        )
        response = await client.get_server_config()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetServerConfigRequest()


@pytest.mark.asyncio
async def test_get_server_config_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = EdgeContainerAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_server_config
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        class AwaitableMock(mock.AsyncMock):
            def __await__(self):
                self.await_count += 1
                return iter([])

        mock_object = AwaitableMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_server_config
        ] = mock_object

        request = {}
        await client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_server_config_async(
    transport: str = "grpc_asyncio", request_type=service.GetServerConfigRequest
):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ServerConfig(
                default_version="default_version_value",
            )
        )
        response = await client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = service.GetServerConfigRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ServerConfig)
    assert response.default_version == "default_version_value"


@pytest.mark.asyncio
async def test_get_server_config_async_from_dict():
    await test_get_server_config_async(request_type=dict)


def test_get_server_config_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value = resources.ServerConfig()
        client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_server_config_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetServerConfigRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ServerConfig()
        )
        await client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_server_config_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ServerConfig()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_server_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_server_config_flattened_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_server_config(
            service.GetServerConfigRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_server_config_flattened_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_server_config), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ServerConfig()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            resources.ServerConfig()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_server_config(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_server_config_flattened_error_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_server_config(
            service.GetServerConfigRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListClustersRequest,
        dict,
    ],
)
def test_list_clusters_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListClustersResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListClustersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_clusters(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListClustersPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_clusters_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_clusters in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_clusters] = mock_rpc

        request = {}
        client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_clusters(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_clusters_rest_required_fields(request_type=service.ListClustersRequest):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_clusters._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_clusters._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListClustersResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = service.ListClustersResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_clusters(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_clusters_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_clusters._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_clusters_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_list_clusters"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_list_clusters"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListClustersRequest.pb(service.ListClustersRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service.ListClustersResponse.to_json(
            service.ListClustersResponse()
        )

        request = service.ListClustersRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListClustersResponse()

        client.list_clusters(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_clusters_rest_bad_request(
    transport: str = "rest", request_type=service.ListClustersRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_clusters(request)


def test_list_clusters_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListClustersResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListClustersResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_clusters(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/clusters" % client.transport._host,
            args[1],
        )


def test_list_clusters_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_clusters(
            service.ListClustersRequest(),
            parent="parent_value",
        )


def test_list_clusters_rest_pager(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                    resources.Cluster(),
                ],
                next_page_token="abc",
            ),
            service.ListClustersResponse(
                clusters=[],
                next_page_token="def",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                ],
                next_page_token="ghi",
            ),
            service.ListClustersResponse(
                clusters=[
                    resources.Cluster(),
                    resources.Cluster(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(service.ListClustersResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_clusters(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Cluster) for i in results)

        pages = list(client.list_clusters(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetClusterRequest,
        dict,
    ],
)
def test_get_cluster_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Cluster(
            name="name_value",
            default_max_pods_per_node=2634,
            endpoint="endpoint_value",
            port=453,
            cluster_ca_certificate="cluster_ca_certificate_value",
            control_plane_version="control_plane_version_value",
            node_version="node_version_value",
            external_load_balancer_ipv4_address_pools=[
                "external_load_balancer_ipv4_address_pools_value"
            ],
            status=resources.Cluster.Status.PROVISIONING,
            target_version="target_version_value",
            release_channel=resources.Cluster.ReleaseChannel.NONE,
            external_load_balancer_ipv6_address_pools=[
                "external_load_balancer_ipv6_address_pools_value"
            ],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.Cluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_cluster(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Cluster)
    assert response.name == "name_value"
    assert response.default_max_pods_per_node == 2634
    assert response.endpoint == "endpoint_value"
    assert response.port == 453
    assert response.cluster_ca_certificate == "cluster_ca_certificate_value"
    assert response.control_plane_version == "control_plane_version_value"
    assert response.node_version == "node_version_value"
    assert response.external_load_balancer_ipv4_address_pools == [
        "external_load_balancer_ipv4_address_pools_value"
    ]
    assert response.status == resources.Cluster.Status.PROVISIONING
    assert response.target_version == "target_version_value"
    assert response.release_channel == resources.Cluster.ReleaseChannel.NONE
    assert response.external_load_balancer_ipv6_address_pools == [
        "external_load_balancer_ipv6_address_pools_value"
    ]


def test_get_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_cluster] = mock_rpc

        request = {}
        client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_cluster_rest_required_fields(request_type=service.GetClusterRequest):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.Cluster()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.Cluster.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_cluster(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_cluster_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_cluster_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_get_cluster"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_get_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetClusterRequest.pb(service.GetClusterRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.Cluster.to_json(resources.Cluster())

        request = service.GetClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.Cluster()

        client.get_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_cluster_rest_bad_request(
    transport: str = "rest", request_type=service.GetClusterRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_cluster(request)


def test_get_cluster_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Cluster()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/clusters/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.Cluster.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/clusters/*}" % client.transport._host,
            args[1],
        )


def test_get_cluster_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cluster(
            service.GetClusterRequest(),
            name="name_value",
        )


def test_get_cluster_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateClusterRequest,
        dict,
    ],
)
def test_create_cluster_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["cluster"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "fleet": {"project": "project_value", "membership": "membership_value"},
        "networking": {
            "cluster_ipv4_cidr_blocks": [
                "cluster_ipv4_cidr_blocks_value1",
                "cluster_ipv4_cidr_blocks_value2",
            ],
            "services_ipv4_cidr_blocks": [
                "services_ipv4_cidr_blocks_value1",
                "services_ipv4_cidr_blocks_value2",
            ],
        },
        "authorization": {"admin_users": {"username": "username_value"}},
        "default_max_pods_per_node": 2634,
        "endpoint": "endpoint_value",
        "port": 453,
        "cluster_ca_certificate": "cluster_ca_certificate_value",
        "maintenance_policy": {
            "window": {
                "recurring_window": {
                    "window": {"start_time": {}, "end_time": {}},
                    "recurrence": "recurrence_value",
                }
            }
        },
        "control_plane_version": "control_plane_version_value",
        "node_version": "node_version_value",
        "control_plane": {
            "remote": {},
            "local": {
                "node_location": "node_location_value",
                "node_count": 1070,
                "machine_filter": "machine_filter_value",
                "shared_deployment_policy": 1,
            },
        },
        "system_addons_config": {
            "ingress": {"disabled": True, "ipv4_vip": "ipv4_vip_value"}
        },
        "external_load_balancer_ipv4_address_pools": [
            "external_load_balancer_ipv4_address_pools_value1",
            "external_load_balancer_ipv4_address_pools_value2",
        ],
        "control_plane_encryption": {
            "kms_key": "kms_key_value",
            "kms_key_active_version": "kms_key_active_version_value",
            "kms_key_state": 1,
            "kms_status": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
        },
        "status": 1,
        "maintenance_events": [
            {
                "uuid": "uuid_value",
                "target_version": "target_version_value",
                "operation": "operation_value",
                "type_": 1,
                "schedule": 1,
                "state": 1,
                "create_time": {},
                "start_time": {},
                "end_time": {},
                "update_time": {},
            }
        ],
        "target_version": "target_version_value",
        "release_channel": 1,
        "survivability_config": {"offline_reboot_ttl": {"seconds": 751, "nanos": 543}},
        "external_load_balancer_ipv6_address_pools": [
            "external_load_balancer_ipv6_address_pools_value1",
            "external_load_balancer_ipv6_address_pools_value2",
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.CreateClusterRequest.meta.fields["cluster"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["cluster"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["cluster"][field])):
                    del request_init["cluster"][field][i][subfield]
            else:
                del request_init["cluster"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.create_cluster] = mock_rpc

        request = {}
        client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_cluster_rest_required_fields(request_type=service.CreateClusterRequest):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["cluster_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "clusterId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "clusterId" in jsonified_request
    assert jsonified_request["clusterId"] == request_init["cluster_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["clusterId"] = "cluster_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "cluster_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "clusterId" in jsonified_request
    assert jsonified_request["clusterId"] == "cluster_id_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_cluster(request)

            expected_params = [
                (
                    "clusterId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_cluster_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "clusterId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "clusterId",
                "cluster",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_cluster_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_create_cluster"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_create_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.CreateClusterRequest.pb(service.CreateClusterRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.CreateClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_cluster_rest_bad_request(
    transport: str = "rest", request_type=service.CreateClusterRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_cluster(request)


def test_create_cluster_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            cluster=resources.Cluster(name="name_value"),
            cluster_id="cluster_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/clusters" % client.transport._host,
            args[1],
        )


def test_create_cluster_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cluster(
            service.CreateClusterRequest(),
            parent="parent_value",
            cluster=resources.Cluster(name="name_value"),
            cluster_id="cluster_id_value",
        )


def test_create_cluster_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateClusterRequest,
        dict,
    ],
)
def test_update_cluster_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "cluster": {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    }
    request_init["cluster"] = {
        "name": "projects/sample1/locations/sample2/clusters/sample3",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "fleet": {"project": "project_value", "membership": "membership_value"},
        "networking": {
            "cluster_ipv4_cidr_blocks": [
                "cluster_ipv4_cidr_blocks_value1",
                "cluster_ipv4_cidr_blocks_value2",
            ],
            "services_ipv4_cidr_blocks": [
                "services_ipv4_cidr_blocks_value1",
                "services_ipv4_cidr_blocks_value2",
            ],
        },
        "authorization": {"admin_users": {"username": "username_value"}},
        "default_max_pods_per_node": 2634,
        "endpoint": "endpoint_value",
        "port": 453,
        "cluster_ca_certificate": "cluster_ca_certificate_value",
        "maintenance_policy": {
            "window": {
                "recurring_window": {
                    "window": {"start_time": {}, "end_time": {}},
                    "recurrence": "recurrence_value",
                }
            }
        },
        "control_plane_version": "control_plane_version_value",
        "node_version": "node_version_value",
        "control_plane": {
            "remote": {},
            "local": {
                "node_location": "node_location_value",
                "node_count": 1070,
                "machine_filter": "machine_filter_value",
                "shared_deployment_policy": 1,
            },
        },
        "system_addons_config": {
            "ingress": {"disabled": True, "ipv4_vip": "ipv4_vip_value"}
        },
        "external_load_balancer_ipv4_address_pools": [
            "external_load_balancer_ipv4_address_pools_value1",
            "external_load_balancer_ipv4_address_pools_value2",
        ],
        "control_plane_encryption": {
            "kms_key": "kms_key_value",
            "kms_key_active_version": "kms_key_active_version_value",
            "kms_key_state": 1,
            "kms_status": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
        },
        "status": 1,
        "maintenance_events": [
            {
                "uuid": "uuid_value",
                "target_version": "target_version_value",
                "operation": "operation_value",
                "type_": 1,
                "schedule": 1,
                "state": 1,
                "create_time": {},
                "start_time": {},
                "end_time": {},
                "update_time": {},
            }
        ],
        "target_version": "target_version_value",
        "release_channel": 1,
        "survivability_config": {"offline_reboot_ttl": {"seconds": 751, "nanos": 543}},
        "external_load_balancer_ipv6_address_pools": [
            "external_load_balancer_ipv6_address_pools_value1",
            "external_load_balancer_ipv6_address_pools_value2",
        ],
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.UpdateClusterRequest.meta.fields["cluster"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["cluster"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["cluster"][field])):
                    del request_init["cluster"][field][i][subfield]
            else:
                del request_init["cluster"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.update_cluster] = mock_rpc

        request = {}
        client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_cluster_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_update_cluster"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_update_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.UpdateClusterRequest.pb(service.UpdateClusterRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.UpdateClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_cluster_rest_bad_request(
    transport: str = "rest", request_type=service.UpdateClusterRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "cluster": {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_cluster(request)


def test_update_cluster_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "cluster": {"name": "projects/sample1/locations/sample2/clusters/sample3"}
        }

        # get truthy value for each flattened field
        mock_args = dict(
            cluster=resources.Cluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{cluster.name=projects/*/locations/*/clusters/*}"
            % client.transport._host,
            args[1],
        )


def test_update_cluster_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cluster(
            service.UpdateClusterRequest(),
            cluster=resources.Cluster(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_cluster_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpgradeClusterRequest,
        dict,
    ],
)
def test_upgrade_cluster_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.upgrade_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_upgrade_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.upgrade_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.upgrade_cluster] = mock_rpc

        request = {}
        client.upgrade_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.upgrade_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_upgrade_cluster_rest_required_fields(
    request_type=service.UpgradeClusterRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["target_version"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).upgrade_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"
    jsonified_request["targetVersion"] = "target_version_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).upgrade_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"
    assert "targetVersion" in jsonified_request
    assert jsonified_request["targetVersion"] == "target_version_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.upgrade_cluster(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_upgrade_cluster_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.upgrade_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "name",
                "targetVersion",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_upgrade_cluster_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_upgrade_cluster"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_upgrade_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.UpgradeClusterRequest.pb(service.UpgradeClusterRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.UpgradeClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.upgrade_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_upgrade_cluster_rest_bad_request(
    transport: str = "rest", request_type=service.UpgradeClusterRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.upgrade_cluster(request)


def test_upgrade_cluster_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/clusters/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            target_version="target_version_value",
            schedule=service.UpgradeClusterRequest.Schedule.IMMEDIATELY,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.upgrade_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/clusters/*}:upgrade"
            % client.transport._host,
            args[1],
        )


def test_upgrade_cluster_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.upgrade_cluster(
            service.UpgradeClusterRequest(),
            name="name_value",
            target_version="target_version_value",
            schedule=service.UpgradeClusterRequest.Schedule.IMMEDIATELY,
        )


def test_upgrade_cluster_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteClusterRequest,
        dict,
    ],
)
def test_delete_cluster_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_cluster(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_cluster_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_cluster in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.delete_cluster] = mock_rpc

        request = {}
        client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_cluster(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_cluster_rest_required_fields(request_type=service.DeleteClusterRequest):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_cluster._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_cluster._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_cluster(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_cluster_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_cluster._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_cluster_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_delete_cluster"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_delete_cluster"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.DeleteClusterRequest.pb(service.DeleteClusterRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.DeleteClusterRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_cluster(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_cluster_rest_bad_request(
    transport: str = "rest", request_type=service.DeleteClusterRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_cluster(request)


def test_delete_cluster_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/clusters/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_cluster(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/clusters/*}" % client.transport._host,
            args[1],
        )


def test_delete_cluster_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cluster(
            service.DeleteClusterRequest(),
            name="name_value",
        )


def test_delete_cluster_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GenerateAccessTokenRequest,
        dict,
    ],
)
def test_generate_access_token_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"cluster": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.GenerateAccessTokenResponse(
            access_token="access_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.GenerateAccessTokenResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.generate_access_token(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateAccessTokenResponse)
    assert response.access_token == "access_token_value"


def test_generate_access_token_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_access_token
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_access_token
        ] = mock_rpc

        request = {}
        client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_access_token(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_generate_access_token_rest_required_fields(
    request_type=service.GenerateAccessTokenRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["cluster"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_access_token._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["cluster"] = "cluster_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_access_token._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "cluster" in jsonified_request
    assert jsonified_request["cluster"] == "cluster_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.GenerateAccessTokenResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = service.GenerateAccessTokenResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.generate_access_token(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_generate_access_token_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.generate_access_token._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("cluster",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_access_token_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_generate_access_token"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_generate_access_token"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GenerateAccessTokenRequest.pb(
            service.GenerateAccessTokenRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service.GenerateAccessTokenResponse.to_json(
            service.GenerateAccessTokenResponse()
        )

        request = service.GenerateAccessTokenRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.GenerateAccessTokenResponse()

        client.generate_access_token(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_generate_access_token_rest_bad_request(
    transport: str = "rest", request_type=service.GenerateAccessTokenRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"cluster": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.generate_access_token(request)


def test_generate_access_token_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.GenerateAccessTokenResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "cluster": "projects/sample1/locations/sample2/clusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            cluster="cluster_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.GenerateAccessTokenResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.generate_access_token(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{cluster=projects/*/locations/*/clusters/*}:generateAccessToken"
            % client.transport._host,
            args[1],
        )


def test_generate_access_token_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_access_token(
            service.GenerateAccessTokenRequest(),
            cluster="cluster_value",
        )


def test_generate_access_token_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GenerateOfflineCredentialRequest,
        dict,
    ],
)
def test_generate_offline_credential_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"cluster": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.GenerateOfflineCredentialResponse(
            client_certificate="client_certificate_value",
            client_key="client_key_value",
            user_id="user_id_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.GenerateOfflineCredentialResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.generate_offline_credential(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.GenerateOfflineCredentialResponse)
    assert response.client_certificate == "client_certificate_value"
    assert response.client_key == "client_key_value"
    assert response.user_id == "user_id_value"


def test_generate_offline_credential_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.generate_offline_credential
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.generate_offline_credential
        ] = mock_rpc

        request = {}
        client.generate_offline_credential(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.generate_offline_credential(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_generate_offline_credential_rest_required_fields(
    request_type=service.GenerateOfflineCredentialRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["cluster"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_offline_credential._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["cluster"] = "cluster_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).generate_offline_credential._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "cluster" in jsonified_request
    assert jsonified_request["cluster"] == "cluster_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.GenerateOfflineCredentialResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = service.GenerateOfflineCredentialResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.generate_offline_credential(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_generate_offline_credential_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.generate_offline_credential._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("cluster",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_offline_credential_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_generate_offline_credential"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_generate_offline_credential"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GenerateOfflineCredentialRequest.pb(
            service.GenerateOfflineCredentialRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service.GenerateOfflineCredentialResponse.to_json(
            service.GenerateOfflineCredentialResponse()
        )

        request = service.GenerateOfflineCredentialRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.GenerateOfflineCredentialResponse()

        client.generate_offline_credential(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_generate_offline_credential_rest_bad_request(
    transport: str = "rest", request_type=service.GenerateOfflineCredentialRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"cluster": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.generate_offline_credential(request)


def test_generate_offline_credential_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.GenerateOfflineCredentialResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "cluster": "projects/sample1/locations/sample2/clusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            cluster="cluster_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.GenerateOfflineCredentialResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.generate_offline_credential(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{cluster=projects/*/locations/*/clusters/*}:generateOfflineCredential"
            % client.transport._host,
            args[1],
        )


def test_generate_offline_credential_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_offline_credential(
            service.GenerateOfflineCredentialRequest(),
            cluster="cluster_value",
        )


def test_generate_offline_credential_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListNodePoolsRequest,
        dict,
    ],
)
def test_list_node_pools_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListNodePoolsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListNodePoolsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_node_pools(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNodePoolsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_node_pools_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_node_pools in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_node_pools] = mock_rpc

        request = {}
        client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_node_pools(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_node_pools_rest_required_fields(
    request_type=service.ListNodePoolsRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_node_pools._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_node_pools._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListNodePoolsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = service.ListNodePoolsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_node_pools(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_node_pools_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_node_pools._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_node_pools_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_list_node_pools"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_list_node_pools"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListNodePoolsRequest.pb(service.ListNodePoolsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service.ListNodePoolsResponse.to_json(
            service.ListNodePoolsResponse()
        )

        request = service.ListNodePoolsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListNodePoolsResponse()

        client.list_node_pools(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_node_pools_rest_bad_request(
    transport: str = "rest", request_type=service.ListNodePoolsRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_node_pools(request)


def test_list_node_pools_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListNodePoolsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/clusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListNodePoolsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_node_pools(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/clusters/*}/nodePools"
            % client.transport._host,
            args[1],
        )


def test_list_node_pools_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_node_pools(
            service.ListNodePoolsRequest(),
            parent="parent_value",
        )


def test_list_node_pools_rest_pager(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                    resources.NodePool(),
                ],
                next_page_token="abc",
            ),
            service.ListNodePoolsResponse(
                node_pools=[],
                next_page_token="def",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                ],
                next_page_token="ghi",
            ),
            service.ListNodePoolsResponse(
                node_pools=[
                    resources.NodePool(),
                    resources.NodePool(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(service.ListNodePoolsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "parent": "projects/sample1/locations/sample2/clusters/sample3"
        }

        pager = client.list_node_pools(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.NodePool) for i in results)

        pages = list(client.list_node_pools(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetNodePoolRequest,
        dict,
    ],
)
def test_get_node_pool_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.NodePool(
            name="name_value",
            node_location="node_location_value",
            node_count=1070,
            machine_filter="machine_filter_value",
            node_version="node_version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.NodePool.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_node_pool(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.NodePool)
    assert response.name == "name_value"
    assert response.node_location == "node_location_value"
    assert response.node_count == 1070
    assert response.machine_filter == "machine_filter_value"
    assert response.node_version == "node_version_value"


def test_get_node_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_node_pool] = mock_rpc

        request = {}
        client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_node_pool_rest_required_fields(request_type=service.GetNodePoolRequest):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_node_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_node_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.NodePool()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.NodePool.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_node_pool(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_node_pool_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_node_pool._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_node_pool_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_get_node_pool"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_get_node_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetNodePoolRequest.pb(service.GetNodePoolRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.NodePool.to_json(resources.NodePool())

        request = service.GetNodePoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.NodePool()

        client.get_node_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_node_pool_rest_bad_request(
    transport: str = "rest", request_type=service.GetNodePoolRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_node_pool(request)


def test_get_node_pool_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.NodePool()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.NodePool.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_node_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}"
            % client.transport._host,
            args[1],
        )


def test_get_node_pool_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_node_pool(
            service.GetNodePoolRequest(),
            name="name_value",
        )


def test_get_node_pool_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateNodePoolRequest,
        dict,
    ],
)
def test_create_node_pool_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/clusters/sample3"}
    request_init["node_pool"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "node_location": "node_location_value",
        "node_count": 1070,
        "machine_filter": "machine_filter_value",
        "local_disk_encryption": {
            "kms_key": "kms_key_value",
            "kms_key_active_version": "kms_key_active_version_value",
            "kms_key_state": 1,
            "kms_status": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
        },
        "node_version": "node_version_value",
        "node_config": {"labels": {}},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.CreateNodePoolRequest.meta.fields["node_pool"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["node_pool"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["node_pool"][field])):
                    del request_init["node_pool"][field][i][subfield]
            else:
                del request_init["node_pool"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_node_pool(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_node_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.create_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_node_pool
        ] = mock_rpc

        request = {}
        client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_node_pool_rest_required_fields(
    request_type=service.CreateNodePoolRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["node_pool_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "nodePoolId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_node_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "nodePoolId" in jsonified_request
    assert jsonified_request["nodePoolId"] == request_init["node_pool_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["nodePoolId"] = "node_pool_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_node_pool._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "node_pool_id",
            "request_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "nodePoolId" in jsonified_request
    assert jsonified_request["nodePoolId"] == "node_pool_id_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_node_pool(request)

            expected_params = [
                (
                    "nodePoolId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_node_pool_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_node_pool._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "nodePoolId",
                "requestId",
            )
        )
        & set(
            (
                "parent",
                "nodePoolId",
                "nodePool",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_node_pool_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_create_node_pool"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_create_node_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.CreateNodePoolRequest.pb(service.CreateNodePoolRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.CreateNodePoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_node_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_node_pool_rest_bad_request(
    transport: str = "rest", request_type=service.CreateNodePoolRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2/clusters/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_node_pool(request)


def test_create_node_pool_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "parent": "projects/sample1/locations/sample2/clusters/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            node_pool=resources.NodePool(name="name_value"),
            node_pool_id="node_pool_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_node_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*/clusters/*}/nodePools"
            % client.transport._host,
            args[1],
        )


def test_create_node_pool_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_node_pool(
            service.CreateNodePoolRequest(),
            parent="parent_value",
            node_pool=resources.NodePool(name="name_value"),
            node_pool_id="node_pool_id_value",
        )


def test_create_node_pool_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.UpdateNodePoolRequest,
        dict,
    ],
)
def test_update_node_pool_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "node_pool": {
            "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
        }
    }
    request_init["node_pool"] = {
        "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "node_location": "node_location_value",
        "node_count": 1070,
        "machine_filter": "machine_filter_value",
        "local_disk_encryption": {
            "kms_key": "kms_key_value",
            "kms_key_active_version": "kms_key_active_version_value",
            "kms_key_state": 1,
            "kms_status": {
                "code": 411,
                "message": "message_value",
                "details": [
                    {
                        "type_url": "type.googleapis.com/google.protobuf.Duration",
                        "value": b"\x08\x0c\x10\xdb\x07",
                    }
                ],
            },
        },
        "node_version": "node_version_value",
        "node_config": {"labels": {}},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.UpdateNodePoolRequest.meta.fields["node_pool"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["node_pool"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["node_pool"][field])):
                    del request_init["node_pool"][field][i][subfield]
            else:
                del request_init["node_pool"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_node_pool(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_node_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.update_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_node_pool
        ] = mock_rpc

        request = {}
        client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.update_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_node_pool_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_update_node_pool"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_update_node_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.UpdateNodePoolRequest.pb(service.UpdateNodePoolRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.UpdateNodePoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_node_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_node_pool_rest_bad_request(
    transport: str = "rest", request_type=service.UpdateNodePoolRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "node_pool": {
            "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_node_pool(request)


def test_update_node_pool_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "node_pool": {
                "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            node_pool=resources.NodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_node_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{node_pool.name=projects/*/locations/*/clusters/*/nodePools/*}"
            % client.transport._host,
            args[1],
        )


def test_update_node_pool_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_node_pool(
            service.UpdateNodePoolRequest(),
            node_pool=resources.NodePool(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_update_node_pool_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteNodePoolRequest,
        dict,
    ],
)
def test_delete_node_pool_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_node_pool(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_node_pool_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.delete_node_pool in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_node_pool
        ] = mock_rpc

        request = {}
        client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_node_pool(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_node_pool_rest_required_fields(
    request_type=service.DeleteNodePoolRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_node_pool._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_node_pool._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_node_pool(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_node_pool_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_node_pool._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_node_pool_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_delete_node_pool"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_delete_node_pool"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.DeleteNodePoolRequest.pb(service.DeleteNodePoolRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.DeleteNodePoolRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_node_pool(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_node_pool_rest_bad_request(
    transport: str = "rest", request_type=service.DeleteNodePoolRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_node_pool(request)


def test_delete_node_pool_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/clusters/sample3/nodePools/sample4"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_node_pool(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/clusters/*/nodePools/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_node_pool_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_node_pool(
            service.DeleteNodePoolRequest(),
            name="name_value",
        )


def test_delete_node_pool_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListMachinesRequest,
        dict,
    ],
)
def test_list_machines_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListMachinesResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListMachinesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_machines(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListMachinesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_machines_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_machines in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.list_machines] = mock_rpc

        request = {}
        client.list_machines(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_machines(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_machines_rest_required_fields(request_type=service.ListMachinesRequest):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_machines._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_machines._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListMachinesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = service.ListMachinesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_machines(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_machines_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_machines._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_machines_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_list_machines"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_list_machines"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListMachinesRequest.pb(service.ListMachinesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service.ListMachinesResponse.to_json(
            service.ListMachinesResponse()
        )

        request = service.ListMachinesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListMachinesResponse()

        client.list_machines(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_machines_rest_bad_request(
    transport: str = "rest", request_type=service.ListMachinesRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_machines(request)


def test_list_machines_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListMachinesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListMachinesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_machines(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/machines" % client.transport._host,
            args[1],
        )


def test_list_machines_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_machines(
            service.ListMachinesRequest(),
            parent="parent_value",
        )


def test_list_machines_rest_pager(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                    resources.Machine(),
                ],
                next_page_token="abc",
            ),
            service.ListMachinesResponse(
                machines=[],
                next_page_token="def",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                ],
                next_page_token="ghi",
            ),
            service.ListMachinesResponse(
                machines=[
                    resources.Machine(),
                    resources.Machine(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(service.ListMachinesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_machines(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.Machine) for i in results)

        pages = list(client.list_machines(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetMachineRequest,
        dict,
    ],
)
def test_get_machine_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/machines/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Machine(
            name="name_value",
            hosted_node="hosted_node_value",
            zone="zone_value",
            version="version_value",
            disabled=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.Machine.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_machine(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.Machine)
    assert response.name == "name_value"
    assert response.hosted_node == "hosted_node_value"
    assert response.zone == "zone_value"
    assert response.version == "version_value"
    assert response.disabled is True


def test_get_machine_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_machine in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[client._transport.get_machine] = mock_rpc

        request = {}
        client.get_machine(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_machine(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_machine_rest_required_fields(request_type=service.GetMachineRequest):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_machine._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_machine._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.Machine()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.Machine.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_machine(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_machine_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_machine._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_machine_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_get_machine"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_get_machine"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetMachineRequest.pb(service.GetMachineRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.Machine.to_json(resources.Machine())

        request = service.GetMachineRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.Machine()

        client.get_machine(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_machine_rest_bad_request(
    transport: str = "rest", request_type=service.GetMachineRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/machines/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_machine(request)


def test_get_machine_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.Machine()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2/machines/sample3"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.Machine.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_machine(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/machines/*}" % client.transport._host,
            args[1],
        )


def test_get_machine_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_machine(
            service.GetMachineRequest(),
            name="name_value",
        )


def test_get_machine_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.ListVpnConnectionsRequest,
        dict,
    ],
)
def test_list_vpn_connections_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListVpnConnectionsResponse(
            next_page_token="next_page_token_value",
            unreachable=["unreachable_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListVpnConnectionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_vpn_connections(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVpnConnectionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_vpn_connections_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_vpn_connections in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_vpn_connections
        ] = mock_rpc

        request = {}
        client.list_vpn_connections(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_vpn_connections(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_vpn_connections_rest_required_fields(
    request_type=service.ListVpnConnectionsRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_vpn_connections._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_vpn_connections._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "filter",
            "order_by",
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = service.ListVpnConnectionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = service.ListVpnConnectionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_vpn_connections(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_vpn_connections_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_vpn_connections._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "filter",
                "orderBy",
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_vpn_connections_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_list_vpn_connections"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_list_vpn_connections"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.ListVpnConnectionsRequest.pb(
            service.ListVpnConnectionsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = service.ListVpnConnectionsResponse.to_json(
            service.ListVpnConnectionsResponse()
        )

        request = service.ListVpnConnectionsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = service.ListVpnConnectionsResponse()

        client.list_vpn_connections(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_vpn_connections_rest_bad_request(
    transport: str = "rest", request_type=service.ListVpnConnectionsRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_vpn_connections(request)


def test_list_vpn_connections_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = service.ListVpnConnectionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = service.ListVpnConnectionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_vpn_connections(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/vpnConnections"
            % client.transport._host,
            args[1],
        )


def test_list_vpn_connections_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_vpn_connections(
            service.ListVpnConnectionsRequest(),
            parent="parent_value",
        )


def test_list_vpn_connections_rest_pager(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
                next_page_token="abc",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[],
                next_page_token="def",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                ],
                next_page_token="ghi",
            ),
            service.ListVpnConnectionsResponse(
                vpn_connections=[
                    resources.VpnConnection(),
                    resources.VpnConnection(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            service.ListVpnConnectionsResponse.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_vpn_connections(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, resources.VpnConnection) for i in results)

        pages = list(client.list_vpn_connections(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetVpnConnectionRequest,
        dict,
    ],
)
def test_get_vpn_connection_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vpnConnections/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.VpnConnection(
            name="name_value",
            nat_gateway_ip="nat_gateway_ip_value",
            bgp_routing_mode=resources.VpnConnection.BgpRoutingMode.REGIONAL,
            cluster="cluster_value",
            vpc="vpc_value",
            enable_high_availability=True,
            router="router_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.VpnConnection.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_vpn_connection(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.VpnConnection)
    assert response.name == "name_value"
    assert response.nat_gateway_ip == "nat_gateway_ip_value"
    assert response.bgp_routing_mode == resources.VpnConnection.BgpRoutingMode.REGIONAL
    assert response.cluster == "cluster_value"
    assert response.vpc == "vpc_value"
    assert response.enable_high_availability is True
    assert response.router == "router_value"


def test_get_vpn_connection_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_vpn_connection in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_vpn_connection
        ] = mock_rpc

        request = {}
        client.get_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_vpn_connection_rest_required_fields(
    request_type=service.GetVpnConnectionRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_vpn_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_vpn_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.VpnConnection()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.VpnConnection.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_vpn_connection(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_vpn_connection_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_vpn_connection._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_vpn_connection_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_get_vpn_connection"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_get_vpn_connection"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetVpnConnectionRequest.pb(
            service.GetVpnConnectionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.VpnConnection.to_json(
            resources.VpnConnection()
        )

        request = service.GetVpnConnectionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.VpnConnection()

        client.get_vpn_connection(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_vpn_connection_rest_bad_request(
    transport: str = "rest", request_type=service.GetVpnConnectionRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vpnConnections/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_vpn_connection(request)


def test_get_vpn_connection_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.VpnConnection()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/vpnConnections/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.VpnConnection.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_vpn_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/vpnConnections/*}"
            % client.transport._host,
            args[1],
        )


def test_get_vpn_connection_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_vpn_connection(
            service.GetVpnConnectionRequest(),
            name="name_value",
        )


def test_get_vpn_connection_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.CreateVpnConnectionRequest,
        dict,
    ],
)
def test_create_vpn_connection_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["vpn_connection"] = {
        "name": "name_value",
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "nat_gateway_ip": "nat_gateway_ip_value",
        "bgp_routing_mode": 1,
        "cluster": "cluster_value",
        "vpc": "vpc_value",
        "vpc_project": {
            "project_id": "project_id_value",
            "service_account": "service_account_value",
        },
        "enable_high_availability": True,
        "router": "router_value",
        "details": {
            "state": 1,
            "error": "error_value",
            "cloud_router": {"name": "name_value"},
            "cloud_vpns": [{"gateway": "gateway_value"}],
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = service.CreateVpnConnectionRequest.meta.fields["vpn_connection"]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["vpn_connection"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["vpn_connection"][field])):
                    del request_init["vpn_connection"][field][i][subfield]
            else:
                del request_init["vpn_connection"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_vpn_connection(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_vpn_connection_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_vpn_connection
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_vpn_connection
        ] = mock_rpc

        request = {}
        client.create_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.create_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_vpn_connection_rest_required_fields(
    request_type=service.CreateVpnConnectionRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["vpn_connection_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped
    assert "vpnConnectionId" not in jsonified_request

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_vpn_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "vpnConnectionId" in jsonified_request
    assert jsonified_request["vpnConnectionId"] == request_init["vpn_connection_id"]

    jsonified_request["parent"] = "parent_value"
    jsonified_request["vpnConnectionId"] = "vpn_connection_id_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_vpn_connection._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "request_id",
            "vpn_connection_id",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"
    assert "vpnConnectionId" in jsonified_request
    assert jsonified_request["vpnConnectionId"] == "vpn_connection_id_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_vpn_connection(request)

            expected_params = [
                (
                    "vpnConnectionId",
                    "",
                ),
                ("$alt", "json;enum-encoding=int"),
            ]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_vpn_connection_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_vpn_connection._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "requestId",
                "vpnConnectionId",
            )
        )
        & set(
            (
                "parent",
                "vpnConnectionId",
                "vpnConnection",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_vpn_connection_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_create_vpn_connection"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_create_vpn_connection"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.CreateVpnConnectionRequest.pb(
            service.CreateVpnConnectionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.CreateVpnConnectionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_vpn_connection(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_vpn_connection_rest_bad_request(
    transport: str = "rest", request_type=service.CreateVpnConnectionRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_vpn_connection(request)


def test_create_vpn_connection_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            vpn_connection=resources.VpnConnection(name="name_value"),
            vpn_connection_id="vpn_connection_id_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_vpn_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/vpnConnections"
            % client.transport._host,
            args[1],
        )


def test_create_vpn_connection_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_vpn_connection(
            service.CreateVpnConnectionRequest(),
            parent="parent_value",
            vpn_connection=resources.VpnConnection(name="name_value"),
            vpn_connection_id="vpn_connection_id_value",
        )


def test_create_vpn_connection_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.DeleteVpnConnectionRequest,
        dict,
    ],
)
def test_delete_vpn_connection_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vpnConnections/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_vpn_connection(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_vpn_connection_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_vpn_connection
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_vpn_connection
        ] = mock_rpc

        request = {}
        client.delete_vpn_connection(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.delete_vpn_connection(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_vpn_connection_rest_required_fields(
    request_type=service.DeleteVpnConnectionRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_vpn_connection._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_vpn_connection._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_vpn_connection(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_vpn_connection_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_vpn_connection._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_vpn_connection_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_delete_vpn_connection"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_delete_vpn_connection"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.DeleteVpnConnectionRequest.pb(
            service.DeleteVpnConnectionRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = service.DeleteVpnConnectionRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_vpn_connection(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_vpn_connection_rest_bad_request(
    transport: str = "rest", request_type=service.DeleteVpnConnectionRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2/vpnConnections/sample3"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_vpn_connection(request)


def test_delete_vpn_connection_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/vpnConnections/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_vpn_connection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/vpnConnections/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_vpn_connection_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_vpn_connection(
            service.DeleteVpnConnectionRequest(),
            name="name_value",
        )


def test_delete_vpn_connection_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        service.GetServerConfigRequest,
        dict,
    ],
)
def test_get_server_config_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.ServerConfig(
            default_version="default_version_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.ServerConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_server_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ServerConfig)
    assert response.default_version == "default_version_value"


def test_get_server_config_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.get_server_config in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_server_config
        ] = mock_rpc

        request = {}
        client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_server_config(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_server_config_rest_required_fields(
    request_type=service.GetServerConfigRequest,
):
    transport_class = transports.EdgeContainerRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_server_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_server_config._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = resources.ServerConfig()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = resources.ServerConfig.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_server_config(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_server_config_rest_unset_required_fields():
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_server_config._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_server_config_rest_interceptors(null_interceptor):
    transport = transports.EdgeContainerRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.EdgeContainerRestInterceptor(),
    )
    client = EdgeContainerClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "post_get_server_config"
    ) as post, mock.patch.object(
        transports.EdgeContainerRestInterceptor, "pre_get_server_config"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = service.GetServerConfigRequest.pb(service.GetServerConfigRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = resources.ServerConfig.to_json(
            resources.ServerConfig()
        )

        request = service.GetServerConfigRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = resources.ServerConfig()

        client.get_server_config(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_server_config_rest_bad_request(
    transport: str = "rest", request_type=service.GetServerConfigRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_server_config(request)


def test_get_server_config_rest_flattened():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = resources.ServerConfig()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = resources.ServerConfig.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_server_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*}/serverConfig" % client.transport._host,
            args[1],
        )


def test_get_server_config_rest_flattened_error(transport: str = "rest"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_server_config(
            service.GetServerConfigRequest(),
            name="name_value",
        )


def test_get_server_config_rest_error():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.EdgeContainerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.EdgeContainerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EdgeContainerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.EdgeContainerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EdgeContainerClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = EdgeContainerClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.EdgeContainerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EdgeContainerClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EdgeContainerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = EdgeContainerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EdgeContainerGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.EdgeContainerGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EdgeContainerGrpcTransport,
        transports.EdgeContainerGrpcAsyncIOTransport,
        transports.EdgeContainerRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = EdgeContainerClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.EdgeContainerGrpcTransport,
    )


def test_edge_container_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.EdgeContainerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_edge_container_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.edgecontainer_v1.services.edge_container.transports.EdgeContainerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.EdgeContainerTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_clusters",
        "get_cluster",
        "create_cluster",
        "update_cluster",
        "upgrade_cluster",
        "delete_cluster",
        "generate_access_token",
        "generate_offline_credential",
        "list_node_pools",
        "get_node_pool",
        "create_node_pool",
        "update_node_pool",
        "delete_node_pool",
        "list_machines",
        "get_machine",
        "list_vpn_connections",
        "get_vpn_connection",
        "create_vpn_connection",
        "delete_vpn_connection",
        "get_server_config",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_edge_container_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.edgecontainer_v1.services.edge_container.transports.EdgeContainerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EdgeContainerTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_edge_container_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.edgecontainer_v1.services.edge_container.transports.EdgeContainerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.EdgeContainerTransport()
        adc.assert_called_once()


def test_edge_container_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        EdgeContainerClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EdgeContainerGrpcTransport,
        transports.EdgeContainerGrpcAsyncIOTransport,
    ],
)
def test_edge_container_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EdgeContainerGrpcTransport,
        transports.EdgeContainerGrpcAsyncIOTransport,
        transports.EdgeContainerRestTransport,
    ],
)
def test_edge_container_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.EdgeContainerGrpcTransport, grpc_helpers),
        (transports.EdgeContainerGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_edge_container_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "edgecontainer.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="edgecontainer.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EdgeContainerGrpcTransport,
        transports.EdgeContainerGrpcAsyncIOTransport,
    ],
)
def test_edge_container_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_edge_container_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.EdgeContainerRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_edge_container_rest_lro_client():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_edge_container_host_no_port(transport_name):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="edgecontainer.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "edgecontainer.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://edgecontainer.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_edge_container_host_with_port(transport_name):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="edgecontainer.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "edgecontainer.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://edgecontainer.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_edge_container_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = EdgeContainerClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = EdgeContainerClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_clusters._session
    session2 = client2.transport.list_clusters._session
    assert session1 != session2
    session1 = client1.transport.get_cluster._session
    session2 = client2.transport.get_cluster._session
    assert session1 != session2
    session1 = client1.transport.create_cluster._session
    session2 = client2.transport.create_cluster._session
    assert session1 != session2
    session1 = client1.transport.update_cluster._session
    session2 = client2.transport.update_cluster._session
    assert session1 != session2
    session1 = client1.transport.upgrade_cluster._session
    session2 = client2.transport.upgrade_cluster._session
    assert session1 != session2
    session1 = client1.transport.delete_cluster._session
    session2 = client2.transport.delete_cluster._session
    assert session1 != session2
    session1 = client1.transport.generate_access_token._session
    session2 = client2.transport.generate_access_token._session
    assert session1 != session2
    session1 = client1.transport.generate_offline_credential._session
    session2 = client2.transport.generate_offline_credential._session
    assert session1 != session2
    session1 = client1.transport.list_node_pools._session
    session2 = client2.transport.list_node_pools._session
    assert session1 != session2
    session1 = client1.transport.get_node_pool._session
    session2 = client2.transport.get_node_pool._session
    assert session1 != session2
    session1 = client1.transport.create_node_pool._session
    session2 = client2.transport.create_node_pool._session
    assert session1 != session2
    session1 = client1.transport.update_node_pool._session
    session2 = client2.transport.update_node_pool._session
    assert session1 != session2
    session1 = client1.transport.delete_node_pool._session
    session2 = client2.transport.delete_node_pool._session
    assert session1 != session2
    session1 = client1.transport.list_machines._session
    session2 = client2.transport.list_machines._session
    assert session1 != session2
    session1 = client1.transport.get_machine._session
    session2 = client2.transport.get_machine._session
    assert session1 != session2
    session1 = client1.transport.list_vpn_connections._session
    session2 = client2.transport.list_vpn_connections._session
    assert session1 != session2
    session1 = client1.transport.get_vpn_connection._session
    session2 = client2.transport.get_vpn_connection._session
    assert session1 != session2
    session1 = client1.transport.create_vpn_connection._session
    session2 = client2.transport.create_vpn_connection._session
    assert session1 != session2
    session1 = client1.transport.delete_vpn_connection._session
    session2 = client2.transport.delete_vpn_connection._session
    assert session1 != session2
    session1 = client1.transport.get_server_config._session
    session2 = client2.transport.get_server_config._session
    assert session1 != session2


def test_edge_container_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EdgeContainerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_edge_container_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.EdgeContainerGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EdgeContainerGrpcTransport,
        transports.EdgeContainerGrpcAsyncIOTransport,
    ],
)
def test_edge_container_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.EdgeContainerGrpcTransport,
        transports.EdgeContainerGrpcAsyncIOTransport,
    ],
)
def test_edge_container_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_edge_container_grpc_lro_client():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_edge_container_grpc_lro_async_client():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_cluster_path():
    project = "squid"
    location = "clam"
    cluster = "whelk"
    expected = "projects/{project}/locations/{location}/clusters/{cluster}".format(
        project=project,
        location=location,
        cluster=cluster,
    )
    actual = EdgeContainerClient.cluster_path(project, location, cluster)
    assert expected == actual


def test_parse_cluster_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "cluster": "nudibranch",
    }
    path = EdgeContainerClient.cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_cluster_path(path)
    assert expected == actual


def test_crypto_key_path():
    project = "cuttlefish"
    location = "mussel"
    key_ring = "winkle"
    crypto_key = "nautilus"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
    )
    actual = EdgeContainerClient.crypto_key_path(
        project, location, key_ring, crypto_key
    )
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "key_ring": "squid",
        "crypto_key": "clam",
    }
    path = EdgeContainerClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_crypto_key_path(path)
    assert expected == actual


def test_crypto_key_version_path():
    project = "whelk"
    location = "octopus"
    key_ring = "oyster"
    crypto_key = "nudibranch"
    crypto_key_version = "cuttlefish"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
        project=project,
        location=location,
        key_ring=key_ring,
        crypto_key=crypto_key,
        crypto_key_version=crypto_key_version,
    )
    actual = EdgeContainerClient.crypto_key_version_path(
        project, location, key_ring, crypto_key, crypto_key_version
    )
    assert expected == actual


def test_parse_crypto_key_version_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "key_ring": "nautilus",
        "crypto_key": "scallop",
        "crypto_key_version": "abalone",
    }
    path = EdgeContainerClient.crypto_key_version_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_crypto_key_version_path(path)
    assert expected == actual


def test_machine_path():
    project = "squid"
    location = "clam"
    machine = "whelk"
    expected = "projects/{project}/locations/{location}/machines/{machine}".format(
        project=project,
        location=location,
        machine=machine,
    )
    actual = EdgeContainerClient.machine_path(project, location, machine)
    assert expected == actual


def test_parse_machine_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "machine": "nudibranch",
    }
    path = EdgeContainerClient.machine_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_machine_path(path)
    assert expected == actual


def test_node_pool_path():
    project = "cuttlefish"
    location = "mussel"
    cluster = "winkle"
    node_pool = "nautilus"
    expected = "projects/{project}/locations/{location}/clusters/{cluster}/nodePools/{node_pool}".format(
        project=project,
        location=location,
        cluster=cluster,
        node_pool=node_pool,
    )
    actual = EdgeContainerClient.node_pool_path(project, location, cluster, node_pool)
    assert expected == actual


def test_parse_node_pool_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "cluster": "squid",
        "node_pool": "clam",
    }
    path = EdgeContainerClient.node_pool_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_node_pool_path(path)
    assert expected == actual


def test_vpn_connection_path():
    project = "whelk"
    location = "octopus"
    vpn_connection = "oyster"
    expected = "projects/{project}/locations/{location}/vpnConnections/{vpn_connection}".format(
        project=project,
        location=location,
        vpn_connection=vpn_connection,
    )
    actual = EdgeContainerClient.vpn_connection_path(project, location, vpn_connection)
    assert expected == actual


def test_parse_vpn_connection_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "vpn_connection": "mussel",
    }
    path = EdgeContainerClient.vpn_connection_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_vpn_connection_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = EdgeContainerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = EdgeContainerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = EdgeContainerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = EdgeContainerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = EdgeContainerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = EdgeContainerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = EdgeContainerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = EdgeContainerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = EdgeContainerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = EdgeContainerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = EdgeContainerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.EdgeContainerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.EdgeContainerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = EdgeContainerClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_location_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.GetLocationRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_location(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.GetLocationRequest,
        dict,
    ],
)
def test_get_location_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.Location()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_location(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_list_locations_rest_bad_request(
    transport: str = "rest", request_type=locations_pb2.ListLocationsRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({"name": "projects/sample1"}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_locations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        locations_pb2.ListLocationsRequest,
        dict,
    ],
)
def test_list_locations_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = locations_pb2.ListLocationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_locations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/locations/sample2"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc_asyncio"):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_delete_operation_from_dict():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc_asyncio"):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc_asyncio"):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.ListLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = locations_pb2.GetLocationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = EdgeContainerClient(credentials=ga_credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = EdgeContainerAsyncClient(credentials=ga_credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = EdgeContainerClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = EdgeContainerAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = EdgeContainerClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (EdgeContainerClient, transports.EdgeContainerGrpcTransport),
        (EdgeContainerAsyncClient, transports.EdgeContainerGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
