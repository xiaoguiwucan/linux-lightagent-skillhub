#!/usr/bin/env python3
"""Verify Hub manifests against a Linux LightAgent source checkout."""

import argparse
import importlib.util
import sys
import types
from pathlib import Path

from packaging.version import InvalidVersion, Version


def _lightagent_parser(lightagent_root):
    agent_package = types.ModuleType("agent")
    agent_package.__path__ = [str(lightagent_root / "agent")]
    skills_package = types.ModuleType("agent.skills")
    skills_package.__path__ = [str(lightagent_root / "agent" / "skills")]
    sys.modules["agent"] = agent_package
    sys.modules["agent.skills"] = skills_package

    types_path = lightagent_root / "agent" / "skills" / "types.py"
    types_spec = importlib.util.spec_from_file_location("agent.skills.types", types_path)
    types_module = importlib.util.module_from_spec(types_spec)
    sys.modules["agent.skills.types"] = types_module
    types_spec.loader.exec_module(types_module)

    path = lightagent_root / "agent" / "skills" / "frontmatter.py"
    spec = importlib.util.spec_from_file_location("lightagent_frontmatter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_frontmatter


def validate_compatibility(hub_root, lightagent_root):
    parse_frontmatter = _lightagent_parser(lightagent_root)
    version_path = lightagent_root / "cli" / "VERSION"
    try:
        current_version = Version(version_path.read_text(encoding="utf-8").strip())
    except (OSError, InvalidVersion) as exc:
        raise SystemExit(f"无法读取 Linux LightAgent 版本: {exc}") from exc

    manifests = sorted((hub_root / "skills").glob("*/SKILL.md"))
    if not manifests:
        raise SystemExit("No Hub skills found")
    active_count = 0
    for manifest in manifests:
        metadata = parse_frontmatter(manifest.read_text(encoding="utf-8"))
        if metadata.get("name") != manifest.parent.name:
            raise SystemExit(f"{manifest}: LightAgent parsed a mismatched name")
        if metadata.get("status", "active") != "active":
            continue
        active_count += 1
        try:
            minimum = Version(str(metadata.get("min_lightagent_version")))
            maximum_raw = metadata.get("max_lightagent_version")
            maximum = Version(str(maximum_raw)) if maximum_raw is not None else None
        except InvalidVersion as exc:
            raise SystemExit(f"{manifest}: LightAgent 兼容版本无效: {exc}") from exc
        if current_version < minimum:
            raise SystemExit(
                f"{manifest}: 需要 Linux LightAgent >= {minimum}，当前为 {current_version}"
            )
        if maximum is not None and current_version > maximum:
            raise SystemExit(
                f"{manifest}: 仅支持 Linux LightAgent <= {maximum}，当前为 {current_version}"
            )
    return current_version, len(manifests), active_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-root", type=Path, default=Path("/hub"))
    parser.add_argument("--lightagent-root", type=Path, default=Path("/lightagent-main"))
    args = parser.parse_args()
    version, total, active = validate_compatibility(
        args.hub_root.resolve(), args.lightagent_root.resolve()
    )
    print(
        f"Linux LightAgent {version} compatibility passed: "
        f"{active} active / {total} total skills"
    )


if __name__ == "__main__":
    main()
