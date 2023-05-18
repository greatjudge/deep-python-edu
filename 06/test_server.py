import unittest
import socket
import json

from unittest import mock
from threading import Thread
from server import Server
from queue import Queue


class TestServer(unittest.TestCase):
    HOST, PORT = 'localhost', 55553

    def test_normal(self):
        server = Server(self.HOST, self.PORT)
        server_th = Thread(target=server.run_server,
                           args=(1, 2))
        url = 'https://some_dom/some_res'
        text = 'word1 word2 word1 word1 word2 word3'
        result = {'word1': 3, 'word2': 2}
        with mock.patch('requests.get') as mock_get:
            res = mock_get.return_value
            res.text = text
            server_th.start()

            try:
                conn = socket.create_connection((self.HOST, self.PORT))
                conn.send(url.encode())
                result_send = json.loads(conn.recv(2048).decode())
                self.assertEqual(result_send, result)
                self.assertEqual(mock_get.mock_calls,
                                 [mock.call(url, timeout=5)])
            finally:
                conn.close()
                server.stop_server()
                server_th.join()

    def client_thread_work(self, url: str, result_queue: Queue[str]):
        conn = socket.create_connection((self.HOST, self.PORT))
        conn.send(url.encode())
        result_queue.put(conn.recv(2048).decode())
        conn.close()

    def test_many_requests(self):
        server = Server(self.HOST, self.PORT)
        server_th = Thread(target=server.run_server,
                           args=(30, 2))
        url = 'https://some_dom/some_res'
        text = 'word1 word2 word1 word1 word2 word3 word2 word1'
        result_queue = Queue()
        threads_num = 20
        answer = [{'word1': 4, 'word2': 3} for i in range(threads_num)]
        threads = [Thread(target=self.client_thread_work,
                          args=(url, result_queue)) for _ in range(threads_num)]

        with mock.patch('requests.get') as mock_get:
            res = mock_get.return_value
            res.text = text
            server_th.start()
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            server.stop_server()
            server_th.join()

            result = []
            while not result_queue.empty():
                result.append(json.loads(result_queue.get()))
            self.assertCountEqual(result, answer)
