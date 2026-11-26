# SPDX-License-Identifier: MIT
"""Real-Life Patch Notes: The Comedy Changelog — entry writer (Akun 2).

Writes exactly one line (117 characters, no trailing newline) to
<out_dir>/entry.txt, where <out_dir> comes from MAKEFUN_OUTPUT_DIR
(default /output). Pure Python standard library only.
"""

import hashlib
import os

ENTRY = (
    "Changelog 6.1.0: the bug where users forget why they entered "
    "a room is fixed. They now remember it in the other room."
)

EXPECTED_SHA256 = (
    "2025d6157dd857c8600416de1869b437a8a5e4f5b8d336a311906a2f488ee0cf"
)


def main():
    text = ENTRY
    assert 1 <= len(text) <= 160, "entry must be 1-160 characters"
    assert "\n" not in text and "\r" not in text, "entry must be one line"
    assert text.strip() == text and text.strip(), "entry must not be blank"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert digest == EXPECTED_SHA256, "entry sha256 mismatch: %s" % digest
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
