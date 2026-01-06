# 📚 INDEX COMPLET - COLLECTION EVILGINX PRO

## 🎯 Vue d'ensemble

Cette collection complète contient **tout ce dont vous avez besoin** pour utiliser Evilginx Pro de manière professionnelle.

**Total de fichiers créés** : 16 fichiers
**Lignes de code/documentation** : ~6800+ lignes
**Date de création** : 25 décembre 2025

---

## 📁 STRUCTURE DES FICHIERS

```
/tmp/
│
├── 📘 DOCUMENTATION GÉNÉRALE
│   ├── README-CODE-SOURCE.md                    # Guide principal
│   ├── GUIDE-STRUCTURE-PHISHLET.md             # Structure détaillée des phishlets
│   ├── PHISHLETS-COLLECTION.md                 # Collection complète
│   ├── GUIDE-SELECTION-STRATEGIQUE.md          # Guide stratégique
│   ├── GUIDE-TELEGRAM-NOTIFICATIONS.md         # Guide Telegram (NOUVEAU)
│   └── INDEX-COMPLET.md                        # Ce fichier
│
├── 🎯 PHISHLETS - GOOGLE
│   ├── google-phishlet-example.yaml            # Version complète avancée
│   └── google-simple.yaml                      # Version simplifiée commentée
│
├── 🎯 PHISHLETS - AUTRES PLATEFORMES
│   ├── microsoft365.yaml                       # Microsoft 365 / Azure AD
│   ├── github.yaml                             # GitHub
│   ├── linkedin.yaml                           # LinkedIn
│   ├── facebook.yaml                           # Facebook
│   └── okta.yaml                               # Okta SSO
│
└── 🛠️ OUTILS
    ├── phishlet_analyzer.py                    # Script d'analyse automatique
    ├── telegram_notifier.py                    # Notifications Telegram (NOUVEAU)
    └── telegram_notifier.service               # Service systemd (NOUVEAU)
```

---

## 📖 GUIDE D'UTILISATION

### Pour les débutants

**Commencez ici** :

1. Lire `README-CODE-SOURCE.md` (vue d'ensemble)
2. Étudier `google-simple.yaml` (exemple simple)
3. Lire `GUIDE-STRUCTURE-PHISHLET.md` (comprendre la structure)
4. Tester en local avec le guide d'installation

### Pour les utilisateurs intermédiaires

**Progressez ici** :

1. Choisir un phishlet dans `PHISHLETS-COLLECTION.md`
2. Lire `GUIDE-SELECTION-STRATEGIQUE.md` (stratégie)
3. Déployer en production
4. Utiliser `phishlet_analyzer.py` pour créer vos propres phishlets

### Pour les experts

**Personnalisez ici** :

1. Étudier `google-phishlet-example.yaml` (fonctionnalités avancées)
2. Créer des phishlets custom
3. Intégrer avec Gophish
4. Utiliser Evilpuppet pour contournements avancés

---

## 📋 DESCRIPTION DÉTAILLÉE DES FICHIERS

### 1. README-CODE-SOURCE.md (354 lignes)

**Contenu** :

- Vue d'ensemble de tous les fichiers
- Utilisation rapide
- Structure d'un phishlet (résumé)
- Analyse de sites web (méthodes)
- Exemples par plateforme
- Debugging et troubleshooting
- Ressources et support
- Checklist finale

**Quand l'utiliser** :

- Point d'entrée principal
- Référence rapide
- Troubleshooting

---

### 2. GUIDE-STRUCTURE-PHISHLET.md (650+ lignes)

**Contenu** :

- Explication complète de chaque section YAML
- `proxy_hosts`, `sub_filters`, `auth_tokens`, etc.
- Variables dynamiques
- Regex courantes
- Processus de création étape par étape
- Checklist de validation
- Outils d'analyse

**Quand l'utiliser** :

- Créer un nouveau phishlet
- Comprendre la structure YAML
- Debugging d'un phishlet existant
- Référence technique

**Sections principales** :

```
1. METADATA
2. PROXY_HOSTS
3. SUB_FILTERS
4. AUTH_TOKENS
5. CREDENTIALS
6. LOGIN
7. FORCE_POST
8. JS_INJECT
9. AUTH_URLS
10. LANDING_URLS
```

---

### 3. PHISHLETS-COLLECTION.md (450+ lignes)

**Contenu** :

- Description de tous les phishlets disponibles
- Configuration rapide pour chaque plateforme
- Cookies capturés
- Champs credentials
- Notes importantes et pièges
- Comparaison des plateformes
- Déploiement multi-phishlets
- Checklist par phishlet

**Quand l'utiliser** :

- Choisir un phishlet
- Configuration rapide
- Comprendre les spécificités de chaque plateforme

**Phishlets documentés** :

1. Google/Gmail
2. Microsoft 365
3. GitHub
4. LinkedIn
5. Facebook
6. Okta

---

### 4. GUIDE-SELECTION-STRATEGIQUE.md (450+ lignes)

**Contenu** :

- Sélection de phishlet par scénario
- Red team corporate, développeurs, C-level
- Stratégies de déploiement
- Matrice de décision
- Recommandations par industrie
- Templates quick start
- KPIs et métriques
- Troubleshooting par phishlet

**Quand l'utiliser** :

- Planifier un engagement red team
- Choisir la meilleure stratégie
- Optimiser le taux de succès

**Scénarios couverts** :

- Red Team Corporate
- Red Team Développeurs
- Red Team Reconnaissance
- Red Team C-Level
- Pentest Awareness Training

---

### 5. google-phishlet-example.yaml (200+ lignes)

**Type** : Phishlet complet et avancé

**Caractéristiques** :

- Tous les domaines Google nécessaires
- Sub-filters exhaustifs
- Tous les cookies de session
- JS injection (Pro)
- Force POST configuré
- Auth URLs complètes

**Quand l'utiliser** :

- Production avec fonctionnalités avancées
- Contournement de protections Google
- Référence pour phishlets complexes

---

### 6. google-simple.yaml (150+ lignes)

**Type** : Phishlet simplifié et commenté

**Caractéristiques** :

- Commentaires ligne par ligne
- Structure minimaliste mais fonctionnelle
- Idéal pour apprendre
- Notes d'utilisation intégrées

**Quand l'utiliser** :

- Apprendre la structure des phishlets
- Premiers tests
- Base pour personnalisation

---

### 7. microsoft365.yaml (250+ lignes)

**Type** : Phishlet Microsoft 365 / Azure AD

**Cibles** :

- Office 365
- Outlook Web Access
- Teams
- SharePoint
- OneDrive

**Spécificités** :

- Authentification Azure AD
- Support ADFS
- Conditional Access
- MFA fréquent

**Difficulté** : ⭐⭐⭐⭐

---

### 8. github.yaml (180+ lignes)

**Type** : Phishlet GitHub

**Cibles** :

- Développeurs
- Repositories privés
- Organizations

**Spécificités** :

- Notifications email actives
- 2FA courant
- Session cookies valides 2 semaines

**Difficulté** : ⭐⭐⭐

---

### 9. linkedin.yaml (200+ lignes)

**Type** : Phishlet LinkedIn

**Cibles** :

- Professionnels
- Recruteurs
- Sales

**Spécificités** :

- ⚠️ Détection élevée
- Device fingerprinting
- Blacklist rapide (<24h)
- Rotation IP obligatoire

**Difficulté** : ⭐⭐⭐⭐

---

### 10. facebook.yaml (190+ lignes)

**Type** : Phishlet Facebook

**Cibles** :

- Utilisateurs Facebook
- Business pages
- Messager

**Spécificités** :

- 🚨 Détection EXTRÊME
- ML detection
- Blacklist instantanée
- ❌ Lab uniquement

**Difficulté** : ⭐⭐⭐⭐⭐

---

### 11. okta.yaml (210+ lignes)

**Type** : Phishlet Okta SSO

**Cibles** :

- Single Sign-On
- Corporate access
- Multi-app access

**Spécificités** :

- Variable {tenant}
- Un compte = toutes les apps
- Très haute valeur
- Device Trust

**Difficulté** : ⭐⭐⭐⭐

---

### 12. phishlet_analyzer.py (300+ lignes)

**Type** : Outil d'analyse Python

**Fonctionnalités** :

- Analyse automatique d'un site web
- Extraction des domaines
- Analyse des cookies
- Détection des champs de formulaire
- Génération de template YAML

**Usage** :

```bash
pip3 install requests
python3 phishlet_analyzer.py https://example.com
```

**Output** :

- Fichier `{domain}-template.yaml`
- Liste des domaines trouvés
- Cookies détectés
- Champs de formulaire

---

### 13. INDEX-COMPLET.md (Ce fichier)

**Type** : Index et guide de navigation

**Contenu** :

- Vue d'ensemble de tous les fichiers
- Guide d'utilisation par niveau
- Description détaillée de chaque fichier
- Workflows recommandés
- FAQ

---

## 🚀 WORKFLOWS RECOMMANDÉS

### Workflow 1 : Premier déploiement

```
1. Lire README-CODE-SOURCE.md
2. Installer Evilginx Pro localement
3. Tester google-simple.yaml en local
4. Suivre GUIDE-STRUCTURE-PHISHLET.md pour comprendre
5. Déployer en production selon PHISHLETS-COLLECTION.md
```

### Workflow 2 : Créer un phishlet custom

```
1. Identifier le site cible
2. Utiliser phishlet_analyzer.py
3. Éditer le template généré
4. Référer GUIDE-STRUCTURE-PHISHLET.md pour détails
5. Tester en local
6. Déployer
```

### Workflow 3 : Engagement red team

```
1. Reconnaissance de la cible
2. Lire GUIDE-SELECTION-STRATEGIQUE.md
3. Choisir le(s) phishlet(s) approprié(s)
4. Consulter PHISHLETS-COLLECTION.md pour configuration
5. Déployer selon stratégie choisie
6. Monitoring et ajustements
7. Reporting
```

### Workflow 4 : Troubleshooting

```
1. Identifier le problème
2. Consulter README-CODE-SOURCE.md (section Debugging)
3. Vérifier GUIDE-STRUCTURE-PHISHLET.md (section concernée)
4. Consulter PHISHLETS-COLLECTION.md (problèmes spécifiques)
5. Tester les solutions proposées
```

---

## 🎯 MATRICE DE NAVIGATION

### Par objectif

| Objectif              | Fichiers à consulter                                     | Ordre |
| --------------------- | -------------------------------------------------------- | ----- |
| Apprendre les bases   | google-simple.yaml → GUIDE-STRUCTURE-PHISHLET.md         | 1 → 2 |
| Déployer rapidement   | PHISHLETS-COLLECTION.md → Phishlet choisi                | 1 → 2 |
| Stratégie red team    | GUIDE-SELECTION-STRATEGIQUE.md → PHISHLETS-COLLECTION.md | 1 → 2 |
| Créer phishlet custom | phishlet_analyzer.py → GUIDE-STRUCTURE-PHISHLET.md       | 1 → 2 |
| Troubleshooting       | README-CODE-SOURCE.md → Fichier spécifique               | 1 → 2 |

### Par niveau d'expertise

| Niveau        | Commencer par           | Progresser vers             |
| ------------- | ----------------------- | --------------------------- |
| Débutant      | README + google-simple  | GUIDE-STRUCTURE             |
| Intermédiaire | PHISHLETS-COLLECTION    | GUIDE-SELECTION-STRATEGIQUE |
| Avancé        | google-phishlet-example | phishlet_analyzer.py        |
| Expert        | Tous les fichiers       | Création custom             |

---

## 💡 TIPS & ASTUCES

### Astuce 1 : Recherche rapide

```bash
# Chercher un concept dans tous les fichiers
grep -r "auth_tokens" /tmp/*.md /tmp/*.yaml

# Chercher une plateforme spécifique
grep -r "Microsoft" /tmp/*.md
```

### Astuce 2 : Comparaison de phishlets

```bash
# Comparer deux phishlets
diff /tmp/google-simple.yaml /tmp/microsoft365.yaml

# Voir uniquement les cookies
grep -A 5 "auth_tokens:" /tmp/*.yaml
```

### Astuce 3 : Génération rapide

```bash
# Copier tous les phishlets dans Evilginx
cp /tmp/*.yaml ~/evilginx-pro/phishlets/private/

# Créer un backup
tar -czf evilginx-phishlets-$(date +%Y%m%d).tar.gz /tmp/*.yaml
```

---

## 📊 STATISTIQUES DE LA COLLECTION

```
Total lignes de code:        ~5000+
Total fichiers:              13
Phishlets disponibles:       6
Plateformes couvertes:       6
Documentation (lignes):      ~3500
Code YAML (lignes):          ~1200
Code Python (lignes):        ~300
```

### Répartition par type

```
Documentation:     60%
Phishlets YAML:    25%
Scripts Python:    5%
Guides pratiques:  10%
```

---

## ❓ FAQ

### Q: Par où commencer ?

**R:** Commencez par `README-CODE-SOURCE.md`, puis `google-simple.yaml`.

### Q: Quel phishlet est le plus facile ?

**R:** Google et GitHub sont les plus simples pour débuter.

### Q: Comment créer mon propre phishlet ?

**R:** Utilisez `phishlet_analyzer.py` puis éditez avec `GUIDE-STRUCTURE-PHISHLET.md`.

### Q: Quel phishlet a le meilleur taux de succès ?

**R:** Microsoft 365 et Google en environnement corporate.

### Q: Comment éviter la détection ?

**R:** Consultez `GUIDE-SELECTION-STRATEGIQUE.md` section "Facteurs de risque".

### Q: Puis-je utiliser plusieurs phishlets simultanément ?

**R:** Oui ! Voir `PHISHLETS-COLLECTION.md` section "Déploiement multi-phishlets".

### Q: Les phishlets fonctionnent-ils avec Evilginx Community (gratuit) ?

**R:** Partiellement. Les fonctionnalités Pro (js_inject, etc.) nécessitent Evilginx Pro.

### Q: Comment débugger un phishlet qui ne fonctionne pas ?

**R:** `README-CODE-SOURCE.md` section "Debugging et Troubleshooting".

---

## 🔄 MISES À JOUR

### Version 1.0 (25 décembre 2025)

- ✅ 13 fichiers créés
- ✅ 6 phishlets complets
- ✅ Documentation exhaustive
- ✅ Guides stratégiques
- ✅ Outils d'analyse

### Mises à jour futures suggérées

- [ ] Phishlets additionnels (AWS, Azure, Dropbox, etc.)
- [ ] Scripts d'automatisation avancés
- [ ] Intégration Gophish
- [ ] Templates de rapports
- [ ] Dashboard de monitoring

---

## 📞 SUPPORT

### Documentation

- **Ce dossier** : Tout est dans `/tmp/`
- **Evilginx Pro** : https://help.evilginx.com/pro
- **BREAKDEV** : https://breakdev.org/

### Communauté

- **Discord BREAKDEV RED** : Phishlets à jour
- **GitHub** : https://github.com/kgretzky/evilginx2

---

## ⚠️ DISCLAIMER LÉGAL

```
📜 UTILISATION RESPONSABLE UNIQUEMENT

Cette collection est fournie à des fins de tests de sécurité
autorisés et d'éducation UNIQUEMENT.

✅ Autorisé :
   - Pentests avec contrat
   - Red team autorisé
   - Formation sécurité
   - Recherche académique

❌ Interdit :
   - Phishing criminel
   - Vol de données
   - Usage malveillant

L'auteur ne peut être tenu responsable d'une utilisation
abusive ou illégale de ces ressources.

En utilisant ces fichiers, vous acceptez de les utiliser de
manière éthique et légale uniquement.
```

---

## 🛠️ NOUVEAUTÉ : INTÉGRATION TELEGRAM

### GUIDE-TELEGRAM-NOTIFICATIONS.md (800+ lignes)

**Contenu** :

- Configuration du bot Telegram
- Installation du script de notifications
- Service systemd pour monitoring automatique
- Exemples de notifications
- Troubleshooting complet

**Fichiers associés** :

- `telegram_notifier.py` : Script Python de monitoring
- `telegram_notifier.service` : Service systemd

**Fonctionnalités** :

- ✅ Notifications instantanées sur Telegram
- ✅ Surveillance 24/7 de la base de données
- ✅ Formatage riche avec émojis
- ✅ Détails complets (credentials, cookies, IP)
- ✅ Support multi-phishlets
- ✅ Système d'état pour éviter les doublons

---

## 🎓 CONCLUSION

Vous disposez maintenant d'une **collection complète et professionnelle** pour utiliser Evilginx Pro efficacement.

**Ce que vous pouvez faire maintenant** :

1. ✅ Déployer 6 phishlets différents
2. ✅ Créer vos propres phishlets
3. ✅ Planifier des engagements red team
4. ✅ Comprendre en profondeur la structure des phishlets
5. ✅ Débugger et troubleshooter efficacement

**Prochaines étapes recommandées** :

1. Tester en local (127.0.0.1)
2. Déployer en production avec autorisation
3. Monitorer et documenter
4. Créer vos propres phishlets custom
5. Partager vos retours d'expérience

---

**🎣 Bonne utilisation et tests de sécurité responsables !**

---

_Index créé le 25 décembre 2025_
_Compatible Evilginx Pro 3.0+_
_Collection version 1.0_

---

## 📋 CHECKLIST FINALE

Avant de commencer votre premier engagement :

```markdown
- [ ] J'ai lu README-CODE-SOURCE.md
- [ ] J'ai compris la structure d'un phishlet
- [ ] J'ai testé au moins un phishlet en local
- [ ] J'ai choisi le bon phishlet pour ma cible
- [ ] J'ai une stratégie claire
- [ ] J'ai l'autorisation écrite nécessaire
- [ ] J'ai un plan de clean-up
- [ ] Je suis prêt à documenter mes résultats
```

**✅ Vous êtes prêt ! Bon engagement !**
