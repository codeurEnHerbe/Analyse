# 🎮 League of Legends Data Features - Complete API Reference

This document lists **ALL** available data that can be retrieved through the Riot API for League of Legends analysis. The data is incredibly rich and covers every aspect of gameplay, from individual player performance to team strategies and match outcomes.

---

## 📊 **MATCH DATA** (`/lol/match/v5/matches/{matchId}`)

### 🎯 **Match Information**
- **`gameId`** - Unique match identifier
- **`gameDuration`** - Match duration in seconds
- **`gameCreation`** - Match start timestamp
- **`gameStartTimestamp`** - Exact game start time
- **`gameEndTimestamp`** - Exact game end time
- **`gameMode`** - Game mode (CLASSIC, ARAM, etc.)
- **`gameType`** - Game type (MATCHED_GAME, CUSTOM_GAME, etc.)
- **`gameVersion`** - Patch version used
- **`mapId`** - Map identifier (11 = Summoner's Rift)
- **`platformId`** - Platform where match was played
- **`queueId`** - Queue type (420 = Ranked Solo/Duo, 440 = Ranked Flex, etc.)
- **`seasonId`** - Season identifier
- **`tournamentCode`** - Tournament code (if applicable)

### 🏆 **Team Statistics**
- **`teamId`** - Team identifier (100 = Blue, 200 = Red)
- **`win`** - Victory status (true/false)
- **`firstBlood`** - First blood achievement
- **`firstTower`** - First tower destroyed
- **`firstInhibitor`** - First inhibitor destroyed
- **`firstBaron`** - First Baron Nashor kill
- **`firstDragon`** - First Dragon kill
- **`firstRiftHerald`** - First Rift Herald kill
- **`towerKills`** - Total towers destroyed
- **`inhibitorKills`** - Total inhibitors destroyed
- **`baronKills`** - Total Baron Nashor kills
- **`dragonKills`** - Total Dragon kills
- **`riftHeraldKills`** - Total Rift Herald kills
- **`totalKills`** - Total team kills
- **`totalDeaths`** - Total team deaths
- **`totalAssists`** - Total team assists
- **`totalGold`** - Total gold earned
- **`totalDamageDealt`** - Total damage dealt
- **`totalDamageTaken`** - Total damage taken
- **`totalHeal`** - Total healing done
- **`totalShieldedOnTeammates`** - Total shields given to teammates
- **`totalMinionsKilled`** - Total minions killed
- **`totalNeutralMinionsKilled`** - Total neutral monsters killed
- **`totalTimeCCDealt`** - Total crowd control time dealt
- **`totalTimeSpentDead`** - Total time spent dead
- **`visionScore`** - Team vision score
- **`wardsPlaced`** - Total wards placed
- **`wardsKilled`** - Total enemy wards killed
- **`visionWardsBoughtInGame`** - Control wards purchased

---

## 👤 **PARTICIPANT DATA** (Individual Player Statistics)

### 🎮 **Player Identity**
- **`puuid`** - Player unique identifier
- **`summonerId`** - Summoner ID
- **`summonerName`** - In-game summoner name
- **`participantId`** - Participant number (1-10)
- **`teamId`** - Team identifier (100/200)
- **`championId`** - Champion played
- **`championName`** - Champion name
- **`championTransform`** - Champion transformation (for Kayn, etc.)
- **`teamPosition`** - Lane position (TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY)
- **`individualPosition`** - Actual position played
- **`role`** - Role (SOLO, NONE, DUO, SUPPORT, CARRY)
- **`lane`** - Lane played
- **`spell1Id`** - First summoner spell
- **`spell2Id`** - Second summoner spell

### ⚔️ **Combat Statistics**
- **`kills`** - Kills achieved
- **`deaths`** - Deaths suffered
- **`assists`** - Assists made
- **`kda`** - Kill/Death/Assist ratio
- **`killParticipation`** - Kill participation percentage
- **`largestKillingSpree`** - Largest killing spree
- **`largestMultiKill`** - Largest multi-kill
- **`killingSprees`** - Number of killing sprees
- **`doubleKills`** - Double kills
- **`tripleKills`** - Triple kills
- **`quadraKills`** - Quadra kills
- **`pentaKills`** - Penta kills
- **`unrealKills`** - Unreal kills (6+ kills in a row)

### 💰 **Gold & Economy**
- **`goldEarned`** - Total gold earned
- **`goldSpent`** - Total gold spent
- **`goldPerMinute`** - Gold per minute
- **`goldAt10`** - Gold at 10 minutes
- **`goldAt15`** - Gold at 15 minutes
- **`goldAt20`** - Gold at 20 minutes
- **`goldDiffAt10`** - Gold difference vs opponent at 10 min
- **`goldDiffAt15`** - Gold difference vs opponent at 15 min
- **`goldDiffAt20`** - Gold difference vs opponent at 20 min

### 🎯 **Damage Statistics**
- **`totalDamageDealt`** - Total damage dealt
- **`totalDamageDealtToChampions`** - Damage to champions
- **`totalDamageDealtToTurrets`** - Damage to turrets
- **`totalDamageDealtToObjectives`** - Damage to objectives
- **`totalDamageTaken`** - Total damage taken
- **`physicalDamageDealt`** - Physical damage dealt
- **`physicalDamageDealtToChampions`** - Physical damage to champions
- **`physicalDamageTaken`** - Physical damage taken
- **`magicDamageDealt`** - Magic damage dealt
- **`magicDamageDealtToChampions`** - Magic damage to champions
- **`magicDamageTaken`** - Magic damage taken
- **`trueDamageDealt`** - True damage dealt
- **`trueDamageDealtToChampions`** - True damage to champions
- **`trueDamageTaken`** - True damage taken
- **`damageDealtToBuildings`** - Damage to buildings
- **`damageDealtToObjectives`** - Damage to objectives
- **`damageSelfMitigated`** - Damage self-mitigated

### 🛡️ **Defensive Statistics**
- **`totalHeal`** - Total healing done
- **`totalHealsOnTeammates`** - Healing done to teammates
- **`totalShieldedOnTeammates`** - Shields given to teammates
- **`totalUnitsHealed`** - Total units healed
- **`damageSelfMitigated`** - Damage self-mitigated
- **`totalTimeSpentDead`** - Total time spent dead
- **`timeCCingOthers`** - Time spent crowd controlling others
- **`totalTimeCCDealt`** - Total crowd control time dealt

### 👁️ **Vision & Map Control**
- **`visionScore`** - Vision score
- **`visionWardsBoughtInGame`** - Control wards purchased
- **`sightWardsBoughtInGame`** - Sight wards purchased
- **`wardsPlaced`** - Wards placed
- **`wardsKilled`** - Enemy wards destroyed
- **`wardsDestroyed`** - Wards destroyed
- **`detectorWardsPlaced`** - Control wards placed
- **`visionWardsBoughtInGame`** - Vision wards bought

### 🏃 **Movement & Positioning**
- **`totalDistanceTraveled`** - Total distance traveled
- **`longestTimeSpentLiving`** - Longest time alive
- **`timeCCingOthers`** - Time crowd controlling others
- **`totalTimeSpentDead`** - Total time dead
- **`totalTimeSpentDead`** - Time spent dead

### 🎯 **Farming & Objectives**
- **`totalMinionsKilled`** - Total minions killed
- **`neutralMinionsKilled`** - Neutral monsters killed
- **`neutralMinionsKilledTeamJungle`** - Team jungle monsters killed
- **`neutralMinionsKilledEnemyJungle`** - Enemy jungle monsters killed
- **`totalMinionsKilled`** - Total minions killed
- **`csPerMinute`** - Creep score per minute
- **`csAt10`** - CS at 10 minutes
- **`csAt15`** - CS at 15 minutes
- **`csAt20`** - CS at 20 minutes
- **`csDiffAt10`** - CS difference vs opponent at 10 min
- **`csDiffAt15`** - CS difference vs opponent at 15 min
- **`csDiffAt20`** - CS difference vs opponent at 20 min

### 📈 **Experience & Leveling**
- **`champLevel`** - Champion level reached
- **`totalExperience`** - Total experience gained
- **`xpAt10`** - Experience at 10 minutes
- **`xpAt15`** - Experience at 15 minutes
- **`xpAt20`** - Experience at 20 minutes
- **`xpDiffAt10`** - Experience difference vs opponent at 10 min
- **`xpDiffAt15`** - Experience difference vs opponent at 15 min
- **`xpDiffAt20`** - Experience difference vs opponent at 20 min

---

## 🎒 **ITEMS & BUILD DATA**

### 🛒 **Items Purchased**
- **`item0`** - Item slot 0
- **`item1`** - Item slot 1
- **`item2`** - Item slot 2
- **`item3`** - Item slot 3
- **`item4`** - Item slot 4
- **`item5`** - Item slot 5
- **`item6`** - Item slot 6 (boots)
- **`consumablesPurchased`** - Consumables purchased
- **`itemsPurchased`** - Total items purchased
- **`itemPurchases`** - Individual item purchases
- **`itemSells`** - Items sold
- **`totalItemsPurchased`** - Total items bought

### 💎 **Runes & Masteries**
- **`perkPrimaryStyle`** - Primary rune tree
- **`perkSubStyle`** - Secondary rune tree
- **`perk0`** - Keystone rune
- **`perk1`** - Primary rune 1
- **`perk2`** - Primary rune 2
- **`perk3`** - Primary rune 3
- **`perk4`** - Secondary rune 1
- **`perk5`** - Secondary rune 2
- **`statPerk0`** - Stat rune 1
- **`statPerk1`** - Stat rune 2
- **`statPerk2`** - Stat rune 3

---

## ⏰ **TIMELINE DATA** (`/lol/match/v5/matches/{matchId}/timeline`)

### 📊 **Frame-by-Frame Data**
- **`frameInterval`** - Time between frames (1 minute)
- **`frames`** - Array of game frames
- **`participantFrames`** - Individual player data per frame
- **`events`** - Game events per frame
- **`timestamp`** - Frame timestamp

### 🎯 **Per-Minute Statistics**
- **`goldPerMinute`** - Gold per minute
- **`csPerMinute`** - CS per minute
- **`damagePerMinute`** - Damage per minute
- **`healingPerMinute`** - Healing per minute
- **`visionScorePerMinute`** - Vision score per minute

### 📈 **Progression Tracking**
- **`levelProgression`** - Level progression over time
- **`goldProgression`** - Gold progression over time
- **`csProgression`** - CS progression over time
- **`damageProgression`** - Damage progression over time
- **`itemProgression`** - Item build progression
- **`runeProgression`** - Rune progression

---

## 🏆 **LEAGUE & RANKED DATA**

### 🎖️ **Ranked Information**
- **`tier`** - Rank tier (IRON, BRONZE, SILVER, GOLD, PLATINUM, DIAMOND, MASTER, GRANDMASTER, CHALLENGER)
- **`rank`** - Division (I, II, III, IV)
- **`leaguePoints`** - League points
- **`wins`** - Ranked wins
- **`losses`** - Ranked losses
- **`winRate`** - Win rate percentage
- **`hotStreak`** - Currently on hot streak
- **`veteran`** - Veteran status
- **`freshBlood`** - Fresh blood status
- **`inactive`** - Inactive status

### 🏅 **Queue Information**
- **`queueType`** - Queue type (RANKED_SOLO_5x5, RANKED_FLEX_SR, etc.)
- **`summonerId`** - Summoner ID
- **`summonerName`** - Summoner name
- **`leagueId`** - League ID
- **`leagueName`** - League name
- **`promosProgress`** - Promotion series progress
- **`miniSeries`** - Mini series information

---

## 🎮 **CHAMPION DATA**

### 🏆 **Champion Mastery**
- **`championId`** - Champion ID
- **`championLevel`** - Mastery level (1-7)
- **`championPoints`** - Mastery points
- **`championPointsSinceLastLevel`** - Points since last level
- **`championPointsUntilNextLevel`** - Points until next level
- **`chestGranted`** - Chest granted
- **`lastPlayTime`** - Last time played
- **`tokensEarned`** - Tokens earned
- **`championName`** - Champion name

### 🔄 **Champion Rotations**
- **`freeChampionIds`** - Free champions this week
- **`freeChampionIdsForNewPlayers`** - Free champions for new players
- **`maxNewPlayerLevel`** - Max level for new player rotation

---

## 👥 **TEAM & TEAMMATE DATA**

### 🤝 **Teammate Information**
- **`teammateIds`** - Teammate PUUIDs
- **`teammateNames`** - Teammate summoner names
- **`teammateChampions`** - Teammate champions
- **`teammateRoles`** - Teammate roles
- **`teammateKDA`** - Teammate KDA ratios
- **`teammateGold`** - Teammate gold earned
- **`teammateDamage`** - Teammate damage dealt
- **`teammateVision`** - Teammate vision scores

### 🎯 **Team Synergy**
- **`teamComposition`** - Team composition analysis
- **`teamSynergy`** - Team synergy score
- **`teamStrategy`** - Team strategy employed
- **`teamCommunication`** - Team communication indicators

---

## 📊 **ANALYTICS & METRICS**

### 📈 **Performance Metrics**
- **`performanceScore`** - Overall performance score
- **`carryScore`** - Carry potential score
- **`supportScore`** - Support effectiveness score
- **`jungleScore`** - Jungle effectiveness score
- **`laneScore`** - Lane performance score
- **`teamfightScore`** - Teamfight performance score
- **`macroScore`** - Macro play score
- **`microScore`** - Micro play score

### 🎯 **Advanced Statistics**
- **`damagePerGold`** - Damage efficiency per gold
- **`damagePerMinute`** - Damage per minute
- **`goldEfficiency`** - Gold efficiency ratio
- **`killParticipation`** - Kill participation percentage
- **`objectiveParticipation`** - Objective participation
- **`visionControl`** - Vision control effectiveness
- **`mapControl`** - Map control effectiveness

---

## 🔍 **MATCH ANALYSIS DATA**

### 📊 **Game Flow**
- **`earlyGame`** - Early game performance (0-15 min)
- **`midGame`** - Mid game performance (15-30 min)
- **`lateGame`** - Late game performance (30+ min)
- **`gamePhase`** - Current game phase
- **`gameState`** - Game state analysis
- **`momentum`** - Team momentum indicators

### 🎯 **Objective Control**
- **`dragonControl`** - Dragon control percentage
- **`baronControl`** - Baron control percentage
- **`towerControl`** - Tower control percentage
- **`inhibitorControl`** - Inhibitor control percentage
- **`objectiveTiming`** - Objective timing analysis
- **`objectivePriority`** - Objective priority analysis

---

## 🌍 **REGIONAL & PLATFORM DATA**

### 🗺️ **Server Information**
- **`platformId`** - Platform identifier
- **`region`** - Regional identifier
- **`server`** - Server name
- **`timezone`** - Server timezone
- **`locale`** - Server locale
- **`language`** - Server language

### 📊 **Regional Statistics**
- **`regionalRank`** - Regional ranking
- **`regionalPercentile`** - Regional percentile
- **`regionalAverage`** - Regional averages
- **`regionalTrends`** - Regional trends
- **`regionalMeta`** - Regional meta analysis

---

## 🎮 **GAME MODE SPECIFIC DATA**

### 🏆 **Ranked Data**
- **`rankedTier`** - Ranked tier
- **`rankedDivision`** - Ranked division
- **`rankedLP`** - Ranked LP
- **`rankedWins`** - Ranked wins
- **`rankedLosses`** - Ranked losses
- **`rankedWinRate`** - Ranked win rate
- **`rankedStreak`** - Ranked streak
- **`rankedPromos`** - Promotion series

### 🎯 **ARAM Data**
- **`aramChampion`** - ARAM champion
- **`aramBuild`** - ARAM build
- **`aramStrategy`** - ARAM strategy
- **`aramPerformance`** - ARAM performance

### 🏃 **URF Data**
- **`urfChampion`** - URF champion
- **`urfBuild`** - URF build
- **`urfStrategy`** - URF strategy
- **`urfPerformance`** - URF performance

---

## 📱 **REAL-TIME DATA**

### ⚡ **Live Game Data**
- **`currentGame`** - Current game information
- **`liveGameState`** - Live game state
- **`liveGameEvents`** - Live game events
- **`liveGameStats`** - Live game statistics
- **`liveGameTimeline`** - Live game timeline

### 📊 **Spectator Data**
- **`spectatorMode`** - Spectator mode
- **`spectatorData`** - Spectator data
- **`spectatorEvents`** - Spectator events
- **`spectatorStats`** - Spectator statistics

---

## 🎯 **USAGE EXAMPLES**

### 📊 **Basic Match Analysis**
```python
# Get match data
match = match_by_id(client, "match_id")
participant = match["info"]["participants"][0]

# Extract key statistics
kda = f"{participant['kills']}/{participant['deaths']}/{participant['assists']}"
damage = participant['totalDamageDealtToChampions']
gold = participant['goldEarned']
cs = participant['totalMinionsKilled']
vision = participant['visionScore']
```

### 📈 **Advanced Analytics**
```python
# Calculate performance metrics
performance_score = (
    participant['kills'] * 2 +
    participant['assists'] * 1.5 -
    participant['deaths'] * 1 +
    participant['totalDamageDealtToChampions'] / 1000 +
    participant['visionScore'] * 0.5
)

# Calculate efficiency ratios
damage_per_gold = participant['totalDamageDealtToChampions'] / participant['goldEarned']
cs_per_minute = participant['totalMinionsKilled'] / (match['info']['gameDuration'] / 60)
```

### 🎮 **Team Analysis**
```python
# Analyze team composition
team_champions = [p['championName'] for p in team_participants]
team_roles = [p['teamPosition'] for p in team_participants]

# Calculate team statistics
team_kills = sum(p['kills'] for p in team_participants)
team_deaths = sum(p['deaths'] for p in team_participants)
team_assists = sum(p['assists'] for p in team_participants)
```

---

## 🚀 **GETTING STARTED**

### 1. **Install the Toolkit**
```bash
cd riot_fetcher
pip install requests python-dotenv
```

### 2. **Configure API Key**
```bash
# Create .env file
echo "RIOT_API_KEY=your_api_key_here" > .env
```

### 3. **Start Fetching Data**
```bash
# Get player profile
python main.py profile --riot-id "Player#TAG" --count 10

# Get match details
python main.py match get --match-id "match_id_here"

# Get match timeline
python main.py match timeline --match-id "match_id_here"
```

### 4. **Analyze the Data**
```python
import json

# Load match data
with open('data/match/get_match_id.json', 'r') as f:
    match_data = json.load(f)

# Extract participant data
participants = match_data['info']['participants']
for participant in participants:
    print(f"Player: {participant['summonerName']}")
    print(f"Champion: {participant['championName']}")
    print(f"KDA: {participant['kills']}/{participant['deaths']}/{participant['assists']}")
    print(f"Damage: {participant['totalDamageDealtToChampions']}")
    print(f"Gold: {participant['goldEarned']}")
    print(f"CS: {participant['totalMinionsKilled']}")
    print(f"Vision: {participant['visionScore']}")
    print("---")
```

---

## 🎯 **CONCLUSION**

The Riot API provides **incredibly rich data** for League of Legends analysis:

- **🎮 100+ individual player statistics** per match
- **📊 50+ team statistics** per match  
- **⏰ Frame-by-frame timeline data** for detailed analysis
- **🏆 Complete ranked and mastery information**
- **👥 Teammate and team synergy data**
- **🌍 Multi-regional support** for global analysis
- **📈 Advanced performance metrics** and analytics

This data can be used for:
- **📊 Performance analysis** and improvement
- **🎯 Meta analysis** and strategy development
- **🏆 Ranked progression** tracking
- **👥 Team composition** optimization
- **📈 Statistical research** and data science
- **🎮 Coaching** and player development
- **📱 Application development** and tools

**The possibilities are endless!** 🚀
