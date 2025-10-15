# 🎮 Multi-Server Analysis Script - All-in-One

Un script unique et simplifié pour analyser les données de match sur tous les serveurs (KR, EUW, NA, etc.).

## 🚀 **Utilisation**

### **Test Rapide (2 matchs)**
```bash
python fetcher_bridge.py --player "Sard#CASS" --test
```

### **Analyse KR (10 matchs)**
```bash
python fetcher_bridge.py --player "Sard#CASS" --depth 10
```

### **Analyse EUW**
```bash
python fetcher_bridge.py --player "Sung Jin woo#SOUL" --platform euw1 --region europe --depth 5
```

### **Analyse NA**
```bash
python fetcher_bridge.py --player "Player#NA1" --platform na1 --region americas --depth 8
```

## 📋 **Paramètres**

- `--player` : Riot ID du joueur (ex: "Sard#CASS", "Sung Jin woo#SOUL")
- `--depth` : Nombre de matchs à analyser par joueur (défaut: 10)
- `--platform` : Plateforme (kr, euw1, na1, eun1, etc.) (défaut: kr)
- `--region` : Région (asia, europe, americas) (défaut: asia)
- `--test` : Mode test avec depth=2

## 📁 **Structure de Sortie**

```
analysis_data/
├── matches/           # Données de match brutes
├── timelines/         # Données temporelles
└── analysis/          # Résultats d'analyse
    ├── complete_analysis.json
    └── download_summary.json
```

## 🎯 **Fonctionnalités**

- **Multi-Serveur** : Support de tous les serveurs (KR, EUW, NA, EUN, etc.)
- **Joueur Principal** : Télécharge les matchs du joueur spécifié
- **Coéquipiers** : Télécharge les matchs de chaque coéquipier
- **Évite les Doublons** : Ne télécharge pas les matchs déjà analysés
- **Analyse Automatique** : Génère des statistiques complètes
- **Un Seul Dossier** : Tout dans `analysis_data/`

## 📊 **Exemples de Résultats**

### **Test Mode (depth=2)**
- **~12 matchs** téléchargés
- **~9 joueurs** analysés
- **~2 minutes** d'exécution

### **Full Mode (depth=10)**
- **~80 matchs** téléchargés
- **~8-15 joueurs** analysés
- **~5-10 minutes** d'exécution

## 🌍 **Serveurs Supportés**

### **Asie**
- **KR** : Korea (kr/asia)
- **JP** : Japan (jp1/asia)

### **Europe**
- **EUW** : Europe West (euw1/europe)
- **EUN** : Europe Nordic & East (eun1/europe)
- **TR** : Turkey (tr1/europe)
- **RU** : Russia (ru/europe)

### **Amériques**
- **NA** : North America (na1/americas)
- **BR** : Brazil (br1/americas)
- **LAN** : Latin America North (la1/americas)
- **LAS** : Latin America South (la2/americas)

## 🔧 **Configuration**

1. **API Key** : Vérifiez que `riot_fetcher/.env` contient votre clé API
2. **Dépendances** : Le script utilise les modules de `riot_fetcher/`
3. **Sortie** : Tous les fichiers sont dans `analysis_data/`

## 🎉 **Avantages**

- **Un seul script** pour tout faire
- **Choix du joueur** et de la profondeur
- **Un seul dossier** de sortie
- **Mode test** pour validation rapide
- **Analyse automatique** des données

## 📈 **Données Collectées**

- **Match Info** : Durée, mode, queue, patch
- **Player Data** : KDA, or, dégâts, vision, CS
- **Timeline Data** : Événements frame par frame
- **Team Data** : Compositions, synergies
- **Champion Data** : Métagame, performances

**Prêt à analyser n'importe quel joueur sur n'importe quel serveur !** 🚀

