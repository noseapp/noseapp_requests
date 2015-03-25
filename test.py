# -*- coding: utf-8 -*-
import unittest

from noseapp_requests.base import Session
from noseapp_requests.urlbuilder import BaseUrlBuilder


class TestUrlBuilder(unittest.TestCase):
    """Test that BaseUrlBuilder supports basic requests lib interface"""
    def setUp(self):
        self.builder = BaseUrlBuilder('http://example.com/v1/')

    def test_get(self):
        res = self.builder('get', 'example', test="test")
        self.assertEqual(
            res,
            {'method': 'get',
             'url': 'http://example.com/v1/example',
             'params': {'test': 'test'}}
        )

    def test_post(self):
        res = self.builder('post', 'example', test="test")
        self.assertEqual(
            res,
            {'method': 'post',
             'url': 'http://example.com/v1/example',
             'data': {'test': 'test'}}
        )

    def test_put(self):
        res = self.builder('put', 'example', {'test': "test"})
        self.assertEqual(
            res,
            {'method': 'put',
             'url': 'http://example.com/v1/example',
             'json': {'test': 'test'}}
        )

    def test_delete(self):
        res = self.builder('delete', 'example')
        self.assertEqual(
            res,
            {'method': 'delete',
             'url': 'http://example.com/v1/example'}
        )

    def test_unknown_method(self):
        with self.assertRaises(AttributeError):
            self.builder('unknown', 'example')


class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session()
