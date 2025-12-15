from flask import Blueprint, request, jsonify
from models import db, User
from utils import generate_tokens, verify_token, token_required, error_response, success_response
from flask import current_app

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/signup', methods=['POST'])
def signup():
    """Criar nova conta"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('name'):
            return error_response('Nome é obrigatório', 400)
        if not data.get('password'):
            return error_response('Senha é obrigatória', 400)
        if not data.get('userId'):
            return error_response('userId é obrigatório', 400)
        
        # Verificar se usuário já existe
        existing_user = User.query.filter(
            (User.user_id == data['userId']) |
            (User.email == data.get('email')) |
            (User.phone == data.get('phone'))
        ).first()
        
        if existing_user:
            return error_response('Usuário já existe', 409)
        
        # Criar usuário
        user = User(
            user_id=data['userId'],
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Gerar tokens
        access_token, refresh_token = generate_tokens(user.user_id, user.id)
        
        return success_response({
            'id': user.id,
            'userId': user.user_id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'avatar': user.avatar,
            'accessToken': access_token,
            'refreshToken': refresh_token
        }, 'Conta criada com sucesso', 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao criar conta: {str(e)}', 500)

@users_bp.route('/login', methods=['POST'])
def login():
    """Fazer login"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('emailOrPhone'):
            return error_response('Email/telefone é obrigatório', 400)
        if not data.get('password'):
            return error_response('Senha é obrigatória', 400)
        
        # Buscar usuário
        user = User.query.filter(
            (User.email == data['emailOrPhone']) |
            (User.phone == data['emailOrPhone']) |
            (User.user_id == data['emailOrPhone'])
        ).first()
        
        if not user or not user.check_password(data['password']):
            return error_response('Email/telefone ou senha incorretos', 401)
        
        # Gerar tokens
        access_token, refresh_token = generate_tokens(user.user_id, user.id)
        
        return success_response({
            'id': user.id,
            'userId': user.user_id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'avatar': user.avatar,
            'accessToken': access_token,
            'refreshToken': refresh_token
        }, 'Login realizado com sucesso')
    
    except Exception as e:
        return error_response(f'Erro ao fazer login: {str(e)}', 500)

@users_bp.route('/refresh', methods=['POST'])
def refresh():
    """Renovar access token"""
    try:
        data = request.get_json()
        
        if not data.get('refreshToken'):
            return error_response('Refresh token é obrigatório', 400)
        
        # Verificar refresh token
        payload = verify_token(data['refreshToken'], current_app.config['JWT_REFRESH_SECRET'])
        
        if not payload:
            return error_response('Refresh token inválido ou expirado', 401)
        
        # Buscar usuário
        user = User.query.get(payload['id'])
        
        if not user:
            return error_response('Usuário não encontrado', 404)
        
        # Gerar novo access token
        access_token, _ = generate_tokens(user.user_id, user.id)
        
        return success_response({'accessToken': access_token}, 'Token renovado com sucesso')
    
    except Exception as e:
        return error_response(f'Erro ao renovar token: {str(e)}', 500)

@users_bp.route('/logout', methods=['POST'])
def logout():
    """Fazer logout"""
    # Em uma aplicação real, você invalidaria o token aqui
    return success_response(None, 'Logout realizado com sucesso')

@users_bp.route('/me', methods=['GET'])
@token_required
def get_me():
    """Obter dados do usuário autenticado"""
    try:
        user = User.query.get(request.user_db_id)
        
        if not user:
            return error_response('Usuário não encontrado', 404)
        
        return success_response(user.to_dict())
    
    except Exception as e:
        return error_response(f'Erro ao obter dados: {str(e)}', 500)

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Obter dados de um usuário específico"""
    try:
        user = User.query.filter(
            (User.user_id == user_id) |
            (User.id == user_id)
        ).first()
        
        if not user:
            return error_response('Usuário não encontrado', 404)
        
        data = user.to_dict()
        data['followers_count'] = len(user.followers)
        data['following_count'] = len(user.following)
        data['experiences_count'] = len(user.created_experiences)
        
        return success_response(data)
    
    except Exception as e:
        return error_response(f'Erro ao obter usuário: {str(e)}', 500)

@users_bp.route('/me', methods=['PATCH'])
@token_required
def update_me():
    """Atualizar dados do usuário autenticado"""
    try:
        user = User.query.get(request.user_db_id)
        
        if not user:
            return error_response('Usuário não encontrado', 404)
        
        data = request.get_json()
        
        # Atualizar campos
        if 'name' in data:
            user.name = data['name']
        if 'bio' in data:
            user.bio = data['bio']
        if 'avatar' in data:
            user.avatar = data['avatar']
        if 'interests' in data:
            user.interests = data['interests']
        
        db.session.commit()
        
        return success_response(user.to_dict(), 'Dados atualizados com sucesso')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao atualizar dados: {str(e)}', 500)
