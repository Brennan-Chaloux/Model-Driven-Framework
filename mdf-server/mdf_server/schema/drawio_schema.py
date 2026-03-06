"""
Draw.io canonical bijection constants — style strings for all MDF model elements.

These constants are the canonical bijection between YAML model elements and
Draw.io mxCell style strings. They are locked values derived from RESEARCH.md.

Do not modify these strings without updating validate_drawio and sync_from_drawio
in Phase 4.
"""

__all__ = [
    "STYLE_CLASS",
    "STYLE_ATTRIBUTE",
    "STYLE_ASSOCIATION",
    "STYLE_ASSOC_LABEL",
    "STYLE_STATE",
    "STYLE_INITIAL_PSEUDO",
    "STYLE_TRANSITION",
    "STYLE_BRIDGE",
    "BIJECTION_TABLE",
    "class_id",
    "attribute_id",
    "association_id",
    "state_id",
    "transition_id",
]

# ---------------------------------------------------------------------------
# Style constants — immutable canonical mxCell style strings
# ---------------------------------------------------------------------------

STYLE_CLASS = (
    "swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;"
    "startSize=26;fillColor=#dae8fc;strokeColor=#6c8ebf;rounded=0;"
)

STYLE_ATTRIBUTE = (
    "text;strokeColor=none;fillColor=none;align=left;"
    "verticalAlign=middle;spacingLeft=4;spacingRight=4;"
)

STYLE_ASSOCIATION = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;"

STYLE_ASSOC_LABEL = "edgeLabel;align=center;"

STYLE_STATE = "rounded=1;whiteSpace=wrap;html=1;arcSize=50;"

STYLE_INITIAL_PSEUDO = (
    "ellipse;whiteSpace=wrap;html=1;aspect=fixed;"
    "fillColor=#000000;strokeColor=#000000;"
)

STYLE_TRANSITION = "edgeStyle=orthogonalEdgeStyle;html=1;"

STYLE_BRIDGE = "dashed=1;endArrow=open;endFill=0;html=1;"

# ---------------------------------------------------------------------------
# Bijection table — maps element type name to its style constant
# ---------------------------------------------------------------------------

BIJECTION_TABLE: dict[str, str] = {
    "class":          STYLE_CLASS,
    "attribute":      STYLE_ATTRIBUTE,
    "association":    STYLE_ASSOCIATION,
    "assoc_label":    STYLE_ASSOC_LABEL,
    "state":          STYLE_STATE,
    "initial_pseudo": STYLE_INITIAL_PSEUDO,
    "transition":     STYLE_TRANSITION,
    "bridge":         STYLE_BRIDGE,
}

# ---------------------------------------------------------------------------
# Deterministic ID generator functions
# Domain is always lowercased — this is the canonical form.
# ---------------------------------------------------------------------------


def class_id(domain: str, class_name: str) -> str:
    """Return deterministic mxCell ID for a class element."""
    return f"{domain.lower()}:class:{class_name}"


def attribute_id(domain: str, class_name: str, attr_name: str) -> str:
    """Return deterministic mxCell ID for an attribute element."""
    return f"{domain.lower()}:attr:{class_name}:{attr_name}"


def association_id(domain: str, assoc_name: str) -> str:
    """Return deterministic mxCell ID for an association element."""
    return f"{domain.lower()}:assoc:{assoc_name}"


def state_id(domain: str, class_name: str, state_name: str) -> str:
    """Return deterministic mxCell ID for a state element."""
    return f"{domain.lower()}:state:{class_name}:{state_name}"


def transition_id(
    domain: str, class_name: str, from_state: str, event: str, idx: int
) -> str:
    """Return deterministic mxCell ID for a transition element.

    idx disambiguates multiple transitions on the same (from_state, event) pair.
    """
    return f"{domain.lower()}:trans:{class_name}:{from_state}:{event}:{idx}"
