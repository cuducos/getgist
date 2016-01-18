import os
from uuid import uuid4

try:
    from unittest import TestCase
    from unittest.mock import patch
except ImportError:
    from unittest2 import TestCase
    from mock import patch

from getgist.local import LocalTools

TEST_FILE = '.test-{}'.format(uuid4())
TEST_FILE_CONTENT = 'Hello, world!'


class LocalFileTestCase(TestCase):

    def setUp(self):
        self.local = LocalTools(TEST_FILE)
        self.cwd = os.getcwd()
        self.path = os.path.join(self.cwd, TEST_FILE)

    def tearDown(self):
        files = [f for f in os.listdir(self.cwd) if os.path.isfile(f)]
        for f in files:
            path = os.path.join(self.cwd, f)
            filename = os.path.basename(path)
            if filename.startswith(TEST_FILE):
                os.remove(path)


class TestReadFile(LocalFileTestCase):

    def test_read(self):
        with open(self.path, 'w') as handler:
            handler.write('TestReadFile')
        self.assertEqual(self.local.read(self.path), 'TestReadFile')

    def test_read_non_existet_file(self):
        self.assertFalse(self.local.read('.no_gist'))

    def test_read_directory(self):
        self.assertFalse(self.local.read(os.getcwd()))


class TestBackup(LocalFileTestCase):

    def test_simple_backup(self):
        with open(self.path, 'w') as handler:
            handler.write('TestBackup')
        self.local.backup()
        path = str(self.path) + '.bkp'
        with self.subTest():
            self.assertTrue(os.path.exists(path))
            self.assertEqual(self.local.read(path), 'TestBackup')

    def test_two_backups(self):
        with open(self.path, 'w') as handler:
            handler.write('TestBackup')
        path_bkp = str(self.path) + '.bkp'
        with open(path_bkp, 'w') as handler:
            handler.write('TestBackup.bkp')
        self.local.backup()
        path_bkp1 = path_bkp + '1'
        with self.subTest():
            self.assertTrue(os.path.exists(path_bkp1))
            self.assertEqual(self.local.read(path_bkp1), 'TestBackup')

    def test_multi_backups(self):
        for ext in ['', '.bkp', '.bkp1', '.bkp2', '.bkp3']:
            path = str(self.path) + ext
            with open(path, 'w') as handler:
                handler.write('TestBackup' + ext)
        self.local.backup()
        path_bkp = path[:-1] + '4'
        with self.subTest():
            self.assertTrue(os.path.exists(path_bkp))
            self.assertEqual(self.local.read(path_bkp), 'TestBackup')


class TestWriteFile(LocalFileTestCase):

    def test_write_file(self):
        self.assertFalse(os.path.exists(self.path))
        self.local.save(TEST_FILE_CONTENT)
        with self.subTest():
            self.assertTrue(os.path.exists(self.path))
            self.assertEqual(self.local.read(), TEST_FILE_CONTENT)

    @patch('getgist.local.LocalTools.ask')
    def test_write_file_overwrite(self, mock_ask):
        mock_ask.return_value = 'y'
        with open(self.path, 'w') as handler:
            handler.write(TEST_FILE_CONTENT.replace('o', '0'))
        with self.subTest():
            self.assertTrue(os.path.exists(self.path))
            self.assertIn('Hell0', self.local.read())
        self.local.save(TEST_FILE_CONTENT)
        with self.subTest():
            self.assertTrue(os.path.exists(self.path))
            self.assertEqual(self.local.read(), TEST_FILE_CONTENT)
            self.assertFalse(os.path.exists(str(self.path) + '.bkp1'))

    @patch('getgist.local.LocalTools.ask')
    def test_write_file_with_backup(self, mock_ask):
        mock_ask.return_value = 'n'
        mock_content = TEST_FILE_CONTENT.replace('o', '0')
        with open(self.path, 'w') as handler:
            handler.write(mock_content)
        self.assertTrue(os.path.exists(self.path))
        self.local.save(TEST_FILE_CONTENT)
        with self.subTest():
            self.assertTrue(os.path.exists(self.path))
            self.assertEqual(self.local.read(), TEST_FILE_CONTENT)
            self.assertTrue(os.path.exists(str(self.path) + '.bkp'))
            self.assertEqual(self.local.read(str(self.path) + '.bkp'),
                             mock_content)

    @patch('getgist.local.LocalTools.ask')
    def test_write_file_with_multiple_backup(self, mock_ask):
        mock_ask.return_value = 'n'
        for bkp in ['', '.bkp', '.bkp1', '.bkp2']:
            with open(self.path + bkp, 'w') as handler:
                marker = bkp if bkp else 'marker'
                handler.write(TEST_FILE_CONTENT + marker)
        self.local.save(TEST_FILE_CONTENT)
        with self.subTest():
            self.assertTrue(os.path.exists(self.path))
            self.assertEqual(self.local.read(), TEST_FILE_CONTENT)
            self.assertTrue(os.path.exists(str(self.path) + '.bkp'))
            self.assertTrue(os.path.exists(str(self.path) + '.bkp1'))
            self.assertTrue(os.path.exists(str(self.path) + '.bkp2'))
            self.assertTrue(os.path.exists(str(self.path) + '.bkp3'))
            self.assertEqual(self.local.read(str(self.path) + '.bkp3'),
                             TEST_FILE_CONTENT + 'marker')
