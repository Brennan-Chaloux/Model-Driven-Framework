"""Tests for template files — SCHEMA-05 (behavior docs), TMPL-01..04 (YAML templates)."""
import pytest
from pathlib import Path

# Resolve repo root relative to this test file (mdf-server/tests/test_templates.py -> repo root is ../../)
REPO_ROOT = Path(__file__).parent.parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"


# --- Existence tests (TMPL-01..04) ---

def test_domains_yaml_template_exists():
    """TMPL-01: templates/DOMAINS.yaml.tmpl exists."""
    assert (TEMPLATES_DIR / "DOMAINS.yaml.tmpl").is_file()


def test_class_diagram_yaml_template_exists():
    """TMPL-02: templates/CLASS_DIAGRAM.yaml.tmpl exists."""
    assert (TEMPLATES_DIR / "CLASS_DIAGRAM.yaml.tmpl").is_file()


def test_state_diagram_yaml_template_exists():
    """TMPL-03: templates/STATE_DIAGRAM.yaml.tmpl exists."""
    assert (TEMPLATES_DIR / "STATE_DIAGRAM.yaml.tmpl").is_file()


def test_behavior_domain_template_exists():
    """TMPL-04 / SCHEMA-05: templates/behavior-domain.md.tmpl exists."""
    assert (TEMPLATES_DIR / "behavior-domain.md.tmpl").is_file()


def test_behavior_class_template_exists():
    """TMPL-04 / SCHEMA-05: templates/behavior-class.md.tmpl exists."""
    assert (TEMPLATES_DIR / "behavior-class.md.tmpl").is_file()


def test_behavior_state_template_exists():
    """TMPL-04 / SCHEMA-05: templates/behavior-state.md.tmpl exists."""
    assert (TEMPLATES_DIR / "behavior-state.md.tmpl").is_file()


# --- Section content tests (SCHEMA-05) ---

def test_behavior_domain_required_sections():
    """SCHEMA-05: behavior-domain.md.tmpl contains Purpose, Scope, Bridge Contracts sections."""
    content = (TEMPLATES_DIR / "behavior-domain.md.tmpl").read_text(encoding="utf-8")
    assert "## Purpose" in content
    assert "## Scope" in content
    assert "## Bridge Contracts" in content


def test_behavior_class_required_sections():
    """SCHEMA-05: behavior-class.md.tmpl contains Purpose, Attributes, Lifecycle, Methods sections."""
    content = (TEMPLATES_DIR / "behavior-class.md.tmpl").read_text(encoding="utf-8")
    assert "## Purpose" in content
    assert "## Attributes" in content
    assert "## Lifecycle" in content
    assert "## Methods" in content


def test_behavior_state_required_sections():
    """SCHEMA-05: behavior-state.md.tmpl contains Purpose, States, Event Catalog sections."""
    content = (TEMPLATES_DIR / "behavior-state.md.tmpl").read_text(encoding="utf-8")
    assert "## Purpose" in content
    assert "## States" in content
    assert "## Event Catalog" in content
