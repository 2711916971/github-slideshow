from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dsl import load_geometry_from_yaml
from .generators import GeometryGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate geometry artifacts from DSL")
    parser.add_argument("--dsl", required=True, help="Path to geometry YAML")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()
    params = load_geometry_from_yaml(args.dsl)
    generator = GeometryGenerator(args.out)
    metadata = generator.generate(params)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
