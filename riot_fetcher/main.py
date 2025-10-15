import os
import sys
import json
import logging
import argparse
from riotkit.config import load_settings
from riotkit.client import RiotClient
from riotkit.endpoints import *
from riotkit.fetcher import diagnose, fetch_profile
from riotkit.io import save_json

def build_logger(level: str):
    logging.basicConfig(level=getattr(logging, level.upper(), 20), format="%(asctime)s %(levelname)s %(message)s")

def main():
    p = argparse.ArgumentParser(description="Riot API CLI - Complete endpoint coverage")
    p.add_argument("--platform", default="euw1", help="Platform region (euw1, na1, etc.)")
    p.add_argument("--region", default="europe", help="Regional routing (europe, americas, asia)")
    p.add_argument("--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)")
    sub = p.add_subparsers(dest="cmd", help="Available commands")

    # Diagnose
    sp = sub.add_parser("diagnose", help="Check API key and platform status")
    sp.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # Account
    ap = sub.add_parser("account", help="Account operations")
    asp = ap.add_subparsers(dest="sub", help="Account subcommands")
    a1 = asp.add_parser("by-riot-id", help="Get account by Riot ID")
    a1.add_argument("--riot-id", required=True, help="Riot ID (Name#Tag)")
    a1.add_argument("--save", action="store_true", help="Save to file")
    a1.add_argument("--stdout", action="store_true", help="Print output to stdout")
    a2 = asp.add_parser("by-puuid", help="Get account by PUUID")
    a2.add_argument("--puuid", required=True, help="Player PUUID")
    a2.add_argument("--save", action="store_true", help="Save to file")
    a2.add_argument("--stdout", action="store_true", help="Print output to stdout")
    a3 = asp.add_parser("active-shard", help="Get active shard")
    a3.add_argument("--game", default="lol", help="Game (default: lol)")
    a3.add_argument("--puuid", required=True, help="Player PUUID")
    a3.add_argument("--save", action="store_true", help="Save to file")
    a3.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # Summoner
    su = sub.add_parser("summoner", help="Summoner operations")
    ssp = su.add_subparsers(dest="sub", help="Summoner subcommands")
    s1 = ssp.add_parser("by-puuid", help="Get summoner by PUUID")
    s1.add_argument("--puuid", required=True, help="Player PUUID")
    s1.add_argument("--save", action="store_true", help="Save to file")
    s1.add_argument("--stdout", action="store_true", help="Print output to stdout")
    s2 = ssp.add_parser("by-id", help="Get summoner by ID")
    s2.add_argument("--summoner-id", required=True, help="Summoner ID")
    s2.add_argument("--save", action="store_true", help="Save to file")
    s2.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # Champion
    ch = sub.add_parser("champion", help="Champion operations")
    chsp = ch.add_subparsers(dest="sub", help="Champion subcommands")
    cr = chsp.add_parser("rotation", help="Get champion rotations")
    cr.add_argument("--save", action="store_true", help="Save to file")
    cr.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # Champion Mastery
    cm = sub.add_parser("cm", help="Champion mastery operations")
    cmsp = cm.add_subparsers(dest="sub", help="Champion mastery subcommands")
    cma = cmsp.add_parser("all", help="Get all champion masteries")
    cma.add_argument("--puuid", required=True, help="Player PUUID")
    cma.add_argument("--save", action="store_true", help="Save to file")
    cma.add_argument("--stdout", action="store_true", help="Print output to stdout")
    cmb = cmsp.add_parser("by-champion", help="Get mastery for specific champion")
    cmb.add_argument("--puuid", required=True, help="Player PUUID")
    cmb.add_argument("--champion-id", type=int, required=True, help="Champion ID")
    cmb.add_argument("--save", action="store_true", help="Save to file")
    cmb.add_argument("--stdout", action="store_true", help="Print output to stdout")
    cmt = cmsp.add_parser("top", help="Get top champion masteries")
    cmt.add_argument("--puuid", required=True, help="Player PUUID")
    cmt.add_argument("--count", type=int, default=3, help="Number of top champions")
    cmt.add_argument("--save", action="store_true", help="Save to file")
    cmt.add_argument("--stdout", action="store_true", help="Print output to stdout")
    cms = cmsp.add_parser("score", help="Get total mastery score")
    cms.add_argument("--puuid", required=True, help="Player PUUID")
    cms.add_argument("--save", action="store_true", help="Save to file")
    cms.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # Match
    m = sub.add_parser("match", help="Match operations")
    msp = m.add_subparsers(dest="sub", help="Match subcommands")
    mi = msp.add_parser("ids", help="Get match IDs")
    mi.add_argument("--puuid", required=True, help="Player PUUID")
    mi.add_argument("--start", type=int, default=0, help="Start index")
    mi.add_argument("--count", type=int, default=20, help="Number of matches")
    mi.add_argument("--save", action="store_true", help="Save to file")
    mi.add_argument("--stdout", action="store_true", help="Print output to stdout")
    mg = msp.add_parser("get", help="Get match details")
    mg.add_argument("--match-id", required=True, help="Match ID")
    mg.add_argument("--save", action="store_true", help="Save to file")
    mg.add_argument("--stdout", action="store_true", help="Print output to stdout")
    mt = msp.add_parser("timeline", help="Get match timeline")
    mt.add_argument("--match-id", required=True, help="Match ID")
    mt.add_argument("--save", action="store_true", help="Save to file")
    mt.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # League
    l = sub.add_parser("league", help="League operations")
    lsp = l.add_subparsers(dest="sub", help="League subcommands")
    l1 = lsp.add_parser("by-summoner", help="Get league entries by summoner")
    l1.add_argument("--summoner-id", required=True, help="Summoner ID")
    l1.add_argument("--save", action="store_true", help="Save to file")
    l1.add_argument("--stdout", action="store_true", help="Print output to stdout")
    l2 = lsp.add_parser("entries", help="Get league entries by queue/tier/division")
    l2.add_argument("--queue", required=True, help="Queue type (RANKED_SOLO_5x5, etc.)")
    l2.add_argument("--tier", required=True, help="Tier (DIAMOND, PLATINUM, etc.)")
    l2.add_argument("--division", required=True, help="Division (I, II, III, IV)")
    l2.add_argument("--page", type=int, default=1, help="Page number")
    l2.add_argument("--save", action="store_true", help="Save to file")
    l2.add_argument("--stdout", action="store_true", help="Print output to stdout")
    l3 = lsp.add_parser("by-league-id", help="Get league by ID")
    l3.add_argument("--league-id", required=True, help="League ID")
    l3.add_argument("--save", action="store_true", help="Save to file")
    l3.add_argument("--stdout", action="store_true", help="Print output to stdout")
    lc = lsp.add_parser("challenger", help="Get challenger league")
    lc.add_argument("--queue", required=True, help="Queue type")
    lc.add_argument("--save", action="store_true", help="Save to file")
    lc.add_argument("--stdout", action="store_true", help="Print output to stdout")
    lg = lsp.add_parser("grandmaster", help="Get grandmaster league")
    lg.add_argument("--queue", required=True, help="Queue type")
    lg.add_argument("--save", action="store_true", help="Save to file")
    lg.add_argument("--stdout", action="store_true", help="Print output to stdout")
    lm = lsp.add_parser("master", help="Get master league")
    lm.add_argument("--queue", required=True, help="Queue type")
    lm.add_argument("--save", action="store_true", help="Save to file")
    lm.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # League EXP
    le = sub.add_parser("league-exp", help="League EXP operations")
    les = le.add_subparsers(dest="sub", help="League EXP subcommands")
    le1 = les.add_parser("entries", help="Get league EXP entries")
    le1.add_argument("--queue", required=True, help="Queue type")
    le1.add_argument("--tier", required=True, help="Tier")
    le1.add_argument("--division", required=True, help="Division")
    le1.add_argument("--page", type=int, default=1, help="Page number")
    le1.add_argument("--save", action="store_true", help="Save to file")
    le1.add_argument("--stdout", action="store_true", help="Print output to stdout")

    # Profile (legacy)
    pf = sub.add_parser("profile", help="Get complete profile (legacy)")
    pf.add_argument("--riot-id", required=True, help="Riot ID (Name#Tag)")
    pf.add_argument("--count", type=int, default=10, help="Number of matches")
    pf.add_argument("--save", action="store_true", help="Save to file")
    pf.add_argument("--stdout", action="store_true", help="Print output to stdout")

    r = p.parse_args()
    build_logger(r.log_level)
    s = load_settings()
    c = RiotClient(s.api_key, r.platform, r.region)

    # Helper function to save data
    def save_data(data, category, stem):
        if getattr(r, 'stdout', False):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            filename = save_json(category, stem, data)
            print(f"Saved to {filename}")

    # Route commands
    if r.cmd == "diagnose":
        out = diagnose(c)
        save_data(out, "status", "diagnose")
    elif r.cmd == "account" and r.sub == "by-riot-id":
        game, tag = r.riot_id.split("#", 1)
        out = account_by_riot_id(c, game, tag)
        save_data(out, "account", f"by-riot-id_{game}_{tag}")
    elif r.cmd == "account" and r.sub == "by-puuid":
        out = account_by_puuid(c, r.puuid)
        save_data(out, "account", f"by-puuid_{r.puuid}")
    elif r.cmd == "account" and r.sub == "active-shard":
        out = account_active_shard(c, r.game, r.puuid)
        save_data(out, "account", f"active-shard_{r.game}_{r.puuid}")
    elif r.cmd == "summoner" and r.sub == "by-puuid":
        out = summoner_by_puuid(c, r.puuid)
        save_data(out, "summoner", f"by-puuid_{r.puuid}")
    elif r.cmd == "summoner" and r.sub == "by-id":
        out = summoner_by_id(c, r.summoner_id)
        save_data(out, "summoner", f"by-id_{r.summoner_id}")
    elif r.cmd == "champion" and r.sub == "rotation":
        out = champion_rotation(c)
        save_data(out, "champion", "rotations")
    elif r.cmd == "cm" and r.sub == "all":
        out = champion_mastery_all(c, r.puuid)
        save_data(out, "champion-mastery", f"all_{r.puuid}")
    elif r.cmd == "cm" and r.sub == "by-champion":
        out = champion_mastery_by_champion(c, r.puuid, r.champion_id)
        save_data(out, "champion-mastery", f"one_{r.puuid}_{r.champion_id}")
    elif r.cmd == "cm" and r.sub == "top":
        out = champion_mastery_top(c, r.puuid, r.count)
        save_data(out, "champion-mastery", f"top_{r.puuid}_{r.count}")
    elif r.cmd == "cm" and r.sub == "score":
        out = champion_mastery_score(c, r.puuid)
        save_data(out, "champion-mastery", f"score_{r.puuid}")
    elif r.cmd == "match" and r.sub == "ids":
        out = match_ids_by_puuid(c, r.puuid, r.start, r.count)
        save_data(out, "match", f"ids_{r.puuid}_{r.start}_{r.count}")
    elif r.cmd == "match" and r.sub == "get":
        out = match_by_id(c, r.match_id)
        save_data(out, "match", f"get_{r.match_id}")
    elif r.cmd == "match" and r.sub == "timeline":
        out = match_timeline(c, r.match_id)
        save_data(out, "match", f"timeline_{r.match_id}")
    elif r.cmd == "league" and r.sub == "by-summoner":
        out = league_by_summoner(c, r.summoner_id)
        save_data(out, "league", f"entries_summ_{r.summoner_id}")
    elif r.cmd == "league" and r.sub == "entries":
        out = league_entries(c, r.queue, r.tier, r.division, r.page)
        save_data(out, "league", f"entries_{r.queue}_{r.tier}_{r.division}_{r.page}")
    elif r.cmd == "league" and r.sub == "by-league-id":
        out = league_by_league_id(c, r.league_id)
        save_data(out, "league", f"by-league-id_{r.league_id}")
    elif r.cmd == "league" and r.sub == "challenger":
        out = league_challenger(c, r.queue)
        save_data(out, "league", f"challenger_{r.queue}")
    elif r.cmd == "league" and r.sub == "grandmaster":
        out = league_grandmaster(c, r.queue)
        save_data(out, "league", f"grandmaster_{r.queue}")
    elif r.cmd == "league" and r.sub == "master":
        out = league_master(c, r.queue)
        save_data(out, "league", f"master_{r.queue}")
    elif r.cmd == "league-exp" and r.sub == "entries":
        out = league_exp_entries(c, r.queue, r.tier, r.division, r.page)
        save_data(out, "league-exp", f"entries_{r.queue}_{r.tier}_{r.division}_{r.page}")
    elif r.cmd == "profile":
        out = fetch_profile(c, r.riot_id, r.count)
        save_data(out, "profile", f"profile_{r.riot_id.replace('#', '_')}")
    else:
        logging.getLogger("riot").error("Invalid command")
        p.print_help()
        sys.exit(2)

if __name__ == "__main__":
    main()