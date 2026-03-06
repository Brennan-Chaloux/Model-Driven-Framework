"""
model_io — MDF model I/O tools: list_domains, read_model, write_model.

Full implementation in plan 02-02.
"""
from pathlib import Path

MODEL_ROOT = Path(".design/model")


def list_domains() -> list[str]:
    """
    Returns all domain names found in .design/model/.
    A domain is any subdirectory containing class-diagram.yaml.
    Returns [] if .design/model/ does not exist or is empty.
    Call this before read_model() to discover available domains.
    """
    return []  # implemented in plan 02-02


def read_model(domain: str) -> str | dict:
    """
    Returns the raw YAML string from .design/model/<domain>/class-diagram.yaml.
    Domain lookup is case-insensitive.
    On success: returns the YAML file content as a string.
    On domain not found: returns {"error": "Domain 'X' not found", "available": [...]}
    Call list_domains() first to discover available domain names.
    """
    return ""  # implemented in plan 02-02


def write_model(domain: str, yaml_str: str) -> list[dict]:
    """
    Saves yaml_str to .design/model/<domain>/class-diagram.yaml after validation.
    Validates YAML syntax and Pydantic schema before writing. Never writes on error.
    Auto-creates .design/model/<domain>/ if it does not exist.
    Returns [] on success.
    Returns [{"issue": str, "location": str, "value": any}] on any error.
    Never raises exceptions — all errors are returned as structured data.
    """
    return []  # implemented in plan 02-02
