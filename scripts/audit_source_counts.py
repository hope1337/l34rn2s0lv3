#!/usr/bin/env python3
"""Check reported code-list dimensions using AST only; never execute source code."""
import ast
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit():
    registry = {s['id']: s for s in json.loads((ROOT / 'catalog/sources/registry.json').read_text())}
    tree = ast.parse((ROOT / registry['hate-detail-2']['snapshot']).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.For))
    sizes = []
    while isinstance(node, ast.For):
        sizes.append(len(ast.literal_eval(node.iter)))
        nested = [n for n in node.body if isinstance(n, ast.For)]
        node = nested[0] if nested else None
    source = ast.parse((ROOT / registry['bloom-file-9']['snapshot']).read_text())
    lengths = {}
    for node in source.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.List):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ['landsat_bands', 'sentinel_bands', 'meta_features', 'lsat_vis', 'snel_vis']:
                    lengths[target.id] = len(ast.literal_eval(node.value))
    return {
        'scope': 'Static AST/list arithmetic, not an executed ML experiment',
        'sweep_axis_sizes': sizes,
        'sweep_configurations': math.prod(sizes),
        'landsat_features': lengths['landsat_bands'] * 4 + lengths['meta_features'] + lengths['lsat_vis'] + 2 * 3,
        'sentinel_features': lengths['sentinel_bands'] * 4 + lengths['meta_features'] + lengths['snel_vis'],
    }


if __name__ == '__main__':
    result = audit()
    (ROOT / 'docs/static_source_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
