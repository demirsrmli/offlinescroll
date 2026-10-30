#!/usr/bin/env python3
"""Read-only source/manifest audit. Run on a clean extracted share copy."""
from pathlib import Path
import argparse
import re
import sys
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument("root", nargs="?", default=".")
parser.add_argument("--manifest", type=Path)
args = parser.parse_args()
root = Path(args.root).resolve()
errors = []
files = []
for path in sorted(root.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(root)
    files.append(relative.as_posix())
    if any(part in {".git", ".gradle", ".idea", "build", "__pycache__"} for part in relative.parts):
        errors.append((relative, "private history, cache, or build directory"))
    if path.name in {"local.properties", "keystore.properties", ".env"} or path.suffix.lower() in {
        ".jks", ".keystore", ".p12", ".pfx", ".pem", ".key", ".apk", ".aab", ".hprof", ".log"
    }:
        errors.append((relative, "excluded local or generated file"))
    if path.is_symlink():
        errors.append((relative, "symlink is not allowed in source delivery"))
    if path.suffix.lower() in {".png", ".jar"}:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeError, OSError):
        errors.append((relative, "unexpected binary file"))
        continue
    patterns = [r"gh[pousr]_[A-Za-z0-9]{30,}", r"github_pat_[A-Za-z0-9_]{30,}",
                r"AKIA[0-9A-Z]{16}", r"AIza[0-9A-Za-z_-]{30,}",
                r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
                r"(?:/" + r"Us" + r"ers/|C:\\Us" + r"ers\\|/ho" + r"me/)[^\s/\\]+"]
    if any(re.search(pattern, text) for pattern in patterns):
        errors.append((relative, "possible credential or personal path; value withheld"))

if args.manifest:
    android = "{http://schemas.android.com/apk/res/android}"
    manifest = ET.parse(args.manifest).getroot()
    permissions = {node.attrib.get(android + "name", "") for node in manifest.findall("uses-permission")}
    forbidden = {"android.permission.INTERNET", "android.permission.ACCESS_NETWORK_STATE",
                 "android.permission.WAKE_LOCK", "android.permission.WRITE_EXTERNAL_STORAGE",
                 "android.permission.FOREGROUND_SERVICE", "android.permission.ACCESS_WIFI_STATE"}
    for permission in permissions & forbidden:
        errors.append(("merged manifest", "forbidden permission " + permission))
    sdk = manifest.find("uses-sdk")
    if sdk is None or int(sdk.attrib.get(android + "targetSdkVersion", "0")) < 36:
        errors.append(("merged manifest", "target SDK is below 36"))
    application = manifest.find("application")
    if application is None or application.attrib.get(android + "allowBackup") != "false":
        errors.append(("merged manifest", "backup is not disabled"))
    print("Merged manifest permissions:", ", ".join(sorted(permissions)))

for path, kind in errors:
    print(str(path) + ": " + kind)
print(f"Audited {len(files)} files; {len(errors)} findings. Pattern scanning is not a proof of absence.")
sys.exit(bool(errors))
