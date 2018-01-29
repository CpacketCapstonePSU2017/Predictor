from unittest import TestCase
import sys
from os import path
from root import ROOT_DIR
sys.path.append(path.join(ROOT_DIR,'CPacket-Common-Modules'))
from io_framework.csv_writer import CsvWriter

# Just for making Travis trigger tests
class TestSample(TestCase):
    _csv_file_path = None
    _client = None
    _measurement = None
    _host = None
    _database = None
    host = 'localhost'
    port = 8086
    username = 'root'
    password = 'root'
    database = 'andrew_test_db'
    def test_add(self):
        test_csv_write = CsvWriter(self.host, self.port, self.username, self.password, self.database)
        self.assertEqual(9, 4+5)
