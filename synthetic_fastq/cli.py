"""synthetic-fastq CLI.

    python -m synthetic_fastq fastq -n 100 -l 150 --seed 42 -o reads.fastq
    python -m synthetic_fastq reference -l 1000 --seed 42 -o ref.fa
"""

import argparse
import sys

from .generator import write_fastq, write_reference


def cmd_fastq(args) -> int:
    n = write_fastq(args.out, args.n, args.length, args.seed)
    print(f"wrote {n} reads -> {args.out}")
    return 0


def cmd_reference(args) -> int:
    write_reference(args.out, args.length, args.seed)
    print(f"wrote reference -> {args.out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="synthetic-fastq", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fastq", help="generate synthetic FASTQ reads")
    f.add_argument("-n", type=int, default=100)
    f.add_argument("-l", "--length", type=int, default=150)
    f.add_argument("--seed", type=int, default=42)
    f.add_argument("-o", "--out", required=True)
    f.set_defaults(fn=cmd_fastq)

    r = sub.add_parser("reference", help="generate a synthetic reference FASTA")
    r.add_argument("-l", "--length", type=int, default=1000)
    r.add_argument("--seed", type=int, default=42)
    r.add_argument("-o", "--out", required=True)
    r.set_defaults(fn=cmd_reference)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
