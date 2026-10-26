"""Builds the Subsidies+ docs page from template.html and icons.js.

index.html is the full page for GitHub Pages. With --fragment PATH the page is also written without the document
skeleton, as the Claude artifact publishes it (the artifact adds doctype, head and body itself).

Usage: python build.py [--fragment PATH]
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main():
    template = (HERE / "template.html").read_text(encoding="utf-8")
    icons = (HERE / "icons.js").read_text(encoding="utf-8").strip()
    assert template.count("/*ICONS*/") == 1, "template.html needs exactly one /*ICONS*/ marker"
    fragment = template.replace("/*ICONS*/", icons)

    # Everything up to the end of the style block goes into <head>, the rest into <body>.
    split = fragment.index("</style>") + len("</style>")
    head, body = fragment[:split], fragment[split:]
    page = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        "<style>body { margin: 0; } [hidden] { display: none !important; }</style>\n"
        f"{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )
    (HERE / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print("index.html", len(page))

    if "--fragment" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--fragment") + 1])
        out.write_text(fragment, encoding="utf-8", newline="\n")
        print(out.name, len(fragment))


if __name__ == "__main__":
    main()
