#!/usr/bin/env python3
"""Build a deterministic installable ZIP and SHA-256 checksum."""

from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "comfortable-ones-act-up"
SKILL_DIR = ROOT / SKILL_NAME
VERSION_FILE = ROOT / "VERSION"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="Override the version from VERSION")
    parser.add_argument("--output-dir", default="dist")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    version = args.version or VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise SystemExit(f"invalid semantic version: {version}")
    if not (SKILL_DIR / "SKILL.md").is_file():
        raise SystemExit(f"missing skill entrypoint: {SKILL_DIR / 'SKILL.md'}")

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{SKILL_NAME}-v{version}.zip"

    with zipfile.ZipFile(archive, "w") as bundle:
        for path in sorted(SKILL_DIR.rglob("*")):
            if not path.is_file() or path.name == ".DS_Store":
                continue
            relative = path.relative_to(SKILL_DIR)
            archive_name = str(Path(SKILL_NAME) / relative)
            info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes(), compresslevel=9)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(".zip.sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")

    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        required = f"{SKILL_NAME}/SKILL.md"
        if required not in names or any(not name.startswith(f"{SKILL_NAME}/") for name in names):
            raise SystemExit("archive layout validation failed")

    print(archive)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
