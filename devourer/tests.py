"""
This module contains tests for generic_api package.
"""
import unittest
from . import GenericAPI, APIMethod, APIError


class APIMethodTest(unittest.TestCase):
    """
    This suite tests APIMethod correctness.
    """
    def test_schema(self):
        """
        This test checks whether URL schema is parsed correctly into parameters.
        :return:
        """
        method = APIMethod('get', 'a/b')
        self.assertEqual(method.http_method, 'get')
        self.assertFalse(method.params)
        method = APIMethod('get', 'a/{b}')
        self.assertEqual(method.params, ['b'])


class GenericAPITest(unittest.TestCase):
    """
    This test suite test correctnes of GenericAPI. Figures.
    Oh, you need a working internet connection to run these tests.
    """
    @classmethod
    def setUpClass(cls):
        """
        This method creates resources needed to test GenericAPI.
        :return:
        """
        class TestAPI(GenericAPI):
            """
            This class uses http://jsonplaceholder.typicode.com/ as API with
            known data to enable full testing without mocking.
            :return:
            """
            posts = APIMethod('get', 'posts/')
            comments = APIMethod('get', 'posts/{id}/comments')
            false = APIMethod('get', 'postssss/{id}/comments')

            def call_posts(self, *args, **kwargs):
                """
                This method calls posts API method.
                :param args:
                :param kwargs:
                :return: result of finalize_posts.
                """
                prepared = self.prepare('posts', *args, **kwargs)
                result = prepared.call(self, *args, **kwargs)
                return self.finalize('posts', result, *args, **kwargs)
        cls.TestAPI = TestAPI
        cls.api = TestAPI('http://jsonplaceholder.typicode.com/', None, load_json=True)

    def test_creation(self):
        """
        This tests checks if the class is correctly created and initialized.
        :return:
        """
        self.assertTrue(hasattr(self.api, 'posts'))
        self.assertTrue(hasattr(self.api, 'comments'))
        self.assertTrue(hasattr(self.api, 'finalize_posts'))
        self.assertTrue(hasattr(self.api, 'finalize_comments'))
        self.assertIsInstance(self.api.prepare('posts').call.api, self.TestAPI)

    def test_calls(self):
        """
        This test checks if successful calls return corect results.
        :return:
        """
        self.assertEqual(self.api.posts()[1]['id'], 2)
        self.assertEqual(self.api.comments(id=2)[0]['email'], 'Presley.Mueller@myrl.com')

    def test_exceptions(self):
        """
        This test call if exceptions are raised correctly.
        :return:
        """
        api = self.TestAPI('http://www.pb.pl/nonexistent', None, load_json=True, throw_on_error=True)
        self.assertRaises(APIError, api.posts)

    def test_without_json_loads(self):
        """
        This test checks if API works without JSON loading. As if you will ever need it.
        :return:
        """
        api = self.TestAPI('http://jsonplaceholder.typicode.com/', None, load_json=False)
        self.assertNotEqual(api.comments(id=2).find(b'Presley.Mueller@myrl.com'), -1)


if __name__ == '__main__':
    unittest.main()
