import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_registry import deterministic_zip  # noqa: E402
from common import parse_skill  # noqa: E402


class RegistryV2Test(unittest.TestCase):
    def test_active_skills_support_linux_release_candidate(self):
        for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
            metadata, _ = parse_skill(skill_md)
            if metadata.get("status", "active") == "active":
                with self.subTest(skill=metadata["name"]):
                    self.assertEqual(
                        "1.0.0-rc.1", metadata["min_lightagent_version"]
                    )

    def test_workflow_actions_are_pinned_to_commits(self):
        workflows = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        )
        references = re.findall(r"^\s*-?\s*uses:\s*[^@\s]+@([^\s#]+)", workflows, re.MULTILINE)

        self.assertTrue(references)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", item) for item in references))

    def test_v2_script_skill_declares_runner_entrypoint(self):
        metadata, text = parse_skill(ROOT / "skills" / "av-meta" / "SKILL.md")
        self.assertEqual(2, metadata["schema_version"])
        self.assertEqual("skill_run", metadata["lightagent"]["tools"][0])
        self.assertNotIn("```bash", text)
        entrypoint = metadata["lightagent"]["entrypoints"][0]
        self.assertEqual("scripts/fetch_meta.py", entrypoint["path"])
        self.assertTrue((ROOT / "skills" / "av-meta" / entrypoint["path"]).is_file())
        self.assertEqual(
            ["text", "attachments"],
            metadata["lightagent"]["output_contract"]["delivery_order"],
        )
        self.assertEqual(
            "stable-room-or-member",
            metadata["lightagent"]["wechat_group"]["authorization_scope"],
        )

    def test_deterministic_package_contains_runner_metadata(self):
        package = deterministic_zip(ROOT / "skills" / "av-meta")
        self.assertGreater(len(package), 100)

    def test_schema_exposes_capabilities_and_change_notes(self):
        schema = json.loads((ROOT / "schemas" / "skill.schema.json").read_text(encoding="utf-8"))
        self.assertIn("release_notes", schema["properties"])
        self.assertIn("capabilities", schema["properties"]["requirements"]["properties"])
        self.assertIn("entrypoints", schema["properties"]["lightagent"]["properties"])
        self.assertIn("wechat_group", schema["properties"]["lightagent"]["properties"])
        self.assertIn("output_contract", schema["properties"]["lightagent"]["properties"])

    def test_schema_restricts_runner_environment_names(self):
        schema = json.loads((ROOT / "schemas" / "skill.schema.json").read_text(encoding="utf-8"))
        env_schema = schema["properties"]["requirements"]["properties"]["env"]
        self.assertTrue(env_schema["uniqueItems"])
        self.assertEqual("^[A-Z_][A-Z0-9_]{0,127}$", env_schema["items"]["pattern"])


if __name__ == "__main__":
    unittest.main()
