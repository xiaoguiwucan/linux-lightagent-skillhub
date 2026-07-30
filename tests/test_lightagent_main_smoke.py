import tempfile
import unittest
from pathlib import Path

from scripts.lightagent_main_smoke import validate_compatibility


ROOT = Path(__file__).resolve().parents[1]


class LightAgentCompatibilitySmokeTest(unittest.TestCase):
    def _lightagent_fixture(self, version):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        (root / "cli").mkdir()
        (root / "cli" / "VERSION").write_text(f"{version}\n", encoding="utf-8")
        parser_dir = root / "agent" / "skills"
        parser_dir.mkdir(parents=True)
        parser_dir.joinpath("types.py").write_text("", encoding="utf-8")
        parser_dir.joinpath("frontmatter.py").write_text(
            "import yaml\n\ndef parse_frontmatter(text):\n"
            "    return yaml.safe_load(text.split('---', 2)[1])\n",
            encoding="utf-8",
        )
        return temp_dir, root

    def test_current_release_candidate_supports_all_active_skills(self):
        fixture, lightagent_root = self._lightagent_fixture("1.0.0-rc.1")
        self.addCleanup(fixture.cleanup)

        version, total, active = validate_compatibility(ROOT, lightagent_root)

        self.assertEqual("1.0.0rc1", str(version))
        self.assertEqual(5, total)
        self.assertEqual(5, active)

    def test_older_release_candidate_is_rejected(self):
        fixture, lightagent_root = self._lightagent_fixture("1.0.0-rc.0")
        self.addCleanup(fixture.cleanup)

        with self.assertRaisesRegex(SystemExit, "需要 Linux LightAgent"):
            validate_compatibility(ROOT, lightagent_root)


if __name__ == "__main__":
    unittest.main()
