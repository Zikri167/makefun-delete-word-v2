#!/usr/bin/env python3
"""make.fun entry: The Word You'd Delete From the Dictionary (v2).

Writes a single word to /output/entry.txt (or the first available output
directory from the documented fallback chain).

The word: "fine" -- the world's most common lie ("I'm fine") and also a
penalty (a parking fine). Delete it and both vanish at once.
"""

import os
import sys

WORD = "fine"


def resolve_output_dir():
    """Return the first usable output directory, in documented order."""
    candidates = []
    for env_name in ("OUTPUT_DIR", "_OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        value = os.environ.get(env_name)
        if value:
            candidates.append(value)
    candidates.extend(["/output", "./output", os.getcwd()])
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            probe = os.path.join(path, ".write_probe")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return path
        except OSError:
            continue
    raise OSError("no writable output directory found")


def validate_word(word):
    """Enforce the competition gate: one word, 1-77 chars, not blank.

    A single token means no whitespace anywhere (no spaces, tabs, or
    newlines inside the word) and no surrounding whitespace. Raises
    ValueError on any violation so a bad word can never be submitted.
    """
    if not isinstance(word, str):
        raise ValueError("word must be a string")
    if not word:
        raise ValueError("word must not be empty")
    if word != word.strip():
        raise ValueError("word must not have surrounding whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must be a single token (no whitespace)")
    if not 1 <= len(word) <= 77:
        raise ValueError("word must be 1-77 characters")
    word.encode("utf-8")  # must be valid UTF-8
    return word


def write_entry(out_dir, word):
    """Write `word` + newline to entry.txt inside out_dir; return path."""
    out_path = os.path.join(out_dir, "entry.txt")
    content = word + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    return out_path, content


def verify_entry(out_path, expected):
    """Read entry.txt back and confirm it is exactly `expected`."""
    with open(out_path, "r", encoding="utf-8", newline="") as fh:
        actual = fh.read()
    if actual != expected:
        raise ValueError(
            f"verification failed: {out_path!r} contains {actual!r}, "
            f"expected {expected!r}"
        )
    return actual


def main():
    word = validate_word(WORD)
    out_dir = resolve_output_dir()
    out_path, content = write_entry(out_dir, word)
    try:
        verify_entry(out_path, content)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {word!r} ({len(word)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
