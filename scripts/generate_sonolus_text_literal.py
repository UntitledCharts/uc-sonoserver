"""
Generates the Text Literal type from the Sonolus i18n JSON.

Usage:
    python scripts/generate_sonolus_text_literal.py [output_path]

Fetches the Sonolus i18n Localization.json and writes the Text = Literal[...] block.
If output_path is given, writes to file. Otherwise prints to stdout.
"""

import json
import sys
import urllib.request


URL = "https://raw.githubusercontent.com/Sonolus/i18n/refs/heads/develop/src/localizations/en/Localization.json"


def main():
    with urllib.request.urlopen(URL) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    texts = data.get("Texts", {})
    keys = sorted(k for k in texts.keys() if k.startswith("#"))

    lines = [
        "# fmt: off",
        "# Auto-generated from Sonolus i18n — do not edit manually",
        "# https://github.com/Sonolus/i18n",
        "from typing import Literal",
        "",
        "Text = Literal[",
    ]
    for key in keys:
        lines.append(f'    "{key}",')
    lines.append("]")

    output = "\n".join(lines) + "\n"

    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Wrote {len(keys)} keys to {sys.argv[1]}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
