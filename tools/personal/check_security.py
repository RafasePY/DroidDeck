#!/usr/bin/env python3
"""Read-only checks for the experimental hardened DroidDeck profile."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
manifest = (ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
gradle = (ROOT / "app/build.gradle").read_text(encoding="utf-8")
for permission in (
    "ACCESS_COARSE_LOCATION",
    "ACCESS_FINE_LOCATION",
    "RECORD_AUDIO",
    "REQUEST_INSTALL_PACKAGES",
):
    assert "android.permission." + permission not in manifest, (
        f"Forbidden Android permission: {permission}"
    )
assert 'android:allowBackup="false"' in manifest
assert "signingConfig signingConfigs.personalRelease" in gradle
assert "personalSigningReady" in gradle
assert "'packageRelease'" in gradle and "'bundleRelease'" in gradle
release = re.search(
    r"(?m)^\s*release\s*\{(?P<body>[\s\S]*?)^\s*\}",
    gradle,
)
assert release, "No release buildType found"
assert "signingConfigs.testkey" not in release.group("body"), (
    "Public AOSP test key must not sign release builds"
)
print("PASS: personal permission and signing guard checks")
