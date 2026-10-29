import os
import tempfile
import unittest

from synthetic_fastq.generator import generate_reference, iter_reads, write_fastq


class TestDeterminism(unittest.TestCase):
    def test_reference_deterministic(self):
        self.assertEqual(generate_reference(100, seed=7), generate_reference(100, seed=7))

    def test_reference_seed_sensitive(self):
        self.assertNotEqual(generate_reference(100, seed=7), generate_reference(100, seed=8))

    def test_reads_deterministic(self):
        a = list(iter_reads(10, 50, seed=1))
        b = list(iter_reads(10, 50, seed=1))
        self.assertEqual(a, b)


class TestFastqFormat(unittest.TestCase):
    def test_four_lines_per_read(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "r.fastq")
            n = write_fastq(path, n_reads=10, read_length=20, seed=3)
            self.assertEqual(n, 10)
            lines = open(path).read().splitlines()
            self.assertEqual(len(lines), 10 * 4)
            # each read: header, seq, '+', qual
            for i in range(0, len(lines), 4):
                self.assertTrue(lines[i].startswith("@read"))
                self.assertEqual(len(lines[i + 1]), 20)
                self.assertEqual(lines[i + 2], "+")
                self.assertEqual(len(lines[i + 3]), 20)

    def test_quality_is_phred40(self):
        for _, _, plus, qual in iter_reads(1, 10, seed=0):
            self.assertEqual(plus, "+")
            self.assertTrue(all(c == "I" for c in qual))


if __name__ == "__main__":
    unittest.main()
