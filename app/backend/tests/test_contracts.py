import pytest
from pydantic import ValidationError

from schemas.lore import LoreCreate
from schemas.theories import TheoryCreate
from utils.catalog import catalog_id


def test_lore_requires_attached_work():
    with pytest.raises(ValidationError):
        LoreCreate(title="A valid title", body="This body has enough words to satisfy the minimum length.")


def test_theory_requires_attached_work():
    with pytest.raises(ValidationError):
        TheoryCreate(title="A valid title", abstract="A theory without a target must not be accepted.")


def test_external_catalogue_ids_are_stable():
    assert catalog_id("track", "itunes", 12345) == "itunes-track-12345"
