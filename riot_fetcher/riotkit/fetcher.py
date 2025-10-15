import logging
from typing import Dict, List, Tuple
from . import RiotError
from .client import RiotClient
from .endpoints import status_probe, account_by_riot_id, summoner_by_puuid, match_ids_by_puuid, match_by_id

def parse_riot_id(riot_id: str) -> Tuple[str, str]:
    if "#" not in riot_id:
        raise RiotError("riot-id must be 'Name#Tag'")
    n, t = riot_id.split("#", 1)
    n = n.strip(); t = t.strip()
    if not n or not t:
        raise RiotError("riot-id must be 'Name#Tag'")
    return n, t

def diagnose(c: RiotClient) -> Dict:
    try:
        s = status_probe(c)
        return {"ok": True, "status": s.get("id", "unknown")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def fetch_profile(c: RiotClient, riot_id: str, count: int) -> Dict:
    log = logging.getLogger("riot")
    n, t = parse_riot_id(riot_id)
    acc = account_by_riot_id(c, n, t)
    puuid = acc.get("puuid")
    log.info("account gameName=%s tag=%s", acc.get("gameName"), acc.get("tagLine"))
    summ = summoner_by_puuid(c, puuid)
    log.info("summoner id=%s level=%s", summ.get("id"), summ.get("summonerLevel"))
    ids: List[str] = match_ids_by_puuid(c, puuid, 0, count)
    log.info("match_ids=%s", len(ids))
    out = []
    for i, mid in enumerate(ids):
        try:
            m = match_by_id(c, mid)
            part = [p for p in m.get("info", {}).get("participants", []) if p.get("puuid") == puuid]
            out.append({"match_id": mid, "participant": part[0] if part else None, "duration": m.get("info", {}).get("gameDuration")})
            log.debug("fetched %s/%s id=%s", i + 1, len(ids), mid)
        except Exception as e:
            log.error("match error id=%s %s", mid, str(e))
    return {"account": acc, "summoner": summ, "matches": out}
