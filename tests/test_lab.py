import argparse
import copy
import csv
import importlib.util
import json
import math
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import lab
import metric_examples as metrics
import audit_source_counts


class CatalogContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'schemas', self.root / 'schemas')
        for folder in ['catalog/discovery', 'catalog/curated', 'catalog/sources', 'competitions']:
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        self.registry = lab.read(ROOT / 'catalog/sources/registry.json')
        # Minimal fixture uses real records and source bytes, so checksum corruption is tested too.
        self.sample = copy.deepcopy(lab.read(ROOT / 'catalog/curated/dd-tick-tick-bloom.json'))
        needed = set(self.sample['source_ids'])
        needed.update(self.sample['identity']['source_ids'])
        needed.update(self.sample['task']['source_ids'])
        for fact in self.sample['availability'].values():
            needed.update(fact['source_ids'])
        for criterion in self.sample['curation']['rating']['criteria'].values():
            needed.update(criterion['source_ids'])
        self.registry = [s for s in self.registry if s['id'] in needed]
        for s in self.registry:
            if s['status'] == 'retrieved':
                dest = self.root / s['snapshot']
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / s['snapshot'], dest)
        self.write_registry()
        report = self.root / self.sample['research']['report_path']
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text('# Fixture')
        self.write_sample()

    def tearDown(self):
        self.temp.cleanup()

    def write_registry(self):
        (self.root / 'catalog/sources/registry.json').write_text(json.dumps(self.registry))

    def write_sample(self):
        path = self.root / 'catalog/curated' / (self.sample['id'] + '.json')
        path.write_text(json.dumps(self.sample))

    def test_valid_record(self):
        self.assertEqual(lab.validate(self.root), [])

    def test_unknown_score_never_becomes_zero(self):
        rating = self.sample['curation']['rating']
        rating['criteria']['dataset_access']['points'] = None
        rating['total'], rating['tier'] = None, 'UNRATED'
        self.write_sample()
        self.assertEqual(lab.validate(self.root), [])
        rating['total'] = 0
        self.write_sample()
        self.assertTrue(any('total/tier' in e for e in lab.validate(self.root)))

    def test_missing_evidence_and_tampered_snapshot(self):
        self.sample['availability']['code']['source_ids'] = ['invented']
        self.write_sample()
        self.assertTrue(any('unknown source' in e for e in lab.validate(self.root)))
        source = next(s for s in self.registry if s['status'] == 'retrieved')
        (self.root / source['snapshot']).write_bytes(b'changed')
        self.assertTrue(any('hash mismatch' in e for e in lab.validate(self.root)))

    def test_track_identity_and_duplicate_detection(self):
        other = copy.deepcopy(self.sample)
        other['id'] = 'second-track'
        other['identity']['track'] = 'track-2'
        (self.root / 'catalog/curated/second-track.json').write_text(json.dumps(other))
        self.assertEqual(lab.validate(self.root), [])
        other['identity']['track'] = self.sample['identity']['track']
        (self.root / 'catalog/curated/second-track.json').write_text(json.dumps(other))
        self.assertTrue(any('duplicate identity' in e for e in lab.validate(self.root)))

    def test_schema_rejects_ambiguous_false_and_unknown_keys(self):
        self.sample['availability']['data']['value'] = False
        self.sample['uncontrolled_schema_extension'] = 'no migration'
        self.write_sample()
        self.assertGreaterEqual(len(lab.validate(self.root)), 2)

    def test_exports_preserve_nulls_and_json(self):
        self.sample['curation']['rating']['criteria']['dataset_access']['points'] = None
        self.sample['curation']['rating']['total'] = None
        self.sample['curation']['rating']['tier'] = 'UNRATED'
        self.write_sample()
        self.assertEqual(lab.build(self.root), 1)
        with (self.root / 'catalog/indexes/competitions.csv').open() as f:
            row = next(csv.DictReader(f))
        self.assertEqual(row['score'], '')
        with sqlite3.connect(self.root / 'catalog/indexes/catalog.sqlite') as db:
            score, full = db.execute('SELECT score, record_json FROM competitions').fetchone()
        self.assertIsNone(score)
        self.assertEqual(json.loads(full)['source_ids'], self.sample['source_ids'])

    def test_snapshot_path_cannot_escape(self):
        with self.assertRaises(ValueError):
            lab.safe_path(self.root, '../secret')

    def test_verified_claim_requires_locator_and_retrieved_source(self):
        folder = self.root / 'competitions' / self.sample['id']
        claim = {'id': 'test-claim', 'claim': 'Claim without a locator', 'status': 'VERIFIED',
                 'scope': 'code', 'source_ids': ['not-a-source'], 'locator': None,
                 'limitations': 'Fixture', 'assumptions': [], 'test': None, 'artifact': None}
        (folder / 'evidence.json').write_text(json.dumps([claim]))
        errors = lab.validate(self.root)
        self.assertTrue(any('unknown source' in e for e in errors))
        self.assertTrue(any('needs source and locator' in e for e in errors))

    def test_inference_claim_requires_assumptions_and_falsification(self):
        folder = self.root / 'competitions' / self.sample['id']
        claim = {'id': 'test-hypothesis', 'claim': 'An untested proposed mechanism', 'status': 'INFERRED',
                 'scope': 'reasoning', 'source_ids': [], 'locator': None,
                 'limitations': 'Fixture', 'assumptions': [], 'test': None, 'artifact': None}
        (folder / 'evidence.json').write_text(json.dumps([claim]))
        self.assertTrue(any('needs assumptions and test' in e for e in lab.validate(self.root)))

    def test_complete_state_cannot_hide_blocked_measurements(self):
        folder = self.root / 'competitions' / self.sample['id']
        state = lab.read(ROOT / 'competitions' / self.sample['id'] / 'state.json')
        state['artifacts'] = ['report.md']
        state['overall_status'] = 'complete'
        (folder / 'state.json').write_text(json.dumps(state))
        self.assertTrue(any('complete state has unresolved' in e for e in lab.validate(self.root)))
        state['overall_status'] = 'partial'
        (folder / 'state.json').write_text(json.dumps(state))
        self.assertEqual(lab.validate(self.root), [])


class MetricSemanticsTests(unittest.TestCase):
    def test_static_counts_match_reported_dimensions(self):
        counts = audit_source_counts.audit()
        self.assertEqual(counts['sweep_configurations'], 96)
        self.assertEqual(counts['landsat_features'], 88)
        self.assertEqual(counts['sentinel_features'], 67)

    def test_horizon_aggregation_denominator(self):
        self.assertAlmostEqual(metrics.examples()['cold_same_10pct_relative_error_three_windows'], 7.2 / 33)

    def test_macro_regions_not_pooled(self):
        results = metrics.examples()
        self.assertEqual(results['bloom_macro_region_rmse'], 1.5)
        self.assertEqual(results['bloom_pooled_rmse'], 1.0)

    def test_auc_ties_and_strict_monotonic_invariance(self):
        result = metrics.examples()
        self.assertEqual(result['auc_tie_half_credit'], .5)
        self.assertEqual(result['auc_before_monotonic_transform'], result['auc_after_monotonic_transform'])
        with self.assertRaises(ValueError):
            metrics.binary_auc([0, 0], [.1, .2])


if __name__ == '__main__':
    unittest.main()
