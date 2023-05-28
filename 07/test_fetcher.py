import unittest
import asyncio
from unittest import mock
from pathlib import Path
from asyncio import Queue
from fetcher import supervisor, fetch_url, work


TEST_URLS = Path('test_urls.txt')


class TestSupervisor(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.filename = TEST_URLS
        with open(TEST_URLS) as file:
            self.urls = tuple(map(str.strip, file.readlines()))

    @mock.patch('fetcher.useful_action')
    @mock.patch('builtins.print')
    @mock.patch('aiohttp.ClientSession')
    async def test_normal(self, mock_sess, mock_print, mock_usful_action):
        count_workers = 1
        client = mock_sess.return_value.__aenter__.return_value = mock.MagicMock()
        res = client.get.return_value.__aenter__.return_value = mock.MagicMock()
        res.text = 'Some text'

        usf_action_mock_calls = [mock.call(res) for i in range(len(self.urls))]
        get_mock_calls = [mock.call.get(url, timeout=10) for url in self.urls]
        await supervisor(self.filename, count_workers)
        self.assertSequenceEqual(client.method_calls,
                                 get_mock_calls)
        self.assertSequenceEqual(mock_usful_action.mock_calls,
                                 usf_action_mock_calls)
        for args in mock_usful_action.call_args_list:
            resp = args[0][0]
            self.assertEqual(resp.text, res.text)
            self.assertEqual(resp, res)


    @mock.patch('fetcher.useful_action')
    @mock.patch('builtins.print')
    @mock.patch('aiohttp.ClientSession')
    async def test_many_workers(self, mock_sess, mock_print, mock_usful_action):
        count_workers = 20
        client = mock_sess.return_value.__aenter__.return_value = mock.MagicMock()
        res = client.get.return_value.__aenter__.return_value = mock.MagicMock()
        res.text = 'Some text'

        usf_action_mock_calls = [mock.call(res) for i in range(len(self.urls))]
        get_mock_calls = [mock.call.get(url, timeout=10) for url in self.urls]
        await supervisor(self.filename, count_workers)
        self.assertSequenceEqual(client.method_calls,
                                 get_mock_calls)
        self.assertSequenceEqual(mock_usful_action.mock_calls,
                                 usf_action_mock_calls)
        for args in mock_usful_action.call_args_list:
            resp = args[0][0]
            self.assertEqual(resp.text, res.text)
            self.assertEqual(resp, res)


class TestFetchUrl(unittest.IsolatedAsyncioTestCase):
    @mock.patch('builtins.print')
    async def test_normal(self, mock_print):
        url = 'https://some_dom.com/some_url'
        client = mock.MagicMock()
        resp = client.get.return_value.__aenter__.return_value = mock.MagicMock()
        resp.text = 'some text'
        res = await fetch_url(url, client)
        self.assertEqual(client.method_calls,
                         [mock.call.get(url, timeout=10)])
        self.assertEqual(res, resp)
        self.assertEqual(res.text, resp.text)


class TestWork(unittest.IsolatedAsyncioTestCase):

    @mock.patch('fetcher.fetch_url')
    @mock.patch('fetcher.useful_action')
    async def test_normal(self, mock_usf_action, mock_fetch_url):
        # print(mock_usf_action)
        url_queue = Queue()
        url = 'https://some_url'
        await url_queue.put(url)
        client = mock.MagicMock()
        res = client.get.return_value.__aenter__.return_value = mock.MagicMock()
        res.text = 'some text'
        mock_fetch_url.return_value = res

        task = asyncio.create_task(work(url_queue, client))
        await url_queue.join()
        task.cancel()
        try:
            await task
        except asyncio.exceptions.CancelledError:
            pass

        self.assertEqual(mock_fetch_url.mock_calls,
                         [mock.call(url, client)])
        self.assertEqual(mock_usf_action.mock_calls,
                         [mock.call(res)])
        for args in mock_usf_action.call_args_list:
            resp = args[0][0]
            self.assertEqual(resp.text, res.text)
            self.assertEqual(resp, res)

