# SPDX-License-Identifier: MIT
"""Real-Life Patch Notes: The Comedy Changelog - entry writer (Akun 2).

Writes exactly one line (117 characters, no trailing newline) to
<out_dir>/entry.txt, where <out_dir> comes from MAKEFUN_OUTPUT_DIR
(default /output). Pure Python standard library only.

Entry formula (winner family): version number + fix -> one specific
real-life bug -> irony -> twist in the final clause, flat tone.
"""

import hashlib
import os

MAX_CHARS = 160
EXPECTED_SHA256 = (
    "2025d6157dd857c8600416de1869b437a8a5e4f5b8d336a311906a2f488ee0cf"
)
EXPECTED_BYTES = 117


def build_entry():
    """Assemble the single-line entry from its fixed parts."""
    header = "Changelog 6.1.0:"
    bug = "the bug where users forget why they entered a room is fixed."
    twist = "They now remember it in the other room."
    return " ".join((header, bug, twist))


def validate_entry(text):
    """Strict checks: one line, bounty length cap, printable, exact hash."""
    if not isinstance(text, str):
        raise TypeError("entry must be str")
    if not text or text.strip() != text:
        raise ValueError("entry must be non-blank with no edge whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError("entry exceeds %d chars: %d" % (MAX_CHARS, len(text)))
    if "\n" in text or "\r" in text or "\t" in text:
        raise ValueError("entry must be a single line without control chars")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must contain only printable characters")
    if not text.startswith("Changelog "):
        raise ValueError("entry must open with a versioned changelog header")
    if not text.endswith("."):
        raise ValueError("entry must end with a period")
    raw = text.encode("utf-8")
    if len(raw) != EXPECTED_BYTES:
        raise ValueError("entry must be %d bytes, got %d" % (EXPECTED_BYTES, len(raw)))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("entry sha256 mismatch: %s" % digest)
    return text


def write_entry(text, out_dir):
    """Write the validated entry with no trailing newline, mode 0644."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(path, 0o644)
    return path


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    text = validate_entry(build_entry())
    write_entry(text, out_dir)


if __name__ == "__main__":
    main()
