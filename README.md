# synthetic-fastq

Deterministic synthetic FASTQ / reference generator for NGS pipeline testing
(stdlib Python, zero dependencies). A given seed reproduces byte-identical
fixtures, so pipeline smoke tests run reproducibly in CI without committing raw
data.

## Usage

```bash
python -m synthetic_fastq fastq -n 100 -l 150 --seed 42 -o reads.fastq
python -m synthetic_fastq reference -l 1000 --seed 42 -o ref.fa
```

## Roadmap

- Truth VCF generation for variant-calling assertions

## License

MIT.
