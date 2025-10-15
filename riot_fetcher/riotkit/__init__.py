__all__ = [
    "RiotError",
    "Settings",
    "load_settings",
    "RiotClient",
    # Status
    "status_probe",
    # Account
    "account_by_riot_id",
    "account_by_puuid", 
    "account_active_shard",
    # Summoner
    "summoner_by_puuid",
    "summoner_by_id",
    # Champion
    "champion_rotation",
    # Champion Mastery
    "champion_mastery_all",
    "champion_mastery_by_champion",
    "champion_mastery_top",
    "champion_mastery_score",
    # Match
    "match_ids_by_puuid",
    "match_by_id",
    "match_timeline",
    # League
    "league_by_summoner",
    "league_entries",
    "league_by_league_id",
    "league_challenger",
    "league_grandmaster",
    "league_master",
    # League EXP
    "league_exp_entries",
    # Fetcher
    "fetch_profile",
]

class RiotError(Exception):
    pass
