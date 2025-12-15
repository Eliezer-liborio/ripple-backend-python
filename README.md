# 🎵 Ripple Backend - Python + Flask

Backend da plataforma Ripple de experiências ao vivo, desenvolvido em Python com Flask e PostgreSQL.

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8+
- PostgreSQL 12+
- pip3

### Instalação

```bash
# 1. Clonar/Navegar para o diretório
cd /home/ubuntu/ripple-backend-python

# 2. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar banco de dados
cp .env.example .env
# Edite .env com suas credenciais

# 5. Iniciar servidor
python3 app.py
```

Servidor rodará em `http://localhost:5000`

---

## 📚 Documentação Completa

Veja [SETUP_GUIDE.md](./SETUP_GUIDE.md) para instruções detalhadas de setup.

---

## 🔌 Endpoints da API

### Autenticação
- `POST /api/users/signup` - Criar conta
- `POST /api/users/login` - Fazer login
- `POST /api/users/refresh` - Renovar token
- `POST /api/users/logout` - Fazer logout

### Usuários
- `GET /api/users/me` - Dados do usuário autenticado
- `GET /api/users/<user_id>` - Dados de um usuário
- `PATCH /api/users/me` - Atualizar dados

### Experiências
- `GET /api/experiences` - Listar todas
- `GET /api/experiences/<id>` - Detalhes
- `GET /api/experiences/creator/<creator_id>` - Por criador
- `POST /api/experiences` - Criar (autenticado)
- `PATCH /api/experiences/<id>` - Atualizar (autenticado)
- `DELETE /api/experiences/<id>` - Deletar (autenticado)

### Vídeos
- `GET /api/videos/<id>` - Detalhes
- `GET /api/videos/creator/<creator_id>` - Por criador
- `POST /api/videos` - Criar (autenticado)
- `PATCH /api/videos/<id>` - Atualizar (autenticado)
- `PATCH /api/videos/<id>/views` - Incrementar views
- `DELETE /api/videos/<id>` - Deletar (autenticado)

### Follows
- `GET /api/follows/<user_id>/followers` - Seguidores
- `GET /api/follows/<user_id>/following` - Seguindo
- `GET /api/follows/<follower_id>/is-following/<following_id>` - Verificar
- `POST /api/follows` - Seguir (autenticado)
- `DELETE /api/follows/<follower_id>/<following_id>` - Deixar de seguir

---

## 🗄️ Banco de Dados

### Modelos
- **User** - Usuários da plataforma
- **Experience** - Experiências ao vivo
- **Video** - Vídeos
- **Follow** - Relacionamentos de seguidores

### Conectar ao PostgreSQL

```bash
psql -U ripple_user -d ripple_db -h localhost
```

---

## 🔐 Segurança

- Senhas hasheadas com bcrypt
- JWT com access tokens (15 min)
- Refresh tokens (7 dias)
- CORS configurável
- Validação de entrada

---

## 📦 Dependências

- **Flask** - Framework web
- **Flask-CORS** - CORS handling
- **Flask-SQLAlchemy** - ORM
- **PyJWT** - JWT tokens
- **bcrypt** - Password hashing
- **python-dotenv** - Variáveis de ambiente
- **psycopg2** - PostgreSQL driver

---

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
ripple-backend-python/
├── app.py              # Aplicação principal
├── config.py           # Configurações
├── models.py           # Modelos ORM
├── utils.py            # Utilitários
├── routes_*.py         # Rotas da API
├── requirements.txt    # Dependências
├── .env.example        # Variáveis de exemplo
└── SETUP_GUIDE.md      # Guia de setup
```

### Adicionar Nova Rota

1. Criar função em `routes_*.py`
2. Usar decorator `@token_required` se protegida
3. Retornar com `success_response()` ou `error_response()`
4. Registrar blueprint em `app.py`

### Exemplo

```python
@users_bp.route('/novo', methods=['POST'])
@token_required
def nova_rota():
    data = request.get_json()
    # Sua lógica aqui
    return success_response(data, 'Sucesso', 201)
```

---

## 🚢 Deploy

### Para Produção

1. Editar `.env` com variáveis de produção
2. Usar servidor WSGI (gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
   ```
3. Configurar reverse proxy (nginx)
4. Usar HTTPS

---

## 🐛 Troubleshooting

Veja [SETUP_GUIDE.md - Troubleshooting](./SETUP_GUIDE.md#-troubleshooting)

---

## 📝 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | String de conexão PostgreSQL | - |
| `FLASK_ENV` | Ambiente (development/production) | development |
| `FLASK_DEBUG` | Debug mode | False |
| `SECRET_KEY` | Chave secreta Flask | dev-secret |
| `JWT_SECRET` | Chave JWT | jwt-secret |
| `JWT_REFRESH_SECRET` | Chave refresh token | jwt-refresh |
| `CORS_ORIGIN` | Origins permitidas | localhost |
| `PORT` | Porta do servidor | 5000 |
| `HOST` | Host do servidor | 0.0.0.0 |

---

## 📞 Suporte

Para problemas, consulte:
1. [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. Logs do servidor
3. Documentação do PostgreSQL

---

## 📄 Licença

MIT

---

**Status:** ✅ Pronto para desenvolvimento
**Última atualização:** 2025-12-15
