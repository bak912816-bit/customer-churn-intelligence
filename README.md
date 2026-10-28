# Customer Churn Intelligence

## 1. Présentation du projet

Ce projet consiste à analyser et à prédire le désabonnement des clients (*customer churn*) d'une entreprise de télécommunications à partir de données historiques.

L'objectif est d'identifier les profils de clients les plus susceptibles de partir, de comprendre les facteurs associés au churn et de proposer des actions de fidélisation fondées sur les données.

**Problématique :** comment exploiter les données clients pour détecter les risques de désabonnement et aider l'entreprise à mieux cibler ses actions de rétention ?

## 2. Objectifs

- Nettoyer et contrôler la qualité des données.
- Réaliser une analyse exploratoire des données (EDA).
- Utiliser SQL pour analyser le churn avec DuckDB.
- Construire un modèle de classification avec Python et scikit-learn.
- Comparer les performances de plusieurs configurations.
- Formuler des recommandations métier.

## 3. Données

Le projet utilise le jeu de données **Telco Customer Churn**, disponible sur Kaggle.

Le jeu de données contient 7 043 clients et 21 colonnes décrivant notamment :

- les caractéristiques des clients ;
- l'ancienneté (`tenure`) ;
- les contrats et les moyens de paiement ;
- les services souscrits ;
- les charges mensuelles et totales ;
- le statut de désabonnement (`Churn`).

La variable cible indique si le client a quitté l'entreprise (`Yes`) ou non (`No`).

## 4. Outils et technologies

- **Python** : traitement et analyse des données.
- **Pandas et NumPy** : manipulation des données.
- **Matplotlib et Seaborn** : visualisation.
- **DuckDB et SQL** : stockage analytique et requêtes.
- **scikit-learn** : préparation des données et apprentissage automatique.
- **Git et GitHub** : versionnement et présentation du projet.

## 5. Méthodologie

### 5.1. Audit et nettoyage

L'audit a révélé 11 valeurs composées d'espaces dans `TotalCharges`. Elles ont été converties en valeurs manquantes lors du nettoyage.

Les contrôles ont également porté sur les doublons et les valeurs manquantes. Aucun doublon complet n'a été détecté.

### 5.2. Analyse exploratoire

L'analyse a montré que :

- le taux global de churn est de 26,54 % ;
- les clients ayant un contrat mensuel présentent un taux de churn de 42,71 % ;
- ce taux est de 11,27 % pour les contrats d'un an ;
- il est de 2,83 % pour les contrats de deux ans ;
- le churn atteint 47,44 % chez les clients ayant entre 0 et 12 mois d'ancienneté, contre 9,51 % chez ceux ayant entre 49 et 72 mois.

Ces résultats mettent en évidence des associations entre le churn, l'ancienneté et le type de contrat. Ils ne démontrent pas à eux seuls de relations causales.

### 5.3. Analyse SQL avec DuckDB

DuckDB a été utilisé pour effectuer des analyses complémentaires, notamment :

- le taux global de churn ;
- le churn selon le type de contrat ;
- le churn selon le moyen de paiement ;
- le churn selon les groupes d'ancienneté.

Cette étape permet de produire des résultats reproductibles avec des requêtes SQL.

### 5.4. Modélisation

Une régression logistique a été entraînée pour prédire le churn.

Les principales étapes sont :

1. Exclusion de l'identifiant client des variables explicatives.
2. Encodage des variables catégorielles avec `get_dummies()`.
3. Séparation des données en ensembles d'entraînement et de test, avec stratification de la variable cible.
4. Standardisation des variables dans un pipeline.
5. Comparaison d'un modèle standard et d'un modèle utilisant `class_weight="balanced"`.
6. Étude de plusieurs seuils de classification.

### 5.5. Résultats du modèle

Pour le modèle équilibré avec un seuil de 0,50 :

| Métrique | Résultat |
|---|---:|
| Accuracy | 73,95 % |
| Precision | 50,60 % |
| Recall | 78,34 % |
| F1-score | 61,49 % |

Le seuil de 0,55 a obtenu le meilleur F1-score parmi les seuils testés :

| Métrique | Résultat au seuil de 0,55 |
|---|---:|
| Accuracy | 75,37 % |
| Precision | 52,51 % |
| Recall | 75,40 % |
| F1-score | 61,91 % |

Le seuil de 0,55 est un choix exploratoire. Il a été sélectionné à partir des résultats du jeu de test ; une validation distincte est nécessaire pour une évaluation méthodologiquement plus rigoureuse.

### 5.6. Interprétation des coefficients

L'analyse des coefficients de la régression logistique met notamment en évidence des associations entre le churn, l'ancienneté, le type de contrat, le service Internet et certains services complémentaires.

Ces coefficients décrivent les associations apprises par le modèle. Ils ne prouvent pas que les variables concernées causent directement le désabonnement.

## 6. Recommandations métier

À partir des résultats exploratoires, plusieurs pistes peuvent être proposées :

- **Renforcer l'intégration des nouveaux clients** : suivre leur expérience durant les premiers mois.
- **Étudier des offres de contrats de longue durée** : évaluer leur capacité à améliorer la fidélisation.
- **Améliorer l'assistance et les services de sécurité** : tester des offres ou un accompagnement adaptés.
- **Prioriser les actions de rétention** : utiliser les probabilités prédites pour identifier les clients à examiner en priorité.
- **Mesurer l'efficacité des campagnes** : comparer les résultats des actions de fidélisation avant de conclure à leur efficacité.

Ces recommandations sont des hypothèses à tester. Leur impact commercial devra être mesuré, idéalement avec des expériences contrôlées.

## 7. Structure du projet

```text
archive/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── inspect_data.py
│   ├── audit_data.py
│   ├── clean_data.py
│   ├── eda.py
│   ├── visualize_eda.py
│   ├── load_duckdb.py
│   ├── run_sql.py
│   └── train_model.py
├── sql/
│   └── churn_analysis.sql
├── notebooks/
├── reports/
│   └── figures/
└── README.md
```

## 8. Limites et améliorations futures

- Choisir le seuil sur un ensemble de validation distinct.
- Intégrer l'imputation des valeurs manquantes au pipeline afin d'éviter les fuites de données.
- Évaluer le modèle avec une validation croisée.
- Comparer la régression logistique à des modèles tels que Random Forest et Gradient Boosting.
- Étudier les coûts des faux positifs et des faux négatifs.
- Évaluer l'impact réel des actions de fidélisation.

## 9. Conclusion

Ce projet met en pratique un flux de travail analytique complet, de l'audit des données à la modélisation prédictive, en passant par l'analyse SQL et les recommandations métier.

Il illustre l'utilisation conjointe de Python, SQL, DuckDB et scikit-learn pour transformer des données clients en informations utiles à la prise de décision.
