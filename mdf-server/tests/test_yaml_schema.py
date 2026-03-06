"""Tests for yaml_schema.py — SCHEMA-01 (valid YAML accepted) and SCHEMA-02 (schema_version required)."""
import pytest
from mdf_server.schema import yaml_schema  # noqa: F401 — import smoke test


@pytest.mark.skip(reason="Implemented in plan 02")
def test_valid_domains_yaml_accepted():
    """SCHEMA-01: A valid DOMAINS.yaml dict is accepted by DomainsFile without error."""
    pass


@pytest.mark.skip(reason="Implemented in plan 02")
def test_valid_class_diagram_accepted():
    """SCHEMA-01: A valid class-diagram.yaml dict is accepted by ClassDiagramFile without error."""
    pass


@pytest.mark.skip(reason="Implemented in plan 02")
def test_valid_state_diagram_accepted():
    """SCHEMA-01: A valid state-diagrams/<Class>.yaml dict is accepted by StateDiagramFile without error."""
    pass


@pytest.mark.skip(reason="Implemented in plan 02")
def test_valid_types_yaml_accepted():
    """SCHEMA-01: A valid types.yaml dict is accepted by TypesFile without error."""
    pass


@pytest.mark.skip(reason="Implemented in plan 02")
def test_missing_schema_version_rejected():
    """SCHEMA-02: Any model file dict missing schema_version raises ValidationError."""
    pass


@pytest.mark.skip(reason="Implemented in plan 02")
def test_invalid_semver_rejected():
    """SCHEMA-02: schema_version not matching semver pattern raises ValidationError."""
    pass


@pytest.mark.skip(reason="Implemented in plan 02")
def test_associative_missing_formalizes_rejected():
    """SCHEMA-01: ClassDef with stereotype=associative and no formalizes raises ValidationError."""
    pass


@pytest.mark.skip(reason="Implemented in plan 02")
def test_guard_all_or_none_violation_rejected():
    """SCHEMA-01: StateDiagramFile with mixed guarded/unguarded transitions on same (from, event) raises ValidationError."""
    pass
