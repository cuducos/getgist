import os
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

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
