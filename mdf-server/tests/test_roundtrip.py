"""Tests for Draw.io round-trip — SCHEMA-04."""
import pytest


@pytest.mark.skip(reason="Implemented in plan 04")
def test_generated_xml_is_valid_xml():
    """SCHEMA-04: XML generated from a sample model is well-formed XML parseable by defusedxml."""
    pass


@pytest.mark.skip(reason="Implemented in plan 04")
def test_roundtrip_structural_equality():
    """SCHEMA-04: generate XML -> parse back -> compare class/state/transition names are identical."""
    pass
