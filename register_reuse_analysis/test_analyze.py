#!/usr/bin/env python3
import tempfile
from pathlib import Path
import unittest
from analyze import stat_blocks, sweep, trace_metrics


class IntervalAccountingTest(unittest.TestCase):
    def test_overlapping_values_count_cycles_once(self):
        result = sweep([(10, 20, 0), (5, 15, 1), (12, 18, 1), (12, 18, 2)])
        self.assertEqual(result['stall_cycles'], 10)
        self.assertEqual(result['single_overlap_cycles'], 8)
        self.assertEqual(result['single_exposure'], 11)
        self.assertEqual(result['eligible_overlap_cycles'], 6)
        self.assertEqual(result['max_single_held_at_stall'], 2)

    def test_release_cycle_is_excluded(self):
        result = sweep([(10, 20, 0), (0, 10, 1), (20, 30, 1)])
        self.assertEqual(result['single_overlap_cycles'], 0)
        self.assertEqual(result['single_exposure'], 0)

    def test_measurement_epoch_and_class_isolation(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'trace.csv'
            path.write_text('kind,epoch,class,start_cycle,end_cycle,eligible,self_redef\n'
                            'stall,1,0,1,100,0,0\n'
                            'stall,2,0,10,20,0,0\n'
                            'value,2,0,15,25,1,1\n'
                            'value,2,1,10,20,1,1\n')
            result = trace_metrics(path, 2)
            self.assertEqual(result[0]['stall_cycles'], 10)
            self.assertEqual(result[0]['self_redef_overlap_cycles'], 5)
            self.assertEqual(result[1]['single_overlap_cycles'], 0)

    def test_last_complete_stats_block(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'stats.txt'
            path.write_text('Begin Simulation Statistics\na 123 # warmup\nEnd Simulation Statistics\n'
                            'Begin Simulation Statistics\na 456 # measured\nEnd Simulation Statistics\n'
                            'Begin Simulation Statistics\na 999\n')
            self.assertEqual(stat_blocks(path)[-1]['a'], 456)


if __name__ == '__main__':
    unittest.main()
