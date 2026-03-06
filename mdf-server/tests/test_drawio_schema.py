"""Tests for drawio_schema.py — SCHEMA-03 (bijection table complete)."""
import pytest
from mdf_server.schema import drawio_schema  # noqa: F401 — import smoke test


@pytest.mark.skip(reason="Implemented in plan 03")
def test_all_yaml_elements_have_style_constant():
    """SCHEMA-03: drawio_schema defines a style constant for every YAML element type."""
    pass


@pytest.mark.skip(reason="Implemented in plan 03")
def test_style_constants_are_nonempty_strings():
    """SCHEMA-03: All style constants are non-empty strings."""
    pass
