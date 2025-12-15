# 🚀 Guia de Setup: Backend Python com Flask

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- pip ou pip3
- Git (opcional)

---

## 🔧 Passo 1: Instalar Dependências

### 1.1 No Kali Linux (ou qualquer Linux)

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e pip
sudo apt install python3 python3-pip -y

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Instalar dependências do sistema
sudo apt install libpq-dev -y
```

### 1.2 Instalar Dependências Python

```bash
# Navegar para o diretório do projeto
cd /home/ubuntu/ripple-backend-python

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar pacotes Python
pip install -r requirements.txt
```

---

## 🗄️ Passo 2: Configurar PostgreSQL

### 2.1 Iniciar PostgreSQL

```bash
# No Kali/Linux
sudo service postgresql start

# Ou
sudo systemctl start postgresql
```

### 2.2 Criar Banco de Dados

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Dentro do PostgreSQL, executar:
CREATE DATABASE ripple_db;
CREATE USER ripple_user WITH PASSWORD 'ripple_password_123';
ALTER ROLE ripple_user SET client_encoding TO 'utf8';
ALTER ROLE ripple_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ripple_user SET default_transaction_deferrable TO on;
ALTER ROLE ripple_user SET default_transaction_read_committed TO off;
GRANT ALL PRIVILEGES ON DATABASE ripple_db TO ripple_user;
\q  # Sair
```

### 2.3 Verificar Conexão

```bash
# Testar conexão
psql -U ripple_user -d ripple_db -h localhost
# Digite a senha: ripple_password_123

# Se conectar com sucesso, digite \q para sair
```

---

## ⚙️ Passo 3: Configurar Variáveis de Ambiente

### 3.1 Criar arquivo .env

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env
nano .env  # ou use seu editor favorito
```

### 3.2 Configurar Variáveis

```env
# Database
DATABASE_URL=postgresql://ripple_user:ripple_password_123@localhost:5432/ripple_db

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-desenvolvimento

# JWT
JWT_SECRET=sua-chave-jwt-desenvolvimento
JWT_REFRESH_SECRET=sua-chave-refresh-desenvolvimento
JWT_EXPIRES_IN=900
JWT_REFRESH_EXPIRES_IN=604800

# CORS
CORS_ORIGIN=http://localhost:3000,http://localhost:5173

# Server
PORT=5000
HOST=0.0.0.0
```

### 3.3 Gerar Chaves Seguras

```bash
# Gerar chave aleatória
python3 -c "import secrets; print(secrets.token_hex(32))"

# Copie o resultado e use para JWT_SECRET e JWT_REFRESH_SECRET
```

---

## 🚀 Passo 4: Iniciar o Backend

### 4.1 Ativar Ambiente Virtual

```bash
# Se ainda não ativou
cd /home/ubuntu/ripple-backend-python
source venv/bin/activate
```

### 4.2 Iniciar Servidor

```bash
# Opção 1: Usando Flask
python3 app.py

# Opção 2: Usando Flask CLI
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

# Opção 3: Com porta customizada
python3 app.py --port 5000
```

### 4.3 Verificar se está Rodando

Abra outro terminal e teste:

```bash
# Health check
curl http://localhost:5000/health

# Resposta esperada:
# {"status":"ok","timestamp":"2025-12-15T10:30:45.123456"}
```

---

## ✅ Passo 5: Testar Endpoints

### 5.1 Criar Conta (Signup)

```bash
curl -X POST http://localhost:5000/api/users/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste Python",
    "email": "teste@python.com",
    "password": "Senha123",
    "userId": "testePython"
  }'
```

**Resposta esperada:**
```json
{
  "data": {
    "id": "uuid-aqui",
    "userId": "testePython",
    "name": "Teste Python",
    "email": "teste@python.com",
    "avatar": null,
    "accessToken": "eyJ...",
    "refreshToken": "eyJ..."
  },
  "message": "Conta criada com sucesso"
}
```

### 5.2 Fazer Login

```bash
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "emailOrPhone": "teste@python.com",
    "password": "Senha123"
  }'
```

### 5.3 Obter Dados do Usuário

```bash
# Substitua TOKEN pelo accessToken recebido
curl -X GET http://localhost:5000/api/users/me \
  -H "Authorization: Bearer TOKEN"
```

---

## 🔄 Passo 6: Conectar Frontend

### 6.1 Configurar Variável de Ambiente

No seu frontend (`experience_creator`):

Edite `.env.local`:
```env
VITE_API_URL=http://localhost:5000
```

### 6.2 Testar Integração

1. Inicie o frontend:
   ```bash
   cd /home/ubuntu/experience_creator
   npm run dev
   ```

2. Vá para `http://localhost:5173`

3. Clique em "Signup"

4. Preencha o formulário

5. Se funcionar, a integração está completa! ✅

---

## 📊 Passo 7: Monitorar Backend

### 7.1 Ver Logs

Os logs aparecem no terminal onde você iniciou o servidor.

### 7.2 Acessar Banco de Dados

```bash
# Conectar ao PostgreSQL
psql -U ripple_user -d ripple_db -h localhost

# Ver tabelas
\dt

# Ver usuários
SELECT * FROM users;

# Sair
\q
```

---

## 🐛 Troubleshooting

### ❌ Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:**
1. Verifique se o ambiente virtual está ativado
2. Reinstale dependências: `pip install -r requirements.txt`

### ❌ Erro: "Connection refused" ao conectar no banco

**Solução:**
1. Verifique se PostgreSQL está rodando: `sudo systemctl status postgresql`
2. Verifique a `DATABASE_URL` em `.env`
3. Verifique se o banco foi criado: `psql -l`

### ❌ Erro: "FATAL: password authentication failed"

**Solução:**
1. Verifique a senha em `.env`
2. Resete a senha do usuário:
   ```bash
   sudo -u postgres psql
   ALTER USER ripple_user WITH PASSWORD 'nova_senha';
   \q
   ```

### ❌ Porta 5000 já está em uso

**Solução:**
1. Mude a porta em `.env`: `PORT=5001`
2. Ou mate o processo:
   ```bash
   lsof -i :5000
   kill -9 <PID>
   ```

### ❌ Erro: "CORS policy"

**Solução:**
1. Verifique `CORS_ORIGIN` em `.env`
2. Adicione o domínio do frontend
3. Exemplo: `CORS_ORIGIN=http://localhost:3000,http://localhost:5173`

---

## 📝 Estrutura do Projeto

```
ripple-backend-python/
├── app.py                 # Aplicação principal
├── config.py              # Configurações
├── models.py              # Modelos do banco
├── utils.py               # Utilitários (JWT, etc)
├── routes_users.py        # Rotas de usuários
├── routes_experiences.py  # Rotas de experiências
├── routes_videos.py       # Rotas de vídeos
├── routes_follows.py      # Rotas de follows
├── requirements.txt       # Dependências Python
├── .env.example           # Variáveis de exemplo
├── .env                   # Variáveis reais (não commitar)
├── venv/                  # Ambiente virtual
└── README.md              # Documentação
```

---

## 🔄 Workflow de Desenvolvimento

1. **Ativar ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

2. **Fazer mudanças** nos arquivos Python

3. **Servidor recarrega automaticamente** (FLASK_DEBUG=True)

4. **Testar endpoints** com curl ou Postman

5. **Commitar mudanças:**
   ```bash
   git add .
   git commit -m "Sua mensagem"
   ```

---

## 🎉 Parabéns!

Seu backend Python está rodando! 🚀

**URL do Backend:** `http://localhost:5000`

**Próximos Passos:**
1. ✅ Testar todos os endpoints
2. ✅ Conectar frontend
3. ✅ Fazer fluxo completo (signup → login → criar experiência)
4. ✅ Adicionar mais funcionalidades conforme necessário

---

**Status:** Pronto para desenvolvimento
**Última atualização:** 2025-12-15
