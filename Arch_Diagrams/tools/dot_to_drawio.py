#!/usr/bin/env python3
"""Simple DOT -> draw.io generator using pydot.

This script parses a DOT file and produces a basic draw.io XML file with
rectangular nodes laid out on a grid and orthogonal edges. It intentionally
avoids `pygraphviz` and uses `pydot` which is pure Python.

Usage:
  python dot_to_drawio.py path/to/file.dot [out.drawio]

Limitations:
- Layout is generated with a simple grid (not Graphviz layout).
- Styles and shapes are basic; use the generated `.drawio` as a starting point
  for manual editing in diagrams.net.
"""
from __future__ import annotations
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
try:
    import pydot
except Exception as e:
    print("Missing dependency `pydot`. Install with: pip install pydot")
    raise


def parse_dot(dot_path: Path):
    graphs = pydot.graph_from_dot_file(str(dot_path))
    if not graphs:
        raise RuntimeError("No graph parsed from DOT file")
    return graphs[0]


def build_drawio_xml(nodes, edges, title="Diagram"):
    mxfile = ET.Element('mxfile', {'host': 'app.diagrams.net'})
    diagram = ET.SubElement(mxfile, 'diagram', {'name': title, 'id': 'gen-' + title.replace(' ', '-')})
    # We'll embed the mxGraphModel as CDATA
    model = ET.Element('mxGraphModel', {
        'dx': '1294', 'dy': '768', 'grid': '1', 'gridSize': '10', 'guides': '1',
        'tooltips': '1', 'connect': '1', 'arrows': '1', 'fold': '1', 'page': '1',
        'pageScale': '1', 'pageWidth': '850', 'pageHeight': '1100'
    })
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})

    # Add node cells
    id_map = {}
    cols = 4
    x0, y0 = 20, 20
    w, h = 160, 60
    spacing_x, spacing_y = 200, 120
    for i, n in enumerate(nodes):
        nid = f'n{i+1}'
        id_map[n.get_name()] = nid
        label = n.get_attributes().get('label') or n.get_name()
        cell = ET.SubElement(root, 'mxCell', {
            'id': nid,
            'value': label.strip('"'),
            'style': 'rounded=1;whiteSpace=wrap;html=1;fillColor=#e6f7ff;strokeColor=#2b6cb0;',
            'vertex': '1',
            'parent': '1'
        })
        col = i % cols
        row = i // cols
        geom = ET.SubElement(cell, 'mxGeometry', {
            'x': str(x0 + col * spacing_x),
            'y': str(y0 + row * spacing_y),
            'width': str(w),
            'height': str(h),
            'as': 'geometry'
        })

    # Add edge cells
    for i, e in enumerate(edges):
        src = e.get_source()
        dst = e.get_destination()
        # pydot may quote node names; strip quotes when mapping
        def norm(n):
            return n.strip('"')
        sname = norm(src)
        dname = norm(dst)
        sid = id_map.get(sname)
        did = id_map.get(dname)
        if not sid or not did:
            # skip edges referencing subgraphs or ports
            continue
        eid = f'e{i+1}'
        cell = ET.SubElement(root, 'mxCell', {
            'id': eid,
            'style': 'edgeStyle=orthogonalEdgeStyle;html=1;',
            'edge': '1',
            'parent': '1',
            'source': sid,
            'target': did
        })
        ET.SubElement(cell, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    # Serialize model to string and wrap in CDATA
    model_str = ET.tostring(model, encoding='utf-8').decode('utf-8')
    # xml.etree.ElementTree has no CDATA helper in the stdlib; embed manually
    diagram.text = '\n' + model_str + '\n'
    # Build final tree
    tree = ET.ElementTree(mxfile)
    return tree


def main(argv):
    if len(argv) < 2:
        print('Usage: python dot_to_drawio.py path/to/file.dot [out.drawio]')
        return 2
    dot_path = Path(argv[1])
    if not dot_path.exists():
        print('DOT file not found:', dot_path)
        return 2
    out_path = Path(argv[2]) if len(argv) >= 3 else dot_path.with_suffix('.drawio')
    graph = parse_dot(dot_path)
    # pydot returns strings or lists; get nodes and edges
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    tree = build_drawio_xml(nodes, edges, title=dot_path.stem)
    tree.write(out_path, encoding='utf-8', xml_declaration=True)
    print('Wrote draw.io file:', out_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
