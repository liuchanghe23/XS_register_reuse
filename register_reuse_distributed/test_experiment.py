import configparser
import copy
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import experiment as exp


class DistributedExperimentTest(unittest.TestCase):
    def test_shards_are_disjoint_complete_and_keep_pairs_together(self):
        tasks=[]
        for i in range(31):
            for mode in ('off','certain'):
                tasks.append(dict(suite='reuse',workload='w',point=str(i),int_regs=192,
                                  float_regs=208,mode=mode,id=f'{i}/{mode}'))
            for ni in (128,160,224):
                tasks.append(dict(suite='capacity',workload='w',point=str(i),int_regs=ni,
                                  float_regs=256,mode='off',id=f'{i}/{ni}'))
        original=copy.deepcopy(tasks)
        counts=exp.assign_shards(tasks,6)
        self.assertEqual(sum(counts),155)
        self.assertLessEqual(max(counts)-min(counts),1)
        self.assertEqual({r['id'] for r in tasks},{r['id'] for r in original})
        for i in range(31):
            pair=[t for t in tasks if t['suite']=='reuse' and t['point']==str(i)]
            self.assertEqual(len({t['shard'] for t in pair}),1)
        exp.assign_shards(original,6)
        self.assertEqual(tasks,original)

    def test_budget_accounts_for_full_waves_and_margin(self):
        result=exp.estimate([2336]*6,64,800,1.25)
        self.assertEqual(result['waves'],37)
        self.assertAlmostEqual(result['budget_hours'],10.2777777778)
        self.assertGreater(exp.estimate([2804]*5,64,800,1.25)['budget_hours'],12)

    def test_weighted_cpi_uses_only_matched_pairs_and_marks_missing(self):
        plan={'tasks':[]}
        rows=[]
        for point,weight,off_cpi,certain_cpi in [('1',.75,1,2),('2',.25,4,2)]:
            for mode,cpi in [('off',off_cpi),('certain',certain_cpi)]:
                task=dict(suite='reuse',workload='w',point=point,weight=weight,
                          int_regs=224,float_regs=256,mode=mode)
                plan['tasks'].append(task)
                rows.append(dict(task,cpi=cpi,binary_sha256='same',reuse_stats={}))
        _,weighted,_=exp.weighted_reuse_rows(plan,rows)
        self.assertAlmostEqual(weighted[0]['speedup'],.875)
        self.assertTrue(weighted[0]['complete'])
        _,partial,_=exp.weighted_reuse_rows(plan,rows[:-1])
        self.assertFalse(partial[0]['complete'])
        self.assertEqual(partial[0]['matched_slices'],1)
        self.assertAlmostEqual(partial[0]['selected_weight'],.75)
        self.assertAlmostEqual(partial[0]['speedup'],.5)
        rows[-1]['binary_sha256']='different'
        with self.assertRaisesRegex(ValueError,'binary mismatch'):
            exp.weighted_reuse_rows(plan,rows)

    def test_capacity_thresholds_exclude_unmatched_partial_points(self):
        tasks=[]
        rows=[]
        for variant,ni in [('baseline',224),('int192',192)]:
            for point in ['1','2']:
                tasks.append(dict(suite='capacity',workload='w',point=point,variant=variant))
                rows.append(dict(workload='w',point=point,variant=variant,weight=.4,
                                 int_regs=ni,float_regs=256,cpi=1,instructions=100,
                                 regfull_cycles=0,int_standalone_shortage_cycles=0,
                                 float_standalone_shortage_cycles=0))
        weighted,thresholds=exp.capacity_weighted_report({'tasks':tasks},rows[:-1])
        self.assertEqual(thresholds,[])
        row=next(r for r in weighted if r['variant']=='int192')
        self.assertFalse(row['complete'])
        self.assertNotIn('ipc_ratio_to_default',row)

    def fixture(self, root):
        ref=root/'reference.so'
        ref.write_bytes(b'ref')
        binary=root/'fake-gem5'
        binary.write_text('''#!/usr/bin/env python3
import configparser, pathlib, sys, time
args=sys.argv[1:]
out=pathlib.Path(next(x.split('=',1)[1] for x in args if x.startswith('--outdir=')))
c=configparser.ConfigParser();c['system.cpu']={}
for i,x in enumerate(args):
    if x=='--param':
        name,value=args[i+1].split('=',1)
        c['system.cpu'][name.split('].',1)[1]]=value.strip("'").lower()
reference=next(x.split('=',1)[1] for x in args if x.startswith('--difftest-ref-so='))
c['system.cpu']['enable_difftest']='true'
c['system.cpu']['difftest_ref_so']=reference
c['system.cpu']['max_insts_any_thread']='300'
with (out/'config.ini').open('w') as f:c.write(f)
if (pathlib.Path(__file__).parent/'slow').exists():
    child=__import__('subprocess').Popen([sys.executable,'-c','import time; time.sleep(60)'])
    (out/'grandchild.pid').write_text(str(child.pid))
    time.sleep(60)
block='---------- Begin Simulation Statistics ----------\\nsimInsts 200\\nsystem.cpu.numCycles 100\\nsystem.cpu.regReuse.sharedVersions 0\\nsystem.cpu.regReuse.deterministicReuses 0\\nsystem.cpu.regReuse.predictedReuses 0\\nsystem.cpu.regReuse.repairCopies 0\\n---------- End Simulation Statistics ----------\\n'
(out/'stats.txt').write_text(block*2)
print('Exiting @ tick because a thread reached the max instruction count')
''')
        binary.chmod(0o755)
        cpts=root/'checkpoints'
        cpts.mkdir()
        (cpts/'checkpoint.zstd').touch()
        (root/'GEM5').mkdir()
        plan=dict(warmup=100,measure=200,plan_id='test-plan',components=dict(
                    reuse_binary='binary-sha',reference='reference-sha',config='config-sha',
                    checkpoint_metadata='metadata-sha'))
        task=dict(suite='reuse',mode='off',variant='baseline-off',workload='w',point='1',
                  weight=1,int_regs=224,float_regs=256,checkpoint_relative='checkpoint.zstd',id='w/1/off')
        paths=dict(reuse_gem5=binary,reference=ref,checkpoints=cpts,repo=root/'GEM5')
        return plan,task,paths

    def test_runner_resumes_and_rejects_corrupted_completed_config(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            plan,task,paths=self.fixture(root)
            out=root/'out'
            stop=threading.Event()
            result=exp.run_one(plan,task,paths,out,stop,10)
            self.assertEqual(result[0],'OK',result)
            self.assertEqual(exp.run_one(plan,task,paths,out,stop,10)[0],'SKIP')
            c=configparser.ConfigParser();c.read(out/'config.ini')
            c['system.cpu']['regReusePrediction']='true'
            with (out/'config.ini').open('w') as f:c.write(f)
            status,_,reason=exp.run_one(plan,task,paths,out,stop,10)
            self.assertEqual(status,'FAIL')
            self.assertIn('regReusePrediction',reason)

    def test_runner_timeout_cleans_child_group(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            plan,task,paths=self.fixture(root)
            (root/'slow').touch()
            out=root/'out'
            result=exp.run_one(plan,task,paths,out,threading.Event(),.3)
            self.assertEqual(result[0],'FAIL')
            self.assertEqual(json.loads((out/'run.json').read_text())['state'],'timeout')
            pid=int((out/'grandchild.pid').read_text())
            stat=Path(f'/proc/{pid}/stat')
            self.assertTrue(not stat.exists() or stat.read_text().split()[2]=='Z')

    def test_cli_stop_terminates_active_process_groups_and_releases_lock(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            plan,task,paths=self.fixture(root)
            (root/'slow').touch()
            config=root/'GEM5/configs/example/kmhv3.py'
            config.parent.mkdir(parents=True)
            config.write_text('# fake config')
            metadata=paths['checkpoints']/'cluster-0-0.json'
            metadata.write_text('{}')
            plan.update(schema=exp.SCHEMA,servers=1,jobs=1,timeout=60,support_files={},
                        paths=dict(workspace=str(root),checkpoints=str(paths['checkpoints']),
                                   reference=str(paths['reference']),
                                   reuse_binary_relative='fake-gem5',capacity_binary_relative='fake-gem5'))
            task['shard']=0
            plan['tasks']=[task]
            plan['components'].update(reuse_binary=exp.file_sha256(paths['reuse_gem5']),
                                      reference=exp.file_sha256(paths['reference']),
                                      config=exp.file_sha256(config),
                                      checkpoint_metadata=exp.file_sha256(metadata))
            plan['plan_id']=exp.digest({k:v for k,v in plan.items() if k not in ('paths','plan_id')})
            planfile=root/'batch/plan.json'
            exp.write_json(planfile,plan)
            out=exp.task_output(planfile,task)
            with (root/'cli.log').open('w') as log:
                proc=subprocess.Popen([sys.executable,str(Path(exp.__file__)),'run',
                                       '--plan',str(planfile),'--shard-id','0'],stdout=log,stderr=log)
                try:
                    deadline=time.monotonic()+10
                    while not (out/'grandchild.pid').exists() and time.monotonic()<deadline and proc.poll() is None:
                        time.sleep(.05)
                    self.assertTrue((out/'grandchild.pid').exists(),(root/'cli.log').read_text())
                    import argparse
                    self.assertEqual(exp.stop_main(argparse.Namespace(plan=planfile,shard_id=0)),0)
                    self.assertEqual(proc.wait(timeout=10),130)
                    self.assertEqual(json.loads((out/'run.json').read_text())['state'],'interrupted')
                    self.assertEqual(json.loads((planfile.parent/'shards/00.json').read_text())['state'],'interrupted')
                    stat=Path(f'/proc/{int((out/"grandchild.pid").read_text())}/stat')
                    self.assertTrue(not stat.exists() or stat.read_text().split()[2]=='Z')
                    self.assertEqual(exp.stop_main(argparse.Namespace(plan=planfile,shard_id=0)),0)
                finally:
                    if proc.poll() is None:
                        proc.terminate()
                        proc.wait(timeout=10)

    def test_plan_checksum_detects_manual_edit(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'plan.json'
            plan={'schema':exp.SCHEMA,'paths':{},'measure':200}
            plan['plan_id']=exp.digest({k:v for k,v in plan.items() if k!='paths'})
            exp.write_json(p,plan)
            self.assertEqual(exp.load_plan(p)['measure'],200)
            plan['measure']=201
            exp.write_json(p,plan)
            with self.assertRaisesRegex(ValueError,'checksum'):
                exp.load_plan(p)


if __name__=='__main__':
    unittest.main()
