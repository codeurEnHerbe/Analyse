from typing import Dict, List
from .client import RiotClient

# Status
def status_probe(c: RiotClient) -> Dict:
    return c._get(c.platform_url("/lol/status/v4/platform-data"))

# Account
def account_by_riot_id(c: RiotClient, game_name: str, tag_line: str) -> Dict:
    return c._get(c.regional_url(f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"))

def account_by_puuid(c: RiotClient, puuid: str) -> Dict:
    return c._get(c.regional_url(f"/riot/account/v1/accounts/by-puuid/{puuid}"))

def account_active_shard(c: RiotClient, game: str, puuid: str) -> Dict:
    return c._get(c.regional_url(f"/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}"))

# Summoner
def summoner_by_puuid(c: RiotClient, puuid: str) -> Dict:
    return c._get(c.platform_url(f"/lol/summoner/v4/summoners/by-puuid/{puuid}"))

def summoner_by_id(c: RiotClient, summoner_id: str) -> Dict:
    return c._get(c.platform_url(f"/lol/summoner/v4/summoners/{summoner_id}"))

# Champion
def champion_rotation(c: RiotClient) -> Dict:
    return c._get(c.platform_url("/lol/platform/v3/champion-rotations"))

# Champion Mastery
def champion_mastery_all(c: RiotClient, puuid: str) -> List[Dict]:
    return c._get(c.platform_url(f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"))

def champion_mastery_by_champion(c: RiotClient, puuid: str, champion_id: int) -> Dict:
    return c._get(c.platform_url(f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}"))

def champion_mastery_top(c: RiotClient, puuid: str, count: int) -> List[Dict]:
    return c._get(c.platform_url(f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"), params={"count": count})

def champion_mastery_score(c: RiotClient, puuid: str) -> int:
    return c._get(c.platform_url(f"/lol/champion-mastery/v4/scores/by-puuid/{puuid}"))

# Match
def match_ids_by_puuid(c: RiotClient, puuid: str, start: int, count: int) -> List[str]:
    return c._get(c.regional_url(f"/lol/match/v5/matches/by-puuid/{puuid}/ids"), params={"start": start, "count": count})

def match_by_id(c: RiotClient, match_id: str) -> Dict:
    return c._get(c.regional_url(f"/lol/match/v5/matches/{match_id}"))

def match_timeline(c: RiotClient, match_id: str) -> Dict:
    return c._get(c.regional_url(f"/lol/match/v5/matches/{match_id}/timeline"))

# League
def league_by_summoner(c: RiotClient, summoner_id: str) -> List[Dict]:
    return c._get(c.platform_url(f"/lol/league/v4/entries/by-summoner/{summoner_id}"))

def league_entries(c: RiotClient, queue: str, tier: str, division: str, page: int) -> List[Dict]:
    return c._get(c.platform_url(f"/lol/league/v4/entries/{queue}/{tier}/{division}"), params={"page": page})

def league_by_league_id(c: RiotClient, league_id: str) -> Dict:
    return c._get(c.platform_url(f"/lol/league/v4/leagues/{league_id}"))

def league_challenger(c: RiotClient, queue: str) -> Dict:
    return c._get(c.platform_url(f"/lol/league/v4/challengerleagues/by-queue/{queue}"))

def league_grandmaster(c: RiotClient, queue: str) -> Dict:
    return c._get(c.platform_url(f"/lol/league/v4/grandmasterleagues/by-queue/{queue}"))

def league_master(c: RiotClient, queue: str) -> Dict:
    return c._get(c.platform_url(f"/lol/league/v4/masterleagues/by-queue/{queue}"))

# League EXP
def league_exp_entries(c: RiotClient, queue: str, tier: str, division: str, page: int) -> List[Dict]:
    return c._get(c.platform_url(f"/lol/league-exp/v4/entries/{queue}/{tier}/{division}"), params={"page": page})
