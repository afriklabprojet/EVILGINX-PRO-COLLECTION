# 📦 ARCHIVE - Fichiers Alternatifs

Ce dossier contient les fichiers alternatifs qui ne sont pas utilisés dans la configuration principale, mais qui peuvent être utiles selon vos besoins.

---

## 📂 Structure

```
archive/
├── scripts-alternatifs/          # Scripts de notification alternatifs
└── phishlets-alternatifs/        # Versions alternatives de phishlets
```

---

## 🔧 Scripts Alternatifs

### `scripts-alternatifs/evilginx_telegram_notifier.py`
**Alternative au script principal `telegram_notifier.py`**

- Version différente du notifier Telegram
- Peut avoir des fonctionnalités légèrement différentes
- Utilisez-le si vous préférez cette implémentation

**Utilisation :**
```bash
cp archive/scripts-alternatifs/evilginx_telegram_notifier.py scripts/
# Modifier la configuration selon vos besoins
```

### `scripts-alternatifs/evilginx_webhook_notifier.py`
**Notifications via Webhook (Discord, Slack, etc.)**

- Alternative aux notifications Telegram
- Supporte les webhooks génériques
- Compatible Discord, Slack, et autres plateformes

**Utilisation :**
```bash
cp archive/scripts-alternatifs/evilginx_webhook_notifier.py scripts/
nano scripts/evilginx_webhook_notifier.py
# Configurer votre URL webhook
```

---

## 🎯 Phishlets Alternatifs

### `phishlets-alternatifs/google-phishlet-example.yaml`
**Version alternative du phishlet Google**

- Autre implémentation pour Google
- Peut avoir des configurations différentes
- Utile pour comparaison ou test

**Utilisation :**
```bash
cp archive/phishlets-alternatifs/google-phishlet-example.yaml phishlets/
# Renommer si nécessaire
```

---

## 💡 Quand utiliser ces fichiers ?

### Scripts alternatifs
- ✅ Si le script principal ne fonctionne pas
- ✅ Si vous préférez une autre implémentation
- ✅ Si vous avez besoin de webhooks au lieu de Telegram
- ✅ Pour tester différentes approches

### Phishlets alternatifs
- ✅ Si le phishlet principal ne fonctionne pas
- ✅ Pour comparer les implémentations
- ✅ Pour apprendre différentes techniques
- ✅ Comme base pour vos propres modifications

---

## 🔄 Restaurer un fichier

Pour utiliser un fichier archivé :

```bash
# Scripts
cp archive/scripts-alternatifs/FICHIER.py scripts/

# Phishlets
cp archive/phishlets-alternatifs/FICHIER.yaml phishlets/
```

---

## ⚠️ Note

Ces fichiers sont **archivés** car :
- Ils sont des doublons de fonctionnalités existantes
- Ils ne sont pas utilisés dans l'installation par défaut
- Ils peuvent créer de la confusion
- Ils restent disponibles si nécessaire

**Fichiers principaux recommandés :**
- `scripts/telegram_notifier.py` (notifications)
- `phishlets/google-simple.yaml` (Google simple)
- `phishlets/google-advanced.yaml` (Google avancé)

---

## 📚 Documentation

Pour la documentation complète :
- [Guide principal](../docs/README-CODE-SOURCE.md)
- [Guide de déploiement VPS](../docs/GUIDE-DEPLOIEMENT-VPS.md)
- [Guide Telegram](../docs/GUIDE-TELEGRAM-NOTIFICATIONS.md)

---

_Archivé le 6 janvier 2026_  
_Ces fichiers restent disponibles pour référence et utilisation alternative_
