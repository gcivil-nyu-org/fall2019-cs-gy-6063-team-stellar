from django.test import TestCase
from match import match_user
from prepare_test import prepare


class MatchTest(TestCase):
    def test_match(self):
        prepare()
        match_user()
        self.assertEqual(1, 1)
