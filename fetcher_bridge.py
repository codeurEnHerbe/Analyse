#!/usr/bin/env python3
"""
KR Analysis Script - All-in-One
===============================

This script downloads and analyzes match data for any player on KR server.
You can choose the player, match depth, and it uses a single analysis_data folder.

Usage:
    python script.py --player "Sard#CASS" --depth 10
    python script.py --player "Sung Jin woo#SOUL" --depth 5
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Set
from pathlib import Path

# Add riot_fetcher to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'riot_fetcher'))

from riotkit.config import load_settings
from riotkit.client import RiotClient
from riotkit.endpoints import (
    account_by_riot_id, summoner_by_puuid, match_ids_by_puuid, 
    match_by_id, match_timeline
)
from riotkit.fetcher import parse_riot_id

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KRAnalysis:
    def __init__(self, player_riot_id: str, match_depth: int = 10, platform: str = "kr", region: str = "asia"):
        """Initialize the analysis."""
        self.player_riot_id = player_riot_id
        self.match_depth = match_depth
        self.platform = platform
        self.region = region
        self.settings = load_settings()
        self.client = RiotClient(
            self.settings.api_key, 
            platform_region=platform, 
            regional_routing=region
        )
        
        # Data storage
        self.downloaded_matches: Set[str] = set()
        self.analyzed_players: Set[str] = set()
        self.match_data: List[Dict] = []
        self.timeline_data: List[Dict] = []
        
        # Create single output directory
        self.output_dir = Path("analysis_data")
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "matches").mkdir(exist_ok=True)
        (self.output_dir / "timelines").mkdir(exist_ok=True)
        (self.output_dir / "analysis").mkdir(exist_ok=True)
        
        logger.info(f"🚀 Analysis initialized for {player_riot_id}")
        logger.info(f"🌍 Platform: {platform} | Region: {region}")
        logger.info(f"📁 Output directory: {self.output_dir.absolute()}")
        logger.info(f"🎯 Match depth: {match_depth}")

    def get_player_puuid(self, riot_id: str) -> str:
        """Get PUUID for a player by Riot ID."""
        try:
            game_name, tag_line = parse_riot_id(riot_id)
            account = account_by_riot_id(self.client, game_name, tag_line)
            puuid = account.get("puuid")
            if not puuid:
                raise ValueError(f"No PUUID found for {riot_id}")
            
            logger.info(f"✅ Found PUUID for {riot_id}")
            return puuid
        except Exception as e:
            logger.error(f"❌ Failed to get PUUID for {riot_id}: {e}")
            raise

    def get_match_ids(self, puuid: str, count: int) -> List[str]:
        """Get match IDs for a player."""
        try:
            match_ids = match_ids_by_puuid(self.client, puuid, start=0, count=count)
            logger.info(f"📊 Found {len(match_ids)} matches for player")
            return match_ids
        except Exception as e:
            logger.error(f"❌ Failed to get match IDs: {e}")
            return []

    def download_match(self, match_id: str) -> Dict:
        """Download match data."""
        if match_id in self.downloaded_matches:
            logger.info(f"⏭️  Match {match_id} already downloaded")
            return None
            
        try:
            logger.info(f"📥 Downloading match {match_id}")
            match_data = match_by_id(self.client, match_id)
            
            # Save match data
            filename = f"match_{match_id}.json"
            filepath = self.output_dir / "matches" / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(match_data, f, indent=2, ensure_ascii=False)
            
            self.downloaded_matches.add(match_id)
            self.match_data.append(match_data)
            
            logger.info(f"✅ Match {match_id} downloaded and saved")
            return match_data
            
        except Exception as e:
            logger.error(f"❌ Failed to download match {match_id}: {e}")
            return None

    def download_timeline(self, match_id: str) -> Dict:
        """Download match timeline data."""
        try:
            logger.info(f"⏰ Downloading timeline for match {match_id}")
            timeline_data = match_timeline(self.client, match_id)
            
            # Save timeline data
            filename = f"timeline_{match_id}.json"
            filepath = self.output_dir / "timelines" / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(timeline_data, f, indent=2, ensure_ascii=False)
            
            self.timeline_data.append(timeline_data)
            
            logger.info(f"✅ Timeline {match_id} downloaded and saved")
            return timeline_data
            
        except Exception as e:
            logger.error(f"❌ Failed to download timeline {match_id}: {e}")
            return None

    def extract_teammates(self, match_data: Dict, player_puuid: str) -> List[Dict]:
        """Extract teammate information from match data."""
        teammates = []
        
        try:
            participants = match_data.get("info", {}).get("participants", [])
            
            # Find player's team
            player_team_id = None
            for participant in participants:
                if participant.get("puuid") == player_puuid:
                    player_team_id = participant.get("teamId")
                    break
            
            if not player_team_id:
                logger.warning("❌ Could not find player's team in match")
                return []
            
            # Extract teammates from the same team
            for participant in participants:
                if (participant.get("teamId") == player_team_id and 
                    participant.get("puuid") != player_puuid):
                    
                    teammate_info = {
                        "puuid": participant.get("puuid"),
                        "summonerName": f"Player_{participant.get('puuid', '')[:8]}",
                        "championId": participant.get("championId"),
                        "championName": participant.get("championName"),
                        "teamPosition": participant.get("teamPosition"),
                        "kills": participant.get("kills", 0),
                        "deaths": participant.get("deaths", 0),
                        "assists": participant.get("assists", 0),
                        "goldEarned": participant.get("goldEarned", 0),
                        "totalDamageDealtToChampions": participant.get("totalDamageDealtToChampions", 0),
                        "visionScore": participant.get("visionScore", 0),
                        "totalMinionsKilled": participant.get("totalMinionsKilled", 0)
                    }
                    teammates.append(teammate_info)
            
            logger.info(f"👥 Found {len(teammates)} teammates")
            return teammates
            
        except Exception as e:
            logger.error(f"❌ Failed to extract teammates: {e}")
            return []

    def analyze_data(self) -> Dict:
        """Analyze the collected data."""
        analysis = {
            "summary": {
                "player": self.player_riot_id,
                "match_depth": self.match_depth,
                "total_matches": len(self.match_data),
                "total_timelines": len(self.timeline_data),
                "unique_players": len(self.analyzed_players),
                "downloaded_at": datetime.now().isoformat()
            },
            "player_stats": {},
            "champion_stats": {},
            "match_analysis": []
        }
        
        # Analyze each match
        for match in self.match_data:
            match_info = match.get("info", {})
            participants = match_info.get("participants", [])
            
            # Extract key metrics
            match_analysis = {
                "matchId": match.get("metadata", {}).get("matchId"),
                "gameDuration": match_info.get("gameDuration"),
                "gameMode": match_info.get("gameMode"),
                "queueId": match_info.get("queueId"),
                "participants": []
            }
            
            for participant in participants:
                player_puuid = participant.get("puuid")
                if player_puuid:
                    # Update player stats
                    if player_puuid not in analysis["player_stats"]:
                        analysis["player_stats"][player_puuid] = {
                            "matches_played": 0,
                            "total_kills": 0,
                            "total_deaths": 0,
                            "total_assists": 0,
                            "total_gold": 0,
                            "total_damage": 0,
                            "champions_played": set()
                        }
                    
                    stats = analysis["player_stats"][player_puuid]
                    stats["matches_played"] += 1
                    stats["total_kills"] += participant.get("kills", 0)
                    stats["total_deaths"] += participant.get("deaths", 0)
                    stats["total_assists"] += participant.get("assists", 0)
                    stats["total_gold"] += participant.get("goldEarned", 0)
                    stats["total_damage"] += participant.get("totalDamageDealtToChampions", 0)
                    stats["champions_played"].add(participant.get("championName", "Unknown"))
                    
                    # Champion stats
                    champion = participant.get("championName")
                    if champion not in analysis["champion_stats"]:
                        analysis["champion_stats"][champion] = {
                            "times_played": 0,
                            "total_kills": 0,
                            "total_deaths": 0,
                            "total_assists": 0
                        }
                    
                    champ_stats = analysis["champion_stats"][champion]
                    champ_stats["times_played"] += 1
                    champ_stats["total_kills"] += participant.get("kills", 0)
                    champ_stats["total_deaths"] += participant.get("deaths", 0)
                    champ_stats["total_assists"] += participant.get("assists", 0)
                
                match_analysis["participants"].append({
                    "puuid": participant.get("puuid"),
                    "championName": participant.get("championName"),
                    "teamPosition": participant.get("teamPosition"),
                    "kills": participant.get("kills", 0),
                    "deaths": participant.get("deaths", 0),
                    "assists": participant.get("assists", 0),
                    "goldEarned": participant.get("goldEarned", 0),
                    "totalDamageDealtToChampions": participant.get("totalDamageDealtToChampions", 0),
                    "visionScore": participant.get("visionScore", 0)
                })
            
            analysis["match_analysis"].append(match_analysis)
        
        # Convert sets to lists for JSON serialization
        for player in analysis["player_stats"]:
            analysis["player_stats"][player]["champions_played"] = list(analysis["player_stats"][player]["champions_played"])
        
        return analysis

    def run_analysis(self):
        """Run the complete analysis."""
        logger.info(f"🎯 Starting analysis for {self.player_riot_id} on {self.platform}/{self.region}")
        
        try:
            # Step 1: Get player PUUID
            player_puuid = self.get_player_puuid(self.player_riot_id)
            self.analyzed_players.add(player_puuid)
            
            # Step 2: Get player's last matches
            logger.info(f"📊 Getting {self.player_riot_id}'s last {self.match_depth} matches...")
            player_match_ids = self.get_match_ids(player_puuid, self.match_depth)
            
            # Step 3: Download player's matches
            logger.info("📥 Downloading player's matches...")
            for match_id in player_match_ids:
                match_data = self.download_match(match_id)
                if match_data:
                    # Download timeline for each match
                    self.download_timeline(match_id)
                    
                    # Extract teammates
                    teammates = self.extract_teammates(match_data, player_puuid)
                    
                    # Step 4: Download teammates' matches
                    for teammate in teammates:
                        teammate_puuid = teammate.get("puuid")
                        teammate_name = teammate.get("summonerName")
                        
                        if teammate_puuid and teammate_puuid not in self.analyzed_players:
                            logger.info(f"👥 Analyzing teammate: {teammate_name}")
                            self.analyzed_players.add(teammate_puuid)
                            
                            # Get teammate's last matches
                            teammate_match_ids = self.get_match_ids(teammate_puuid, self.match_depth)
                            
                            # Download teammate's matches
                            for tm_match_id in teammate_match_ids:
                                if tm_match_id not in self.downloaded_matches:
                                    self.download_match(tm_match_id)
                                    self.download_timeline(tm_match_id)
                                    
                                    # Small delay to respect rate limits
                                    time.sleep(0.1)
            
            # Step 5: Analyze all collected data
            logger.info("📈 Analyzing collected data...")
            analysis = self.analyze_data()
            
            # Save analysis
            analysis_file = self.output_dir / "analysis" / "complete_analysis.json"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            # Save summary
            summary = {
                "download_summary": {
                    "player": self.player_riot_id,
                    "match_depth": self.match_depth,
                    "total_matches_downloaded": len(self.downloaded_matches),
                    "total_timelines_downloaded": len(self.timeline_data),
                    "unique_players_analyzed": len(self.analyzed_players),
                    "completion_time": datetime.now().isoformat(),
                    "output_directory": str(self.output_dir.absolute())
                },
                "expected_vs_actual": {
                    "expected_matches": f"~{self.match_depth * 8} (depth * 8 teammates)",
                    "actual_matches": len(self.downloaded_matches),
                    "efficiency": f"{len(self.downloaded_matches)/(self.match_depth * 8)*100:.1f}%" if len(self.downloaded_matches) > 0 else "0%"
                }
            }
            
            summary_file = self.output_dir / "analysis" / "download_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            logger.info("🎉 Analysis complete!")
            logger.info(f"📊 Downloaded {len(self.downloaded_matches)} matches")
            logger.info(f"👥 Analyzed {len(self.analyzed_players)} unique players")
            logger.info(f"📁 Data saved to: {self.output_dir.absolute()}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            raise

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Multi-Server Analysis Script - All-in-One")
    parser.add_argument("--player", required=True, help="Player Riot ID (e.g., 'Sard#CASS')")
    parser.add_argument("--depth", type=int, default=10, help="Match depth (default: 10)")
    parser.add_argument("--platform", default="kr", help="Platform (kr, euw1, na1, eun1, etc.)")
    parser.add_argument("--region", default="asia", help="Region (asia, europe, americas)")
    parser.add_argument("--test", action="store_true", help="Run test mode (depth=2)")
    
    args = parser.parse_args()
    
    # Override depth for test mode
    if args.test:
        args.depth = 2
        print("Running in TEST MODE (depth=2)")
    
    print(f"Analysis for {args.player}")
    print(f"Server: {args.platform}/{args.region}")
    print(f"Match depth: {args.depth}")
    print(f"Output: analysis_data/")
    print("=" * 50)
    
    try:
        analyzer = KRAnalysis(args.player, args.depth, args.platform, args.region)
        analysis = analyzer.run_analysis()
        
        print("\nAnalysis Complete!")
        print(f"Total matches: {len(analyzer.downloaded_matches)}")
        print(f"Unique players: {len(analyzer.analyzed_players)}")
        print(f"Output directory: {analyzer.output_dir.absolute()}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
