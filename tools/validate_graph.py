#!/usr/bin/env python3
"""Validate the learning graph against docs/graph-schema.md.

Architecture that is not enforced is a suggestion. This script is the
enforcement. It runs in CI on every pull request.

Checks, in order:

  registry   unique ids, known domain, valid level/status, dir presence rules,
             prerequisites only on planned nodes
  topics     topic.yml agrees with its registry entry; required fields present;
             the nine standard files exist and none is a placeholder
  graph      all references resolve; hard-prerequisite graph is acyclic; hard
             prerequisites never exceed the level of the topic requiring them
  projects   required fields; topic references resolve
  paths      step references resolve; a step's hard prerequisites appear earlier
             in the path, in a prerequisite path, or below the path's entry level
  resources  tier1 and tier2 non-empty; every entry has a why; no duplicate URLs
  links      relative markdown links resolve to files that exist

No network access. External URLs are checked by a separate scheduled job so a
temporarily unreachable site cannot block a pull request.

Usage:
    python3 tools/validate_graph.py [--stats] [--no-links] [--quiet]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent

ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

STATUSES = {"published", "drafting", "planned"}
DEPTHS = {"aware", "working", "deep"}
GATE_KINDS = {"build", "break", "debug", "explain", "benchmark", "review", "design", "research"}
MANDATORY_GATES = {"build", "explain"}
VERSION_SENSITIVITY = {"low", "medium", "high"}
TIERS = ("tier1", "tier2", "tier3")

TOPIC_FILES = [
    "README.md",
    "fundamentals.md",
    "concepts.md",
    "practical.md",
    "exercises.md",
    "projects.md",
    "interview.md",
    "advanced.md",
    "resources.md",
]

# A file shorter than this, or containing one of the placeholder markers, is
# treated as an empty stub. See docs/architecture.md section 9.
MIN_FILE_CHARS = 400
PLACEHOLDER_MARKERS = ("todo", "tbd", "coming soon", "work in progress", "wip", "fixme")

REGISTRY_KEYS = {"schema", "domain", "topics"}
REGISTRY_TOPIC_KEYS = {"id", "title", "level", "status", "summary", "dir", "prerequisites"}
TOPIC_KEYS = {
    "schema", "id", "title", "domain", "level", "status", "summary", "why_it_matters",
    "effort", "prerequisites", "first_principles_chain", "concepts", "gates", "projects",
    "resources", "next", "version_sensitivity", "last_reviewed", "maintainers",
}
TOPIC_REQUIRED = TOPIC_KEYS - {"projects"}
PROJECT_KEYS = {
    "schema", "id", "title", "level", "summary", "validates", "topics", "constraints",
    "stages", "break_it", "anti_patterns", "stretch",
}
PROJECT_REQUIRED = PROJECT_KEYS - {"stretch"}
PATH_KEYS = {
    "schema", "id", "title", "audience", "entry_level", "exit_level",
    "prerequisite_paths", "steps",
}
PATH_REQUIRED = PATH_KEYS - {"prerequisite_paths"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def load_yaml(path: Path, report: Report) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(rel(path), f"unreadable ({exc})")
        return None
    if "\t" in text:
        report.error(rel(path), "contains a tab character; YAML indentation must use spaces")
    for banned, why in (("&", "anchor"), ("*", "alias")):
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith(("#",)):
                continue
            if re.search(rf"(?<=:\s){re.escape(banned)}\w", line):
                report.error(rel(path), f"line {lineno}: YAML {why} not allowed by the schema subset")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        report.error(rel(path), f"invalid YAML ({exc})")
        return None
    if not isinstance(data, dict):
        report.error(rel(path), "top level must be a mapping")
        return None
    for location in suspicious_keys(data, ""):
        report.error(
            rel(path),
            f"{location} looks like prose that YAML parsed as a mapping, because it "
            'contains ": ". Quote the whole value.',
        )
    return data


def suspicious_keys(node: object, path: str) -> list[str]:
    """Find mapping keys that are almost certainly accidental colon-in-scalar.

    A prose sentence containing ": " silently becomes a single-key mapping. It is the
    most common authoring mistake in this schema, and the resulting downstream error
    ("must be a list of strings") does not point at the cause.
    """
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(key, str) and (" " in key or len(key) > 48):
                found.append(f"{path or '(root)'} key {key[:60]!r}")
            found.extend(suspicious_keys(value, f"{path}/{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(suspicious_keys(value, f"{path}[{index}]"))
    return found


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check_keys(where: str, data: dict, allowed: set[str], required: set[str], report: Report) -> None:
    for key in sorted(set(data) - allowed):
        report.error(where, f"unknown key '{key}' (add it to docs/graph-schema.md and the validator first)")
    for key in sorted(required - set(data)):
        report.error(where, f"missing required key '{key}'")


def nonempty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def prereq_ids(prereqs: object) -> list[tuple[str, str]]:
    """Return (kind, id) pairs from a prerequisites block, tolerating both forms.

    Registry entries for planned nodes use bare id lists; topic.yml uses
    {id, why} mappings. Both are normalised here.
    """
    out: list[tuple[str, str]] = []
    if not isinstance(prereqs, dict):
        return out
    for kind in ("hard", "soft"):
        items = prereqs.get(kind) or []
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, str):
                out.append((kind, item))
            elif isinstance(item, dict) and isinstance(item.get("id"), str):
                out.append((kind, item["id"]))
    return out


# --------------------------------------------------------------------------- load

def load_registries(report: Report) -> tuple[dict, dict, dict]:
    domains_data = load_yaml(ROOT / "graph" / "domains.yml", report) or {}
    domains = {}
    for entry in domains_data.get("domains") or []:
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            domains[entry["id"]] = entry

    levels_data = load_yaml(ROOT / "graph" / "levels.yml", report) or {}
    levels = {}
    for entry in levels_data.get("levels") or []:
        if isinstance(entry, dict) and isinstance(entry.get("id"), int):
            levels[entry["id"]] = entry

    nodes: dict[str, dict] = {}
    registry_dir = ROOT / "graph" / "registry"
    files = sorted(registry_dir.glob("*.yml"))
    if not files:
        report.error("graph/registry", "no registry files found")

    for path in files:
        where = rel(path)
        data = load_yaml(path, report)
        if data is None:
            continue
        check_keys(where, data, REGISTRY_KEYS, REGISTRY_KEYS, report)
        if data.get("schema") != "registry/v1":
            report.error(where, f"schema must be 'registry/v1', got {data.get('schema')!r}")
        domain = data.get("domain")
        if domain != path.stem:
            report.error(where, f"domain '{domain}' does not match filename '{path.stem}'")
        if domain not in domains:
            report.error(where, f"domain '{domain}' is not declared in graph/domains.yml")

        topics = data.get("topics")
        if not isinstance(topics, list):
            report.error(where, "'topics' must be a list")
            continue

        for entry in topics:
            if not isinstance(entry, dict):
                report.error(where, "each topic entry must be a mapping")
                continue
            tid = entry.get("id")
            ewhere = f"{where} [{tid}]"
            check_keys(ewhere, entry, REGISTRY_TOPIC_KEYS, {"id", "title", "level", "status", "summary"}, report)
            if not isinstance(tid, str) or not ID_RE.match(tid):
                report.error(ewhere, f"invalid id {tid!r}")
                continue
            if tid in nodes:
                report.error(ewhere, f"duplicate id (also in {nodes[tid]['_file']})")
                continue
            if entry.get("level") not in levels:
                report.error(ewhere, f"level {entry.get('level')!r} is not declared in graph/levels.yml")
            if entry.get("status") not in STATUSES:
                report.error(ewhere, f"status {entry.get('status')!r} not in {sorted(STATUSES)}")
            if not nonempty_str(entry.get("summary")):
                report.error(ewhere, "summary must be a non-empty string")
            entry["_file"] = where
            entry["_domain"] = domain
            nodes[tid] = entry

    return domains, levels, nodes


def check_registry_dirs(nodes: dict, report: Report) -> None:
    for tid, node in sorted(nodes.items()):
        where = f"{node['_file']} [{tid}]"
        status = node.get("status")
        directory = node.get("dir")

        if status in ("published", "drafting"):
            if not directory:
                report.error(where, f"status '{status}' requires 'dir'")
                continue
            path = ROOT / directory
            if not path.is_dir():
                report.error(where, f"dir '{directory}' does not exist")
            elif not (path / "topic.yml").is_file():
                report.error(where, f"dir '{directory}' has no topic.yml")
            expected = f"topics/{node['_domain']}/{tid}"
            if directory != expected:
                report.error(where, f"dir should be '{expected}' (one level per domain, no nesting)")
            if "prerequisites" in node:
                report.error(
                    where,
                    "prerequisites must live in topic.yml for published/drafting nodes, "
                    "not in the registry (single source of truth)",
                )
        else:  # planned
            if directory:
                report.error(where, "status 'planned' must not declare 'dir'")
            path = ROOT / "topics" / node["_domain"] / tid
            if path.exists():
                report.error(
                    where,
                    f"status 'planned' but {rel(path)} exists; promote the node to 'drafting' "
                    "or delete the directory (no empty stubs)",
                )


# -------------------------------------------------------------------------- topics

def load_topics(nodes: dict, domains: dict, levels: dict, report: Report) -> dict[str, dict]:
    topics: dict[str, dict] = {}
    for tid, node in sorted(nodes.items()):
        if node.get("status") not in ("published", "drafting"):
            continue
        directory = node.get("dir")
        if not directory:
            continue
        path = ROOT / directory / "topic.yml"
        if not path.is_file():
            continue
        where = rel(path)
        data = load_yaml(path, report)
        if data is None:
            continue
        check_keys(where, data, TOPIC_KEYS, TOPIC_REQUIRED, report)

        if data.get("schema") != "topic/v1":
            report.error(where, f"schema must be 'topic/v1', got {data.get('schema')!r}")
        for field in ("id", "title", "level", "status"):
            if data.get(field) != node.get(field):
                report.error(
                    where,
                    f"{field} is {data.get(field)!r} but the registry says {node.get(field)!r}",
                )
        if data.get("domain") != node.get("_domain"):
            report.error(
                where,
                f"domain is {data.get('domain')!r} but the topic is registered under "
                f"{node.get('_domain')!r}",
            )
        if data.get("domain") not in domains:
            report.error(where, f"unknown domain {data.get('domain')!r}")
        if data.get("level") not in levels:
            report.error(where, f"unknown level {data.get('level')!r}")

        for field in ("summary", "why_it_matters"):
            if not nonempty_str(data.get(field)):
                report.error(where, f"'{field}' must be a non-empty string")

        effort = data.get("effort")
        if not isinstance(effort, dict):
            report.error(where, "'effort' must be a mapping")
        else:
            if not isinstance(effort.get("focused_hours"), int):
                report.error(where, "effort.focused_hours must be an integer")
            for field in ("calendar_weeks", "assumes"):
                if not nonempty_str(effort.get(field)):
                    report.error(where, f"effort.{field} must be a non-empty string")

        chain = data.get("first_principles_chain")
        if not isinstance(chain, list) or len(chain) < 3:
            report.error(where, "first_principles_chain must be a list of at least 3 steps")
        elif not all(nonempty_str(step) for step in chain):
            report.error(where, "every first_principles_chain step must be a non-empty string")

        concepts = data.get("concepts")
        if not isinstance(concepts, list) or not concepts:
            report.error(where, "'concepts' must be a non-empty list")
        else:
            seen: set[str] = set()
            depths: list[str] = []
            for concept in concepts:
                if not isinstance(concept, dict):
                    report.error(where, "each concept must be a mapping")
                    continue
                cid = concept.get("id")
                if not isinstance(cid, str) or not ID_RE.match(cid):
                    report.error(where, f"invalid concept id {cid!r}")
                elif cid in seen:
                    report.error(where, f"duplicate concept id '{cid}'")
                else:
                    seen.add(cid)
                if not nonempty_str(concept.get("name")):
                    report.error(where, f"concept '{cid}' needs a name")
                if not nonempty_str(concept.get("note")):
                    report.error(where, f"concept '{cid}' needs a note saying what to take from it")
                depth = concept.get("depth")
                if depth not in DEPTHS:
                    report.error(where, f"concept '{cid}' depth {depth!r} not in {sorted(DEPTHS)}")
                else:
                    depths.append(depth)
            if depths and len(set(depths)) == 1 and depths[0] == "deep" and len(depths) > 3:
                report.error(
                    where,
                    "every concept is marked 'deep'; the topic has not answered "
                    "'how deeply should I learn it?' (see docs/graph-schema.md)",
                )

        gates = data.get("gates")
        if not isinstance(gates, dict) or not gates:
            report.error(where, "'gates' must be a non-empty mapping")
        else:
            for kind, items in gates.items():
                if kind not in GATE_KINDS:
                    report.error(where, f"unknown gate kind '{kind}', expected one of {sorted(GATE_KINDS)}")
                if not isinstance(items, list) or not items or not all(nonempty_str(i) for i in items):
                    report.error(where, f"gate '{kind}' must be a non-empty list of strings")
            for kind in sorted(MANDATORY_GATES - set(gates)):
                report.error(where, f"missing mandatory gate '{kind}'")

        nxt = data.get("next")
        if not isinstance(nxt, list) or not nxt:
            report.error(where, "'next' must be a non-empty list")
        else:
            for item in nxt:
                if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                    report.error(where, "each 'next' entry needs an id")
                elif not nonempty_str(item.get("why")):
                    report.error(where, f"next '{item.get('id')}' needs a 'why'")

        if data.get("version_sensitivity") not in VERSION_SENSITIVITY:
            report.error(
                where,
                f"version_sensitivity {data.get('version_sensitivity')!r} not in {sorted(VERSION_SENSITIVITY)}",
            )
        reviewed = data.get("last_reviewed")
        if not isinstance(reviewed, str) or not DATE_RE.match(str(reviewed)):
            report.error(where, "last_reviewed must be a YYYY-MM-DD string (quote it in YAML)")
        if not isinstance(data.get("maintainers"), list):
            report.error(where, "'maintainers' must be a list (may be empty)")

        check_resources(where, data.get("resources"), report)

        if node.get("status") == "published":
            check_topic_files(ROOT / directory, report)

        data["_file"] = where
        topics[tid] = data
    return topics


def check_resources(where: str, resources: object, report: Report) -> None:
    if not isinstance(resources, dict):
        report.error(where, "'resources' must be a mapping with tier1/tier2/tier3")
        return
    for key in sorted(set(resources) - set(TIERS)):
        report.error(where, f"unknown resource tier '{key}'")
    urls: dict[str, str] = {}
    for tier in TIERS:
        items = resources.get(tier) or []
        if not isinstance(items, list):
            report.error(where, f"resources.{tier} must be a list")
            continue
        if tier in ("tier1", "tier2") and not items:
            report.error(where, f"resources.{tier} must have at least one entry (see docs/resource-tiers.md)")
        if tier == "tier3" and len(items) > 5:
            report.error(where, "resources.tier3 is capped at 5 entries; prefer fewer excellent resources")
        for item in items:
            if not isinstance(item, dict):
                report.error(where, f"each resources.{tier} entry must be a mapping")
                continue
            for field in ("title", "url", "why"):
                if not nonempty_str(item.get(field)):
                    report.error(where, f"resources.{tier} entry '{item.get('title')}' needs '{field}'")
            url = item.get("url")
            if isinstance(url, str):
                if not url.startswith(("http://", "https://")):
                    report.error(where, f"resource url must be absolute: {url!r}")
                if url in urls:
                    report.error(where, f"duplicate resource url {url!r} (also in {urls[url]})")
                else:
                    urls[url] = tier


def check_topic_files(directory: Path, report: Report) -> None:
    where = rel(directory)
    for name in TOPIC_FILES:
        path = directory / name
        if not path.is_file():
            report.error(where, f"published topic is missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        body = text.strip()
        if len(body) < MIN_FILE_CHARS:
            report.error(
                f"{where}/{name}",
                f"only {len(body)} characters; a file may be short but not a placeholder "
                "(see docs/architecture.md section 9)",
            )
        lowered = body.lower()
        for marker in PLACEHOLDER_MARKERS:
            if re.search(rf"(^|[^a-z]){re.escape(marker)}([^a-z]|$)", lowered):
                report.error(f"{where}/{name}", f"contains placeholder marker '{marker}'")
                break
        if not body.startswith("# "):
            report.error(f"{where}/{name}", "must start with a single level-1 heading")
    for path in sorted(directory.iterdir()):
        if path.is_file() and path.name not in TOPIC_FILES and path.name != "topic.yml":
            report.error(where, f"unexpected file '{path.name}'; the topic file set is fixed")


# ------------------------------------------------------------------------ projects

def load_projects(nodes: dict, levels: dict, report: Report) -> dict[str, dict]:
    projects: dict[str, dict] = {}
    projects_dir = ROOT / "projects"
    if not projects_dir.is_dir():
        report.error("projects", "directory is missing")
        return projects

    for path in sorted(projects_dir.glob("*/project.yml")):
        where = rel(path)
        data = load_yaml(path, report)
        if data is None:
            continue
        check_keys(where, data, PROJECT_KEYS, PROJECT_REQUIRED, report)
        if data.get("schema") != "project/v1":
            report.error(where, f"schema must be 'project/v1', got {data.get('schema')!r}")
        pid = data.get("id")
        if not isinstance(pid, str) or not ID_RE.match(pid):
            report.error(where, f"invalid id {pid!r}")
            continue
        if pid != path.parent.name:
            report.error(where, f"id '{pid}' does not match directory '{path.parent.name}'")
        if pid in projects:
            report.error(where, f"duplicate project id '{pid}'")
            continue
        if data.get("level") not in levels:
            report.error(where, f"unknown level {data.get('level')!r}")
        for field in ("title", "summary"):
            if not nonempty_str(data.get(field)):
                report.error(where, f"'{field}' must be a non-empty string")
        for field in ("validates", "constraints", "break_it", "anti_patterns"):
            items = data.get(field)
            if not isinstance(items, list) or not items or not all(nonempty_str(i) for i in items):
                report.error(where, f"'{field}' must be a non-empty list of strings")
        topic_refs = data.get("topics")
        if not isinstance(topic_refs, list) or not topic_refs:
            report.error(where, "'topics' must be a non-empty list of topic ids")
        else:
            for ref in topic_refs:
                if ref not in nodes:
                    report.error(where, f"topics references unknown topic '{ref}'")
        stages = data.get("stages")
        if not isinstance(stages, list) or len(stages) < 2:
            report.error(where, "'stages' must have at least 2 entries")
        else:
            for stage in stages:
                if not isinstance(stage, dict):
                    report.error(where, "each stage must be a mapping")
                    continue
                for field in ("name", "goal"):
                    if not nonempty_str(stage.get(field)):
                        report.error(where, f"stage '{stage.get('name')}' needs '{field}'")
                done = stage.get("done_when")
                if not isinstance(done, list) or not done or not all(nonempty_str(d) for d in done):
                    report.error(where, f"stage '{stage.get('name')}' needs a non-empty done_when list")
        readme = path.parent / "README.md"
        if not readme.is_file():
            report.error(where, "project is missing README.md with the full specification")
        data["_file"] = where
        projects[pid] = data
    return projects


# --------------------------------------------------------------------------- graph

def check_graph(nodes: dict, topics: dict, projects: dict, report: Report) -> dict[str, set[str]]:
    """Resolve every edge, enforce level monotonicity, and detect cycles."""
    hard_edges: dict[str, set[str]] = defaultdict(set)

    for tid, node in sorted(nodes.items()):
        topic = topics.get(tid)
        source = topic if topic is not None else node
        where = source.get("_file", node["_file"]) + f" [{tid}]"
        prereqs = source.get("prerequisites")

        if topic is not None and not isinstance(prereqs, dict):
            report.error(where, "'prerequisites' must be a mapping with hard and/or soft")
            prereqs = {}

        if isinstance(prereqs, dict):
            for key in sorted(set(prereqs) - {"hard", "soft"}):
                report.error(where, f"unknown prerequisites key '{key}'")

        for kind, pid in prereq_ids(prereqs):
            if pid not in nodes:
                report.error(where, f"{kind} prerequisite '{pid}' does not exist in the registry")
                continue
            if pid == tid:
                report.error(where, "topic lists itself as a prerequisite")
                continue
            if kind == "hard":
                hard_edges[tid].add(pid)
                plevel, tlevel = nodes[pid].get("level"), node.get("level")
                if isinstance(plevel, int) and isinstance(tlevel, int) and plevel > tlevel:
                    report.error(
                        where,
                        f"hard prerequisite '{pid}' is level {plevel} but this topic is level "
                        f"{tlevel}; a prerequisite cannot be more advanced than what it unlocks",
                    )

        # topic.yml prerequisites must carry a 'why'
        if topic is not None and isinstance(prereqs, dict):
            for kind in ("hard", "soft"):
                for item in prereqs.get(kind) or []:
                    if isinstance(item, dict) and not nonempty_str(item.get("why")):
                        report.error(where, f"{kind} prerequisite '{item.get('id')}' needs a 'why'")
                    elif isinstance(item, str):
                        report.error(
                            where,
                            f"{kind} prerequisite '{item}' must be a mapping with id and why in topic.yml",
                        )

    for tid, topic in sorted(topics.items()):
        where = topic["_file"]
        hard = hard_edges.get(tid, set())
        for item in topic.get("next") or []:
            if not isinstance(item, dict):
                continue
            nid = item.get("id")
            if nid not in nodes:
                report.error(where, f"next references unknown topic '{nid}'")
            elif nid in hard:
                report.error(where, f"'{nid}' is both a hard prerequisite and a 'next' step")
            elif nid == tid:
                report.error(where, "topic lists itself in 'next'")
        for item in topic.get("projects") or []:
            if not isinstance(item, dict):
                report.error(where, "each projects entry must be a mapping")
                continue
            pid = item.get("id")
            if pid not in projects:
                report.error(where, f"projects references unknown project '{pid}'")
            role = item.get("role")
            if role not in ("core", "stretch"):
                report.error(where, f"project '{pid}' role {role!r} must be 'core' or 'stretch'")
            for cid in item.get("validates") or []:
                known = {c.get("id") for c in topic.get("concepts") or [] if isinstance(c, dict)}
                if cid not in known:
                    report.error(where, f"project '{pid}' validates unknown concept '{cid}'")

    for cycle in find_cycles(hard_edges):
        report.error("graph", "hard prerequisite cycle: " + " -> ".join(cycle))

    return hard_edges


def find_cycles(edges: dict[str, set[str]]) -> list[list[str]]:
    """Return one representative cycle per strongly connected component."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour: dict[str, int] = defaultdict(int)
    cycles: list[list[str]] = []

    def visit(node: str, stack: list[str]) -> None:
        colour[node] = GREY
        stack.append(node)
        for nxt in sorted(edges.get(node, ())):
            if colour[nxt] == GREY:
                cycles.append(stack[stack.index(nxt):] + [nxt])
            elif colour[nxt] == WHITE:
                visit(nxt, stack)
        stack.pop()
        colour[node] = BLACK

    for node in sorted(edges):
        if colour[node] == WHITE:
            visit(node, [])
    return cycles


def transitive_prereqs(tid: str, hard_edges: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    stack = list(hard_edges.get(tid, ()))
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(hard_edges.get(current, ()))
    return seen


# ---------------------------------------------------------------------------- paths

def load_paths(nodes: dict, projects: dict, levels: dict, report: Report) -> dict[str, dict]:
    paths: dict[str, dict] = {}
    files = sorted((ROOT / "paths").glob("*.yml")) + sorted((ROOT / "paths" / "stacks").glob("*.yml"))
    if not files:
        report.error("paths", "no path files found")

    for path in files:
        where = rel(path)
        data = load_yaml(path, report)
        if data is None:
            continue
        check_keys(where, data, PATH_KEYS, PATH_REQUIRED, report)
        if data.get("schema") != "path/v1":
            report.error(where, f"schema must be 'path/v1', got {data.get('schema')!r}")
        pid = data.get("id")
        if not isinstance(pid, str) or not ID_RE.match(pid):
            report.error(where, f"invalid id {pid!r}")
            continue
        if pid != path.stem:
            report.error(where, f"id '{pid}' does not match filename '{path.stem}'")
        if pid in paths:
            report.error(where, f"duplicate path id '{pid}'")
            continue
        if not (path.parent / f"{pid}.md").is_file():
            report.error(where, f"missing companion narrative {pid}.md")
        if not nonempty_str(data.get("title")) or not nonempty_str(data.get("audience")):
            report.error(where, "'title' and 'audience' must be non-empty strings")
        entry, exit_ = data.get("entry_level"), data.get("exit_level")
        for name, value in (("entry_level", entry), ("exit_level", exit_)):
            if value not in levels:
                report.error(where, f"{name} {value!r} is not a declared level")
        if isinstance(entry, int) and isinstance(exit_, int) and exit_ <= entry:
            report.error(where, "exit_level must be greater than entry_level")
        data["_file"] = where
        paths[pid] = data

    for pid, data in sorted(paths.items()):
        where = data["_file"]
        for ref in data.get("prerequisite_paths") or []:
            if ref not in paths:
                report.error(where, f"prerequisite_paths references unknown path '{ref}'")
            elif ref == pid:
                report.error(where, "path lists itself as a prerequisite path")

        steps = data.get("steps")
        if not isinstance(steps, list) or not steps:
            report.error(where, "'steps' must be a non-empty list")
            continue
        if not any(isinstance(s, dict) and "milestone" in s for s in steps):
            report.error(where, "a path must contain at least one milestone")
        seen: set[str] = set()
        for index, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                report.error(where, f"step {index} must be a mapping")
                continue
            if "milestone" in step:
                if set(step) != {"milestone"}:
                    report.error(where, f"step {index}: a milestone carries only 'milestone'")
                elif not nonempty_str(step.get("milestone")):
                    report.error(where, f"step {index}: milestone must be a non-empty string")
                continue
            for key in sorted(set(step) - {"topic", "emphasis", "projects"}):
                report.error(where, f"step {index}: unknown key '{key}'")
            tid = step.get("topic")
            if not isinstance(tid, str):
                report.error(where, f"step {index} needs 'topic' or 'milestone'")
                continue
            if tid not in nodes:
                report.error(where, f"step {index} references unknown topic '{tid}'")
                continue
            if tid in seen:
                report.error(where, f"step {index}: topic '{tid}' appears twice in this path")
            seen.add(tid)
            for ref in step.get("projects") or []:
                if ref not in projects:
                    report.error(where, f"step {index} ('{tid}') references unknown project '{ref}'")
    return paths


def check_path_ordering(paths: dict, nodes: dict, hard_edges: dict[str, set[str]], report: Report) -> None:
    """A step's hard prerequisites must be reachable before it.

    Satisfied when the prerequisite appears earlier in this path, appears in a
    transitively-included prerequisite path, or sits strictly below the path's
    entry level (in which case the path assumes it).
    """
    def covered_by_prereq_paths(pid: str, seen: set[str] | None = None) -> set[str]:
        seen = seen or set()
        if pid in seen or pid not in paths:
            return set()
        seen.add(pid)
        out: set[str] = set()
        for step in paths[pid].get("steps") or []:
            if isinstance(step, dict) and isinstance(step.get("topic"), str):
                out.add(step["topic"])
        for parent in paths[pid].get("prerequisite_paths") or []:
            out |= covered_by_prereq_paths(parent, seen)
        return out

    for pid, data in sorted(paths.items()):
        where = data["_file"]
        entry = data.get("entry_level")
        if not isinstance(entry, int):
            continue
        assumed = set()
        for parent in data.get("prerequisite_paths") or []:
            assumed |= covered_by_prereq_paths(parent)
        earlier: set[str] = set()
        for step in data.get("steps") or []:
            if not isinstance(step, dict) or not isinstance(step.get("topic"), str):
                continue
            tid = step["topic"]
            if tid not in nodes:
                continue
            for prereq in sorted(hard_edges.get(tid, ())):
                level = nodes.get(prereq, {}).get("level")
                if prereq in earlier or prereq in assumed:
                    continue
                if isinstance(level, int) and level < entry:
                    continue
                report.error(
                    where,
                    f"step '{tid}' has hard prerequisite '{prereq}' (level {level}) that the path "
                    "never covers and that is not below its entry level; add it earlier, list a "
                    "prerequisite_path that covers it, or lower entry_level",
                )
            earlier.add(tid)


# ---------------------------------------------------------------------------- links

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def check_links(report: Report) -> int:
    checked = 0
    skip_dirs = {".git", "node_modules"}
    # Files under these directories are copied elsewhere before use, so their relative links
    # are written for the DESTINATION depth (topics/<domain>/<id>/, projects/<id>/, paths/)
    # and deliberately do not resolve from where the template lives. templates/README.md and
    # templates/resource-list.md are not copied, so they stay checked.
    template_dirs = (
        ROOT / "templates" / "topic",
        ROOT / "templates" / "project",
        ROOT / "templates" / "path",
    )
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in skip_dirs for part in path.parts):
            continue
        if any(path.is_relative_to(d) for d in template_dirs):
            continue
        raw = path.read_text(encoding="utf-8")
        text = strip_code_blocks(raw)
        anchors = {slugify(line) for line in text.splitlines() if line.startswith("#")}
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            if target.startswith("#"):
                if slugify_anchor(target[1:]) not in anchors:
                    report.warn(rel(path), f"anchor '{target}' not found in this file")
                continue
            file_part, _, anchor = target.partition("#")
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            if not resolved.exists():
                report.error(rel(path), f"broken relative link '{target}'")
                continue
            if anchor and resolved.suffix == ".md":
                other = strip_code_blocks(resolved.read_text(encoding="utf-8"))
                other_anchors = {slugify(line) for line in other.splitlines() if line.startswith("#")}
                if slugify_anchor(anchor) not in other_anchors:
                    report.warn(rel(path), f"anchor '#{anchor}' not found in {file_part}")
    return checked


def strip_code_blocks(text: str) -> str:
    """Blank out fenced code blocks so examples are not treated as real links."""
    out, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def slugify(heading: str) -> str:
    return slugify_anchor(heading.lstrip("#").strip())


def slugify_anchor(text: str) -> str:
    """Approximate GitHub's heading-anchor algorithm.

    Lowercase, drop characters that are not alphanumeric/space/hyphen, then map each
    remaining space to a single hyphen. Spaces are mapped individually rather than
    collapsed, because GitHub does the same: "A -> B" becomes "a--b".
    """
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"\s", "-", text).strip("-")


# ----------------------------------------------------------------------------- main

def print_stats(nodes: dict, topics: dict, projects: dict, paths: dict, hard_edges: dict) -> None:
    by_level: dict[int, int] = defaultdict(int)
    by_status: dict[str, int] = defaultdict(int)
    by_domain: dict[str, int] = defaultdict(int)
    for node in nodes.values():
        by_level[node.get("level")] += 1
        by_status[node.get("status")] += 1
        by_domain[node.get("_domain")] += 1

    print("\nGraph statistics")
    print(f"  topics           {len(nodes)}")
    for status in ("published", "drafting", "planned"):
        print(f"    {status:<14} {by_status.get(status, 0)}")
    print("  by level")
    for level in sorted(k for k in by_level if k is not None):
        print(f"    level {level}        {by_level[level]}")
    print("  by domain")
    for domain in sorted(by_domain):
        print(f"    {domain:<20} {by_domain[domain]}")
    print(f"  hard edges       {sum(len(v) for v in hard_edges.values())}")
    print(f"  projects         {len(projects)}")
    print(f"  paths            {len(paths)}")

    roots = sorted(t for t in nodes if not hard_edges.get(t))
    print(f"  entry points     {len(roots)}: {', '.join(roots[:8])}" + (" ..." if len(roots) > 8 else ""))
    depth = {t: len(transitive_prereqs(t, hard_edges)) for t in nodes}
    deepest = sorted(depth.items(), key=lambda kv: -kv[1])[:5]
    print("  deepest topics (transitive hard prerequisites)")
    for tid, count in deepest:
        print(f"    {tid:<38} {count}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stats", action="store_true", help="print graph statistics")
    parser.add_argument("--no-links", action="store_true", help="skip relative markdown link checking")
    parser.add_argument("--quiet", action="store_true", help="only print errors")
    args = parser.parse_args()

    report = Report()
    domains, levels, nodes = load_registries(report)
    check_registry_dirs(nodes, report)
    topics = load_topics(nodes, domains, levels, report)
    projects = load_projects(nodes, levels, report)
    hard_edges = check_graph(nodes, topics, projects, report)
    paths = load_paths(nodes, projects, levels, report)
    check_path_ordering(paths, nodes, hard_edges, report)

    links = 0 if args.no_links else check_links(report)

    if report.warnings and not args.quiet:
        print(f"{len(report.warnings)} warning(s):")
        for warning in report.warnings:
            print(f"  ! {warning}")

    if report.errors:
        print(f"\n{len(report.errors)} error(s):")
        for error in report.errors:
            print(f"  x {error}")
        return 1

    if not args.quiet:
        print(
            f"OK: {len(nodes)} topics ({sum(1 for n in nodes.values() if n.get('status') == 'published')} "
            f"published), {len(projects)} projects, {len(paths)} paths, {links} relative links checked."
        )
    if args.stats:
        print_stats(nodes, topics, projects, paths, hard_edges)
    return 0


if __name__ == "__main__":
    sys.exit(main())
