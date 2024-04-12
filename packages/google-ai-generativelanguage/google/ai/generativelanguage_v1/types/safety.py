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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.ai.generativelanguage.v1",
    manifest={
        "HarmCategory",
        "SafetyRating",
        "SafetySetting",
    },
)


class HarmCategory(proto.Enum):
    r"""The category of a rating.

    These categories cover various kinds of harms that developers
    may wish to adjust.

    Values:
        HARM_CATEGORY_UNSPECIFIED (0):
            Category is unspecified.
        HARM_CATEGORY_DEROGATORY (1):
            Negative or harmful comments targeting
            identity and/or protected attribute.
        HARM_CATEGORY_TOXICITY (2):
            Content that is rude, disrespectful, or
            profane.
        HARM_CATEGORY_VIOLENCE (3):
            Describes scenarios depicting violence
            against an individual or group, or general
            descriptions of gore.
        HARM_CATEGORY_SEXUAL (4):
            Contains references to sexual acts or other
            lewd content.
        HARM_CATEGORY_MEDICAL (5):
            Promotes unchecked medical advice.
        HARM_CATEGORY_DANGEROUS (6):
            Dangerous content that promotes, facilitates,
            or encourages harmful acts.
        HARM_CATEGORY_HARASSMENT (7):
            Harasment content.
        HARM_CATEGORY_HATE_SPEECH (8):
            Hate speech and content.
        HARM_CATEGORY_SEXUALLY_EXPLICIT (9):
            Sexually explicit content.
        HARM_CATEGORY_DANGEROUS_CONTENT (10):
            Dangerous content.
    """
    HARM_CATEGORY_UNSPECIFIED = 0
    HARM_CATEGORY_DEROGATORY = 1
    HARM_CATEGORY_TOXICITY = 2
    HARM_CATEGORY_VIOLENCE = 3
    HARM_CATEGORY_SEXUAL = 4
    HARM_CATEGORY_MEDICAL = 5
    HARM_CATEGORY_DANGEROUS = 6
    HARM_CATEGORY_HARASSMENT = 7
    HARM_CATEGORY_HATE_SPEECH = 8
    HARM_CATEGORY_SEXUALLY_EXPLICIT = 9
    HARM_CATEGORY_DANGEROUS_CONTENT = 10


class SafetyRating(proto.Message):
    r"""Safety rating for a piece of content.

    The safety rating contains the category of harm and the harm
    probability level in that category for a piece of content.
    Content is classified for safety across a number of harm
    categories and the probability of the harm classification is
    included here.

    Attributes:
        category (google.ai.generativelanguage_v1.types.HarmCategory):
            Required. The category for this rating.
        probability (google.ai.generativelanguage_v1.types.SafetyRating.HarmProbability):
            Required. The probability of harm for this
            content.
        blocked (bool):
            Was this content blocked because of this
            rating?
    """

    class HarmProbability(proto.Enum):
        r"""The probability that a piece of content is harmful.

        The classification system gives the probability of the content
        being unsafe. This does not indicate the severity of harm for a
        piece of content.

        Values:
            HARM_PROBABILITY_UNSPECIFIED (0):
                Probability is unspecified.
            NEGLIGIBLE (1):
                Content has a negligible chance of being
                unsafe.
            LOW (2):
                Content has a low chance of being unsafe.
            MEDIUM (3):
                Content has a medium chance of being unsafe.
            HIGH (4):
                Content has a high chance of being unsafe.
        """
        HARM_PROBABILITY_UNSPECIFIED = 0
        NEGLIGIBLE = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4

    category: "HarmCategory" = proto.Field(
        proto.ENUM,
        number=3,
        enum="HarmCategory",
    )
    probability: HarmProbability = proto.Field(
        proto.ENUM,
        number=4,
        enum=HarmProbability,
    )
    blocked: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class SafetySetting(proto.Message):
    r"""Safety setting, affecting the safety-blocking behavior.

    Passing a safety setting for a category changes the allowed
    proability that content is blocked.

    Attributes:
        category (google.ai.generativelanguage_v1.types.HarmCategory):
            Required. The category for this setting.
        threshold (google.ai.generativelanguage_v1.types.SafetySetting.HarmBlockThreshold):
            Required. Controls the probability threshold
            at which harm is blocked.
    """

    class HarmBlockThreshold(proto.Enum):
        r"""Block at and beyond a specified harm probability.

        Values:
            HARM_BLOCK_THRESHOLD_UNSPECIFIED (0):
                Threshold is unspecified.
            BLOCK_LOW_AND_ABOVE (1):
                Content with NEGLIGIBLE will be allowed.
            BLOCK_MEDIUM_AND_ABOVE (2):
                Content with NEGLIGIBLE and LOW will be
                allowed.
            BLOCK_ONLY_HIGH (3):
                Content with NEGLIGIBLE, LOW, and MEDIUM will
                be allowed.
            BLOCK_NONE (4):
                All content will be allowed.
        """
        HARM_BLOCK_THRESHOLD_UNSPECIFIED = 0
        BLOCK_LOW_AND_ABOVE = 1
        BLOCK_MEDIUM_AND_ABOVE = 2
        BLOCK_ONLY_HIGH = 3
        BLOCK_NONE = 4

    category: "HarmCategory" = proto.Field(
        proto.ENUM,
        number=3,
        enum="HarmCategory",
    )
    threshold: HarmBlockThreshold = proto.Field(
        proto.ENUM,
        number=4,
        enum=HarmBlockThreshold,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
