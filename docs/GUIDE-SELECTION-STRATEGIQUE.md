# 🎯 GUIDE STRATÉGIQUE - SÉLECTION DE PHISHLETS

## 📊 Vue d'ensemble

Vous avez maintenant **6 phishlets complets** à votre disposition :

```
/tmp/
├── google-simple.yaml          # Google/Gmail
├── microsoft365.yaml           # Microsoft 365/Azure AD
├── github.yaml                 # GitHub
├── linkedin.yaml               # LinkedIn
├── facebook.yaml               # Facebook
└── okta.yaml                   # Okta SSO
```

---

## 🎓 GUIDE DE SÉLECTION PAR SCÉNARIO

### 1. Red Team - Entreprise Corporate

**Objectif** : Accès aux systèmes internes d'entreprise

**Phishlets recommandés** :

1. **Microsoft 365** (Priorité 1)

   - 90% des entreprises utilisent Office 365
   - Accès : Email, Teams, SharePoint, OneDrive
   - Token de session valide pour tous les services Microsoft

2. **Okta** (Priorité 2)
   - Un compte = accès à toutes les apps SSO
   - Très haute valeur
   - Nécessite reconnaissance du tenant

**Pretext suggéré** :

```
"Action Required: Verify Your Microsoft Account"
"Your access will be suspended in 24h"
"IT Security: Password Policy Update"
"Teams Meeting Invitation - [Nom du CEO]"
```

**Configuration DNS recommandée** :

```
login.votredomaine.com      → Microsoft 365
sso.votredomaine.com        → Okta
portal.votredomaine.com     → Backup Microsoft
```

---

### 2. Red Team - Développeurs / Tech

**Objectif** : Accès aux repositories, code source, secrets

**Phishlets recommandés** :

1. **GitHub** (Priorité 1)

   - Accès aux repos privés
   - Secrets dans les repos (API keys, tokens)
   - Actions/Workflows avec credentials

2. **Google** (Priorité 2)
   - Gmail pour reset password d'autres services
   - Google Drive avec documentation technique
   - Google Cloud Platform si utilisé

**Pretext suggéré** :

```
"Security Alert: Unusual Activity on Your GitHub Account"
"[Nom du projet] - Pull Request Review Required"
"GitHub Security: Enable 2FA to Continue"
"Repository Access: [Nom repo important]"
```

**Configuration DNS recommandée** :

```
github.votredomaine.com     → GitHub
accounts.votredomaine.com   → Google
security.votredomaine.com   → Variante GitHub
```

---

### 3. Red Team - Reconnaissance / OSINT

**Objectif** : Collecte d'informations, cartographie de l'organisation

**Phishlets recommandés** :

1. **LinkedIn** (Avec précautions)

   - Structure organisationnelle
   - Contacts et relations
   - Informations sur projets/technologies

2. **Microsoft 365**
   - Emails pour reconnaissance
   - Calendriers (meetings, absences)
   - SharePoint (organigrammes, docs internes)

**⚠️ Attention LinkedIn** :

- Détection très élevée
- Utiliser en début d'engagement seulement
- Domaine jetable obligatoire
- Maximum 10-20 cibles

**Pretext suggéré** :

```
"LinkedIn Security Alert: Verify Your Identity"
"Your Profile Was Viewed by [Nom crédible]"
"Premium Trial: Unlock InMail Credits"
```

---

### 4. Red Team - C-Level / Executives

**Objectif** : Cibler les dirigeants pour accès haut privilège

**Phishlets recommandés** :

1. **Microsoft 365** (Adapté)

   - Executives utilisent surtout Outlook
   - Pretext: Meetings, documents confidentiels
   - High impact, low volume

2. **Okta** (Si utilisé)
   - Accès administrateur potentiel
   - Privilèges élevés

**Pretext suggéré** :

```
"Board Meeting Materials - Confidential"
"CEO: Urgent Review Required"
"Executive Briefing - Q4 Results"
"DocuSign: Contract Requiring Signature"
```

**Particularités** :

- Volume très faible (1-5 cibles max)
- Pretext ultra-crédible nécessaire
- Timing critique (éviter weekends)
- Suivi rapproché obligatoire

---

### 5. Pentest - Awareness Training

**Objectif** : Tester la sensibilisation des employés

**Phishlets recommandés** :

1. **Microsoft 365** ou **Google** (selon l'entreprise)
   - Plateformes familières
   - Realistic scenario
   - Safe landing pages

**Configuration spéciale** :

```yaml
# Landing URL vers page d'awareness
landing_urls:
  - "https://training.company.com/phishing-awareness"
  - "/security-training"
```

**Pretext éthique** :

```
"IT Update: System Maintenance Required"
"Password Expiration Notice"
"Access Renewal Request"
```

**Metrics à collecter** :

- Taux de clic
- Taux de soumission credentials
- Temps de réaction
- Reporting par les utilisateurs

---

## 📈 STRATÉGIES DE DÉPLOIEMENT

### Stratégie 1 : Spear Phishing (Haute Précision)

**Caractéristiques** :

- 1-10 cibles très spécifiques
- Pretext hautement personnalisé
- Reconnaissance approfondie préalable

**Phishlets** : Microsoft 365, Okta
**Domaine** : Très crédible (typosquatting léger)
**Exemple** : `microsoft-services.com`, `okta-verify.com`

**Timeline** :

```
Jour 1-3  : Reconnaissance
Jour 4    : Déploiement infrastructure
Jour 5    : Envoi phishing
Jour 5-7  : Monitoring actif
Jour 8    : Clean-up
```

---

### Stratégie 2 : Campagne Large (Volume)

**Caractéristiques** :

- 50-500 cibles
- Pretext générique mais crédible
- Rotation d'infrastructure

**Phishlets** : Google, GitHub, Microsoft 365
**Domaines** : Multiples, rotation tous les 2 jours
**Exemple** : `accounts-verify.com`, `github-security.com`

**Timeline** :

```
Semaine 1 : Setup + Envoi batch 1 (Google)
Semaine 2 : Rotation + Envoi batch 2 (Microsoft)
Semaine 3 : Rotation + Envoi batch 3 (GitHub)
Semaine 4 : Analysis + Reporting
```

---

### Stratégie 3 : Multi-Vector (Combiné)

**Caractéristiques** :

- Plusieurs plateformes simultanément
- Pretext coordonné
- Infrastructure distribuée

**Exemple de scénario** :

```
1. Email depuis "IT Department" → Microsoft 365 phishing
2. Si échec : LinkedIn message → LinkedIn phishing
3. Si échec : Notification GitHub → GitHub phishing
```

**Phishlets utilisés** : 3-4 simultanés
**Serveurs** : 2-3 serveurs Evilginx différents

---

## 🎯 MATRICE DE DÉCISION

### Choix du phishlet selon les critères

| Critère                       | Microsoft 365 | Google     | GitHub     | Okta       | LinkedIn | Facebook |
| ----------------------------- | ------------- | ---------- | ---------- | ---------- | -------- | -------- |
| **Entreprise Corporate**      | ⭐⭐⭐⭐⭐    | ⭐⭐⭐     | ⭐⭐       | ⭐⭐⭐⭐⭐ | ⭐⭐     | ⭐       |
| **Tech/Startups**             | ⭐⭐⭐        | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ⭐⭐     | ⭐       |
| **Facilité d'implémentation** | ⭐⭐⭐        | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐       | ⭐⭐     | ⭐       |
| **Taux de succès**            | ⭐⭐⭐⭐      | ⭐⭐⭐⭐   | ⭐⭐⭐     | ⭐⭐⭐     | ⭐⭐     | ⭐       |
| **Valeur des accès**          | ⭐⭐⭐⭐⭐    | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐     | ⭐⭐     |
| **Durée de vie session**      | ⭐⭐⭐⭐      | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ⭐⭐⭐     | ⭐⭐⭐   | ⭐⭐⭐   |

---

## 🛡️ FACTEURS DE RISQUE

### Niveau de détection par plateforme

**Faible** (Sûr pour production) :

- ✅ Google
- ✅ GitHub
- ✅ Microsoft 365 (avec bonne infrastructure)

**Moyen** (Précautions nécessaires) :

- ⚠️ Okta (selon configuration)
- ⚠️ LinkedIn (rotation IP obligatoire)

**Élevé** (Lab/Demo uniquement) :

- ❌ Facebook

---

## 💡 RECOMMANDATIONS PAR INDUSTRIE

### Finance / Banking

**Phishlets** : Microsoft 365, Okta
**Raison** : Environnement hautement régulé, focus sur compliance

### Technology / Software

**Phishlets** : GitHub, Google, Okta
**Raison** : Développeurs cibles, repos de code

### Healthcare

**Phishlets** : Microsoft 365, Okta
**Raison** : HIPAA compliance, systèmes legacy

### Manufacturing

**Phishlets** : Microsoft 365
**Raison** : Infrastructure IT traditionnelle

### Education

**Phishlets** : Google, Microsoft 365
**Raison** : Mix Google Workspace / Office 365

### Government

**Phishlets** : Microsoft 365, Okta
**Raison** : Sécurité renforcée, audits fréquents

---

## 🚀 QUICK START TEMPLATES

### Template 1 : Corporate Standard

```bash
#!/bin/bash
# Déploiement corporate standard
DOMAIN="secure-verify.com"

phishlets push private/microsoft365
phishlets set private/microsoft365 hostname login.$DOMAIN
phishlets enable private/microsoft365
lures create private/microsoft365 /common/oauth2/authorize
```

### Template 2 : Tech Company

```bash
#!/bin/bash
# Déploiement tech company
DOMAIN="dev-secure.com"

phishlets push private/github
phishlets set private/github hostname github.$DOMAIN
phishlets enable private/github

phishlets push private/google-simple
phishlets set private/google-simple hostname accounts.$DOMAIN
phishlets enable private/google-simple
```

### Template 3 : Multi-Platform

```bash
#!/bin/bash
# Déploiement multi-plateforme
DOMAIN="identity-check.com"

for phishlet in microsoft365 google-simple github okta; do
    phishlets push private/$phishlet
    phishlets set private/$phishlet hostname ${phishlet%%-*}.$DOMAIN
    phishlets enable private/$phishlet
done
```

---

## 📋 CHECKLIST DE SÉLECTION

Avant de choisir votre phishlet :

```markdown
- [ ] J'ai identifié la ou les plateformes utilisées par la cible
- [ ] J'ai vérifié le taux d'utilisation MFA
- [ ] J'ai un pretext crédible adapté à la plateforme
- [ ] J'ai un domaine crédible disponible
- [ ] Je connais le niveau de détection de la plateforme
- [ ] J'ai une stratégie de rotation si nécessaire
- [ ] Je sais quelles données je veux exfiltrer
- [ ] J'ai l'autorisation écrite pour ce test
- [ ] J'ai un plan de clean-up
- [ ] Je peux justifier ce choix dans mon rapport
```

---

## 🎓 EXERCICES PRATIQUES

### Exercice 1 : Reconnaissance

```
Scénario : Red team contre "Acme Corp"
Tâche : Identifier quelle(s) plateforme(s) ils utilisent

Méthodologie :
1. Analyse DNS (MX records → Microsoft ou Google?)
2. Jobs postings (technologies mentionnées)
3. LinkedIn employees (mentionner les outils)
4. Error pages (leak de plateforme)

Résultat attendu : Liste prioritée de 2-3 phishlets
```

### Exercice 2 : Pretext Design

```
Scénario : Cibler des développeurs
Plateforme : GitHub
Tâche : Créer 3 pretexts différents

Exemples :
1. Security alert → Lure: /security/alert
2. PR review → Lure: /pull/12345
3. Issue mention → Lure: /issues/789

Critères : Crédibilité, urgence, personnalisation
```

---

## 📊 MÉTRIQUES DE SUCCÈS

### KPIs à suivre

```yaml
Taux de clic: (Clics / Envois) * 100
Taux de soumission: (Credentials / Clics) * 100
Taux de capture session: (Sessions / Soumissions) * 100
Time-to-click: Temps moyen avant clic
Time-to-submit: Temps moyen avant soumission
Detection rate: Signalements / Envois
```

### Benchmarks industry

```
Taux de clic moyen: 15-30%
Taux de soumission moyen: 40-60%
Taux de capture session moyen: 80-95%

Excellents résultats: >30% / >60% / >90%
Bons résultats: 20-30% / 40-60% / 80-90%
À améliorer: <20% / <40% / <80%
```

---

## 🔍 TROUBLESHOOTING PAR PHISHLET

### Google

**Problème** : reCAPTCHA bloque
**Solution** : Utiliser Evilpuppet (Pro)

### Microsoft 365

**Problème** : Conditional Access bloque
**Solution** : IP du pays de la cible, User-Agent cohérent

### GitHub

**Problème** : Email de notification envoyé
**Solution** : Capture rapide, pretext cohérent

### LinkedIn

**Problème** : Blacklist rapide
**Solution** : Domaine jetable, rotation IP, volume limité

### Okta

**Problème** : Device Trust fail
**Solution** : User-Agent matching, no automation flags

---

**🎯 Vous êtes maintenant prêt à sélectionner le phishlet optimal pour votre engagement !**

_Guide créé le 25 décembre 2025_
_Pour Evilginx Pro 3.0+_
