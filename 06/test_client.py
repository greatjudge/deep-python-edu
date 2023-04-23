import unittest
import json

from unittest import mock
from io import StringIO

from client import work


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

