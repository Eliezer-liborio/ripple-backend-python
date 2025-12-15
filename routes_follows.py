from flask import Blueprint, request
from models import db, Follow, User
from utils import token_required, error_response, success_response

follows_bp = Blueprint('follows', __name__, url_prefix='/api/follows')

@follows_bp.route('', methods=['POST'])
@token_required
def follow_user():
    """Seguir um usuário"""
    try:
        data = request.get_json()
        
        follower_id = data.get('followerId')
        following_id = data.get('followingId')
        
        if not follower_id or not following_id:
            return error_response('followerId e followingId são obrigatórios', 400)
        
        # Verificar se está tentando seguir a si mesmo
        if follower_id == following_id:
            return error_response('Você não pode seguir a si mesmo', 400)
        
        # Verificar se o usuário existe
        following_user = User.query.get(following_id)
        if not following_user:
            return error_response('Usuário não encontrado', 404)
        
        # Verificar se já está seguindo
        existing_follow = Follow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()
        
        if existing_follow:
            return error_response('Você já está seguindo este usuário', 409)
        
        # Criar follow
        follow = Follow(
            follower_id=follower_id,
            following_id=following_id
        )
        
        db.session.add(follow)
        db.session.commit()
        
        return success_response(follow.to_dict(), 'Usuário seguido com sucesso', 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao seguir usuário: {str(e)}', 500)

@follows_bp.route('/<follower_id>/<following_id>', methods=['DELETE'])
@token_required
def unfollow_user(follower_id, following_id):
    """Deixar de seguir um usuário"""
    try:
        # Verificar se está tentando deixar de seguir a si mesmo
        if follower_id == following_id:
            return error_response('Você não pode deixar de seguir a si mesmo', 400)
        
        follow = Follow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()
        
        if not follow:
            return error_response('Você não está seguindo este usuário', 404)
        
        db.session.delete(follow)
        db.session.commit()
        
        return success_response(None, 'Usuário deixado de seguir com sucesso')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao deixar de seguir: {str(e)}', 500)

@follows_bp.route('/<follower_id>/is-following/<following_id>', methods=['GET'])
def is_following(follower_id, following_id):
    """Verificar se está seguindo um usuário"""
    try:
        follow = Follow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()
        
        return success_response({'is_following': follow is not None})
    
    except Exception as e:
        return error_response(f'Erro ao verificar follow: {str(e)}', 500)

@follows_bp.route('/<user_id>/followers', methods=['GET'])
def get_followers(user_id):
    """Listar seguidores de um usuário"""
    try:
        # Verificar se o usuário existe
        user = User.query.get(user_id)
        if not user:
            return error_response('Usuário não encontrado', 404)
        
        skip = int(request.args.get('skip', 0))
        take = int(request.args.get('take', 20))
        
        query = Follow.query.filter_by(following_id=user_id)
        total = query.count()
        follows = query.order_by(Follow.created_at.desc()).offset(skip).limit(take).all()
        
        # Obter dados dos seguidores
        followers_data = []
        for follow in follows:
            follower = User.query.get(follow.follower_id)
            if follower:
                followers_data.append({
                    'id': follower.id,
                    'user_id': follower.user_id,
                    'name': follower.name,
                    'avatar': follower.avatar
                })
        
        return success_response({
            'data': followers_data,
            'total': total,
            'skip': skip,
            'take': take
        })
    
    except Exception as e:
        return error_response(f'Erro ao listar seguidores: {str(e)}', 500)

@follows_bp.route('/<user_id>/following', methods=['GET'])
def get_following(user_id):
    """Listar usuários que um usuário está seguindo"""
    try:
        # Verificar se o usuário existe
        user = User.query.get(user_id)
        if not user:
            return error_response('Usuário não encontrado', 404)
        
        skip = int(request.args.get('skip', 0))
        take = int(request.args.get('take', 20))
        
        query = Follow.query.filter_by(follower_id=user_id)
        total = query.count()
        follows = query.order_by(Follow.created_at.desc()).offset(skip).limit(take).all()
        
        # Obter dados dos usuários seguidos
        following_data = []
        for follow in follows:
            following_user = User.query.get(follow.following_id)
            if following_user:
                following_data.append({
                    'id': following_user.id,
                    'user_id': following_user.user_id,
                    'name': following_user.name,
                    'avatar': following_user.avatar
                })
        
        return success_response({
            'data': following_data,
            'total': total,
            'skip': skip,
            'take': take
        })
    
    except Exception as e:
        return error_response(f'Erro ao listar seguindo: {str(e)}', 500)
