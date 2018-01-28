from unittest import TestCase

from io_framework.csv_writer import CsvWriter


# Just for making Travis trigger tests
class TestSample(TestCase):
    def test_add(self):
        writer_test = CsvWriter('', '', '', '', '')
        self.assertEqual(9, 4+5)
