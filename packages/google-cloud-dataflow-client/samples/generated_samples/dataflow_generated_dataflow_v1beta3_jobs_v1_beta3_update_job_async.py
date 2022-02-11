# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
# Generated code. DO NOT EDIT!
#
# Snippet for UpdateJob
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dataflow-client


# [START dataflow_generated_dataflow_v1beta3_JobsV1Beta3_UpdateJob_async]
from google.cloud import dataflow_v1beta3


async def sample_update_job():
    # Create a client
    client = dataflow_v1beta3.JobsV1Beta3AsyncClient()

    # Initialize request argument(s)
    request = dataflow_v1beta3.UpdateJobRequest(
    )

    # Make the request
    response = await client.update_job(request=request)

    # Handle the response
    print(response)

# [END dataflow_generated_dataflow_v1beta3_JobsV1Beta3_UpdateJob_async]
