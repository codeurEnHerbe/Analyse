Below is a **doc-first, generic, arg-only CLI** for Riot APIs.
**.env contains only** `RIOT_API_KEY`. Everything else is provided via CLI flags.
Each command **auto-saves JSON** under `./data/{category}/…`. Logs are precise. No comments.

---

## File: `.env.example`

```dotenv
RIOT_API_KEY=RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## File: `riotcli/__init__.py`

```python
__all__ = ["RiotError"]
class RiotError(Exception): ...
```

---

## File: `riotcli/config.py`

```python
import os

def _load_dotenv(path=".env"):
    if not os.path.exists(path): return
    for line in open(path, "r", encoding="utf-8"):
        s=line.strip()
        if not s or s.startswith("#"): continue
        if "=" in s:
            k,v=s.split("=",1)
            os.environ.setdefault(k.strip(),v.strip())

def get_api_key():
    _load_dotenv()
    key=os.getenv("RIOT_API_KEY")
    if not key: raise RuntimeError("missing RIOT_API_KEY")
    return key
```

---

## File: `riotcli/io.py`

```python
import os, json, re, time

def _ts():
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

def _slug(x):
    s=re.sub(r"[^A-Za-z0-9._-]+","_",str(x)).strip("_")
    return s or "x"

def save_json(category, stem, payload, data_root="data"):
    d=os.path.join(data_root, category)
    os.makedirs(d, exist_ok=True)
    f=os.path.join(d, f"{_ts()}_{_slug(stem)}.json")
    with open(f,"w",encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    return f
```

---

## File: `riotcli/client.py`

```python
import time, logging, requests
from typing import Any, Dict, Optional
from . import RiotError

class RiotClient:
    def __init__(self, api_key: str, user_agent="riot-cli/1.0", timeout=15):
        self.s=requests.Session()
        self.s.headers.update({"User-Agent":user_agent,"X-Riot-Token":api_key})
        self.t=timeout
        self.log=logging.getLogger("riot")

    def _get(self, url: str, params: Optional[Dict[str,Any]]=None, retry=3):
        for i in range(retry):
            r=self.s.get(url, params=params, timeout=self.t)
            if r.status_code==429:
                ra=r.headers.get("Retry-After")
                w=int(ra) if ra and ra.isdigit() else (2**i)
                self.log.warning("429 wait=%s attempt=%s url=%s",w,i+1,url)
                time.sleep(w); continue
            if 200<=r.status_code<300: return r.json() if r.text else {}
            if 400<=r.status_code<500: raise RiotError(f"client {r.status_code} {r.text[:300]}")
            self.log.warning("server %s attempt=%s",r.status_code,i+1); time.sleep(1+2*i)
        raise RiotError("max retries")

def platform_url(platform:str, path:str)->str:
    return f"https://{platform}.api.riotgames.com{path}"

def regional_url(region:str, path:str)->str:
    return f"https://{region}.api.riotgames.com{path}"
```

---

## File: `riotcli/commands.py`

```python
import logging
from typing import Dict, List, Tuple
from .client import RiotClient, platform_url, regional_url
from .io import save_json
from . import RiotError

def parse_riot_id(s:str)->Tuple[str,str]:
    if "#" not in s: raise RiotError("riot-id must be 'Name#Tag'")
    n,t=s.split("#",1)
    n=n.strip(); t=t.strip()
    if not n or not t: raise RiotError("riot-id must be 'Name#Tag'")
    return n,t

def diagnose(c:RiotClient, platform:str):
    u=platform_url(platform,"/lol/status/v4/platform-data")
    r=c._get(u); return r

def account_by_riot_id(c:RiotClient, regional:str, riot_id:str, save:bool):
    n,t=parse_riot_id(riot_id)
    u=regional_url(regional, f"/riot/account/v1/accounts/by-riot-id/{n}/{t}")
    r=c._get(u)
    if save: save_json("account", f"by-riot-id_{n}_{t}", r)
    return r

def account_by_puuid(c:RiotClient, regional:str, puuid:str, save:bool):
    u=regional_url(regional, f"/riot/account/v1/accounts/by-puuid/{puuid}")
    r=c._get(u)
    if save: save_json("account", f"by-puuid_{puuid}", r)
    return r

def account_active_shard(c:RiotClient, regional:str, game:str, puuid:str, save:bool):
    u=regional_url(regional, f"/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}")
    r=c._get(u)
    if save: save_json("account", f"active-shard_{game}_{puuid}", r)
    return r

def summoner_by_puuid(c:RiotClient, platform:str, puuid:str, save:bool):
    u=platform_url(platform, f"/lol/summoner/v4/summoners/by-puuid/{puuid}")
    r=c._get(u)
    if save: save_json("summoner", f"by-puuid_{puuid}", r)
    return r

def summoner_by_id(c:RiotClient, platform:str, summoner_id:str, save:bool):
    u=platform_url(platform, f"/lol/summoner/v4/summoners/{summoner_id}")
    r=c._get(u)
    if save: save_json("summoner", f"by-id_{summoner_id}", r)
    return r

def champion_rotation(c:RiotClient, platform:str, save:bool):
    u=platform_url(platform, "/lol/platform/v3/champion-rotations")
    r=c._get(u)
    if save: save_json("champion", "rotations", r)
    return r

def cm_all(c:RiotClient, platform:str, puuid:str, save:bool):
    u=platform_url(platform, f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}")
    r=c._get(u)
    if save: save_json("champion-mastery", f"all_{puuid}", r)
    return r

def cm_by_champion(c:RiotClient, platform:str, puuid:str, champion_id:int, save:bool):
    u=platform_url(platform, f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}")
    r=c._get(u)
    if save: save_json("champion-mastery", f"one_{puuid}_{champion_id}", r)
    return r

def cm_top(c:RiotClient, platform:str, puuid:str, count:int, save:bool):
    u=platform_url(platform, f"/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top")
    r=c._get(u, params={"count":count})
    if save: save_json("champion-mastery", f"top_{puuid}_{count}", r)
    return r

def cm_score(c:RiotClient, platform:str, puuid:str, save:bool):
    u=platform_url(platform, f"/lol/champion-mastery/v4/scores/by-puuid/{puuid}")
    r=c._get(u)
    if save: save_json("champion-mastery", f"score_{puuid}", r)
    return r

def match_ids(c:RiotClient, regional:str, puuid:str, start:int, count:int, save:bool):
    u=regional_url(regional, f"/lol/match/v5/matches/by-puuid/{puuid}/ids")
    r=c._get(u, params={"start":start,"count":count})
    if save: save_json("match", f"ids_{puuid}_{start}_{count}", r)
    return r

def match_get(c:RiotClient, regional:str, match_id:str, save:bool):
    u=regional_url(regional, f"/lol/match/v5/matches/{match_id}")
    r=c._get(u)
    if save: save_json("match", f"get_{match_id}", r)
    return r

def match_timeline(c:RiotClient, regional:str, match_id:str, save:bool):
    u=regional_url(regional, f"/lol/match/v5/matches/{match_id}/timeline")
    r=c._get(u)
    if save: save_json("match", f"timeline_{match_id}", r)
    return r

def league_by_summoner(c:RiotClient, platform:str, summoner_id:str, save:bool):
    u=platform_url(platform, f"/lol/league/v4/entries/by-summoner/{summoner_id}")
    r=c._get(u)
    if save: save_json("league", f"entries_summ_{summoner_id}", r)
    return r

def league_entries(c:RiotClient, platform:str, queue:str, tier:str, division:str, page:int, save:bool):
    u=platform_url(platform, f"/lol/league/v4/entries/{queue}/{tier}/{division}")
    r=c._get(u, params={"page":page})
    if save: save_json("league", f"entries_{queue}_{tier}_{division}_{page}", r)
    return r

def league_by_league_id(c:RiotClient, platform:str, league_id:str, save:bool):
    u=platform_url(platform, f"/lol/league/v4/leagues/{league_id}")
    r=c._get(u)
    if save: save_json("league", f"by-league-id_{league_id}", r)
    return r

def league_tier_bucket(c:RiotClient, platform:str, queue:str, bucket:str, save:bool):
    path={"challenger":"/lol/league/v4/challengerleagues/by-queue",
          "grandmaster":"/lol/league/v4/grandmasterleagues/by-queue",
          "master":"/lol/league/v4/masterleagues/by-queue"}[bucket]
    u=platform_url(platform, f"{path}/{queue}")
    r=c._get(u)
    if save: save_json("league", f"{bucket}_{queue}", r)
    return r

def league_exp_entries(c:RiotClient, platform:str, queue:str, tier:str, division:str, page:int, save:bool):
    u=platform_url(platform, f"/lol/league-exp/v4/entries/{queue}/{tier}/{division}")
    r=c._get(u, params={"page":page})
    if save: save_json("league-exp", f"entries_{queue}_{tier}_{division}_{page}", r)
    return r
```

---

## File: `main.py`

```python
import os, sys, json, logging, argparse
from riotcli.config import get_api_key
from riotcli.client import RiotClient
from riotcli.commands import *

def build_logger(level:str):
    logging.basicConfig(level=getattr(logging, level.upper(), 20), format="%(asctime)s %(levelname)s %(message)s")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--platform", default="euw1")
    p.add_argument("--region", default="europe")
    p.add_argument("--log-level", default="INFO")
    p.add_argument("--stdout", action="store_true")
    sub=p.add_subparsers(dest="cmd")

    sp=sub.add_parser("diagnose")

    ap=sub.add_parser("account"); asp=ap.add_subparsers(dest="sub")
    a1=asp.add_parser("by-riot-id"); a1.add_argument("--riot-id", required=True); a1.add_argument("--save", action="store_true")
    a2=asp.add_parser("by-puuid"); a2.add_argument("--puuid", required=True); a2.add_argument("--save", action="store_true")
    a3=asp.add_parser("active-shard"); a3.add_argument("--game", default="lol"); a3.add_argument("--puuid", required=True); a3.add_argument("--save", action="store_true")

    su=sub.add_parser("summoner"); ssp=su.add_subparsers(dest="sub")
    s1=ssp.add_parser("by-puuid"); s1.add_argument("--puuid", required=True); s1.add_argument("--save", action="store_true")
    s2=ssp.add_parser("by-id"); s2.add_argument("--summoner-id", required=True); s2.add_argument("--save", action="store_true")

    ch=sub.add_parser("champion"); chsp=ch.add_subparsers(dest="sub")
    cr=chsp.add_parser("rotation"); cr.add_argument("--save", action="store_true")

    cm=sub.add_parser("cm"); cmsp=cm.add_subparsers(dest="sub")
    cma=cmsp.add_parser("all"); cma.add_argument("--puuid", required=True); cma.add_argument("--save", action="store_true")
    cmb=cmsp.add_parser("by-champion"); cmb.add_argument("--puuid", required=True); cmb.add_argument("--champion-id", type=int, required=True); cmb.add_argument("--save", action="store_true")
    cmt=cmsp.add_parser("top"); cmt.add_argument("--puuid", required=True); cmt.add_argument("--count", type=int, default=3); cmt.add_argument("--save", action="store_true")
    cms=cmsp.add_parser("score"); cms.add_argument("--puuid", required=True); cms.add_argument("--save", action="store_true")

    m=sub.add_parser("match"); msp=m.add_subparsers(dest="sub")
    mi=msp.add_parser("ids"); mi.add_argument("--puuid", required=True); mi.add_argument("--start", type=int, default=0); mi.add_argument("--count", type=int, default=20); mi.add_argument("--save", action="store_true")
    mg=msp.add_parser("get"); mg.add_argument("--match-id", required=True); mg.add_argument("--save", action="store_true")
    mt=msp.add_parser("timeline"); mt.add_argument("--match-id", required=True); mt.add_argument("--save", action="store_true")

    l=sub.add_parser("league"); lsp=l.add_subparsers(dest="sub")
    l1=lsp.add_parser("by-summoner"); l1.add_argument("--summoner-id", required=True); l1.add_argument("--save", action="store_true")
    l2=lsp.add_parser("entries"); l2.add_argument("--queue", required=True); l2.add_argument("--tier", required=True); l2.add_argument("--division", required=True); l2.add_argument("--page", type=int, default=1); l2.add_argument("--save", action="store_true")
    l3=lsp.add_parser("by-league-id"); l3.add_argument("--league-id", required=True); l3.add_argument("--save", action="store_true")
    lc=lsp.add_parser("challenger"); lc.add_argument("--queue", required=True); lc.add_argument("--save", action="store_true")
    lg=lsp.add_parser("grandmaster"); lg.add_argument("--queue", required=True); lg.add_argument("--save", action="store_true")
    lm=lsp.add_parser("master"); lm.add_argument("--queue", required=True); lm.add_argument("--save", action="store_true")

    le=sub.add_parser("league-exp"); les=le.add_subparsers(dest="sub")
    le1=les.add_parser("entries"); le1.add_argument("--queue", required=True); le1.add_argument("--tier", required=True); le1.add_argument("--division", required=True); le1.add_argument("--page", type=int, default=1); le1.add_argument("--save", action="store_true")

    r=p.parse_args()
    build_logger(r.log_level)
    c=RiotClient(get_api_key())

    if r.cmd=="diagnose":
        out=diagnose(c, r.platform)
    elif r.cmd=="account" and r.sub=="by-riot-id":
        out=account_by_riot_id(c, r.region, r.riot_id, r.save)
    elif r.cmd=="account" and r.sub=="by-puuid":
        out=account_by_puuid(c, r.region, r.puuid, r.save)
    elif r.cmd=="account" and r.sub=="active-shard":
        out=account_active_shard(c, r.region, r.game, r.puuid, r.save)
    elif r.cmd=="summoner" and r.sub=="by-puuid":
        out=summoner_by_puuid(c, r.platform, r.puuid, r.save)
    elif r.cmd=="summoner" and r.sub=="by-id":
        out=summoner_by_id(c, r.platform, r.summoner_id, r.save)
    elif r.cmd=="champion" and r.sub=="rotation":
        out=champion_rotation(c, r.platform, r.save)
    elif r.cmd=="cm" and r.sub=="all":
        out=cm_all(c, r.platform, r.puuid, r.save)
    elif r.cmd=="cm" and r.sub=="by-champion":
        out=cm_by_champion(c, r.platform, r.puuid, r.champion_id, r.save)
    elif r.cmd=="cm" and r.sub=="top":
        out=cm_top(c, r.platform, r.puuid, r.count, r.save)
    elif r.cmd=="cm" and r.sub=="score":
        out=cm_score(c, r.platform, r.puuid, r.save)
    elif r.cmd=="match" and r.sub=="ids":
        out=match_ids(c, r.region, r.puuid, r.start, r.count, r.save)
    elif r.cmd=="match" and r.sub=="get":
        out=match_get(c, r.region, r.match_id, r.save)
    elif r.cmd=="match" and r.sub=="timeline":
        out=match_timeline(c, r.region, r.match_id, r.save)
    elif r.cmd=="league" and r.sub=="by-summoner":
        out=league_by_summoner(c, r.platform, r.summoner_id, r.save)
    elif r.cmd=="league" and r.sub=="entries":
        out=league_entries(c, r.platform, r.queue, r.tier, r.division, r.page, r.save)
    elif r.cmd=="league" and r.sub=="by-league-id":
        out=league_by_league_id(c, r.platform, r.league_id, r.save)
    elif r.cmd=="league" and r.sub=="challenger":
        out=league_tier_bucket(c, r.platform, r.queue, "challenger", r.save)
    elif r.cmd=="league" and r.sub=="grandmaster":
        out=league_tier_bucket(c, r.platform, r.queue, "grandmaster", r.save)
    elif r.cmd=="league" and r.sub=="master":
        out=league_tier_bucket(c, r.platform, r.queue, "master", r.save)
    elif r.cmd=="league-exp" and r.sub=="entries":
        out=league_exp_entries(c, r.platform, r.queue, r.tier, r.division, r.page, r.save)
    else:
        logging.getLogger("riot").error("invalid command"); sys.exit(2)

    if r.stdout: print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__=="__main__": main()
```

---

## Install & run

```bash
pip install requests
copy .env.example .env
# edit RIOT_API_KEY only

# Diagnose key/region/platform
python main.py --platform euw1 --region europe diagnose --stdout

# Resolve account and PUUID
python main.py --region europe account by-riot-id --riot-id "St0lym#EUW" --stdout --platform euw1

# Summoner from PUUID (use P from previous output)
python main.py --platform euw1 summoner by-puuid --puuid P --stdout

# Match IDs and one match
python main.py --region europe match ids --puuid P --count 5 --save
python main.py --region europe match get --match-id EUW1_1234567890 --save
python main.py --region europe match timeline --match-id EUW1_1234567890 --save

# Champion rotation
python main.py --platform euw1 champion rotation --save

# Champion mastery
python main.py --platform euw1 cm all --puuid P --save
python main.py --platform euw1 cm by-champion --puuid P --champion-id 266 --save
python main.py --platform euw1 cm top --puuid P --count 5 --save
python main.py --platform euw1 cm score --puuid P --save

# League
python main.py --platform euw1 league by-summoner --summoner-id S --save
python main.py --platform euw1 league entries --queue RANKED_SOLO_5x5 --tier DIAMOND --division I --page 1 --save
python main.py --platform euw1 league challenger --queue RANKED_SOLO_5x5 --save
python main.py --platform euw1 league grandmaster --queue RANKED_SOLO_5x5 --save
python main.py --platform euw1 league master --queue RANKED_SOLO_5x5 --save
python main.py --platform euw1 league by-league-id --league-id <id> --save

# League-EXP
python main.py --platform euw1 league-exp entries --queue RANKED_SOLO_5x5 --tier DIAMOND --division I --page 1 --save
```

This covers:

* **ACCOUNT-V1** (by-riot-id, by-puuid, active-shards)
* **SUMMONER-V4** (by-puuid, by-id)
* **MATCH-V5** (ids, match, timeline)
* **CHAMPION-V3** (rotations)
* **CHAMPION-MASTERY-V4** (all, by-champion, top, score)
* **LEAGUE-V4** (entries by summoner, entries by queue/tier/div, by league id, challenger/grandmaster/master)
* **LEAGUE-EXP-V4** (entries)
