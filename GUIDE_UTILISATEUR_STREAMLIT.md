# 📊 Guide Utilisateur - Dashboard de Monitoring Solaire

**Installation HKL GGI - 269.28 kWp**
**Localisation : Dhaka, Bangladesh**

---

## 🚀 Démarrage Rapide

### Lancer le Dashboard

```bash
streamlit run app_solar_monitoring.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse : **http://localhost:8503**

### Arrêter le Dashboard

Appuyez sur **Ctrl+C** dans le terminal.

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Interface Générale](#interface-générale)
3. [Onglet 1 : Overview](#onglet-1--overview)
4. [Onglet 2 : Detailed Analysis](#onglet-2--detailed-analysis)
5. [Onglet 3 : Anomaly Detection](#onglet-3--anomaly-detection)
6. [Onglet 4 : Model Performance](#onglet-4--model-performance)
7. [Configuration et Paramètres](#configuration-et-paramètres)
8. [Interprétation des Résultats](#interprétation-des-résultats)
9. [FAQ et Troubleshooting](#faq-et-troubleshooting)

---

## 🎯 Vue d'ensemble

### Objectif du Dashboard

Ce dashboard utilise le **Machine Learning (Ridge Regression)** pour :

1. **Prédire la production attendue** en fonction de la météo réelle
2. **Comparer** la production réelle vs prédiction ML vs maximum théorique (Clear-Sky)
3. **Détecter automatiquement les anomalies** (pannes, soiling, problèmes techniques)
4. **Monitorer les performances** au quotidien, hebdomadaire, mensuel

### Différence avec une approche traditionnelle

#### ❌ Approche traditionnelle (Clear-Sky) :
- Compare la production réelle au maximum théorique (ciel parfaitement clair)
- **Problème** : Signale les journées nuageuses comme des "problèmes"
- Trop de fausses alertes

#### ✅ Approche ML (ce dashboard) :
- Compare la production réelle à ce qui est **attendu avec la météo actuelle**
- Apprend les patterns historiques
- **Alerte seulement** sur les vrais problèmes (matériel, soiling, etc.)

---

## 🖥️ Interface Générale

### Barre Latérale (Sidebar) - À Gauche

La sidebar contient tous les contrôles pour personnaliser votre analyse :

#### 📅 **Date Range**
```
┌─────────────────────────┐
│ Select date range       │
│ ┌──────────┬──────────┐ │
│ │2025-10-15│2025-10-22│ │
│ └──────────┴──────────┘ │
└─────────────────────────┘
```
- **Usage** : Sélectionnez la période à analyser
- **Conseil** :
  - 7 jours pour le monitoring quotidien
  - 30 jours pour les analyses mensuelles
  - Périodes spécifiques pour investiguer des événements

#### 🚨 **Alert Threshold**
```
┌─────────────────────────┐
│ Alert threshold (%)     │
│ ◄─────●─────────────► │
│        20%              │
└─────────────────────────┘
```
- **Signification** : Seuil en-dessous duquel une alerte est déclenchée
- **Calcul** : Alerte si `(Actual / Predicted) × 100% < (100% - Threshold)`
- **Exemple** :
  - Threshold = 20%
  - Actual = 75 kWh, Predicted = 100 kWh → Ratio = 75% → **ALERTE** (25% en-dessous)
  - Actual = 85 kWh, Predicted = 100 kWh → Ratio = 85% → OK (15% en-dessous)
- **Recommandations** :
  - **15%** : Monitoring strict (plus d'alertes, détection précoce)
  - **20%** : Équilibré (recommandé)
  - **30%** : Tolérant (seulement problèmes majeurs)

#### 📊 **Display Options**
- **Show Clear-Sky Reference** : Affiche/masque la ligne rouge du maximum théorique
- **Recent days to analyze** : Nombre de jours pour les graphiques de tendance (7-90)

### Zone Principale

4 onglets pour différents types d'analyses :
- **📊 Overview** : Vue d'ensemble quotidienne
- **📈 Detailed Analysis** : Analyse détaillée avec graphiques
- **🚨 Anomaly Detection** : Liste des jours problématiques
- **📉 Model Performance** : Précision du modèle ML

---

## 📊 Onglet 1 : Overview

**Usage principal** : Check quotidien rapide (1-2 minutes)

### Section 1 : Métriques du Jour

#### Carte 1 : 📅 Latest Date
```
┌─────────────────────┐
│ 📅 Latest Date      │
│    2025-10-22       │
└─────────────────────┘
```
- Date des données les plus récentes disponibles

#### Carte 2 : ⚡ Actual Production
```
┌─────────────────────┐
│ ⚡ Actual Production│
│    1,234.5 kWh      │
│    ▲ +45.2 kWh      │
└─────────────────────┘
```
- **Valeur** : Production totale réelle de la journée
- **Delta** : Différence vs prédiction ML
  - 🟢 Vert positif : Production supérieure à la prédiction (bon signe)
  - 🔴 Rouge négatif : Production inférieure à la prédiction (à surveiller)

#### Carte 3 : 🎯 Predicted Production
```
┌─────────────────────┐
│ 🎯 Predicted        │
│    1,189.3 kWh      │
└─────────────────────┘
```
- **Valeur** : Ce que le modèle ML attendait avec la météo du jour
- Prend en compte : irradiance, température, nébulosité, jour de l'année

#### Carte 4 : 📊 Performance Ratio
```
┌─────────────────────┐
│ 📊 Performance      │
│    103.8%           │
│    ▲ +3.8%          │
└─────────────────────┘
```
- **Formule** : `(Actual / Predicted) × 100%`
- **Interprétation** :
  - **> 100%** : ✅ Excellente journée (mieux que prévu)
  - **90-100%** : ✅ Performance normale
  - **80-90%** : ⚠️ Légère sous-performance
  - **< 80%** : 🚨 Problème à investiguer

### Section 2 : Boîte d'Alerte

#### Alerte Performance (Rouge)
```
┌─────────────────────────────────────────┐
│ ⚠️ Performance Alert                    │
│                                         │
│ Actual production is 25.3% below       │
│ predicted value.                        │
│                                         │
│ Please check for:                       │
│ • Equipment malfunction                 │
│ • Soiling or shading issues            │
│ • Inverter problems                     │
└─────────────────────────────────────────┘
```
**Quand apparaît-elle ?** Si Performance Ratio < (100% - Alert Threshold)

**Actions à prendre** :
1. Vérifier l'état des onduleurs (inverters)
2. Inspecter visuellement les panneaux (soiling, ombre, débris)
3. Consulter Tab 3 pour voir l'historique des anomalies
4. Vérifier les logs des équipements

#### Système OK (Vert)
```
┌─────────────────────────────────────────┐
│ ✅ System Operating Normally            │
│                                         │
│ Performance is within expected range.   │
└─────────────────────────────────────────┘
```
**Signification** : Aucun problème détecté, le plant fonctionne normalement.

### Section 3 : Tendance de Performance (30 jours)

```
Performance Ratio Trend (Actual / Predicted × 100%)
│
120%├─────────────────────────────────
│    🟢●        🟢●
100%├──🟢●──🟢●──────🟢●──────────────
│              🟢●
80%├────────────────────────🔴●───────
│
60%├─────────────────────────────────
    └────┬────┬────┬────┬────┬────
       10/15 10/17 10/19 10/21 10/23
```

**Comment lire** :
- **Ligne verte pointillée (100%)** : Performance parfaite (actual = predicted)
- **Ligne orange pointillée (80%)** : Seuil de vigilance
- **Points verts** 🟢 : Journées normales
- **Points rouges** 🔴 : Journées avec anomalie

**Patterns à surveiller** :
- **Déclin progressif** : Soiling qui s'accumule → Nettoyer les panneaux
- **Chute brutale** : Panne d'équipement → Inspection urgente
- **Oscillations** : Normal (variations météo)

### Section 4 : Production Quotidienne (30 jours)

```
Daily Production Summary
│
300├────────────────────────────────
kWh  ▄▄  ▄▄     ▄▄  ▄▄
200├─▄▄──▄▄──▄▄─▄▄──▄▄──────────
│   ██  ██  ██ ██  ██
100├──██──██──██─██──██──────────
│    ██  ██  ██ ██  ██
0  ├──██──██──██─██──██──────────
    └──┬───┬───┬──┬───┬───
     10/15 10/17 10/19 10/21 10/23
```

**Légende** :
- 🔵 **Barres bleues** : Production réelle
- 🟢 **Barres vertes (transparentes)** : Prédiction ML

**Comment lire** :
- **Barres qui se chevauchent bien** : Production conforme aux attentes
- **Bleu >> Vert** : Meilleure journée que prévu (bon soleil)
- **Bleu << Vert** : Production inférieure (vérifier cause)

---

## 📈 Onglet 2 : Detailed Analysis

**Usage principal** : Analyse approfondie d'une période spécifique

### Section 1 : Métriques de Période

```
┌──────────────┬──────────────┬──────────────┐
│ Total Actual │ Total        │ Period       │
│ 8,456.7 kWh  │ Predicted    │ Performance  │
│              │ 8,234.1 kWh  │ 102.7%       │
└──────────────┴──────────────┴──────────────┘
```

**Calculs sur la période sélectionnée** (pas seulement un jour)

### Section 2 : Graphique 3-Lignes (Le Plus Important)

```
Production Comparison: Actual vs ML Prediction vs Clear-Sky

250├─────────────────────────────────────────
kWh│     ╱╲                  ╱╲
200├────╱──╲────────────────╱──╲───────── Red (dashed)
│   ╱    ╲              ╱    ╲          Clear-Sky Max
150├──╱──────╲──────────╱──────╲──────── Green
│ ╱        ╲        ╱        ╲        ML Predicted
100├╱──────────╲────╱──────────╲─────── Blue
│              ╲  ╱              ╲      Actual
50├────────────╲╱──────────────────────
│
0 ├─────────────────────────────────────
  └───┬─────┬─────┬─────┬─────┬─────
    06:00  09:00  12:00  15:00  18:00
```

#### 🔴 Ligne Rouge Pointillée (Clear-Sky - Théorique)
**Signification** : Maximum théorique si le ciel était parfaitement clair toute la journée

**Interprétation** :
- C'est un **plafond** irréaliste
- Aucune installation n'atteint jamais 100% du clear-sky
- **Ne pas utiliser** pour détecter des problèmes (trop optimiste)

**Exemple** :
- Clear-Sky = 200 kWh
- Actual = 120 kWh
- ❌ Ne signifie PAS qu'il y a un problème ! (peut être une journée nuageuse normale)

#### 🟢 Ligne Verte (ML Predicted - Attendu)
**Signification** : Production attendue avec la météo réelle du jour

**Ce que le modèle prend en compte** :
- ☁️ Nébulosité réelle
- 🌡️ Température
- ☀️ Irradiance mesurée
- 📅 Saison (angle du soleil)
- 📊 Patterns historiques

**Interprétation** :
- C'est votre **référence principale**
- Ligne réaliste et adaptée aux conditions météo

#### 🔵 Ligne Bleue (Actual - Réel)
**Signification** : Production réelle mesurée

**Comment lire** :
- **Bleu proche de Vert** ✅ : Performance normale
- **Bleu > Vert** ✅ : Mieux que prévu (excellent)
- **Bleu << Vert** 🚨 : Sous-performance (investiguer)

### Cas d'Usage Typiques

#### Cas 1 : Journée Ensoleillée Normale
```
Clear-Sky ─ ─ ─ ╱╲ ─ ─ ─  (Rouge, haute)
ML Predict ────╱──╲────  (Vert, proche du max)
Actual     ───╱────╲───  (Bleu, suit le vert)
```
✅ **Interprétation** : Tout va bien, production optimale

#### Cas 2 : Journée Nuageuse Normale
```
Clear-Sky ─ ─ ─ ╱╲ ─ ─ ─  (Rouge, toujours haute)
ML Predict ──╱╲─╱╲─╱╲──  (Vert, bas et oscillant)
Actual     ─╱╲─╱╲─╱╲───  (Bleu, suit le vert)
```
✅ **Interprétation** :
- Production faible MAIS normale (météo nuageuse)
- Le bleu suit le vert → Pas de problème !
- ❌ Ne pas comparer au rouge (clear-sky)

#### Cas 3 : Problème Technique (Panne)
```
Clear-Sky ─ ─ ─ ╱╲ ─ ─ ─  (Rouge, haute)
ML Predict ────╱──╲────  (Vert, normal)
Actual     ──╱▁▁▁▁╲───  (Bleu, plat au milieu)
```
🚨 **Interprétation** :
- Bleu << Vert au milieu de la journée
- Production plate alors que prédiction en pic
- **Cause probable** : Onduleur en panne, disjoncteur déclenché

#### Cas 4 : Soiling (Panneaux Sales)
```
Clear-Sky ─ ─ ─ ╱╲ ─ ─ ─  (Rouge)
ML Predict ────╱──╲────  (Vert)
Actual     ───╱────╲───  (Bleu, 20% en-dessous)
```
🚨 **Interprétation** :
- Bleu systématiquement 15-25% sous le vert
- Pattern constant toute la journée
- **Cause probable** : Soiling, poussière, fientes d'oiseaux

### Section 3 : Analyse des Résidus

```
Residual Analysis (Actual - Predicted)

+30%├──────────────────────────────
    │    ▄           ▄              Green bars
+10%├────▄─────▄─────────▄───────  (above 0 = good)
    ├────┼─────┼─────┼───┼───────
0%  ├════●═════●═════●═══●═══════  Zero line
    │              ▄                Orange bars
-10%├──────────────▄───────────────  (slight under)
    │                   ▄▄▄         Red bars
-20%├───────────────────███───────  Alert Zone
    │                   ███         (below threshold)
-30%├───────────────────███───────
    └───┬─────┬─────┬───┬─────
      10/15 10/17 10/19 10/21
```

**Formule** : `Résidu (%) = ((Actual - Predicted) / Predicted) × 100%`

**Code couleur** :
- 🟢 **Vert (> 0%)** : Production supérieure à la prédiction
  - Excellent, météo meilleure que prévu
- 🟠 **Orange (0% à -20%)** : Légère sous-performance
  - Dans la tolérance normale
- 🔴 **Rouge (< -20%)** : Sous-performance significative
  - **ALERTE** : Investiguer la cause

**Ligne Rouge Pointillée** : Seuil d'alerte (configurable dans la sidebar)

**Utilisation** :
- **Identifier les jours problématiques** en un coup d'œil
- **Patterns** :
  - Barres rouges isolées → Problème ponctuel
  - Barres rouges consécutives → Problème persistant

---

## 🚨 Onglet 3 : Anomaly Detection

**Usage principal** : Liste exhaustive de tous les jours problématiques

### Tableau des Anomalies

```
┌──────────┬────────┬──────────┬──────────┬─────────┐
│   Date   │ Actual │ Predicted│ Perform. │ Deficit │
│          │ (kWh)  │  (kWh)   │   (%)    │  (kWh)  │
├──────────┼────────┼──────────┼──────────┼─────────┤
│2025-10-20│  567.2 │   892.4  │   63.5%  │  325.2  │  🔴
│2025-10-18│  712.8 │   945.1  │   75.4%  │  232.3  │  🟠
│2025-10-12│  834.5 │ 1,045.2  │   79.8%  │  210.7  │  🟠
│2025-09-28│  891.2 │ 1,134.7  │   78.5%  │  243.5  │  🟠
└──────────┴────────┴──────────┴──────────┴─────────┘
```

**Colonnes expliquées** :

#### 📅 Date
Date du jour anomal

#### ⚡ Actual (kWh)
Production réelle totale de la journée

#### 🎯 Predicted (kWh)
Production attendue par le modèle ML

#### 📊 Performance (%)
= `(Actual / Predicted) × 100%`

**Couleur de fond** (dégradé) :
- 🔴 **Rouge (< 60%)** : Problème grave
- 🟠 **Orange (60-80%)** : Problème modéré
- 🟡 **Jaune (80-90%)** : Légère sous-performance
- 🟢 **Vert (> 90%)** : Normal (ne devrait pas être dans ce tableau)

#### 💸 Deficit (kWh)
= `Predicted - Actual`

**Signification** : Perte d'énergie (et donc financière) due au problème

**Calcul financier** :
```
Perte financière = Deficit × Prix du kWh
Exemple : 325.2 kWh × 0.12 $/kWh = 39.02 $ de perte
```

### Statistiques Récapitulatives

```
┌──────────────────┬──────────────────┬──────────────────┐
│ Total Anomalous  │ Avg Performance  │ Total Energy     │
│ Days             │                  │ Deficit          │
├──────────────────┼──────────────────┼──────────────────┤
│       23         │     74.2%        │   5,234.7 kWh    │
└──────────────────┴──────────────────┴──────────────────┘
```

**Utilisation** :
- **Total Anomalous Days** : Fréquence des problèmes
  - > 10% des jours → Problème récurrent à investiguer
- **Avg Performance** : Gravité moyenne
  - < 70% → Problèmes sévères
- **Total Energy Deficit** : Impact financier cumulé

### Workflow Recommandé

1. **Trier le tableau par date** (plus récent en premier)
2. **Identifier les clusters** :
   - 3+ jours consécutifs → Problème persistant (soiling, panne)
   - Jours isolés → Événements ponctuels (météo extrême, coupure)
3. **Prioriser par Performance (%)** :
   - < 60% : Urgence élevée
   - 60-70% : Urgence moyenne
   - 70-80% : À surveiller
4. **Corréler avec les événements** :
   - Consulter les logs de maintenance
   - Vérifier les conditions météo extrêmes
   - Investiguer les changements récents

---

## 📉 Onglet 4 : Model Performance

**Usage principal** : Évaluer la précision du modèle ML

### Métriques de Performance

```
┌──────────┬──────────┬──────────┬──────────┐
│   MAE    │   RMSE   │   R²     │   MAPE   │
├──────────┼──────────┼──────────┼──────────┤
│ 24.60 kWh│ 34.06 kWh│  0.5692  │  40.4%   │
└──────────┴──────────┴──────────┴──────────┘
```

#### 1. MAE (Mean Absolute Error)
**Signification** : Erreur moyenne en valeur absolue

**Formule** : `MAE = moyenne(|Actual - Predicted|)`

**Interprétation** :
- **24.60 kWh** = En moyenne, le modèle se trompe de ±24.6 kWh par heure
- **Contexte** : Sur une production moyenne de ~65 kWh/h, c'est ~38% d'erreur

**Échelle de qualité** :
- < 15 kWh : Excellent
- 15-25 kWh : Bon ✅ ← Votre cas
- 25-40 kWh : Acceptable
- > 40 kWh : À améliorer

#### 2. RMSE (Root Mean Square Error)
**Signification** : Erreur quadratique (pénalise les grosses erreurs)

**Formule** : `RMSE = √(moyenne((Actual - Predicted)²))`

**Interprétation** :
- Toujours > MAE (pénalise les outliers)
- **34.06 kWh** vs MAE 24.60 kWh → Pas trop d'outliers extrêmes (bon signe)

**Si RMSE >> MAE** :
- Modèle a des erreurs très variables
- Quelques prédictions très mauvaises

#### 3. R² (Coefficient de Détermination)
**Signification** : % de variance expliquée par le modèle

**Formule** : `R² = 1 - (SS_residual / SS_total)`

**Interprétation** :
- **0.5692** = Le modèle explique 56.92% de la variance
- **43.08% inexpliqué** = Dû à la variabilité météo imprévisible

**Échelle** :
- **0.0-0.3** : Faible
- **0.3-0.5** : Modéré
- **0.5-0.7** : Bon ✅ ← Votre cas
- **0.7-0.9** : Très bon
- **0.9-1.0** : Excellent (rare pour prédiction solaire)

**Pour la prédiction solaire** :
- R² = 0.57 est un **très bon score**
- Difficile d'atteindre > 0.7 sans données météo ultra-précises

#### 4. MAPE (Mean Absolute Percentage Error)
**Signification** : Erreur moyenne en pourcentage

**Formule** : `MAPE = moyenne(|Actual - Predicted| / Actual) × 100%`

**Interprétation** :
- **40.4%** = Erreur relative moyenne de 40%
- ⚠️ **Attention** : MAPE élevé pour les heures de faible production (matin/soir)

**Échelle** :
- < 20% : Excellent
- 20-40% : Bon
- 40-60% : Acceptable ✅ ← Votre cas (normal pour solaire horaire)
- > 60% : À améliorer

**Pourquoi MAPE élevé pour le solaire ?** :
- Heures de faible production (tôt le matin, fin d'après-midi)
- Erreur de 10 kWh sur production de 20 kWh = 50% d'erreur
- Même erreur de 10 kWh sur 200 kWh = 5% seulement

### Graphique : Predicted vs Actual

```
Predicted vs Actual (Test Set)

Actual ↑
200 ├────────────────────────●─
kWh │              ●──●──●──
    │        ●──●──●──●──●──
150 ├───●──●──●──●──────────
    │●──●──●──
100 ├●──●─────────────────────
    │●──
50  ├●───────────────────────
    │●
0   ├─────────────────────────
    └─┬───┬───┬───┬───┬───┬→
      0  50 100 150 200   Predicted (kWh)
```

**Ligne Rouge Pointillée** : Prédiction parfaite (y = x)

**Interprétation** :
- **Points proches de la ligne** : Bonnes prédictions
- **Points au-dessus** : Modèle sous-estime
- **Points en-dessous** : Modèle sur-estime
- **Dispersion** : Indique l'incertitude

**Pattern idéal** :
- Nuage de points concentré autour de la ligne diagonale

**Patterns problématiques** :
- **Dispersion uniforme** : Modèle trop simple
- **Courbe** : Modèle biaisé (systématiquement sur/sous-estime)

### Graphique : Distribution des Erreurs

```
Prediction Error Distribution

Frequency ↑
800 ├──────────────▄▄▄─────────
    │        ▄▄▄▄▄▄███▄▄▄▄▄
600 ├────▄▄▄███████████████▄▄
    │  ▄▄███████████████████▄▄
400 ├▄▄██████████████████████▄
    │████████████████████████▄
200 ├███████████████████████▄
    │███████████████████████
0   ├─────────┼─────────────→
    -100    -50  0  +50  +100
                Error (kWh)
```

**Forme idéale** : Cloche centrée sur 0 (distribution normale)

**Interprétation** :
- **Centré sur 0** : Pas de biais systématique ✅
- **Pic à gauche (négatif)** : Modèle sur-estime systématiquement
- **Pic à droite (positif)** : Modèle sous-estime systématiquement
- **Queues longues** : Erreurs extrêmes fréquentes

**Statistiques affichées** :
```
┌────────────┬────────────┐
│ Mean Error │ Std Error  │
├────────────┼────────────┤
│  -2.34 kWh │  32.45 kWh │
└────────────┴────────────┘
```

- **Mean Error proche de 0** : Bon signe (pas de biais)
- **Std Error** : Variabilité des erreurs

---

## ⚙️ Configuration et Paramètres

### Modifier la Configuration de l'Installation

Éditez le fichier `app_solar_monitoring.py` (lignes 58-67) :

```python
PLANT_CONFIG = {
    'name': 'HKL GGI',              # Nom de l'installation
    'capacity_kwp': 269.28,         # Puissance crête (kWp)
    'latitude': 24.0223,            # Latitude (Dhaka)
    'longitude': 90.2957,           # Longitude (Dhaka)
    'timezone': 'Asia/Dhaka',       # Fuseau horaire
    'alert_threshold_pct': 20       # Seuil d'alerte par défaut (%)
}
```

### Modifier la Date de Split Train/Test

Par défaut, le modèle considère les données après le 31/12/2024 comme données de test.

Pour changer (ligne 579) :
```python
test_date = pd.Timestamp('2024-12-31')  # Modifier cette date
```

**Recommandations** :
- Garder 20-30% des données pour le test
- Utiliser les données les plus récentes comme test

---

## 🎯 Interprétation des Résultats

### Scénarios Typiques

#### Scénario 1 : Performance Normale
**Indicateurs** :
- ✅ Performance Ratio : 95-105%
- ✅ Boîte verte "System Operating Normally"
- ✅ Courbe bleue suit la courbe verte
- ✅ Résidus majoritairement entre -10% et +10%

**Action** : Aucune, continuer le monitoring de routine

#### Scénario 2 : Soiling (Panneaux Sales)
**Indicateurs** :
- 🚨 Performance Ratio : 75-85% (constant)
- 🚨 Bleu systématiquement 15-25% sous vert
- 🚨 Pattern stable sur plusieurs jours consécutifs
- 🚨 Déficit cumulé augmente régulièrement

**Diagnostic** : Poussière, pollen, fientes d'oiseaux

**Actions** :
1. Inspection visuelle des panneaux
2. Planifier un nettoyage
3. Vérifier fréquence de nettoyage (mensuel/trimestriel)

#### Scénario 3 : Panne d'Onduleur
**Indicateurs** :
- 🚨 Performance Ratio : < 50% ou 0%
- 🚨 Production plate ou nulle au milieu de la journée
- 🚨 Début brutal (pas progressif)
- 🚨 Peut affecter 1 seule chaîne (baisse partielle)

**Diagnostic** : Onduleur en panne, disjoncteur déclenché

**Actions** :
1. Vérifier les alarmes des onduleurs
2. Contrôler les disjoncteurs
3. Consulter les logs de l'onduleur
4. Contacter le technicien si nécessaire

#### Scénario 4 : Ombrage Nouveau
**Indicateurs** :
- 🚨 Baisse de performance à heure fixe (ex: 14h-16h)
- 🚨 Pattern répétitif chaque jour
- 🚨 Avant cette période et après : performance normale

**Diagnostic** : Nouvel obstacle (arbre, bâtiment, antenne)

**Actions** :
1. Inspection visuelle à l'heure concernée
2. Identifier la source d'ombre
3. Évaluer possibilité d'éliminer l'obstacle
4. Recalculer le potentiel de production

#### Scénario 5 : Dégradation Progressive
**Indicateurs** :
- ⚠️ Performance Ratio diminue lentement (ex: 100% → 95% → 90%)
- ⚠️ Tendance sur plusieurs mois
- ⚠️ Pas de cause évidente

**Diagnostic** :
- Vieillissement normal des panneaux (~0.5-1%/an)
- Hot spots
- Délamination

**Actions** :
1. Thermographie infrarouge
2. Test I-V des chaînes
3. Vérifier garantie de performance
4. Évaluer besoin de remplacement

---

## 🔧 FAQ et Troubleshooting

### Questions Fréquentes

#### Q1 : Pourquoi la courbe rouge (Clear-Sky) est toujours au-dessus ?
**R** : C'est normal ! Clear-Sky représente le maximum théorique avec un ciel parfaitement clair. Dans la réalité :
- Nuages partiels
- Brume, pollution
- Pertes système (câbles, onduleur)
- Soiling léger

Votre installation n'atteindra JAMAIS 100% du clear-sky. Utilisez la courbe verte (ML) comme référence.

#### Q2 : Le modèle prédit parfois des valeurs négatives
**R** : Impossible, le code limite les prédictions à des valeurs >= 0. Si vous voyez cela, contactez le support.

#### Q3 : Pourquoi MAPE (40%) est si élevé alors que R² (0.57) est bon ?
**R** : MAPE est sensible aux faibles valeurs :
- Erreur de 5 kWh le matin (production 10 kWh) = 50% d'erreur
- Même erreur à midi (production 200 kWh) = 2.5% seulement
- MAPE amplifie les erreurs sur faibles productions

Pour le solaire, R² est une meilleure métrique que MAPE.

#### Q4 : Combien de temps garder l'historique ?
**R** : Recommandations :
- **Minimum** : 1 an (pour capturer toutes les saisons)
- **Optimal** : 2-3 ans (meilleur entraînement du modèle)
- **Limite** : Dépend de l'espace disque et performance

#### Q5 : Puis-je modifier le seuil d'alerte ?
**R** : Oui, dans la sidebar : "Alert threshold (%)"
- Démarrez avec 20%
- Ajustez selon vos retours d'expérience
- Diminuez si trop de fausses alertes
- Augmentez si vous ratez des vrais problèmes

#### Q6 : Le dashboard est lent avec beaucoup de données
**R** : Solutions :
1. Réduire la plage de dates analysée (sidebar)
2. Diminuer "Recent days to analyze"
3. Agréger les données (quotidien au lieu d'horaire)

### Problèmes Courants

#### Problème : TypeError timezone
**Symptôme** :
```
TypeError: Invalid comparison between dtype=datetime64[us, Asia/Dhaka] and Timestamp
```

**Solution** : Toutes les comparaisons de dates ont été corrigées. Si l'erreur persiste :
```bash
pkill -9 -f "streamlit run"
streamlit run app_solar_monitoring.py
```

#### Problème : Module 'sklearn' not found
**Symptôme** :
```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution** :
```bash
pip install scikit-learn matplotlib
```

#### Problème : Fichier predictions.parquet not found
**Symptôme** : Dashboard affiche "Unable to load data"

**Solution** :
1. Ouvrir `HKL_ML_comparison_v2.ipynb`
2. Exécuter toutes les cellules
3. Copier le code de `notebook_export_cell.py` dans une nouvelle cellule
4. Exécuter pour générer `data/predictions.parquet`

#### Problème : Dashboard ne se met pas à jour
**Solution** :
1. Dans le dashboard : Menu (☰) → Clear cache → Clear cache
2. Rafraîchir le navigateur (F5)
3. Si problème persiste : Redémarrer Streamlit

---

## 📞 Support et Contact

### Fichiers Importants

- **Dashboard** : `app_solar_monitoring.py`
- **Guide utilisateur** : `GUIDE_UTILISATEUR_STREAMLIT.md` (ce fichier)
- **Quick start** : `QUICK_START.md`
- **Notebook ML** : `HKL_ML_comparison_v2.ipynb`
- **Données** : `data/predictions.parquet`
- **Modèle** : `models/ridge_model.pkl`

### Logs et Diagnostic

Pour obtenir les logs détaillés :
```bash
streamlit run app_solar_monitoring.py --logger.level=debug
```

---

## 📊 Résumé : Workflow Quotidien

### Monitoring Quotidien (2 minutes)

1. **Ouvrir le dashboard** : `http://localhost:8503`
2. **Tab 1 (Overview)** :
   - Vérifier la boîte d'alerte (verte = OK)
   - Noter le Performance Ratio du jour
3. **Si alerte rouge** → Aller au Tab 3 pour détails

### Analyse Hebdomadaire (10 minutes)

1. **Tab 1** : Analyser la tendance 7 jours
2. **Tab 2** :
   - Sélectionner les 7 derniers jours (sidebar)
   - Examiner le graphique 3-lignes
   - Vérifier les résidus
3. **Tab 3** : Lister les anomalies de la semaine
4. **Documenter** les actions prises

### Revue Mensuelle (30 minutes)

1. **Tab 1** : Tendance 30 jours
2. **Tab 3** :
   - Export de la liste d'anomalies
   - Calcul du coût des pertes
   - Analyse des causes récurrentes
3. **Tab 4** : Vérifier les métriques du modèle
4. **Rapport** : Préparer synthèse pour le management
5. **Maintenance** : Planifier nettoyage/inspections

---

**🎉 Félicitations ! Vous savez maintenant utiliser le dashboard de monitoring solaire ML.**

**Pour toute question, consultez ce guide ou les fichiers README du projet.**
