# 🎯 Guia Completo: Backend Ripple no Kali Linux + Integração Frontend

Este guia é 100% prático e passo a passo. Siga exatamente como está!

---

## 📋 Índice

1. [Preparar Máquina Kali](#-passo-1-preparar-máquina-kali)
2. [Instalar Dependências](#-passo-2-instalar-dependências)
3. [Configurar PostgreSQL](#-passo-3-configurar-postgresql)
4. [Copiar Código Backend](#-passo-4-copiar-código-backend)
5. [Configurar Backend](#-passo-5-configurar-backend)
6. [Iniciar Backend](#-passo-6-iniciar-backend)
7. [Testar Backend](#-passo-7-testar-backend)
8. [Integrar com Frontend](#-passo-8-integrar-com-frontend)
9. [Troubleshooting](#-passo-9-troubleshooting)

---

## 🔧 PASSO 1: Preparar Máquina Kali

### 1.1 Abrir Terminal

Pressione: `Ctrl + Alt + T`

### 1.2 Atualizar Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

Aguarde a conclusão (pode levar alguns minutos).

### 1.3 Criar Diretório do Projeto

```bash
mkdir -p ~/ripple-backend
cd ~/ripple-backend
pwd  # Copie o caminho que aparecer
```

**Exemplo de saída:**
```
/root/ripple-backend
```

---

## 📦 PASSO 2: Instalar Dependências

### 2.1 Instalar Python 3

```bash
sudo apt install python3 python3-pip python3-venv -y
```

Verifique:
```bash
python3 --version
pip3 --version
```

### 2.2 Instalar PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib libpq-dev -y
```

Verifique:
```bash
psql --version
```

### 2.3 Iniciar PostgreSQL

```bash
sudo service postgresql start
```

Verifique se está rodando:
```bash
sudo service postgresql status
```

Deve mostrar: `● postgresql is running`

---

## 🗄️ PASSO 3: Configurar PostgreSQL

### 3.1 Acessar PostgreSQL

```bash
sudo -u postgres psql
```

Você verá o prompt: `postgres=#`

### 3.2 Criar Banco de Dados

Cole cada linha uma por uma:

```sql
CREATE DATABASE ripple_db;
```

Pressione Enter. Resposta esperada: `CREATE DATABASE`

### 3.3 Criar Usuário

```sql
CREATE USER ripple_user WITH PASSWORD 'ripple_password_123';
```

Resposta esperada: `CREATE ROLE`

### 3.4 Dar Permissões

```sql
ALTER ROLE ripple_user SET client_encoding TO 'utf8';
ALTER ROLE ripple_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ripple_user SET default_transaction_deferrable TO on;
ALTER ROLE ripple_user SET default_transaction_read_committed TO off;
GRANT ALL PRIVILEGES ON DATABASE ripple_db TO ripple_user;
```

Cada linha deve retornar: `ALTER ROLE` ou `GRANT`

### 3.5 Sair do PostgreSQL

```sql
\q
```

Você voltará ao terminal normal.

### 3.6 Testar Conexão

```bash
psql -U ripple_user -d ripple_db -h localhost
```

Digite a senha: `ripple_password_123`

Se conectar com sucesso, digite:
```sql
\q
```

✅ **PostgreSQL está pronto!**

---

## 📂 PASSO 4: Copiar Código Backend

### 4.1 Opção A: Copiar de um Pen Drive ou Arquivo Compactado

Se você tem os arquivos em um pen drive ou arquivo `.zip`:

```bash
# Se for arquivo zip
cd ~/ripple-backend
unzip /caminho/do/arquivo.zip

# Se for pen drive
cp -r /media/seu-usuario/pen-drive/ripple-backend-python/* ~/ripple-backend/
```

### 4.2 Opção B: Criar Manualmente

Se não tem os arquivos, crie-os manualmente:

```bash
cd ~/ripple-backend

# Criar arquivos
touch app.py config.py models.py utils.py requirements.txt .env.example
touch routes_users.py routes_experiences.py routes_videos.py routes_follows.py
```

**Depois copie o conteúdo de cada arquivo** (vou fornecer abaixo)

### 4.3 Verificar Arquivos

```bash
ls -la ~/ripple-backend/
```

Deve mostrar:
```
app.py
config.py
models.py
utils.py
requirements.txt
.env.example
routes_users.py
routes_experiences.py
routes_videos.py
routes_follows.py
```

---

## ⚙️ PASSO 5: Configurar Backend

### 5.1 Criar Ambiente Virtual

```bash
cd ~/ripple-backend
python3 -m venv venv
```

### 5.2 Ativar Ambiente Virtual

```bash
source venv/bin/activate
```

Você verá `(venv)` no início da linha do terminal.

### 5.3 Instalar Dependências Python

```bash
pip install -r requirements.txt
```

Aguarde a instalação (pode levar 2-3 minutos).

### 5.4 Criar Arquivo .env

```bash
cp .env.example .env
```

### 5.5 Editar Arquivo .env

```bash
nano .env
```

Você verá um editor de texto. Modifique para:

```env
DATABASE_URL=postgresql://ripple_user:ripple_password_123@localhost:5432/ripple_db
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-12345
JWT_SECRET=jwt-secret-key-67890
JWT_REFRESH_SECRET=jwt-refresh-secret-key-abcde
CORS_ORIGIN=http://localhost:3000,http://localhost:5173,http://192.168.1.XXX:5173
PORT=5000
HOST=0.0.0.0
```

**IMPORTANTE:** Substitua `192.168.1.XXX` pelo IP da sua máquina Kali!

Para encontrar seu IP:
```bash
hostname -I
```

Exemplo de saída:
```
192.168.1.100
```

Use esse IP no CORS_ORIGIN.

### 5.6 Salvar Arquivo .env

Pressione: `Ctrl + X` → `Y` → `Enter`

✅ **Backend configurado!**

---

## 🚀 PASSO 6: Iniciar Backend

### 6.1 Verificar Ambiente Virtual

```bash
cd ~/ripple-backend
source venv/bin/activate  # Se não estiver ativado
```

Deve mostrar `(venv)` no terminal.

### 6.2 Iniciar Servidor

```bash
python3 app.py
```

Você deve ver:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

✅ **Backend está rodando!**

---

## ✅ PASSO 7: Testar Backend

### 7.1 Abrir Outro Terminal

Pressione: `Ctrl + Alt + T` (novo terminal)

### 7.2 Testar Health Check

```bash
curl http://localhost:5000/health
```

Resposta esperada:
```json
{"status":"ok","timestamp":"2025-12-15T10:30:45.123456"}
```

### 7.3 Testar Signup

```bash
curl -X POST http://localhost:5000/api/users/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste Kali",
    "email": "teste@kali.com",
    "password": "Senha123",
    "userId": "testeKali"
  }'
```

Resposta esperada:
```json
{
  "data": {
    "id": "uuid-aqui",
    "userId": "testeKali",
    "name": "Teste Kali",
    "email": "teste@kali.com",
    "avatar": null,
    "accessToken": "eyJ...",
    "refreshToken": "eyJ..."
  },
  "message": "Conta criada com sucesso"
}
```

✅ **Backend está funcionando!**

---

## 🔗 PASSO 8: Integrar com Frontend

### 8.1 Encontrar IP da Máquina Kali

```bash
hostname -I
```

Copie o IP (exemplo: `192.168.1.100`)

### 8.2 Configurar Frontend

Na máquina onde o frontend está rodando (pode ser a mesma ou outra):

**Se estiver na mesma máquina Kali:**

Edite o arquivo `.env.local` do frontend:

```bash
cd /caminho/do/frontend
nano .env.local
```

Adicione:
```env
VITE_API_URL=http://localhost:5000
```

**Se estiver em outra máquina:**

Edite o arquivo `.env.local` do frontend:

```bash
cd /caminho/do/frontend
nano .env.local
```

Adicione:
```env
VITE_API_URL=http://192.168.1.100:5000
```

(Substitua `192.168.1.100` pelo IP da sua máquina Kali)

### 8.3 Reiniciar Frontend

```bash
# Parar o servidor (Ctrl + C)
# Depois reiniciar
npm run dev
```

### 8.4 Testar Integração

1. Abra o navegador
2. Vá para `http://localhost:5173` (ou seu IP)
3. Clique em "Signup"
4. Preencha o formulário
5. Se funcionar, a integração está completa! ✅

---

## 🐛 PASSO 9: Troubleshooting

### ❌ Erro: "Connection refused" ao iniciar backend

**Solução:**
```bash
# Verifique se PostgreSQL está rodando
sudo service postgresql status

# Se não estiver, inicie
sudo service postgresql start
```

### ❌ Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:**
```bash
# Verifique se ambiente virtual está ativado
source venv/bin/activate

# Reinstale dependências
pip install -r requirements.txt
```

### ❌ Erro: "FATAL: password authentication failed"

**Solução:**
```bash
# Resete a senha do PostgreSQL
sudo -u postgres psql
ALTER USER ripple_user WITH PASSWORD 'ripple_password_123';
\q
```

### ❌ Erro: "Port 5000 already in use"

**Solução:**
```bash
# Mude a porta em .env
nano .env
# Altere: PORT=5001

# Ou mate o processo
sudo lsof -i :5000
sudo kill -9 <PID>
```

### ❌ Erro: "CORS policy" no frontend

**Solução:**
```bash
# Edite .env do backend
nano .env

# Verifique CORS_ORIGIN
# Deve incluir o domínio do frontend
CORS_ORIGIN=http://localhost:3000,http://localhost:5173,http://192.168.1.100:5173
```

### ❌ Frontend não consegue conectar ao backend

**Solução:**
```bash
# 1. Verifique o IP correto
hostname -I

# 2. Edite .env.local do frontend
VITE_API_URL=http://192.168.1.XXX:5000

# 3. Reinicie o frontend
npm run dev

# 4. Teste no navegador
curl http://192.168.1.XXX:5000/health
```

---

## 📊 Verificar Dados no Banco

### Conectar ao PostgreSQL

```bash
psql -U ripple_user -d ripple_db -h localhost
```

Digite a senha: `ripple_password_123`

### Ver Usuários Criados

```sql
SELECT * FROM users;
```

### Ver Experiências

```sql
SELECT * FROM experiences;
```

### Sair

```sql
\q
```

---

## 🔄 Manter Backend Rodando

### Opção 1: Terminal Dedicado

Deixe um terminal aberto apenas para o backend:

```bash
cd ~/ripple-backend
source venv/bin/activate
python3 app.py
```

### Opção 2: Usar Screen (Avançado)

```bash
# Criar nova sessão screen
screen -S ripple-backend

# Dentro da sessão
cd ~/ripple-backend
source venv/bin/activate
python3 app.py

# Para sair: Ctrl + A, depois D
# Para reconectar: screen -r ripple-backend
```

### Opção 3: Usar Systemd (Avançado)

Criar arquivo `/etc/systemd/system/ripple-backend.service`:

```ini
[Unit]
Description=Ripple Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ripple-backend
ExecStart=/root/ripple-backend/venv/bin/python3 /root/ripple-backend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Depois:
```bash
sudo systemctl enable ripple-backend
sudo systemctl start ripple-backend
sudo systemctl status ripple-backend
```

---

## 📝 Checklist Final

- [ ] Python 3 instalado
- [ ] PostgreSQL instalado e rodando
- [ ] Banco de dados criado
- [ ] Usuário PostgreSQL criado
- [ ] Código backend copiado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Arquivo .env configurado
- [ ] Backend iniciado com sucesso
- [ ] Health check funcionando
- [ ] Signup testado com sucesso
- [ ] Frontend configurado com VITE_API_URL
- [ ] Frontend consegue fazer requisições ao backend
- [ ] Fluxo completo testado (signup → login → criar experiência)

---

## 🎉 Parabéns!

Você tem um backend Python rodando na sua máquina Kali! 🚀

### Resumo do que você fez:

✅ Instalou Python e PostgreSQL  
✅ Configurou banco de dados  
✅ Copiou código backend  
✅ Criou ambiente virtual  
✅ Instalou dependências  
✅ Configurou variáveis de ambiente  
✅ Iniciou servidor  
✅ Testou endpoints  
✅ Integrou com frontend  

### Próximos Passos:

1. Manter backend rodando enquanto desenvolve
2. Testar todos os endpoints
3. Adicionar mais funcionalidades conforme necessário
4. Quando estiver pronto, fazer deploy em produção

---

**Status:** ✅ Pronto para usar
**Última atualização:** 2025-12-15
**Versão:** 1.0
