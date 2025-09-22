from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import ast


def _parse_scalar(value: str):
    value = value.strip()
    if not value:
        return value
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if value.startswith('[') or value.startswith('{'):
            return ast.literal_eval(value)
    except Exception:
        pass
    try:
        if '.' in value or 'e' in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        return value


def _parse_lines(lines, start=0, indent=0):
    result = {}
    seq = []
    i = start
    is_seq = False
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            i += 1
            continue
        stripped = raw.lstrip()
        current_indent = len(raw) - len(stripped)
        if current_indent < indent:
            break
        if stripped.startswith('- '):
            is_seq = True
            item_text = stripped[2:].strip()
            if item_text:
                seq.append(_parse_scalar(item_text))
            else:
                nested, new_index = _parse_lines(lines, i + 1, current_indent + 2)
                seq.append(nested)
                i = new_index - 1
        else:
            if is_seq:
                break
            if ':' not in stripped:
                raise ValueError(f"Invalid line: {raw}")
            key, rest = stripped.split(':', 1)
            key = key.strip()
            rest = rest.strip()
            if rest:
                result[key] = _parse_scalar(rest)
            else:
                nested, new_index = _parse_lines(lines, i + 1, current_indent + 2)
                result[key] = nested
                i = new_index - 1
        i += 1
    return (seq if is_seq else result), i


def _simple_yaml_load(text: str):
    clean_lines: list[str] = []
    for line in text.splitlines():
        if line.strip().startswith('#'):
            continue
        clean_lines.append(line.rstrip("\n"))
    data, _ = _parse_lines(clean_lines, 0, 0)
    return data

@dataclass
class GeometryParameters:
    name: str
    lpp: float
    beam: float
    depth: float
    draft: float
    cb: float
    bulbous_bow_length: float = 0.0
    bulbous_bow_radius: float = 0.0
    sections: list[list[float]] | None = None

    @property
    def hash(self) -> str:
        payload = {
            "name": self.name,
            "lpp": self.lpp,
            "beam": self.beam,
            "depth": self.depth,
            "draft": self.draft,
            "cb": self.cb,
            "bulbous_bow_length": self.bulbous_bow_length,
            "bulbous_bow_radius": self.bulbous_bow_radius,
            "sections": self.sections or [],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def load_geometry_from_yaml(path: str | Path) -> GeometryParameters:
    with open(path, "r", encoding="utf-8") as handle:
        raw = handle.read()
    data: dict[str, Any] = _simple_yaml_load(raw)
    return GeometryParameters(
        name=data["name"],
        lpp=float(data["lpp"]),
        beam=float(data["beam"]),
        depth=float(data["depth"]),
        draft=float(data["draft"]),
        cb=float(data["cb"]),
        bulbous_bow_length=float(data.get("bulbous_bow", {}).get("length_ratio", 0.0)),
        bulbous_bow_radius=float(data.get("bulbous_bow", {}).get("radius_ratio", 0.0)),
        sections=data.get("sections"),
    )


def geometry_to_dict(params: GeometryParameters) -> dict[str, Any]:
    return {
        "name": params.name,
        "lpp": params.lpp,
        "beam": params.beam,
        "depth": params.depth,
        "draft": params.draft,
        "cb": params.cb,
        "bulbous_bow_length": params.bulbous_bow_length,
        "bulbous_bow_radius": params.bulbous_bow_radius,
        "sections": params.sections or [],
        "hash": params.hash,
    }
