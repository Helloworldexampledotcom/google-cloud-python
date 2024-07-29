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
from google.cloud.discoveryengine_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.completion_service import (
    CompletionServiceAsyncClient,
    CompletionServiceClient,
)
from .services.control_service import ControlServiceAsyncClient, ControlServiceClient
from .services.conversational_search_service import (
    ConversationalSearchServiceAsyncClient,
    ConversationalSearchServiceClient,
)
from .services.data_store_service import (
    DataStoreServiceAsyncClient,
    DataStoreServiceClient,
)
from .services.document_service import DocumentServiceAsyncClient, DocumentServiceClient
from .services.engine_service import EngineServiceAsyncClient, EngineServiceClient
from .services.evaluation_service import (
    EvaluationServiceAsyncClient,
    EvaluationServiceClient,
)
from .services.grounded_generation_service import (
    GroundedGenerationServiceAsyncClient,
    GroundedGenerationServiceClient,
)
from .services.project_service import ProjectServiceAsyncClient, ProjectServiceClient
from .services.rank_service import RankServiceAsyncClient, RankServiceClient
from .services.recommendation_service import (
    RecommendationServiceAsyncClient,
    RecommendationServiceClient,
)
from .services.sample_query_service import (
    SampleQueryServiceAsyncClient,
    SampleQueryServiceClient,
)
from .services.sample_query_set_service import (
    SampleQuerySetServiceAsyncClient,
    SampleQuerySetServiceClient,
)
from .services.schema_service import SchemaServiceAsyncClient, SchemaServiceClient
from .services.search_service import SearchServiceAsyncClient, SearchServiceClient
from .services.search_tuning_service import (
    SearchTuningServiceAsyncClient,
    SearchTuningServiceClient,
)
from .services.serving_config_service import (
    ServingConfigServiceAsyncClient,
    ServingConfigServiceClient,
)
from .services.site_search_engine_service import (
    SiteSearchEngineServiceAsyncClient,
    SiteSearchEngineServiceClient,
)
from .services.user_event_service import (
    UserEventServiceAsyncClient,
    UserEventServiceClient,
)
from .types.answer import Answer
from .types.chunk import Chunk
from .types.common import (
    CustomAttribute,
    DoubleList,
    EmbeddingConfig,
    IndustryVertical,
    Interval,
    SearchAddOn,
    SearchTier,
    SearchUseCase,
    SolutionType,
    UserInfo,
)
from .types.completion import CompletionSuggestion, SuggestionDenyListEntry
from .types.completion_service import CompleteQueryRequest, CompleteQueryResponse
from .types.control import Condition, Control
from .types.control_service import (
    CreateControlRequest,
    DeleteControlRequest,
    GetControlRequest,
    ListControlsRequest,
    ListControlsResponse,
    UpdateControlRequest,
)
from .types.conversation import (
    Conversation,
    ConversationContext,
    ConversationMessage,
    Reply,
    TextInput,
)
from .types.conversational_search_service import (
    AnswerQueryRequest,
    AnswerQueryResponse,
    ConverseConversationRequest,
    ConverseConversationResponse,
    CreateConversationRequest,
    CreateSessionRequest,
    DeleteConversationRequest,
    DeleteSessionRequest,
    GetAnswerRequest,
    GetConversationRequest,
    GetSessionRequest,
    ListConversationsRequest,
    ListConversationsResponse,
    ListSessionsRequest,
    ListSessionsResponse,
    UpdateConversationRequest,
    UpdateSessionRequest,
)
from .types.custom_tuning_model import CustomTuningModel
from .types.data_store import DataStore, LanguageInfo
from .types.data_store_service import (
    CreateDataStoreMetadata,
    CreateDataStoreRequest,
    DeleteDataStoreMetadata,
    DeleteDataStoreRequest,
    GetDataStoreRequest,
    ListDataStoresRequest,
    ListDataStoresResponse,
    UpdateDataStoreRequest,
)
from .types.document import Document
from .types.document_processing_config import DocumentProcessingConfig
from .types.document_service import (
    CreateDocumentRequest,
    DeleteDocumentRequest,
    GetDocumentRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    UpdateDocumentRequest,
)
from .types.engine import Engine
from .types.engine_service import (
    CreateEngineMetadata,
    CreateEngineRequest,
    DeleteEngineMetadata,
    DeleteEngineRequest,
    GetEngineRequest,
    ListEnginesRequest,
    ListEnginesResponse,
    PauseEngineRequest,
    ResumeEngineRequest,
    TuneEngineMetadata,
    TuneEngineRequest,
    TuneEngineResponse,
    UpdateEngineRequest,
)
from .types.evaluation import Evaluation, QualityMetrics
from .types.evaluation_service import (
    CreateEvaluationMetadata,
    CreateEvaluationRequest,
    GetEvaluationRequest,
    ListEvaluationResultsRequest,
    ListEvaluationResultsResponse,
    ListEvaluationsRequest,
    ListEvaluationsResponse,
)
from .types.grounded_generation_service import (
    CheckGroundingRequest,
    CheckGroundingResponse,
    CheckGroundingSpec,
)
from .types.grounding import FactChunk, GroundingFact
from .types.import_config import (
    AlloyDbSource,
    BigQuerySource,
    BigtableOptions,
    BigtableSource,
    CloudSqlSource,
    FhirStoreSource,
    FirestoreSource,
    GcsSource,
    ImportCompletionSuggestionsMetadata,
    ImportCompletionSuggestionsRequest,
    ImportCompletionSuggestionsResponse,
    ImportDocumentsMetadata,
    ImportDocumentsRequest,
    ImportDocumentsResponse,
    ImportErrorConfig,
    ImportSampleQueriesMetadata,
    ImportSampleQueriesRequest,
    ImportSampleQueriesResponse,
    ImportSuggestionDenyListEntriesMetadata,
    ImportSuggestionDenyListEntriesRequest,
    ImportSuggestionDenyListEntriesResponse,
    ImportUserEventsMetadata,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
    SpannerSource,
)
from .types.project import Project
from .types.project_service import ProvisionProjectMetadata, ProvisionProjectRequest
from .types.purge_config import (
    PurgeCompletionSuggestionsMetadata,
    PurgeCompletionSuggestionsRequest,
    PurgeCompletionSuggestionsResponse,
    PurgeDocumentsMetadata,
    PurgeDocumentsRequest,
    PurgeDocumentsResponse,
    PurgeSuggestionDenyListEntriesMetadata,
    PurgeSuggestionDenyListEntriesRequest,
    PurgeSuggestionDenyListEntriesResponse,
    PurgeUserEventsMetadata,
    PurgeUserEventsRequest,
    PurgeUserEventsResponse,
)
from .types.rank_service import RankingRecord, RankRequest, RankResponse
from .types.recommendation_service import RecommendRequest, RecommendResponse
from .types.sample_query import SampleQuery
from .types.sample_query_service import (
    CreateSampleQueryRequest,
    DeleteSampleQueryRequest,
    GetSampleQueryRequest,
    ListSampleQueriesRequest,
    ListSampleQueriesResponse,
    UpdateSampleQueryRequest,
)
from .types.sample_query_set import SampleQuerySet
from .types.sample_query_set_service import (
    CreateSampleQuerySetRequest,
    DeleteSampleQuerySetRequest,
    GetSampleQuerySetRequest,
    ListSampleQuerySetsRequest,
    ListSampleQuerySetsResponse,
    UpdateSampleQuerySetRequest,
)
from .types.schema import Schema
from .types.schema_service import (
    CreateSchemaMetadata,
    CreateSchemaRequest,
    DeleteSchemaMetadata,
    DeleteSchemaRequest,
    GetSchemaRequest,
    ListSchemasRequest,
    ListSchemasResponse,
    UpdateSchemaMetadata,
    UpdateSchemaRequest,
)
from .types.search_service import SearchRequest, SearchResponse
from .types.search_tuning_service import (
    ListCustomModelsRequest,
    ListCustomModelsResponse,
    TrainCustomModelMetadata,
    TrainCustomModelRequest,
    TrainCustomModelResponse,
)
from .types.serving_config import ServingConfig
from .types.serving_config_service import (
    GetServingConfigRequest,
    ListServingConfigsRequest,
    ListServingConfigsResponse,
    UpdateServingConfigRequest,
)
from .types.session import Query, Session
from .types.site_search_engine import SiteSearchEngine, SiteVerificationInfo, TargetSite
from .types.site_search_engine_service import (
    BatchCreateTargetSiteMetadata,
    BatchCreateTargetSitesRequest,
    BatchCreateTargetSitesResponse,
    BatchVerifyTargetSitesMetadata,
    BatchVerifyTargetSitesRequest,
    BatchVerifyTargetSitesResponse,
    CreateTargetSiteMetadata,
    CreateTargetSiteRequest,
    DeleteTargetSiteMetadata,
    DeleteTargetSiteRequest,
    DisableAdvancedSiteSearchMetadata,
    DisableAdvancedSiteSearchRequest,
    DisableAdvancedSiteSearchResponse,
    EnableAdvancedSiteSearchMetadata,
    EnableAdvancedSiteSearchRequest,
    EnableAdvancedSiteSearchResponse,
    FetchDomainVerificationStatusRequest,
    FetchDomainVerificationStatusResponse,
    GetSiteSearchEngineRequest,
    GetTargetSiteRequest,
    ListTargetSitesRequest,
    ListTargetSitesResponse,
    RecrawlUrisMetadata,
    RecrawlUrisRequest,
    RecrawlUrisResponse,
    UpdateTargetSiteMetadata,
    UpdateTargetSiteRequest,
)
from .types.user_event import (
    CompletionInfo,
    DocumentInfo,
    MediaInfo,
    PageInfo,
    PanelInfo,
    SearchInfo,
    TransactionInfo,
    UserEvent,
)
from .types.user_event_service import CollectUserEventRequest, WriteUserEventRequest

__all__ = (
    "CompletionServiceAsyncClient",
    "ControlServiceAsyncClient",
    "ConversationalSearchServiceAsyncClient",
    "DataStoreServiceAsyncClient",
    "DocumentServiceAsyncClient",
    "EngineServiceAsyncClient",
    "EvaluationServiceAsyncClient",
    "GroundedGenerationServiceAsyncClient",
    "ProjectServiceAsyncClient",
    "RankServiceAsyncClient",
    "RecommendationServiceAsyncClient",
    "SampleQueryServiceAsyncClient",
    "SampleQuerySetServiceAsyncClient",
    "SchemaServiceAsyncClient",
    "SearchServiceAsyncClient",
    "SearchTuningServiceAsyncClient",
    "ServingConfigServiceAsyncClient",
    "SiteSearchEngineServiceAsyncClient",
    "UserEventServiceAsyncClient",
    "AlloyDbSource",
    "Answer",
    "AnswerQueryRequest",
    "AnswerQueryResponse",
    "BatchCreateTargetSiteMetadata",
    "BatchCreateTargetSitesRequest",
    "BatchCreateTargetSitesResponse",
    "BatchVerifyTargetSitesMetadata",
    "BatchVerifyTargetSitesRequest",
    "BatchVerifyTargetSitesResponse",
    "BigQuerySource",
    "BigtableOptions",
    "BigtableSource",
    "CheckGroundingRequest",
    "CheckGroundingResponse",
    "CheckGroundingSpec",
    "Chunk",
    "CloudSqlSource",
    "CollectUserEventRequest",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionInfo",
    "CompletionServiceClient",
    "CompletionSuggestion",
    "Condition",
    "Control",
    "ControlServiceClient",
    "Conversation",
    "ConversationContext",
    "ConversationMessage",
    "ConversationalSearchServiceClient",
    "ConverseConversationRequest",
    "ConverseConversationResponse",
    "CreateControlRequest",
    "CreateConversationRequest",
    "CreateDataStoreMetadata",
    "CreateDataStoreRequest",
    "CreateDocumentRequest",
    "CreateEngineMetadata",
    "CreateEngineRequest",
    "CreateEvaluationMetadata",
    "CreateEvaluationRequest",
    "CreateSampleQueryRequest",
    "CreateSampleQuerySetRequest",
    "CreateSchemaMetadata",
    "CreateSchemaRequest",
    "CreateSessionRequest",
    "CreateTargetSiteMetadata",
    "CreateTargetSiteRequest",
    "CustomAttribute",
    "CustomTuningModel",
    "DataStore",
    "DataStoreServiceClient",
    "DeleteControlRequest",
    "DeleteConversationRequest",
    "DeleteDataStoreMetadata",
    "DeleteDataStoreRequest",
    "DeleteDocumentRequest",
    "DeleteEngineMetadata",
    "DeleteEngineRequest",
    "DeleteSampleQueryRequest",
    "DeleteSampleQuerySetRequest",
    "DeleteSchemaMetadata",
    "DeleteSchemaRequest",
    "DeleteSessionRequest",
    "DeleteTargetSiteMetadata",
    "DeleteTargetSiteRequest",
    "DisableAdvancedSiteSearchMetadata",
    "DisableAdvancedSiteSearchRequest",
    "DisableAdvancedSiteSearchResponse",
    "Document",
    "DocumentInfo",
    "DocumentProcessingConfig",
    "DocumentServiceClient",
    "DoubleList",
    "EmbeddingConfig",
    "EnableAdvancedSiteSearchMetadata",
    "EnableAdvancedSiteSearchRequest",
    "EnableAdvancedSiteSearchResponse",
    "Engine",
    "EngineServiceClient",
    "Evaluation",
    "EvaluationServiceClient",
    "FactChunk",
    "FetchDomainVerificationStatusRequest",
    "FetchDomainVerificationStatusResponse",
    "FhirStoreSource",
    "FirestoreSource",
    "GcsSource",
    "GetAnswerRequest",
    "GetControlRequest",
    "GetConversationRequest",
    "GetDataStoreRequest",
    "GetDocumentRequest",
    "GetEngineRequest",
    "GetEvaluationRequest",
    "GetSampleQueryRequest",
    "GetSampleQuerySetRequest",
    "GetSchemaRequest",
    "GetServingConfigRequest",
    "GetSessionRequest",
    "GetSiteSearchEngineRequest",
    "GetTargetSiteRequest",
    "GroundedGenerationServiceClient",
    "GroundingFact",
    "ImportCompletionSuggestionsMetadata",
    "ImportCompletionSuggestionsRequest",
    "ImportCompletionSuggestionsResponse",
    "ImportDocumentsMetadata",
    "ImportDocumentsRequest",
    "ImportDocumentsResponse",
    "ImportErrorConfig",
    "ImportSampleQueriesMetadata",
    "ImportSampleQueriesRequest",
    "ImportSampleQueriesResponse",
    "ImportSuggestionDenyListEntriesMetadata",
    "ImportSuggestionDenyListEntriesRequest",
    "ImportSuggestionDenyListEntriesResponse",
    "ImportUserEventsMetadata",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "IndustryVertical",
    "Interval",
    "LanguageInfo",
    "ListControlsRequest",
    "ListControlsResponse",
    "ListConversationsRequest",
    "ListConversationsResponse",
    "ListCustomModelsRequest",
    "ListCustomModelsResponse",
    "ListDataStoresRequest",
    "ListDataStoresResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ListEnginesRequest",
    "ListEnginesResponse",
    "ListEvaluationResultsRequest",
    "ListEvaluationResultsResponse",
    "ListEvaluationsRequest",
    "ListEvaluationsResponse",
    "ListSampleQueriesRequest",
    "ListSampleQueriesResponse",
    "ListSampleQuerySetsRequest",
    "ListSampleQuerySetsResponse",
    "ListSchemasRequest",
    "ListSchemasResponse",
    "ListServingConfigsRequest",
    "ListServingConfigsResponse",
    "ListSessionsRequest",
    "ListSessionsResponse",
    "ListTargetSitesRequest",
    "ListTargetSitesResponse",
    "MediaInfo",
    "PageInfo",
    "PanelInfo",
    "PauseEngineRequest",
    "Project",
    "ProjectServiceClient",
    "ProvisionProjectMetadata",
    "ProvisionProjectRequest",
    "PurgeCompletionSuggestionsMetadata",
    "PurgeCompletionSuggestionsRequest",
    "PurgeCompletionSuggestionsResponse",
    "PurgeDocumentsMetadata",
    "PurgeDocumentsRequest",
    "PurgeDocumentsResponse",
    "PurgeSuggestionDenyListEntriesMetadata",
    "PurgeSuggestionDenyListEntriesRequest",
    "PurgeSuggestionDenyListEntriesResponse",
    "PurgeUserEventsMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "QualityMetrics",
    "Query",
    "RankRequest",
    "RankResponse",
    "RankServiceClient",
    "RankingRecord",
    "RecommendRequest",
    "RecommendResponse",
    "RecommendationServiceClient",
    "RecrawlUrisMetadata",
    "RecrawlUrisRequest",
    "RecrawlUrisResponse",
    "Reply",
    "ResumeEngineRequest",
    "SampleQuery",
    "SampleQueryServiceClient",
    "SampleQuerySet",
    "SampleQuerySetServiceClient",
    "Schema",
    "SchemaServiceClient",
    "SearchAddOn",
    "SearchInfo",
    "SearchRequest",
    "SearchResponse",
    "SearchServiceClient",
    "SearchTier",
    "SearchTuningServiceClient",
    "SearchUseCase",
    "ServingConfig",
    "ServingConfigServiceClient",
    "Session",
    "SiteSearchEngine",
    "SiteSearchEngineServiceClient",
    "SiteVerificationInfo",
    "SolutionType",
    "SpannerSource",
    "SuggestionDenyListEntry",
    "TargetSite",
    "TextInput",
    "TrainCustomModelMetadata",
    "TrainCustomModelRequest",
    "TrainCustomModelResponse",
    "TransactionInfo",
    "TuneEngineMetadata",
    "TuneEngineRequest",
    "TuneEngineResponse",
    "UpdateControlRequest",
    "UpdateConversationRequest",
    "UpdateDataStoreRequest",
    "UpdateDocumentRequest",
    "UpdateEngineRequest",
    "UpdateSampleQueryRequest",
    "UpdateSampleQuerySetRequest",
    "UpdateSchemaMetadata",
    "UpdateSchemaRequest",
    "UpdateServingConfigRequest",
    "UpdateSessionRequest",
    "UpdateTargetSiteMetadata",
    "UpdateTargetSiteRequest",
    "UserEvent",
    "UserEventServiceClient",
    "UserInfo",
    "WriteUserEventRequest",
)
