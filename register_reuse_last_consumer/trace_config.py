"""Enable existing debug probes only after the ordinary warmup stats reset."""
import json
import os
from pathlib import Path
import runpy
import sys

import m5

workspace = Path(__file__).resolve().parent.parent
config = workspace / 'GEM5/configs/example/kmhv3.py'
original_reset = m5.stats.reset
reset_count = 0
flags = ('Rename', 'O3PipeView', 'Exec', 'ExecFlags', 'ExecFetchSeq')


def reset_with_trace():
    global reset_count
    original_reset()
    reset_count += 1
    if reset_count == 2:
        if os.environ.get('LAST_CONSUMER_TRACE', '1') == '1':
            for name in flags:
                m5.debug.flags[name].enable()
        path = Path(m5.options.outdir) / 'trace-window.json'
        path.write_text(json.dumps(dict(start_tick=int(m5.curTick()), reset_count=reset_count,
                             enabled=os.environ.get('LAST_CONSUMER_TRACE', '1') == '1'))+'\n')


m5.stats.reset = reset_with_trace
sys.path[:0] = [str(config.parent), str(config.parent.parent), str(workspace / 'GEM5')]
sys.argv[0] = str(config)
runpy.run_path(str(config), run_name='__m5_main__')
