import json
import unittest
from unittest.mock import patch, MagicMock
from riotkit.client import RiotClient
from riotkit.fetcher import fetch_profile, parse_riot_id, diagnose
from riotkit.endpoints import champion_rotation, champion_mastery_all, match_timeline

class UnitTests(unittest.TestCase):
    def make_client(self):
        return RiotClient("RGAPI-test", "euw1", "europe")

    def test_parse_riot_id(self):
        game, tag = parse_riot_id("G#T")
        self.assertEqual(game, "G")
        self.assertEqual(tag, "T")

    @patch("riotkit.fetcher.account_by_riot_id")
    @patch("riotkit.fetcher.summoner_by_puuid")
    @patch("riotkit.fetcher.match_ids_by_puuid")
    @patch("riotkit.fetcher.match_by_id")
    def test_flow(self, mock_match, mock_ids, mock_summ, mock_acc):
        acc = {"puuid": "P", "gameName": "G", "tagLine": "T"}
        summ = {"id": "S", "summonerLevel": 100}
        ids = ["M1", "M2"]
        match = {"info": {"gameDuration": 1800, "participants": [{"puuid": "P", "kills": 10, "deaths": 2, "assists": 5}]}}

        mock_acc.return_value = acc
        mock_summ.return_value = summ
        mock_ids.return_value = ids
        mock_match.return_value = match

        c = self.make_client()
        r = fetch_profile(c, "G#T", 2)
        self.assertEqual(len(r["matches"]), 2)
        self.assertEqual(r["account"]["gameName"], "G")

    @patch("riotkit.fetcher.status_probe")
    def test_diagnose(self, mock_status):
        mock_status.return_value = {"id": "EUW1"}
        c = self.make_client()
        result = diagnose(c)
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "EUW1")

    @patch("riotkit.client.RiotClient._get")
    def test_champion_rotation(self, mock_get):
        mock_get.return_value = {"freeChampionIds": [1, 2, 3]}
        c = self.make_client()
        result = champion_rotation(c)
        self.assertEqual(len(result["freeChampionIds"]), 3)

    @patch("riotkit.client.RiotClient._get")
    def test_champion_mastery_all(self, mock_get):
        mock_get.return_value = [{"championId": 1, "championLevel": 5}]
        c = self.make_client()
        result = champion_mastery_all(c, "test-puuid")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["championId"], 1)

    @patch("riotkit.client.RiotClient._get")
    def test_match_timeline(self, mock_get):
        mock_get.return_value = {"frames": []}
        c = self.make_client()
        result = match_timeline(c, "test-match-id")
        self.assertIn("frames", result)
