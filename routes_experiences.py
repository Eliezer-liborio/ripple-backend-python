from flask import Blueprint, request
from models import db, Experience
from utils import token_required, error_response, success_response

experiences_bp = Blueprint('experiences', __name__, url_prefix='/api/experiences')

@experiences_bp.route('', methods=['GET'])
def get_experiences():
    """Listar todas as experiências"""
    try:
        category = request.args.get('category')
        is_live = request.args.get('isLive', 'false').lower() == 'true'
        skip = int(request.args.get('skip', 0))
        take = int(request.args.get('take', 20))
        
        query = Experience.query
        
        if category:
            query = query.filter_by(category=category)
        if is_live:
            query = query.filter_by(is_live=True)
        
        total = query.count()
        experiences = query.order_by(Experience.created_at.desc()).offset(skip).limit(take).all()
        
        return success_response({
            'data': [exp.to_dict() for exp in experiences],
            'total': total,
            'skip': skip,
            'take': take
        })
    
    except Exception as e:
        return error_response(f'Erro ao listar experiências: {str(e)}', 500)

@experiences_bp.route('/<experience_id>', methods=['GET'])
def get_experience(experience_id):
    """Obter detalhes de uma experiência"""
    try:
        experience = Experience.query.get(experience_id)
        
        if not experience:
            return error_response('Experiência não encontrada', 404)
        
        data = experience.to_dict()
        data['videos'] = [v.to_dict() for v in experience.videos]
        
        return success_response(data)
    
    except Exception as e:
        return error_response(f'Erro ao obter experiência: {str(e)}', 500)

@experiences_bp.route('/creator/<creator_id>', methods=['GET'])
def get_experiences_by_creator(creator_id):
    """Listar experiências de um criador"""
    try:
        skip = int(request.args.get('skip', 0))
        take = int(request.args.get('take', 20))
        
        query = Experience.query.filter_by(creator_id=creator_id)
        total = query.count()
        experiences = query.order_by(Experience.created_at.desc()).offset(skip).limit(take).all()
        
        return success_response({
            'data': [exp.to_dict() for exp in experiences],
            'total': total,
            'skip': skip,
            'take': take
        })
    
    except Exception as e:
        return error_response(f'Erro ao listar experiências: {str(e)}', 500)

@experiences_bp.route('', methods=['POST'])
@token_required
def create_experience():
    """Criar nova experiência"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('title'):
            return error_response('Título é obrigatório', 400)
        if not data.get('category'):
            return error_response('Categoria é obrigatória', 400)
        if not data.get('duration'):
            return error_response('Duração é obrigatória', 400)
        
        # Criar experiência
        experience = Experience(
            title=data['title'],
            description=data.get('description'),
            category=data['category'],
            tags=data.get('tags', []),
            duration=data['duration'],
            is_live=data.get('is_live', False),
            creator_id=request.user_db_id,
            creator_name=data.get('creator_name', '')
        )
        
        db.session.add(experience)
        db.session.commit()
        
        return success_response(experience.to_dict(), 'Experiência criada com sucesso', 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao criar experiência: {str(e)}', 500)

@experiences_bp.route('/<experience_id>', methods=['PATCH'])
@token_required
def update_experience(experience_id):
    """Atualizar experiência"""
    try:
        experience = Experience.query.get(experience_id)
        
        if not experience:
            return error_response('Experiência não encontrada', 404)
        
        if experience.creator_id != request.user_db_id:
            return error_response('Você não tem permissão para atualizar esta experiência', 403)
        
        data = request.get_json()
        
        # Atualizar campos
        if 'title' in data:
            experience.title = data['title']
        if 'description' in data:
            experience.description = data['description']
        if 'category' in data:
            experience.category = data['category']
        if 'tags' in data:
            experience.tags = data['tags']
        if 'duration' in data:
            experience.duration = data['duration']
        if 'is_live' in data:
            experience.is_live = data['is_live']
        if 'participants' in data:
            experience.participants = data['participants']
        if 'engagement' in data:
            experience.engagement = data['engagement']
        
        db.session.commit()
        
        return success_response(experience.to_dict(), 'Experiência atualizada com sucesso')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao atualizar experiência: {str(e)}', 500)

@experiences_bp.route('/<experience_id>', methods=['DELETE'])
@token_required
def delete_experience(experience_id):
    """Deletar experiência"""
    try:
        experience = Experience.query.get(experience_id)
        
        if not experience:
            return error_response('Experiência não encontrada', 404)
        
        if experience.creator_id != request.user_db_id:
            return error_response('Você não tem permissão para deletar esta experiência', 403)
        
        db.session.delete(experience)
        db.session.commit()
        
        return success_response(None, 'Experiência deletada com sucesso')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao deletar experiência: {str(e)}', 500)
