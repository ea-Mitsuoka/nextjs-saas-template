import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DependencyOverridesTest(unittest.TestCase):
    def test_brace_expansion_override_includes_security_fix(self) -> None:
        package = json.loads((ROOT / "package.json").read_text())
        version = package["pnpm"]["overrides"].get("brace-expansion")

        self.assertIsNotNone(version)
        self.assertGreaterEqual(
            tuple(int(part) for part in version.split(".")),
            (5, 0, 9),
        )

    def test_nanoid_override_includes_security_fixes(self) -> None:
        package = json.loads((ROOT / "package.json").read_text())
        version = package["pnpm"]["overrides"].get("nanoid")

        self.assertIsNotNone(version)
        self.assertGreaterEqual(
            tuple(int(part) for part in version.split(".")),
            (3, 3, 18),
        )

    def test_sharp_override_includes_libheif_fixes(self) -> None:
        # GHSA-rgj7-g3m4-5g8c (HIGH): libheif vulnerabilities bundled by sharp < 0.35.4.
        package = json.loads((ROOT / "package.json").read_text())
        version = package["pnpm"]["overrides"].get("sharp")

        self.assertIsNotNone(version)
        self.assertGreaterEqual(
            tuple(int(part) for part in version.split(".")),
            (0, 35, 4),
        )

    def test_next_range_starts_at_rce_fix(self) -> None:
        # CVE-2026-75604 (CRITICAL): unauthenticated RCE in Next.js < 15.5.24.
        package = json.loads((ROOT / "package.json").read_text())
        spec = package["dependencies"]["next"]
        minimum = spec.lstrip("^~")

        self.assertGreaterEqual(
            tuple(int(part) for part in minimum.split(".")),
            (15, 5, 24),
        )

    def test_postcss_override_includes_security_fix(self) -> None:
        package = json.loads((ROOT / "package.json").read_text())
        version = package["pnpm"]["overrides"].get("postcss")

        self.assertIsNotNone(version)
        self.assertGreaterEqual(
            tuple(int(part) for part in version.split(".")),
            (8, 5, 23),
        )


if __name__ == "__main__":
    unittest.main()
