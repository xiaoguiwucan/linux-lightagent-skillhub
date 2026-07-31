import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "ian-xiaohei-illustrations"
SKILL_PATH = SKILL_ROOT / "SKILL.md"


def load_skill():
    text = SKILL_PATH.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    return yaml.safe_load(frontmatter), body


class IanXiaoheiIllustrationsContractTest(unittest.TestCase):
    def test_linux_lightagent_metadata_uses_safe_native_tool(self):
        metadata, body = load_skill()
        self.assertEqual("ian-xiaohei-illustrations", metadata["name"])
        self.assertEqual(2, metadata["schema_version"])
        self.assertEqual("1.0.0", metadata["version"])
        self.assertEqual("MIT", metadata["license"])
        self.assertEqual(["read", "image_generate"], metadata["lightagent"]["tools"])
        self.assertEqual("restricted", metadata["lightagent"]["wechat_group"]["access"])
        self.assertEqual(
            "stable-room-or-member",
            metadata["lightagent"]["wechat_group"]["authorization_scope"],
        )
        self.assertIn("一次请求只调用一次 `image_generate`", body)
        self.assertNotIn("内置 `image_gen`", body)

    def test_license_attribution_and_reference_assets_are_packaged(self):
        license_text = (SKILL_ROOT / "LICENSE").read_text(encoding="utf-8")
        notice = (SKILL_ROOT / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 Ian", license_text)
        self.assertIn("GitHub: <https://github.com/helloianneo>", notice)
        examples = list((SKILL_ROOT / "assets" / "examples").glob("*.png"))
        self.assertEqual(14, len(examples))

    def test_skill_does_not_bundle_executable_scripts_or_dependencies(self):
        metadata, _ = load_skill()
        self.assertFalse((SKILL_ROOT / "scripts").exists())
        self.assertEqual([], metadata["lightagent"]["entrypoints"])
        self.assertEqual([], metadata["requirements"]["env"])
        self.assertEqual([], metadata["requirements"]["python"])
        self.assertEqual([], metadata["requirements"]["npm"])


if __name__ == "__main__":
    unittest.main()
