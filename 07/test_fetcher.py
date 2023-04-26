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
            self.urls = map(str.strip, file.readlines())

    @mock.patch('builtins.print')
    @mock.patch('aiohttp.ClientSession')
    async def test_normal(self, mock_sess, mock_print):
        count_workers = 1
        client = mock_sess.return_value.__aenter__.return_value = mock.MagicMock()
        get_mock_calls = [mock.call.get(url, timeout=10) for url in self.urls]
        await supervisor(self.filename, count_workers)
        self.assertSequenceEqual(client.method_calls,
                                 get_mock_calls)

    @mock.patch('builtins.print')
    @mock.patch('aiohttp.ClientSession')
    async def test_many_workers(self, mock_sess, mock_print):
        count_workers = 20
        client = mock_sess.return_value.__aenter__.return_value = mock.MagicMock()
        get_mock_calls = [mock.call.get(url, timeout=10) for url in self.urls]
        await supervisor(self.filename, 1)
        self.assertSequenceEqual(client.method_calls,
                                 get_mock_calls)