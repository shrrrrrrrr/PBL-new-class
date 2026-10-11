#!/usr/bin/env python3
"""Read-only checks for bundled references or a new course asset manifest."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote
try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python -m pip install Pillow")

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
errors: list[str] = []
checked = 0

def fail(message: str) -> None:
    errors.append(message)

def local(base: Path, name: str, boundary: Path) -> Path | None:
    if not isinstance(name, str) or not name:
        fail("Missing asset path")
        return None
    result = (base / unquote(name)).resolve()
    if not result.is_relative_to(boundary.resolve()):
        fail(f"Path escapes asset root: {name}")
        return None
    if not result.is_file():
        fail(f"File not found: {name}")
        return None
    return result

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_image(path: Path, expected: dict, label: str, candidate: bool = False) -> None:
    global checked
    checked += 1
    digest = expected.get("sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        fail(f"{label}: fill a real SHA256")
    elif sha(path) != digest:
        fail(f"{label}: SHA256 mismatch")
    try:
        with Image.open(path) as im:
            im.load()
            width, height = im.size
            if (width, height) != (expected.get("width"), expected.get("height")):
                fail(f"{label}: dimensions are {width}x{height}, not declared size")
            alpha = list(im.getchannel("A").getextrema()) if "A" in im.getbands() else None
            if candidate:
                if expected.get("alphaRequired") is True and (alpha is None or alpha[0] != 0 or alpha[1] != 255):
                    fail(f"{label}: needs fully transparent outside and opaque artwork")
            elif alpha != expected.get("alphaExtrema"):
                fail(f"{label}: alpha extrema changed")
            if "bytes" in expected and path.stat().st_size != expected["bytes"]:
                fail(f"{label}: byte count changed")
    except Exception as exc:
        fail(f"{label}: cannot decode image: {exc}")

def check_links() -> None:
    # Markdown local links, including preview/CSS/template links. No network requests.
    documents = [p for p in (REPO / "README.md", REPO / "ASSET-SOURCES.md") if p.is_file()] + [SKILL / "SKILL.md"]
    documents += list((SKILL / "references").glob("*.md"))
    for document in documents:
        if not document.is_file():
            fail(f"Missing document: {document.name}")
            continue
        content = document.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)\s]+)\)", content):
            if re.match(r"(?:https?://|mailto:|#)", target):
                continue
            local(document.parent, target.split("#")[0], REPO)
    preview = local(SKILL, "assets/preview.html", REPO)
    if preview:
        content = preview.read_text(encoding="utf-8")
        for target in re.findall(r'(?:src|href)="([^"]+)"', content):
            if not re.match(r"(?:https?://|#|data:)", target):
                local(preview.parent, target, REPO)
    css = local(SKILL, "assets/pbl-pixel.css", REPO)
    if css:
        for target in re.findall(r'url\(["\']?([^)"\']+)', css.read_text(encoding="utf-8")):
            local(css.parent, target, REPO)
    source = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not source.startswith("---\n") or "name: pbl-pixel-course" not in source:
        fail("SKILL.md needs valid skill metadata")
    for template in ("course-brief.json", "asset-manifest.example.json"):
        path = local(SKILL, "assets/templates/" + template, REPO)
        if path:
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                fail(f"{template}: invalid JSON: {exc}")

def bundled() -> None:
    manifest = json.loads((SKILL / "assets/reference-manifest.json").read_text(encoding="utf-8"))
    ids: set[str] = set()
    for item in manifest["assets"]:
        label = item["id"]
        if label in ids:
            fail(f"Duplicate reference id: {label}")
        ids.add(label)
        path = local(SKILL, item["path"], SKILL)
        if path:
            check_image(path, item, label)
    font = manifest["font"]
    path = local(SKILL, font["path"], SKILL)
    if path and sha(path) != font["sha256"]:
        fail("Font SHA256 mismatch")
    license_path = local(SKILL, font["license"], SKILL)
    if license_path and "SIL OPEN FONT LICENSE" not in license_path.read_text(encoding="utf-8").upper():
        fail("Missing SIL Open Font License text")
    check_links()

def candidate(manifest_path: Path) -> None:
    manifest_path = manifest_path.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("styleVersion") != "1.0.0":
        fail("Unsupported styleVersion; verify the style baseline")
    known = {a["id"] for a in json.loads((SKILL / "assets/reference-manifest.json").read_text(encoding="utf-8"))["assets"]}
    ids: set[str] = set()
    for asset in data.get("assets", []):
        label = asset.get("id", "(unnamed)")
        if not asset.get("id") or label in ids:
            fail(f"Missing or duplicate asset id: {label}")
        ids.add(label)
        references = asset.get("referenceIds", [])
        if not references or any(ref not in known for ref in references):
            fail(f"{label}: declare existing referenceIds")
        generation = asset.get("generation", {})
        if not generation.get("tool") or not generation.get("prompt"):
            fail(f"{label}: record actual tool and prompt; model may be null")
        files = asset.get("files", [])
        if not files:
            fail(f"{label}: no files declared")
        ratios = set()
        for item in files:
            path = local(manifest_path.parent, item.get("path"), manifest_path.parent)
            if path:
                check_image(path, item, label + "/" + item["path"], candidate=True)
            width, height = item.get("width"), item.get("height")
            if not isinstance(width, int) or not isinstance(height, int) or min(width, height) <= 0:
                fail(f"{label}: dimensions must be positive integers")
            else:
                ratios.add(round(width / height, 3))
        if len(ratios) > 1:
            fail(f"{label}: variants change aspect ratio; list distinct compositions as separate assets")
        anchor = asset.get("landingAnchor")
        if anchor is not None and not all(isinstance(anchor.get(k), (int, float)) and 0 <= anchor[k] <= 1 for k in ("x", "y")):
            fail(f"{label}: landing anchor must use normalized x/y in [0,1]")
    if not ids:
        fail("Candidate manifest has no assets")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, help="Validate new assets; all paths relative to this manifest")
    args = parser.parse_args()
    try:
        candidate(args.candidate) if args.candidate else bundled()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        fail(f"Cannot read manifest: {exc}")
    print(json.dumps({"ok": not errors, "imagesChecked": checked, "errors": errors,
                      "manualReview": "Required: pixel style, thematic fit, baked text, layout and real UI behavior"}, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
