import os
import unittest
from riotkit.config import load_settings
from riotkit.client import RiotClient
from riotkit.fetcher import diagnose, fetch_profile

class LiveTests(unittest.TestCase):
    def setUp(self):
        self.settings = load_settings()
        # Client par défaut (EUW1)
        self.client = RiotClient(self.settings.api_key, self.settings.platform_region, self.settings.regional_routing)
        # Client pour KR (Corée)
        self.client_kr = RiotClient(self.settings.api_key, "kr", "asia")

    def test_diagnose(self):
        d = diagnose(self.client)
        self.assertTrue("ok" in d)

    def test_profile_euw(self):
        # Test avec l'utilisateur Sung Jin woo#SOUL sur EUW1
        rid = "Sung Jin woo#SOUL"
        r = fetch_profile(self.client, rid, 1)
        self.assertIn("matches", r)
        self.assertIn("account", r)
        self.assertIn("summoner", r)

    def test_profile_kr(self):
        # Test avec l'utilisateur Sard#CASS sur KR
        rid = "Sard#CASS"
        r = fetch_profile(self.client_kr, rid, 1)
        self.assertIn("matches", r)
        self.assertIn("account", r)
        self.assertIn("summoner", r)
