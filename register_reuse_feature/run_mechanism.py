#!/usr/bin/env python3
"""Witness deterministic slot reuse in Rename trace, with a multi-consumer control."""
import argparse
import configparser
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT / 'GEM5'
sys.path.insert(0, str(ROOT / 'register_reuse_analysis'))
from analyze import stat_blocks
from run import file_sha256

SOURCE = REPO / 'tests/test-progs/register-reuse/mechanism.S'
CASES = [('single-off', 'single', False, 3),
         ('single-one-shadow', 'single', True, 1),
         ('single-three-shadows', 'single', True, 3),
         ('multi-off', 'multi', False, 3),
         ('multi-three-shadows', 'multi', True, 3)]
PC = re.compile(r'\[sn:(\d+)\] Renaming instruction with PC \((0x[0-9a-fA-F]+)=>')
READ = re.compile(r'Register (\d+) \(flat: (\d+)\) \((IntRegClass|FloatRegClass)\)')
DEST = re.compile(r'Rename arch reg x(\d+) \((IntRegClass|FloatRegClass)\) '
                  r'from \[phys: (\d+)\] to \[phys: (\d+)\]')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


def compile_programs(out):
    symbols = {}
    for program in ('single', 'multi'):
        elf = out / f'{program}.elf'
        command = ['riscv64-linux-gnu-gcc', '-nostdlib', '-nostartfiles', '-static',
                   '-march=rv64gc', '-mabi=lp64d', '-Wl,-Ttext=0x80000000',
                   '-Wl,--build-id=none', '-o', str(elf), str(SOURCE)]
        if program == 'multi':
            command += ['-DTEST_MULTI_CONSUMER']
        subprocess.run(command, check=True)
        subprocess.run(['riscv64-linux-gnu-objcopy', '-O', 'binary', str(elf),
                        str(out / f'{program}.bin')], check=True)
        table = subprocess.check_output(['riscv64-linux-gnu-nm', '-n', str(elf)], text=True)
        symbols[program] = {parts[2]: int(parts[0], 16)
                            for line in table.splitlines() if len(parts := line.split()) == 3
                            and parts[2] in ('int_chain_begin', 'int_chain_end',
                                             'fp_chain_begin', 'fp_chain_end')}
        require(len(symbols[program]) == 4, 'missing chain boundary symbols')
    write_json(out / 'symbols.json', symbols)
    return symbols


def inspect_trace(path, symbols, int_regs=224, float_regs=256):
    """Use the logged register index to decode identity; do not infer from counters."""
    identities, destinations = {}, []
    current = None
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        match = PC.search(line)
        if match:
            current = (int(match[1]), int(match[2], 16))
        match = READ.search(line)
        if match:
            index, flat, cls = int(match[1]), int(match[2]), match[3]
            slots = int_regs if cls == 'IntRegClass' else float_regs
            identity = dict(reg_class=cls, base_slot=index % slots, version=index // slots)
            require(flat not in identities or identities[flat] == identity,
                    f'inconsistent physical identity for tag {flat}')
            identities[flat] = identity
        match = DEST.search(line)
        if match and current:
            arch, cls, old, new = int(match[1]), match[2], int(match[3]), int(match[4])
            for label, expected_arch, expected_cls in [('int', 9, 'IntRegClass'),
                                                       ('fp', 8, 'FloatRegClass')]:
                if (symbols[f'{label}_chain_begin'] <= current[1] < symbols[f'{label}_chain_end']
                        and arch == expected_arch and cls == expected_cls):
                    destinations.append(dict(chain=label, seq=current[0], pc=hex(current[1]),
                                             old_tag=old, new_tag=new, trace_line=line_number))
    result = {}
    for label, expected_count in [('int', 64), ('fp', 16)]:
        chain = [entry for entry in destinations if entry['chain'] == label]
        require(len(chain) == expected_count, f'{label}: expected {expected_count} renames, got {len(chain)}')
        require(len({entry['pc'] for entry in chain}) == expected_count,
                f'{label}: instructions renamed multiple times or missing from trace')
        reused, fresh = [], []
        for entry in chain:
            require(entry['old_tag'] in identities and entry['new_tag'] in identities,
                    f'missing read identity at PC {entry["pc"]}')
            old, new = identities[entry['old_tag']], identities[entry['new_tag']]
            require(old['reg_class'] == new['reg_class'], 'register class changed')
            entry.update(old=old, new=new)
            if new['version']:
                require(old['base_slot'] == new['base_slot'], 'shadow changed base slot')
                require(new['version'] == old['version'] + 1, 'version tag did not advance')
                require(entry['old_tag'] != entry['new_tag'], 'old and new dependency tags alias')
                reused.append(entry)
            else:
                require(old['base_slot'] != new['base_slot'], 'fresh allocation overlaps live source')
                fresh.append(entry)
        result[label] = dict(instructions=len(chain), reused=len(reused),
                             fresh_allocations=len(fresh),
                             versions=sorted({e['new']['version'] for e in chain}),
                             witnesses=reused[:4] if reused else fresh[:2])
    return result


def check_case(out, case, symbols, reference):
    name, program, enabled, shadows = case
    destination = out / name
    config = configparser.ConfigParser(interpolation=None)
    config.read(destination / 'config.ini')
    cpu = config['system.cpu']
    expected = {'enableRegisterReuse': enabled, 'regReusePrediction': False,
                'enableRegPressureStats': False, 'enableMoveElimination': False,
                'enableConstantFolding': False, 'enableMovImmElimination': False,
                'enable_difftest': True}
    for key, value in expected.items():
        require(cpu.getboolean(key) == value, f'{name}: config {key} differs')
    for key, value in [('numPhysIntRegs', 224), ('numPhysFloatRegs', 256),
                       ('regReuseShadowCopies', shadows), ('numThreads', 1)]:
        require(cpu.getint(key) == value, f'{name}: config {key} differs')
    require(cpu['RobCompressPolicy'] == 'none', f'{name}: compressed ROB')
    require(Path(cpu['difftest_ref_so']).resolve() == reference.resolve(), 'reference path mismatch')
    require('because m5_exit instruction encountered' in (destination / 'run.log').read_text(),
            f'{name}: did not reach the success exit')
    blocks = stat_blocks(destination / 'stats.txt')
    require(bool(blocks), f'{name}: no complete stats block')
    stats = blocks[-1]
    trace = inspect_trace(destination / 'rename.log', symbols[program])
    for label, count in [('int', 64), ('fp', 16)]:
        expected_reuses = count - count // (shadows + 1) if enabled and program == 'single' else 0
        require(trace[label]['reused'] == expected_reuses,
                f'{name}/{label}: expected {expected_reuses} trace-proven reuses; got {trace[label]["reused"]}')
        require(trace[label]['fresh_allocations'] == count - expected_reuses,
                f'{name}/{label}: fresh slot allocation count differs')
        require(max(trace[label]['versions']) <= (shadows if enabled else 0), 'shadow bound exceeded')
    reuse = {key.split('.regReuse.')[1]: value for key, value in stats.items() if '.regReuse.' in key}
    for key in ('predictedReuses', 'repairCopies', 'predictionMisses'):
        require(reuse[key] == 0, f'{name}: unexpected predictor or repair activity')
    if enabled:
        trace_reuses = sum(chain['reused'] for chain in trace.values())
        require(reuse['deterministicReuses'] >= trace_reuses, 'counter misses trace-proven reuse')
        require(reuse['deterministicReuses'] == reuse['sharedVersions'], 'shared versions accounting mismatch')
        if program == 'single':
            require(reuse['versionLimitRejects'] > 0, 'version limit was not exercised')
    else:
        require(reuse['sharedVersions'] == 0, 'OFF run reused slots')
    return dict(case=name, program=program, ok=True, instructions=stats['simInsts'],
                cycles=stats['system.cpu.numCycles'], chain_trace=trace, reuse_stats=reuse)


def check_pairs(results):
    by_name = {result['case']: result for result in results}
    for program in ('single', 'multi'):
        group = [result for result in results if result['program'] == program]
        require(len({result['instructions'] for result in group}) == 1,
                f'{program}: committed instruction counts differ between configurations')
        off = by_name[program + '-off']
        for result in group:
            result['full_program_ipc_ratio_to_off'] = off['cycles'] / result['cycles']
    for label in ('int', 'fp'):
        require(by_name['single-three-shadows']['chain_trace'][label]['fresh_allocations'] <
                by_name['single-one-shadow']['chain_trace'][label]['fresh_allocations'] <
                by_name['single-off']['chain_trace'][label]['fresh_allocations'],
                f'{label}: increasing shadow capacity did not reduce fresh allocations')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=HERE / 'mechanism-proof')
    parser.add_argument('--gem5', type=Path, default=HERE / 'build/RISCV/gem5.opt')
    parser.add_argument('--reference', type=Path, default=Path(os.environ.get('GCBV_REF_SO') or
                        '/nfs/home/share/gem5_ci/ref/normal/riscv64-nemu-interpreter-so'))
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('--analyze-only', action='store_true')
    args = parser.parse_args()
    out = args.out.expanduser().absolute()
    binary = args.gem5.expanduser().absolute()
    reference = args.reference.expanduser().absolute()
    out.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        require(args.timeout > 0, 'timeout must be positive')
        require(binary.is_file() and os.access(binary, os.X_OK), f'missing executable: {binary}')
        require(reference.is_file(), f'missing NEMU reference: {reference}; set GCBV_REF_SO')
        identity = dict(binary_sha256=file_sha256(binary), reference_sha256=file_sha256(reference),
                        source_sha256=file_sha256(SOURCE))
        if args.analyze_only:
            recorded = json.loads((out / 'manifest.json').read_text())
            require(recorded['identity'] == identity, 'binary/reference/test source changed since run')
            symbols = json.loads((out / 'symbols.json').read_text())
        else:
            symbols = compile_programs(out)
            recorded = dict(identity=identity, commands={}, returncodes={})
            for case in CASES:
                name, program, enabled, shadows = case
                destination = out / name
                destination.mkdir(parents=True, exist_ok=True)
                command = [str(binary), '--debug-flags=Rename', '--debug-file=rename.log',
                           '--outdir=' + str(destination), str(REPO / 'configs/example/kmhv3.py'),
                           '--raw-cpt', '--generic-rv-cpt=' + str(out / f'{program}.bin'),
                           '--warmup-insts-no-switch=0', '--maxinsts=10000',
                           '--difftest-ref-so=' + str(reference)]
                params = dict(enableRegisterReuse=enabled, regReusePrediction=False,
                              regReuseShadowCopies=shadows, enableRegPressureStats=False,
                              enableMoveElimination=False, enableConstantFolding=False,
                              enableMovImmElimination=False, numPhysIntRegs=224, numPhysFloatRegs=256,
                              RobCompressPolicy="'none'", numThreads=1)
                for key, value in params.items():
                    command += ['--param', f'system.cpu[0].{key}={value}']
                recorded['commands'][name] = command
                start = time.monotonic()
                with (destination / 'run.log').open('w') as log:
                    try:
                        rc = subprocess.run(command, cwd=REPO, stdout=log, stderr=subprocess.STDOUT,
                                            timeout=args.timeout).returncode
                    except subprocess.TimeoutExpired:
                        rc = 124
                recorded['returncodes'][name] = rc
                write_json(out / 'manifest.json', recorded)
                require(rc == 0, f'{name}: gem5 failed ({rc}); see {destination / "run.log"}')
                result = check_case(out, case, symbols, reference)
                results.append(result)
                print(f'PASS {name}: INT reuse={result["chain_trace"]["int"]["reused"]}/64; '
                      f'FP reuse={result["chain_trace"]["fp"]["reused"]}/16; '
                      f'{time.monotonic()-start:.1f}s', flush=True)
        if args.analyze_only:
            for case in CASES:
                require(recorded['returncodes'].get(case[0]) == 0, f'{case[0]}: failed simulator exit')
                results.append(check_case(out, case, symbols, reference))
        check_pairs(results)
        write_json(out / 'proof.json', dict(ok=True, identity=identity, cases=results))
        lines = ['# 寄存器复用机制定向验证', '',
                 '同一个 feature 二进制，固定 INT/FP=224/256，预测、move elimination 和 constant folding 均关闭，全部开启 NEMU difftest。',
                 'INT：64 次 `addi s1,s1,1`，17→81；FP：16 次 `fadd.d f8,f8,f8`，1.0→65536.0。',
                 '负对照在每次运算前保存旧值，检查内存最终为 80 和 32768.0；已有消费者应禁止复用。', '',
                 '计数来自按 ELF PC 边界筛选的 Rename trace；不把全程序复用计数或 IPC 当作充分证据。', '',
                 '| 用例 | INT 同槽位新版本 | INT 新槽位分配 | FP 同槽位新版本 | FP 新槽位分配 |',
                 '|---|---:|---:|---:|---:|']
        for result in results:
            i, f = result['chain_trace']['int'], result['chain_trace']['fp']
            lines.append(f'| {result["case"]} | {i["reused"]} | {i["fresh_allocations"]} | {f["reused"]} | {f["fresh_allocations"]} |')
        witness = next(r for r in results if r['case'] == 'single-three-shadows')['chain_trace']['int']['witnesses'][:3]
        lines += ['', '三次连续 INT 复用的实际记录：', '', '| PC | 基槽位 | 版本 | 依赖标签 |', '|---|---:|---|---|']
        for entry in witness:
            lines.append(f'| {entry["pc"]} | {entry["old"]["base_slot"]} | {entry["old"]["version"]}→{entry["new"]["version"]} | {entry["old_tag"]}→{entry["new_tag"]} |')
        lines += ['', '结论：正例复用同一基槽位、使用不同且递增的版本依赖标签，并减少新槽位分配；负对照拒绝复用；重复 FP 操作数按一个消费者处理。',
                  '这验证了该输入上的功能机制和容量限制，不是所有恢复场景的证明，也不保证应用性能提高。',
                  '完整统计、命令、SHA256 和 trace 证据见 `proof.json`、`manifest.json`、各用例的 `rename.log`。']
        (out / 'report.md').write_text('\n'.join(lines) + '\n')
        print(f'PASS: all 5 cases; report: {out / "report.md"}', flush=True)
        return 0
    except (OSError, ValueError, KeyError, configparser.Error, subprocess.CalledProcessError) as exc:
        write_json(out / 'proof.json', dict(ok=False, error=str(exc), cases=results))
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
