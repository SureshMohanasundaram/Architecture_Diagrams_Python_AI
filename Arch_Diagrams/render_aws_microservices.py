"""Render the AWS microservices DOT file to an image.

This script attempts to use the Python `graphviz` package to render
the DOT file `Arch_Diagrams/diagrams/aws_microservices.dot` to PNG.

Usage:
  python render_aws_microservices.py

Requirements:
  - Install Graphviz (system package) and ensure `dot` is on PATH
    https://graphviz.org/download/
  - Install Python package: `pip install graphviz`
"""
from pathlib import Path
import sys

DOT_PATH = Path(__file__).parent / "diagrams" / "aws_microservices.dot"


def render(dot_path: Path, out_format: str = "png") -> None:
    if not dot_path.exists():
        print(f"DOT file not found: {dot_path}")
        return

    try:
        from graphviz import Source
    except Exception as e:
        print("Missing Python dependency `graphviz` or import failed:", e)
        print("Install with: pip install graphviz")
        return

    src = dot_path.read_text(encoding="utf-8")
    s = Source(src)
    out_dir = dot_path.parent
    try:
        output_path = s.render(filename=dot_path.stem, directory=out_dir, format=out_format, cleanup=True)
        print(f"Rendered diagram: {output_path}")
    except Exception as e:
        print("Rendering failed:", e)
        print("Ensure Graphviz (dot) is installed and available on PATH:")
        print("  https://graphviz.org/download/")


if __name__ == "__main__":
    fmt = "png"
    if len(sys.argv) > 1:
        fmt = sys.argv[1]
    render(DOT_PATH, out_format=fmt)
