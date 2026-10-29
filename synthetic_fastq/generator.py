"""Deterministic synthetic FASTQ / reference generation for NGS pipeline tests.

Everything is seeded, so a given seed reproduces byte-identical fixtures —
useful for smoke-testing pipelines in CI without committing raw data.
"""

from __future__ import annotations

import random
from typing import Iterator

BASES = "ACGT"
QUAL_I = "I"  # Phred+33 'I' == quality 40


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def random_sequence(rng: random.Random, length: int) -> str:
    return "".join(rng.choice(BASES) for _ in range(length))


def generate_reference(length: int, seed: int = 42) -> str:
    """Deterministic reference sequence."""
    return random_sequence(_rng(seed), length)


def iter_reads(n_reads: int, read_length: int, seed: int = 42) -> Iterator[tuple[str, str, str, str]]:
    """Yield (header, sequence, '+', quality) FASTQ records."""
    rng = _rng(seed)
    for i in range(n_reads):
        seq = random_sequence(rng, read_length)
        yield f"@read{i}", seq, "+", QUAL_I * read_length


def write_fastq(path: str, n_reads: int, read_length: int, seed: int = 42) -> int:
    """Write a FASTQ file; returns the number of reads written."""
    count = 0
    with open(path, "w", encoding="utf-8") as fh:
        for header, seq, plus, qual in iter_reads(n_reads, read_length, seed):
            fh.write(f"{header}\n{seq}\n{plus}\n{qual}\n")
            count += 1
    return count


def write_reference(path: str, length: int, seed: int = 42) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(">reference\n")
        seq = generate_reference(length, seed)
        for i in range(0, len(seq), 80):
            fh.write(seq[i:i + 80] + "\n")
