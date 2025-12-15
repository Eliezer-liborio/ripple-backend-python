import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def generate_tokens(user_id, user_db_id):
    """Gerar access token e refresh token"""
    now = datetime.utcnow()
    
    # Access token
    access_payload = {
        'user_id': user_id,
        'id': user_db_id,
        'iat': now,
        'exp': now + timedelta(seconds=current_app.config['JWT_EXPIRES_IN'])
    }
    access_token = jwt.encode(
        access_payload,
        current_app.config['JWT_SECRET'],
        algorithm='HS256'
    )
    
    # Refresh token
    refresh_payload = {
        'user_id': user_id,
        'id': user_db_id,
        'iat': now,
        'exp': now + timedelta(seconds=current_app.config['JWT_REFRESH_EXPIRES_IN'])
    }
    refresh_token = jwt.encode(
        refresh_payload,
        current_app.config['JWT_REFRESH_SECRET'],
        algorithm='HS256'
    )
    
    return access_token, refresh_token

def verify_token(token, secret_key):
    """Verificar token JWT"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator para proteger rotas com token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Procurar token no header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Token inválido'}), 401
        
        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401
        
        # Verificar token
        payload = verify_token(token, current_app.config['JWT_SECRET'])
        if not payload:
            return jsonify({'error': 'Token inválido ou expirado'}), 401
        
        # Adicionar payload ao request
        request.user_id = payload.get('user_id')
        request.user_db_id = payload.get('id')
        
        return f(*args, **kwargs)
    
    return decorated

def error_response(message, status_code=400):
    """Retornar erro em formato JSON"""
    return jsonify({'error': message}), status_code

def success_response(data=None, message=None, status_code=200):
    """Retornar sucesso em formato JSON"""
    response = {}
    if message:
        response['message'] = message
    if data:
        response['data'] = data
    return jsonify(response), status_code
