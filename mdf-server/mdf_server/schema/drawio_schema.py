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
    "render_sample_xml",
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


# ---------------------------------------------------------------------------
# XML generator — for SCHEMA-04 round-trip testing only
# ---------------------------------------------------------------------------

from lxml import etree  # noqa: E402 — imported here to keep module lighter


def render_sample_xml() -> bytes:
    """Generate a minimal representative Draw.io XML for round-trip testing.

    Produces an uncompressed mxfile (compressed='false') so Draw.io does not
    base64-encode the diagram on save, avoiding the Pitfall 2 decompression
    issue documented in RESEARCH.md.

    Returns UTF-8 encoded bytes of the full mxfile XML.
    """
    domain = "Hydraulics"

    mxfile = etree.Element("mxfile", compressed="false", version="24.0.0")
    diagram = etree.SubElement(mxfile, "diagram", name="Page-1", id="page1")
    etree.SubElement(
        diagram, "mxGraphModel",
        dx="1034", dy="546", grid="1", gridSize="10",
        guides="1", tooltips="1", connect="1", arrows="1",
        fold="1", page="1", pageScale="1",
        pageWidth="1169", pageHeight="827",
        math="0", shadow="0",
    )
    model_el = diagram[0]
    root_el = etree.SubElement(model_el, "root")
    etree.SubElement(root_el, "mxCell", id="0")
    etree.SubElement(root_el, "mxCell", id="1", parent="0")

    # --- Class: Valve ---
    valve_cid = class_id(domain, "Valve")
    valve_cell = etree.SubElement(
        root_el, "mxCell",
        id=valve_cid, value="<<entity>>\nValve",
        style=STYLE_CLASS, vertex="1", parent="1",
    )
    etree.SubElement(
        valve_cell, "mxGeometry",
        x="100", y="100", width="200", height="60",
        attrib={"as": "geometry"},
    )

    # Attribute child cells
    for i, (attr_name, attr_label) in enumerate([
        ("valve_id", "[I] valve_id: ValveID"),
        ("position", "position: Real"),
    ]):
        a_id = attribute_id(domain, "Valve", attr_name)
        a_cell = etree.SubElement(
            root_el, "mxCell",
            id=a_id, value=attr_label,
            style=STYLE_ATTRIBUTE, vertex="1", parent=valve_cid,
        )
        etree.SubElement(
            a_cell, "mxGeometry",
            y=str(60 + i * 20), width="200", height="20",
            attrib={"as": "geometry"},
        )

    # --- Class: ActuatorPosition ---
    ap_cid = class_id(domain, "ActuatorPosition")
    ap_cell = etree.SubElement(
        root_el, "mxCell",
        id=ap_cid, value="<<entity>>\nActuatorPosition",
        style=STYLE_CLASS, vertex="1", parent="1",
    )
    etree.SubElement(
        ap_cell, "mxGeometry",
        x="400", y="100", width="200", height="60",
        attrib={"as": "geometry"},
    )

    # --- Association R1: Valve -> ActuatorPosition ---
    r1_cid = association_id(domain, "R1")
    r1_cell = etree.SubElement(
        root_el, "mxCell",
        id=r1_cid, value="R1",
        style=STYLE_ASSOCIATION, edge="1",
        source=valve_cid, target=ap_cid, parent="1",
    )
    etree.SubElement(r1_cell, "mxGeometry", attrib={"relative": "1", "as": "geometry"})

    # --- State machine: Valve ---
    idle_cid = state_id(domain, "Valve", "Idle")
    idle_cell = etree.SubElement(
        root_el, "mxCell",
        id=idle_cid, value="Idle",
        style=STYLE_STATE, vertex="1", parent="1",
    )
    etree.SubElement(
        idle_cell, "mxGeometry",
        x="100", y="300", width="120", height="60",
        attrib={"as": "geometry"},
    )

    opening_cid = state_id(domain, "Valve", "Opening")
    opening_cell = etree.SubElement(
        root_el, "mxCell",
        id=opening_cid, value="Opening",
        style=STYLE_STATE, vertex="1", parent="1",
    )
    etree.SubElement(
        opening_cell, "mxGeometry",
        x="300", y="300", width="120", height="60",
        attrib={"as": "geometry"},
    )

    # Initial pseudostate
    init_cid = f"{domain.lower()}:state:Valve:__initial__"
    init_cell = etree.SubElement(
        root_el, "mxCell",
        id=init_cid, value="",
        style=STYLE_INITIAL_PSEUDO, vertex="1", parent="1",
    )
    etree.SubElement(
        init_cell, "mxGeometry",
        x="40", y="320", width="20", height="20",
        attrib={"as": "geometry"},
    )

    # Initial -> Idle transition
    init_trans_cid = f"{domain.lower()}:trans:Valve:__initial__:__init__:0"
    init_trans = etree.SubElement(
        root_el, "mxCell",
        id=init_trans_cid, value="",
        style=STYLE_TRANSITION, edge="1",
        source=init_cid, target=idle_cid, parent="1",
    )
    etree.SubElement(init_trans, "mxGeometry", attrib={"relative": "1", "as": "geometry"})

    # Idle -> Opening on Open [guard]
    trans_cid = transition_id(domain, "Valve", "Idle", "Open", 0)
    trans_cell = etree.SubElement(
        root_el, "mxCell",
        id=trans_cid, value="Open [self.pressure < max_pressure]",
        style=STYLE_TRANSITION, edge="1",
        source=idle_cid, target=opening_cid, parent="1",
    )
    etree.SubElement(trans_cell, "mxGeometry", attrib={"relative": "1", "as": "geometry"})

    return etree.tostring(mxfile, encoding="unicode", xml_declaration=False).encode("utf-8")
