import argparse
import json
from pathlib import Path
import tempfile
import unittest

from analyze import aggregate
from large_run import make_plan, simulation_identity
from run import select_points


class LargeRunTest(unittest.TestCase):
    def test_full_coverage_includes_rounded_weight_tail(self):
        points = {'a': '0.6', 'b': '0.4', 'c': '0.000001'}
        selected, _ = select_points(points, coverage=1)
        self.assertEqual([point for point, _ in selected], ['a', 'b', 'c'])
        self.assertEqual(len(select_points(points, coverage=.8)[0]), 2)
        self.assertEqual(len(select_points(points, top=1)[0]), 1)

    def test_cycle_weighted_capacity_fraction(self):
        rows = [dict(workload='test', variant='baseline', weight=.75, cpi=1,
                     regfull_cycles=0, instructions=100, demand_stall_cycles=0,
                     standalone_stall_cycles=0),
                dict(workload='test', variant='baseline', weight=.25, cpi=2,
                     regfull_cycles=100, instructions=100, demand_stall_cycles=100,
                     standalone_stall_cycles=100)]
        row = aggregate(rows)[0]
        self.assertAlmostEqual(row['weighted_cpi'], 1.25)
        self.assertAlmostEqual(row['weighted_demand_stall_fraction'], .2)
        self.assertAlmostEqual(row['weighted_standalone_stall_fraction'], .2)

    def test_plan_and_resume_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cpts = root / 'checkpoints'
            for point in ('1', '2'):
                directory = cpts / 'test' / point
                directory.mkdir(parents=True)
                (directory / 'checkpoint.zstd').touch()
            (cpts / 'cluster-0-0.json').write_text(json.dumps({
                'test': {'points': {'1': '.7', '2': '.3'}}}))
            binary = root / 'gem5.opt'
            binary.write_bytes(b'fake binary')
            reference = root / 'reference.so'
            reference.write_bytes(b'fake ref')
            config = dict(profile='threshold', repo='repo', gem5='gem5.opt',
                          checkpoints='checkpoints', out='output', coverage=.8,
                          warmup=1000, measure=2000, jobs=2, timeout=300,
                          reference=str(reference), difftest=True, trace=False,
                          profiles={'threshold': [['baseline', 224, 256],
                                                  ['int192', 192, 256]]})
            args = argparse.Namespace(profile=None, out=None, warmup=None,
                                      measure=None, jobs=None, timeout=None,
                                      coverage=None, top=None, workloads=None,
                                      trace=False)
            plan = make_plan(config, root, args)
            self.assertEqual(plan['selected_slices'], 2)
            self.assertEqual(plan['total_runs'], 4)
            self.assertFalse((root / 'output').exists())
            self.assertIn('--no-trace', plan['command'])
            identity = simulation_identity(plan)
            args.jobs = 8
            args.timeout = 900
            other = make_plan(config, root, args)
            self.assertEqual(identity, simulation_identity(other))
            args.measure = 3000
            other = make_plan(config, root, args)
            self.assertNotEqual(identity, simulation_identity(other))


if __name__ == '__main__':
    unittest.main()
