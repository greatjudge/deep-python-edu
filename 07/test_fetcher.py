import unittest
import asyncio
from unittest import mock
from pathlib import Path
from fetcher import supervisor


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

        usf_action_mock_calls = [mock.call(res) for i in range(len(self.urls))]
        get_mock_calls = [mock.call.get(url, timeout=10) for url in self.urls]
        await supervisor(self.filename, count_workers)
        self.assertSequenceEqual(client.method_calls,
                                 get_mock_calls)
        self.assertSequenceEqual(mock_usful_action.mock_calls,
                                 usf_action_mock_calls)

    @mock.patch('fetcher.useful_action')
    @mock.patch('builtins.print')
    @mock.patch('aiohttp.ClientSession')
    async def test_many_workers(self, mock_sess, mock_print, mock_usful_action):
        count_workers = 20
        client = mock_sess.return_value.__aenter__.return_value = mock.MagicMock()
        res = client.get.return_value.__aenter__.return_value = mock.MagicMock()

        usf_action_mock_calls = [mock.call(res) for i in range(len(self.urls))]
        get_mock_calls = [mock.call.get(url, timeout=10) for url in self.urls]
        await supervisor(self.filename, count_workers)
        self.assertSequenceEqual(client.method_calls,
                                 get_mock_calls)
        self.assertSequenceEqual(mock_usful_action.mock_calls,
                                 usf_action_mock_calls)
