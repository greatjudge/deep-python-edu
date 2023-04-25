import unittest
import json

from unittest import mock
from io import StringIO

from client import work, run_client


class TestWork(unittest.TestCase):
    def test_normal(self):
        lock = mock.MagicMock()
        addr = ('127.0.0.1', 8000)
        urls = ['http://some_dom/some_res', 'http://some_dom/jdjdj']
        fp = StringIO('\n'.join(urls))

        with (mock.patch('socket.create_connection') as mock_create_conn,
              mock.patch('client.print') as mock_print):
            conn = mock_create_conn.return_value
            conn.recv.return_value = b'{"test": 1}'
            mock_send_calls, mock_recv_calls = [], []
            mock_print_calls = []
            for url in urls:
                mock_send_calls.append(mock.call(url.encode()))
                mock_recv_calls.append(mock.call(2048))
                mock_print_calls.append(mock.call(f'{url}:'
                                                  f' {conn.recv.return_value.decode()}'))

            work(fp, addr, lock)
            mock_create_conn.assert_called_with(addr)
            self.assertEqual(conn.send.mock_calls,
                             mock_send_calls)
            self.assertEqual(conn.recv.mock_calls,
                             mock_recv_calls)
            self.assertEqual(mock_print.mock_calls,
                             mock_print_calls)


class TestClient(unittest.TestCase):
    def test_normal(self):
        addr = ('127.0.0.1', 16000)
        urls = ['http://some_dom/some_res', 'http://some_dom/jdjdj']

        mock_open = mock.mock_open(read_data='\n'.join(urls))
        with (mock.patch('socket.create_connection') as mock_create_conn,
              mock.patch('client.print') as mock_print,
              mock.patch('builtins.open', mock_open) as mock_open):
            conn = mock_create_conn.return_value
            conn.recv.return_value = b'{"test": 1}'

            mock_send_calls, mock_recv_calls = [], []
            mock_print_calls = []
            for url in urls:
                mock_send_calls.append(mock.call(url.encode()))
                mock_recv_calls.append(mock.call(2048))
                mock_print_calls.append(mock.call(f'{url}:'
                                                  f' {conn.recv.return_value.decode()}'))
            run_client(*addr, 'some_file.txt', 10)
            self.assertCountEqual(conn.send.mock_calls,
                                  mock_send_calls)
            self.assertCountEqual(conn.recv.mock_calls,
                                  mock_recv_calls)
            self.assertCountEqual(mock_print.mock_calls,
                                  mock_print_calls)
