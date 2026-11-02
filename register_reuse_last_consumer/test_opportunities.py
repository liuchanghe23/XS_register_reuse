import gzip
from pathlib import Path
import tempfile
import unittest

from opportunities import Instruction, Intervals, classify_prior, parse_trace


class LastConsumerOpportunityTest(unittest.TestCase):
    def test_program_order_last_does_not_prove_read_done(self):
        prior=Instruction(1,flags=frozenset(['IsInteger']),complete=400,retire=500)
        result=classify_prior([prior],rename_tick=300,writeback_tick=350)
        self.assertFalse(any(result.values()))

    def test_writeback_proxy_is_separate_from_commit(self):
        prior=Instruction(1,flags=frozenset(['IsInteger']),complete=200,retire=500)
        result=classify_prior([prior],rename_tick=300,writeback_tick=350)
        self.assertFalse(result['committed_before_rename'])
        self.assertTrue(result['restricted_wb_before_rename'])
        self.assertTrue(result['any_wb_before_rename'])

    def test_uncommitted_load_only_counts_in_optimistic_bound(self):
        prior=Instruction(1,flags=frozenset(['IsInteger','IsLoad']),complete=200,retire=500)
        result=classify_prior([prior],300,350)
        self.assertFalse(result['restricted_wb_before_rename'])
        self.assertTrue(result['any_wb_before_rename'])
        prior.retire=250
        self.assertTrue(classify_prior([prior],300,350)['committed_before_rename'])

    def test_stall_overlap_uses_half_open_union_intervals(self):
        intervals=Intervals([(10,20),(15,25),(40,50)])
        self.assertEqual(intervals.prefix[-1],25)
        self.assertEqual(intervals.overlap(20,40),5)
        self.assertEqual(intervals.overlap(25,40),0)
        self.assertEqual(intervals.overlap(0,100),25)

    def test_physical_reallocation_has_distinct_generation_and_sources_deduplicate(self):
        trace='''100: system.cpu.rename: [tid:0] [sn:1] Renaming instruction with PC (0x100=>0x104).
100: system.cpu.rename: [tid:0] Rename arch reg x5 (IntRegClass) from [phys: 5] to [phys: 40].
200: system.cpu.rename: [tid:0] [sn:2] Renaming instruction with PC (0x104=>0x108).
200: system.cpu.rename: [tid:0] Looking up IntRegClass arch reg x5, got [phys: 40]
200: system.cpu.rename: [tid:0] Looking up IntRegClass arch reg x5, got [phys: 40]
200: system.cpu.rename: [tid:0] Rename arch reg x6 (IntRegClass) from [phys: 6] to [phys: 41].
300: system.cpu.rename: [tid:0] [sn:3] Renaming instruction with PC (0x108=>0x10c).
300: system.cpu.rename: [tid:0] Looking up IntRegClass arch reg x5, got [phys: 40]
300: system.cpu.rename: [tid:0] Rename arch reg x5 (IntRegClass) from [phys: 40] to [phys: 42].
600: system.cpu.rename: Really free up p40 on squash with ref=0
700: system.cpu.rename: [tid:0] [sn:4] Renaming instruction with PC (0x10c=>0x110).
700: system.cpu.rename: [tid:0] Rename arch reg x7 (IntRegClass) from [phys: 7] to [phys: 40].
800: system.cpu.rename: [tid:0] [sn:5] Renaming instruction with PC (0x110=>0x114).
800: system.cpu.rename: [tid:0] Looking up IntRegClass arch reg x7, got [phys: 40]
'''
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'trace.gz'
            with gzip.open(path,'wt') as handle:handle.write(trace)
            inst,values=parse_trace(path)
        old=inst[2].sources[0];new=inst[5].sources[0]
        self.assertEqual(len(inst[2].sources),1)
        self.assertEqual(values[old].readers,[2,3])
        self.assertEqual(values[old].release,600)
        self.assertNotEqual(old,new)
        self.assertEqual(values[new].producer,4)

    def test_exec_line_timestamp_is_not_used_as_commit_time(self):
        trace="""100: system.cpu.rename: [tid:0] [sn:8] Renaming instruction with PC (0x100=>0x104).
200: system.cpu: addi x5, x5, 1 FetchSeq=8 flags=(IsInteger|IsAddImm)
O3PipeView:fetch:50:0x100:0:8:addi x5, x5, 1
O3PipeView:complete:220
O3PipeView:retire:500:store:0
"""
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'trace.gz'
            with gzip.open(path,'wt') as handle:handle.write(trace)
            inst,_=parse_trace(path)
        self.assertEqual(inst[8].retire,500)
        self.assertFalse(classify_prior([inst[8]],300,350)['committed_before_rename'])

    def test_squash_marks_readers_even_without_destination(self):
        trace='''100: system.cpu.rename: [tid:0] [sn:8] Renaming instruction with PC (0x100=>0x104).
100: system.cpu.rename: [tid:0] Looking up IntRegClass arch reg x5, got [phys: 40]
200: system.cpu.rename: [tid:0] [squash sn:7] Squashing instructions.
'''
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'trace.gz'
            with gzip.open(path,'wt') as handle:handle.write(trace)
            inst,_=parse_trace(path)
        self.assertEqual(inst[8].squash,200)


if __name__=='__main__':unittest.main()
