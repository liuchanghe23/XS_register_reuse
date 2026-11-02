#!/usr/bin/env python3
"""Run a Kunminghu V3 register-capacity sweep with the other class controlled."""
import argparse
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def capacity_points(axis, counts, high):
    points = [('baseline', 224, 256), ('large', high, high)]
    for count in sorted(set(counts), reverse=True):
        if count < 48:
            raise ValueError('counts must be >=48')
        if axis == 'joint':
            points.append((f'both{count}', count, count))
        elif axis == 'int':
            if count != 224:
                points.append((f'int{count}', count, 256))
        elif axis == 'float':
            if count != 256:
                points.append((f'fp{count}', 224, count))
    return ','.join(f'{name}:{ni}:{nf}' for name, ni, nf in points)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--axis', choices=['joint', 'int', 'float'], default='joint')
    p.add_argument('--counts', default='192,160,128,96,64')
    p.add_argument('--high', type=int, default=512)
    p.add_argument('--out', type=Path, required=True)
    args, remaining = p.parse_known_args()
    try:
        points = capacity_points(args.axis, [int(x) for x in args.counts.split(',')], args.high)
    except ValueError as exc:
        p.error(str(exc))
    command = [sys.executable, str(HERE / 'run.py'), '--reg-points', points,
               '--out', str(args.out), *remaining]
    print('Capacity sweep:', args.axis, points, flush=True)
    rc = subprocess.call(command)
    if '--dry-run' not in remaining:
        analysis_rc = subprocess.call([sys.executable, str(HERE / 'analyze.py'), str(args.out)])
        rc = rc or analysis_rc
    return rc


if __name__ == '__main__':
    sys.exit(main())
