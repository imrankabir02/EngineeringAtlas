#!/usr/bin/env python3
"""Generate the dependency-map diagrams from the learning graph.

The diagrams under graph/diagrams/ used to be hand-maintained Mermaid, which made them
the only duplication in the repository: the graph said one thing and a human-drawn
picture said another, with nothing to catch the drift. This script removes that by
deriving every diagram from graph/registry/*.yml and the published topic.yml files.

Two stages, deliberately separated so CI needs no browser:

    python3 tools/generate_diagrams.py     graph  -> .mmd   (pure Python, ~instant)
    tools/render_diagrams.sh               .mmd   -> .svg   (needs node + chromium)

Stage 1 also writes a manifest of .mmd checksums. Stage 2 stamps the checksum it
rendered from into each SVG. `--check` verifies both links in that chain, so a stale
diagram fails CI without anything having to render.

Usage:
    python3 tools/generate_diagrams.py            # write .mmd files and the manifest
    python3 tools/generate_diagrams.py --check     # verify committed output is current
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
DIAGRAM_DIR = ROOT / "graph" / "diagrams"
VIEWS_FILE = ROOT / "graph" / "diagrams.yml"
MANIFEST = DIAGRAM_DIR / "manifest.yml"

# Mermaid node ids cannot contain hyphens, so topic ids are transliterated. The label
# keeps the real id, because that is what a learner references everywhere else.
def node_id(topic_id: str) -> str:
    return re.sub(r"[^a-z0-9]", "_", topic_id)


def load_graph() -> dict[str, dict]:
    """Return {topic_id: {...}} with hard prerequisites resolved from the real source.

    Prerequisites live in the registry for planned nodes and in topic.yml for written
    ones. That asymmetry is the schema's single-source-of-truth rule, so it is honoured
    here rather than worked around.
    """
    nodes: dict[str, dict] = {}
    for path in sorted((ROOT / "graph" / "registry").glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        domain = data["domain"]
        for entry in data.get("topics") or []:
            nodes[entry["id"]] = {
                "id": entry["id"],
                "title": entry["title"],
                "level": entry["level"],
                "status": entry["status"],
                "domain": domain,
                "hard": list((entry.get("prerequisites") or {}).get("hard") or []),
            }

    for node in nodes.values():
        if node["status"] == "planned":
            continue
        topic_yml = ROOT / "topics" / node["domain"] / node["id"] / "topic.yml"
        if not topic_yml.is_file():
            continue
        data = yaml.safe_load(topic_yml.read_text(encoding="utf-8"))
        hard = (data.get("prerequisites") or {}).get("hard") or []
        node["hard"] = [h["id"] if isinstance(h, dict) else h for h in hard]

    return nodes


def resolve_view(view: dict, nodes: dict[str, dict], default_boundary: str) -> tuple[list[str], set[str]]:
    """Return (ordered node ids, boundary ids) for one view."""
    core: list[str] = []

    for domain in view.get("domains") or []:
        matched = [n["id"] for n in nodes.values() if n["domain"] == domain]
        if not matched:
            sys.exit(f"view '{view['id']}': domain '{domain}' matched no topics")
        # Level then id: gives every diagram a stable, readable top-to-bottom order.
        core += sorted(matched, key=lambda t: (nodes[t]["level"], t))

    for topic in (view.get("topics") or []) + (view.get("extra") or []):
        if topic not in nodes:
            sys.exit(f"view '{view['id']}': unknown topic '{topic}'")
        core.append(topic)

    seen: set[str] = set()
    ordered = [t for t in core if not (t in seen or seen.add(t))]

    boundary: set[str] = set()
    if view.get("boundary", default_boundary) == "prerequisites":
        # Only cross-domain prerequisites that more than one topic in the view depends on.
        # Drawing every one-off dependency spread the widest diagrams to 4,000px of thin
        # strip, which is illegible at any screen size. The generated table carries the
        # complete prerequisite list, so nothing is lost - only the picture is simplified.
        dependents: dict[str, int] = {}
        for topic in ordered:
            for prereq in nodes[topic]["hard"]:
                if prereq in nodes and prereq not in seen:
                    dependents[prereq] = dependents.get(prereq, 0) + 1
        threshold = view.get("boundary_min_dependents", 2)
        boundary = {p for p, count in dependents.items() if count >= threshold}

    return ordered, boundary


def render_mmd(view: dict, nodes: dict[str, dict], ordered: list[str], boundary: set[str]) -> str:
    """Emit Mermaid source.

    Two deliberate choices, both learned from the hand-written version:

    - Every label is quoted. Unquoted labels containing markup work by accident and
      break on characters nobody anticipated.
    - No inline HTML for emphasis. `<b>` renders only while Mermaid's htmlLabels are
      enabled, so classDef carries the distinction instead. `<br/>` is safe either way,
      because Mermaid converts it to tspans regardless of that setting.
    - No hard-coded colours, so the same source renders correctly in the light and dark
      themes.
    """
    in_view = set(ordered) | boundary
    lines = [
        "%% GENERATED FILE - do not edit.",
        "%% Source: graph/registry/*.yml + graph/diagrams.yml",
        "%% Regenerate: python3 tools/generate_diagrams.py",
        "graph TD",
        "    classDef published stroke-width:3px;",
        "    classDef boundary stroke-dasharray:5 3;",
    ]

    for topic in ordered + sorted(boundary):
        node = nodes[topic]
        lines.append(f'    {node_id(topic)}["{topic}<br/>L{node["level"]}"]')

    edges: list[tuple[str, str]] = []
    for topic in ordered:
        for prereq in nodes[topic]["hard"]:
            if prereq in in_view:
                edges.append((prereq, topic))
    for prereq, topic in sorted(set(edges)):
        lines.append(f"    {node_id(prereq)} --> {node_id(topic)}")

    published = [t for t in ordered if nodes[t]["status"] == "published"]
    if published:
        lines.append("    class " + ",".join(node_id(t) for t in published) + " published;")
    if boundary:
        lines.append("    class " + ",".join(node_id(t) for t in sorted(boundary)) + " boundary;")

    return "\n".join(lines) + "\n"


BEGIN_MARKER = "<!-- BEGIN GENERATED DIAGRAMS -->"
END_MARKER = "<!-- END GENERATED DIAGRAMS -->"
MAP_FILE = ROOT / "graph" / "dependency-map.md"


def render_markdown(
    view: dict, nodes: dict[str, dict], ordered: list[str], boundary: set[str], edge_count: int
) -> str:
    """Emit the markdown section for one view.

    Every diagram ships as an image *and* as a table of the same data. The image is the
    overview; the table is what actually works on a phone, in a screen reader, and under
    ctrl-F. Both come from the graph, so they cannot disagree with each other.
    """
    vid = view["id"]
    out = [f"## {view['title']}", ""]
    caption = " ".join((view.get("caption") or "").split())
    if caption:
        out += [caption, ""]

    # GitHub honours prefers-color-scheme in <picture>, in the web UI and the mobile apps.
    out += [
        "<picture>",
        f'  <source media="(prefers-color-scheme: dark)" srcset="diagrams/{vid}-dark.svg">',
        f'  <img alt="Prerequisite graph — {view["title"]}" src="diagrams/{vid}-light.svg">',
        "</picture>",
        "",
    ]

    legend = ["**Thick border** = written."]
    if boundary:
        legend.append("Dashed = prerequisite from another area, shared by two or more topics here.")
    legend.append(f"{len(ordered)} topics, {edge_count} edges drawn.")
    legend.append(f"[Mermaid source](diagrams/{vid}.mmd)")
    out += [" · ".join(legend), ""]

    out += [
        "<details>",
        "<summary>Every prerequisite as a table — complete, searchable, and readable on a phone</summary>",
        "",
        "| Topic | Level | Requires (all hard prerequisites) |",
        "|---|---|---|",
    ]
    for topic in ordered:
        node = nodes[topic]
        name = f"**`{topic}`**" if node["status"] == "published" else f"`{topic}`"
        reqs = [f"`{p}`" for p in sorted(nodes[topic]["hard"])]
        out.append(f"| {name} | {node['level']} | {', '.join(reqs) if reqs else '—'} |")
    out += ["", "</details>", ""]

    notes = (view.get("notes") or "").strip()
    if notes:
        out += [notes, ""]

    return "\n".join(out)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def svg_stamp(path: Path) -> str | None:
    """Read the source checksum render_diagrams.sh stamped into an SVG."""
    if not path.is_file():
        return None
    match = re.search(r"<!--\s*mmd-sha256:([0-9a-f]+)\s*-->", path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="verify committed output matches the graph")
    args = parser.parse_args()

    nodes = load_graph()
    spec = yaml.safe_load(VIEWS_FILE.read_text(encoding="utf-8"))
    if spec.get("schema") != "diagrams/v1":
        sys.exit(f"{VIEWS_FILE.name}: schema must be 'diagrams/v1'")
    default_boundary = (spec.get("defaults") or {}).get("boundary", "none")

    DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)
    generated: dict[str, str] = {}
    errors: list[str] = []
    sections: list[str] = []

    for view in spec["views"]:
        ordered, boundary = resolve_view(view, nodes, default_boundary)
        text = render_mmd(view, nodes, ordered, boundary)
        sha = digest(text)
        generated[view["id"]] = sha
        edge_count = sum(1 for line in text.splitlines() if " --> " in line)
        sections.append(render_markdown(view, nodes, ordered, boundary, edge_count))
        target = DIAGRAM_DIR / f"{view['id']}.mmd"

        if args.check:
            current = target.read_text(encoding="utf-8") if target.is_file() else None
            if current != text:
                errors.append(
                    f"{target.relative_to(ROOT)} is stale — run: python3 tools/generate_diagrams.py"
                )
                continue
            for variant in ("light", "dark"):
                svg = DIAGRAM_DIR / f"{view['id']}-{variant}.svg"
                stamped = svg_stamp(svg)
                if stamped is None:
                    errors.append(f"{svg.relative_to(ROOT)} is missing or unstamped — run: tools/render_diagrams.sh")
                elif stamped != sha:
                    errors.append(
                        f"{svg.relative_to(ROOT)} was rendered from an older source "
                        f"({stamped} != {sha}) — run: tools/render_diagrams.sh"
                    )
        else:
            target.write_text(text, encoding="utf-8")
            print(f"  {target.relative_to(ROOT)}  ({len(ordered)} nodes, {len(boundary)} boundary)")

    manifest = "\n".join(
        ["schema: diagrams-manifest/v1", "# Generated. Checksums of the .mmd sources, for the CI staleness check.", "sources:"]
        + [f"  {vid}: {sha}" for vid, sha in generated.items()]
    ) + "\n"

    region = "\n".join(sections).rstrip() + "\n"
    map_text = MAP_FILE.read_text(encoding="utf-8")
    if BEGIN_MARKER not in map_text or END_MARKER not in map_text:
        sys.exit(f"{MAP_FILE.relative_to(ROOT)} is missing the {BEGIN_MARKER} / {END_MARKER} markers")
    head, rest = map_text.split(BEGIN_MARKER, 1)
    _, tail = rest.split(END_MARKER, 1)
    updated = f"{head}{BEGIN_MARKER}\n\n{region}\n{END_MARKER}{tail}"

    if args.check:
        current = MANIFEST.read_text(encoding="utf-8") if MANIFEST.is_file() else None
        if current != manifest:
            errors.append(f"{MANIFEST.relative_to(ROOT)} is stale — run: python3 tools/generate_diagrams.py")
        if map_text != updated:
            errors.append(
                f"{MAP_FILE.relative_to(ROOT)}: the generated region is stale — "
                "run: python3 tools/generate_diagrams.py"
            )
        if errors:
            print(f"{len(errors)} error(s):")
            for error in errors:
                print(f"  x {error}")
            return 1
        print(f"OK: {len(generated)} diagrams are current with the graph.")
        return 0

    MANIFEST.write_text(manifest, encoding="utf-8")
    print(f"  {MANIFEST.relative_to(ROOT)}")
    MAP_FILE.write_text(updated, encoding="utf-8")
    print(f"  {MAP_FILE.relative_to(ROOT)}  (generated region: {len(sections)} sections)")
    print(f"\nWrote {len(generated)} diagram sources. Now run: tools/render_diagrams.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
