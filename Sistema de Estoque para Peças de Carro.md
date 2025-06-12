# Sistema de Estoque para Peças de Carro

**Versão:** 1.0  
**Data:** Junho 2025  
**Desenvolvido por:** Manus AI  

---

## 📋 Visão Geral

O Sistema de Estoque para Peças de Carro é uma solução completa e moderna desenvolvida especificamente para empresas que trabalham com venda de peças automotivas. O sistema oferece controle total sobre o inventário, integração automática com o Mercado Livre, e uma interface web intuitiva para gerenciamento eficiente do negócio.

### 🎯 Principais Funcionalidades

- **Controle Completo de Estoque**: Gerenciamento detalhado de produtos com alertas automáticos para estoque baixo
- **Integração com Mercado Livre**: Sincronização automática de estoque e recebimento de pedidos em tempo real
- **Interface Web Moderna**: Dashboard intuitivo com métricas importantes e navegação responsiva
- **Sistema de Usuários**: Controle de acesso com diferentes níveis de permissão
- **Relatórios Detalhados**: Análise de vendas, estoque e performance do negócio
- **API REST Completa**: Integração com sistemas externos através de API documentada

### 🏗️ Arquitetura do Sistema

- **Backend**: Flask (Python) com SQLAlchemy ORM
- **Frontend**: React com Vite e Tailwind CSS
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Integração**: API REST do Mercado Livre com OAuth 2.0
- **Deploy**: Nginx como proxy reverso, Systemd para gerenciamento de serviços

---

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 12+ (para produção)
- Nginx (para produção)

### Instalação Rápida (Desenvolvimento)

```bash
# 1. Backend
cd sistema_estoque_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py

# 2. Frontend (em outro terminal)
cd sistema_estoque_frontend
pnpm install
pnpm run dev
```

O sistema estará disponível em:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5001

### Login Padrão

- **Email**: admin@empresa.com
- **Senha**: 123456

> ⚠️ **Importante**: Altere a senha padrão após o primeiro acesso!

---

## 📁 Estrutura do Projeto

```
sistema_estoque/
├── sistema_estoque_backend/          # Backend Flask
│   ├── src/
│   │   ├── main.py                   # Aplicação principal
│   │   ├── models/                   # Modelos de dados
│   │   ├── routes/                   # Rotas da API
│   │   └── services/                 # Serviços de integração
│   ├── requirements.txt              # Dependências Python
│   └── .env.example                  # Exemplo de configuração
├── sistema_estoque_frontend/         # Frontend React
│   ├── src/
│   │   ├── App.jsx                   # Componente principal
│   │   ├── components/               # Componentes React
│   │   └── assets/                   # Recursos estáticos
│   ├── package.json                  # Dependências Node.js
│   └── vite.config.js               # Configuração Vite
└── documentacao/                     # Documentação completa
    ├── manual_usuario.md             # Manual do usuário
    ├── guia_instalacao.md           # Guia de instalação
    ├── documentacao_api.md          # Documentação da API
    └── *.pdf                        # Versões em PDF
```

---

## 📚 Documentação

### Documentos Disponíveis

1. **[Manual do Usuário](manual_usuario.md)** ([PDF](manual_usuario.pdf))
   - Guia completo para uso do sistema
   - Instruções passo a passo para todas as funcionalidades
   - Solução de problemas comuns

2. **[Guia de Instalação](guia_instalacao.md)** ([PDF](guia_instalacao.pdf))
   - Instalação completa para desenvolvimento e produção
   - Configuração do banco de dados
   - Deploy com Nginx e SSL

3. **[Documentação da API](documentacao_api.md)** ([PDF](documentacao_api.pdf))
   - Referência completa da API REST
   - Exemplos de uso em Python e JavaScript
   - Códigos de resposta e tratamento de erros

### Documentos Técnicos Adicionais

- **[Requisitos do Sistema](requisitos_sistema_interno.md)**: Análise detalhada dos requisitos
- **[Design da Arquitetura](design_arquitetura_banco_dados.md)**: Arquitetura e banco de dados
- **[API Mercado Livre](api_mercadolivre_*.md)**: Documentação da integração

---

## 🔧 Configuração

### Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```bash
# Mercado Livre
ML_CLIENT_ID=seu_client_id
ML_CLIENT_SECRET=seu_client_secret
ML_REDIRECT_URI=http://seu-dominio.com/api/ml/callback

# Banco de Dados (Produção)
DATABASE_URL=postgresql://usuario:senha@localhost/sistema_estoque

# Segurança
SECRET_KEY=sua_chave_secreta_muito_segura
FLASK_ENV=production
```

### Integração com Mercado Livre

1. Acesse o [Portal de Desenvolvedores do ML](https://developers.mercadolivre.com.br)
2. Crie uma nova aplicação
3. Configure as credenciais no arquivo `.env`
4. Autorize o acesso através da interface do sistema

---

## 🛠️ Desenvolvimento

### Executar em Modo Desenvolvimento

```bash
# Backend
cd sistema_estoque_backend
source venv/bin/activate
python src/main.py

# Frontend
cd sistema_estoque_frontend
pnpm run dev
```

### Executar Testes

```bash
# Testar API
curl http://localhost:5001/api/produtos

# Testar frontend
# Acesse http://localhost:5173 no navegador
```

### Estrutura da API

- `GET /api/produtos` - Listar produtos
- `POST /api/produtos` - Criar produto
- `GET /api/pedidos` - Listar pedidos
- `POST /api/auth/login` - Fazer login
- `GET /api/ml/status` - Status da integração ML

Consulte a [documentação completa da API](documentacao_api.md) para todos os endpoints.

---

## 🚀 Deploy em Produção

### Deploy Automático

Use o script de instalação automatizada:

```bash
chmod +x install.sh
sudo ./install.sh
```

### Deploy Manual

1. **Preparar servidor**:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 nodejs nginx postgresql -y
```

2. **Configurar banco de dados**:
```bash
sudo -u postgres createdb sistema_estoque
sudo -u postgres createuser estoque_user
```

3. **Deploy backend**:
```bash
cd sistema_estoque_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Deploy frontend**:
```bash
cd sistema_estoque_frontend
pnpm install
pnpm run build
```

5. **Configurar Nginx**:
```bash
sudo cp nginx.conf /etc/nginx/sites-available/sistema_estoque
sudo ln -s /etc/nginx/sites-available/sistema_estoque /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

Consulte o [Guia de Instalação](guia_instalacao.md) para instruções detalhadas.

---

## 📊 Funcionalidades Principais

### Gerenciamento de Produtos

- Cadastro completo com informações específicas para peças automotivas
- Controle de estoque com alertas automáticos
- Upload de múltiplas imagens
- Compatibilidade veicular detalhada
- Sincronização automática com Mercado Livre

### Controle de Estoque

- Monitoramento em tempo real
- Alertas de estoque baixo
- Histórico de movimentações
- Relatórios de giro de estoque
- Sincronização automática com vendas

### Integração Mercado Livre

- Autenticação OAuth 2.0 segura
- Sincronização automática de estoque
- Recebimento automático de pedidos
- Webhooks para atualizações em tempo real
- Monitoramento de status da integração

### Dashboard e Relatórios

- Métricas em tempo real
- Análise de vendas por período
- Produtos mais vendidos
- Controle de margem de lucro
- Exportação de relatórios

---

## 🔐 Segurança

### Medidas Implementadas

- Autenticação baseada em sessão
- Controle de acesso por níveis (admin, estoque, visualizador)
- Validação de dados de entrada
- Proteção contra CSRF
- Logs de auditoria
- Comunicação HTTPS em produção

### Boas Práticas

- Altere senhas padrão imediatamente
- Use HTTPS em produção
- Mantenha backups regulares
- Monitore logs de acesso
- Atualize dependências regularmente

---

## 🔄 Backup e Manutenção

### Backup Automático

O sistema inclui scripts para backup automático:

```bash
# Backup diário do banco de dados
0 2 * * * /home/estoque/backup_db.sh

# Backup semanal completo
0 3 * * 0 /home/estoque/backup_completo.sh
```

### Manutenção Regular

- Limpeza de logs antigos
- Otimização do banco de dados
- Monitoramento de performance
- Atualizações de segurança

---

## 🆘 Suporte e Solução de Problemas

### Problemas Comuns

1. **Erro de login**: Verifique credenciais e conexão
2. **Sincronização ML**: Verifique tokens e conectividade
3. **Performance lenta**: Monitore recursos do servidor
4. **Erro de banco**: Verifique configuração PostgreSQL

### Logs do Sistema

```bash
# Logs da aplicação
journalctl -u sistema-estoque -f

# Logs do Nginx
sudo tail -f /var/log/nginx/error.log

# Logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Contato para Suporte

Para suporte técnico ou dúvidas:
- Consulte a documentação completa
- Verifique os logs do sistema
- Entre em contato com o administrador

---

## 📈 Próximos Passos

### Melhorias Futuras

- Integração com outras plataformas (OLX, Facebook Marketplace)
- App mobile para consulta de estoque
- Integração com sistemas de transportadoras
- Relatórios avançados com BI
- Sistema de código de barras
- Integração com ERP existente

### Expansão do Sistema

- Multi-loja para franquias
- Marketplace próprio
- Sistema de fornecedores
- Gestão financeira integrada
- CRM para clientes

---

## 📄 Licença e Créditos

**Desenvolvido por:** Manus AI  
**Versão:** 1.0  
**Data:** Junho 2025  

Este sistema foi desenvolvido especificamente para atender às necessidades de empresas do setor de peças automotivas, oferecendo uma solução completa e moderna para gestão de estoque e vendas online.

### Tecnologias Utilizadas

- **Backend**: Flask, SQLAlchemy, Requests
- **Frontend**: React, Vite, Tailwind CSS, Lucide Icons
- **Banco de Dados**: PostgreSQL, SQLite
- **Infraestrutura**: Nginx, Systemd, Let's Encrypt
- **Integração**: API Mercado Livre, OAuth 2.0

---

## 🎯 Conclusão

O Sistema de Estoque para Peças de Carro representa uma solução completa e moderna para gestão de inventário e vendas online. Com integração automática ao Mercado Livre, interface intuitiva, e documentação abrangente, o sistema está pronto para transformar a eficiência operacional do seu negócio.

Para começar a usar o sistema, siga o [Guia de Instalação](guia_instalacao.md) e consulte o [Manual do Usuário](manual_usuario.md) para instruções detalhadas de uso.

**Sucesso com seu novo sistema de estoque! 🚀**

