# © 2018 Software Freedom Conservancy (SFC)
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
# SPDX-License-Identifier: Apache-2.0


"""
cwlprov Command Line internal utility functions
"""
__author__ = "Stian Soiland-Reyes <https://orcid.org/0000-0001-9842-9718>"
__copyright__ = "© 2018 Software Freedom Conservancy (SFC)"
__license__ = (
    "Apache License, version 2.0 (https://www.apache.org/licenses/LICENSE-2.0)"
)

import datetime
from functools import partial
from typing import Any, Iterable, Optional, Sequence, Set, Tuple, TypeVar, Union

prov_type = Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]]

_T = TypeVar("_T")


def first(iterable: Iterable[_T]) -> Optional[_T]:
    """Return the first item from an interable."""
    return next(iter(iterable), None)


def many(s: Set[Any]) -> str:
    """Convert a set of strings into a comma separated string."""
    return ", ".join(map(str, s))


ANY_VALUE = object()


def find_dict_with_item(
    json: Any, val: Any = ANY_VALUE, key: str = "id"
) -> Optional[Any]:
    if hasattr(json, "get"):
        if json.get(key, ANY_VALUE) == val:
            return json

    # Search children
    if hasattr(json, "values"):
        return find_dict_with_item(json.values(), val, key)
    elif hasattr(json, "__iter__") and not isinstance(json, str):
        return first(
            filter(None, map(partial(find_dict_with_item, key=key, val=val), json))
        )
    else:
        # Can't iterate further, look elsewhere
        return None


def average(it: Sequence[datetime.timedelta]) -> Optional[datetime.timedelta]:
    """Average one or more timedeltas."""
    if not it:
        return None
    return sum(it[1:], it[0]) / len(it)
