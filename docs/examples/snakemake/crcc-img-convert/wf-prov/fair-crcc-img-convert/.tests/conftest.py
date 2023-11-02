
import logging
import shutil
import tempfile
import urllib.request

from pathlib import Path

import pytest

_logger = logging.getLogger(__file__)

TmpPrefix = "fair-crcc-test"


@pytest.fixture(scope="session")
def mirax_1_zip():
    link_to_slide = "https://openslide.cs.cmu.edu/download/openslide-testdata/Mirax/CMU-1-Saved-1_16.zip"
    with tempfile.NamedTemporaryFile(prefix=(TmpPrefix + "-mirax1zip")) as f:
        urllib.request.urlretrieve(link_to_slide, f.name)
        _logger.info("Retrieved archive %s", link_to_slide)
        yield f.name


@pytest.fixture
def empty_repository():
    """
    A directory that can be used as an image repository. It contains the public
    and a private crypt4gh key.
    """
    with tempfile.TemporaryDirectory(prefix=TmpPrefix) as dir_name:
        keys = [Path(__file__).parent / 'data' / filename
                for filename in ('repo.sec', 'repo.pub')]
        for key in keys:
            shutil.copy2(key, Path(dir_name, key.name))
        yield Path(dir_name)
