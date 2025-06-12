#!/bin/bash

# Script de Instalação Automatizada - Sistema de Estoque para Peças de Carro
# Versão: 1.0
# Desenvolvido por: Manus AI

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[AVISO] $1${NC}"
}

error() {
    echo -e "${RED}[ERRO] $1${NC}"
    exit 1
}

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
   error "Este script não deve ser executado como root. Execute como usuário normal com sudo."
fi

# Verificar sistema operacional
if [[ ! -f /etc/os-release ]]; then
    error "Sistema operacional não suportado. Este script funciona apenas em distribuições Linux baseadas em Debian/Ubuntu."
fi

source /etc/os-release
if [[ "$ID" != "ubuntu" && "$ID" != "debian" ]]; then
    warn "Sistema operacional não testado: $ID. Continuando mesmo assim..."
fi

log "Iniciando instalação do Sistema de Estoque para Peças de Carro"

# Configurações
INSTALL_DIR="/home/$(whoami)/sistema_estoque"
SERVICE_USER="$(whoami)"
DOMAIN=""
EMAIL=""

# Perguntar configurações ao usuário
echo -e "${BLUE}=== Configuração da Instalação ===${NC}"
read -p "Diretório de instalação [$INSTALL_DIR]: " input_dir
INSTALL_DIR=${input_dir:-$INSTALL_DIR}

read -p "Domínio para o sistema (ex: estoque.empresa.com) [localhost]: " input_domain
DOMAIN=${input_domain:-localhost}

if [[ "$DOMAIN" != "localhost" ]]; then
    read -p "Email para certificado SSL: " EMAIL
fi

echo -e "${BLUE}=== Resumo da Configuração ===${NC}"
echo "Diretório: $INSTALL_DIR"
echo "Domínio: $DOMAIN"
echo "Usuário: $SERVICE_USER"
echo ""
read -p "Continuar com a instalação? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "Instalação cancelada."
    exit 0
fi

# Atualizar sistema
log "Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências básicas
log "Instalando dependências básicas..."
sudo apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Instalar Python 3.11
log "Instalando Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Instalar Node.js 18
log "Instalando Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar pnpm
log "Instalando pnpm..."
sudo npm install -g pnpm

# Instalar PostgreSQL
log "Instalando PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

# Instalar Nginx
log "Instalando Nginx..."
sudo apt install -y nginx

# Configurar PostgreSQL
log "Configurando PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Criar banco de dados
DB_PASSWORD=$(openssl rand -base64 32)
sudo -u postgres psql << EOF
CREATE DATABASE sistema_estoque;
CREATE USER estoque_user WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE sistema_estoque TO estoque_user;
\q
EOF

log "Banco de dados criado com sucesso"

# Criar diretório de instalação
log "Criando diretório de instalação..."
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Verificar se os arquivos do sistema estão no diretório atual
if [[ ! -d "sistema_estoque_backend" || ! -d "sistema_estoque_frontend" ]]; then
    error "Arquivos do sistema não encontrados. Certifique-se de que os diretórios 'sistema_estoque_backend' e 'sistema_estoque_frontend' estão no diretório atual."
fi

# Configurar backend
log "Configurando backend..."
cd "$INSTALL_DIR/sistema_estoque_backend"

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Criar arquivo .env
cat > .env << EOF
# Configurações do banco de dados
DATABASE_URL=postgresql://estoque_user:$DB_PASSWORD@localhost/sistema_estoque

# Configurações de segurança
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production

# Configurações do Mercado Livre (configure manualmente)
ML_CLIENT_ID=
ML_CLIENT_SECRET=
ML_REDIRECT_URI=https://$DOMAIN/api/ml/callback
EOF

log "Arquivo .env criado. Configure as credenciais do Mercado Livre manualmente."

# Configurar frontend
log "Configurando frontend..."
cd "$INSTALL_DIR/sistema_estoque_frontend"

# Instalar dependências
pnpm install

# Criar arquivo de configuração
cat > .env.local << EOF
VITE_API_BASE_URL=https://$DOMAIN/api
EOF

# Compilar para produção
pnpm run build

# Criar serviço systemd
log "Criando serviço systemd..."
sudo tee /etc/systemd/system/sistema-estoque.service > /dev/null << EOF
[Unit]
Description=Sistema de Estoque Backend
After=network.target postgresql.service

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR/sistema_estoque_backend
Environment=PATH=$INSTALL_DIR/sistema_estoque_backend/venv/bin
ExecStart=$INSTALL_DIR/sistema_estoque_backend/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configurar Nginx
log "Configurando Nginx..."
sudo tee /etc/nginx/sites-available/sistema-estoque > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN;

    # Frontend estático
    location / {
        root $INSTALL_DIR/sistema_estoque_frontend/dist;
        try_files \$uri \$uri/ /index.html;
        
        # Headers de cache para assets estáticos
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Logs
    access_log /var/log/nginx/sistema-estoque-access.log;
    error_log /var/log/nginx/sistema-estoque-error.log;
}
EOF

# Ativar site
sudo ln -sf /etc/nginx/sites-available/sistema-estoque /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração do Nginx
sudo nginx -t

# Configurar SSL se não for localhost
if [[ "$DOMAIN" != "localhost" ]]; then
    log "Configurando SSL com Let's Encrypt..."
    sudo apt install -y certbot python3-certbot-nginx
    
    if [[ -n "$EMAIL" ]]; then
        sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "$EMAIL"
    else
        warn "Email não fornecido. Configure SSL manualmente com: sudo certbot --nginx -d $DOMAIN"
    fi
fi

# Configurar firewall
log "Configurando firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Inicializar banco de dados
log "Inicializando banco de dados..."
cd "$INSTALL_DIR/sistema_estoque_backend"
source venv/bin/activate
python -c "
from src.models.database import db
from src.main import app
with app.app_context():
    db.create_all()
    print('Banco de dados inicializado com sucesso')
"

# Iniciar serviços
log "Iniciando serviços..."
sudo systemctl daemon-reload
sudo systemctl enable sistema-estoque
sudo systemctl start sistema-estoque
sudo systemctl restart nginx

# Verificar status dos serviços
log "Verificando status dos serviços..."
sleep 5

if sudo systemctl is-active --quiet sistema-estoque; then
    log "✓ Serviço backend está rodando"
else
    error "✗ Falha ao iniciar serviço backend"
fi

if sudo systemctl is-active --quiet nginx; then
    log "✓ Nginx está rodando"
else
    error "✗ Falha ao iniciar Nginx"
fi

if sudo systemctl is-active --quiet postgresql; then
    log "✓ PostgreSQL está rodando"
else
    error "✗ Falha ao iniciar PostgreSQL"
fi

# Criar scripts de backup
log "Configurando scripts de backup..."
mkdir -p "$INSTALL_DIR/scripts"

# Script de backup do banco
cat > "$INSTALL_DIR/scripts/backup_db.sh" << 'EOF'
#!/bin/bash
BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -h localhost -U estoque_user -d sistema_estoque > $BACKUP_DIR/backup_$DATE.sql

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

echo "Backup realizado: backup_$DATE.sql"
EOF

chmod +x "$INSTALL_DIR/scripts/backup_db.sh"

# Configurar crontab para backup diário
(crontab -l 2>/dev/null; echo "0 2 * * * $INSTALL_DIR/scripts/backup_db.sh") | crontab -

# Criar arquivo de informações da instalação
cat > "$INSTALL_DIR/INSTALACAO.txt" << EOF
=== INFORMAÇÕES DA INSTALAÇÃO ===

Data da instalação: $(date)
Diretório: $INSTALL_DIR
Domínio: $DOMAIN
Usuário do serviço: $SERVICE_USER

=== CREDENCIAIS DO BANCO ===
Usuário: estoque_user
Senha: $DB_PASSWORD
Banco: sistema_estoque

=== CREDENCIAIS PADRÃO DO SISTEMA ===
Email: admin@empresa.com
Senha: 123456

⚠️  IMPORTANTE: Altere a senha padrão após o primeiro acesso!

=== CONFIGURAÇÃO DO MERCADO LIVRE ===
Edite o arquivo: $INSTALL_DIR/sistema_estoque_backend/.env
Configure as variáveis:
- ML_CLIENT_ID
- ML_CLIENT_SECRET

=== COMANDOS ÚTEIS ===
# Verificar status do serviço
sudo systemctl status sistema-estoque

# Reiniciar serviço
sudo systemctl restart sistema-estoque

# Ver logs
journalctl -u sistema-estoque -f

# Backup manual
$INSTALL_DIR/scripts/backup_db.sh

=== ARQUIVOS DE LOG ===
- Aplicação: journalctl -u sistema-estoque
- Nginx: /var/log/nginx/sistema-estoque-*.log
- PostgreSQL: /var/log/postgresql/

=== PRÓXIMOS PASSOS ===
1. Acesse https://$DOMAIN (ou http://$DOMAIN se SSL não configurado)
2. Faça login com as credenciais padrão
3. Altere a senha do administrador
4. Configure as credenciais do Mercado Livre
5. Comece a cadastrar seus produtos!
EOF

# Finalização
echo ""
echo -e "${GREEN}=== INSTALAÇÃO CONCLUÍDA COM SUCESSO! ===${NC}"
echo ""
echo -e "${BLUE}Sistema instalado em:${NC} $INSTALL_DIR"
echo -e "${BLUE}URL de acesso:${NC} https://$DOMAIN"
echo -e "${BLUE}Login padrão:${NC} admin@empresa.com / 123456"
echo ""
echo -e "${YELLOW}PRÓXIMOS PASSOS:${NC}"
echo "1. Acesse o sistema através da URL"
echo "2. Altere a senha padrão"
echo "3. Configure as credenciais do Mercado Livre"
echo "4. Consulte o arquivo INSTALACAO.txt para mais informações"
echo ""
echo -e "${GREEN}Documentação completa disponível em: $INSTALL_DIR/README.md${NC}"
echo ""
log "Instalação finalizada!"

