import time
import unittest

from core import parse_commandline
from models import DB
from actions import create_post, read_user, follow, wall
from response import Response


class TestCommandParams(unittest.TestCase):
    def test_params_parse(self):
        request = parse_commandline('test -> some random content')

        self.assertEqual(request.user.username, 'test')
        self.assertEqual(request.command, '->')
        self.assertEqual(request.content, 'some random content')

    def test_invalid_command(self):
        with self.assertRaises(ValueError):
            request = parse_commandline('test invalid_command some random content')


class TestSocialApp(unittest.TestCase):
    def setUp(self):
        DB['USER'] = {}
        DB['POST'] = {}

    def test_create_user(self):
        request = parse_commandline('user')
        user = DB['USER'].get(request.user.username, None)
        self.assertEqual(user.username, 'user')
        self.assertEqual(len(user.follows), 0)

    def test_follow(self):
        user1 = DB['USER'].get(parse_commandline('user1').user.username, None)
        user2 = DB['USER'].get(parse_commandline('user2').user.username, None)

        request = parse_commandline('user1 follows user2')
        response = follow(request)

        self.assertIn('user2', user1.follows)

        self.assertEqual(response.content, None)

    def test_post(self):
        response = create_post(parse_commandline('user1 -> test post'))

        self.assertIn('user1', DB['POST'])
        self.assertEqual(DB['POST']['user1'][0].content, 'test post')

        self.assertEqual(response.content, None)

    def test_user_posts(self):
        _ = create_post(parse_commandline('user1 -> test post'))

        response = read_user(parse_commandline('user1'))

        self.assertIsInstance(response, Response)
        self.assertEqual(len(response.content), 1)
        self.assertIn('user1', response.content[0])
        self.assertIn('test post', response.content[0])

    def test_wall_posts(self):
        _ = create_post(parse_commandline('user1 -> test post 1'))
        _ = create_post(parse_commandline('user2 -> test post 3'))
        _ = create_post(parse_commandline('user1 -> test post 2'))
        _ = create_post(parse_commandline('user2 -> test post 4'))

        _ = follow(parse_commandline('user1 follows user2'))

        response = wall(parse_commandline('user1 wall'))
        print(response)

        self.assertIsInstance(response, Response)
        self.assertEqual(len(response.content), 4)
        self.assertIn('test post 4', response.content[0])
        self.assertIn('test post 2', response.content[1])
        self.assertIn('test post 3', response.content[2])
        self.assertIn('test post 1', response.content[3])
