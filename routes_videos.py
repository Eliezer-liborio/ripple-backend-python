from flask import Blueprint, request
from models import db, Video
from utils import token_required, error_response, success_response

videos_bp = Blueprint('videos', __name__, url_prefix='/api/videos')

@videos_bp.route('/<video_id>', methods=['GET'])
def get_video(video_id):
    """Obter detalhes de um vídeo"""
    try:
        video = Video.query.get(video_id)
        
        if not video:
            return error_response('Vídeo não encontrado', 404)
        
        return success_response(video.to_dict())
    
    except Exception as e:
        return error_response(f'Erro ao obter vídeo: {str(e)}', 500)

@videos_bp.route('/creator/<creator_id>', methods=['GET'])
def get_videos_by_creator(creator_id):
    """Listar vídeos de um criador"""
    try:
        skip = int(request.args.get('skip', 0))
        take = int(request.args.get('take', 20))
        
        query = Video.query.filter_by(creator_id=creator_id)
        total = query.count()
        videos = query.order_by(Video.created_at.desc()).offset(skip).limit(take).all()
        
        return success_response({
            'data': [v.to_dict() for v in videos],
            'total': total,
            'skip': skip,
            'take': take
        })
    
    except Exception as e:
        return error_response(f'Erro ao listar vídeos: {str(e)}', 500)

@videos_bp.route('', methods=['POST'])
@token_required
def create_video():
    """Criar novo vídeo"""
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('title'):
            return error_response('Título é obrigatório', 400)
        if not data.get('url'):
            return error_response('URL é obrigatória', 400)
        if not data.get('duration'):
            return error_response('Duração é obrigatória', 400)
        
        # Criar vídeo
        video = Video(
            title=data['title'],
            description=data.get('description'),
            url=data['url'],
            thumbnail=data.get('thumbnail'),
            duration=data['duration'],
            creator_id=request.user_db_id,
            creator_name=data.get('creator_name', ''),
            experience_id=data.get('experience_id')
        )
        
        db.session.add(video)
        db.session.commit()
        
        return success_response(video.to_dict(), 'Vídeo criado com sucesso', 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao criar vídeo: {str(e)}', 500)

@videos_bp.route('/<video_id>', methods=['PATCH'])
@token_required
def update_video(video_id):
    """Atualizar vídeo"""
    try:
        video = Video.query.get(video_id)
        
        if not video:
            return error_response('Vídeo não encontrado', 404)
        
        if video.creator_id != request.user_db_id:
            return error_response('Você não tem permissão para atualizar este vídeo', 403)
        
        data = request.get_json()
        
        # Atualizar campos
        if 'title' in data:
            video.title = data['title']
        if 'description' in data:
            video.description = data['description']
        if 'thumbnail' in data:
            video.thumbnail = data['thumbnail']
        if 'duration' in data:
            video.duration = data['duration']
        
        db.session.commit()
        
        return success_response(video.to_dict(), 'Vídeo atualizado com sucesso')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao atualizar vídeo: {str(e)}', 500)

@videos_bp.route('/<video_id>/views', methods=['PATCH'])
def update_video_views(video_id):
    """Incrementar visualizações"""
    try:
        video = Video.query.get(video_id)
        
        if not video:
            return error_response('Vídeo não encontrado', 404)
        
        video.views += 1
        db.session.commit()
        
        return success_response(video.to_dict(), 'Visualizações atualizadas')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao atualizar visualizações: {str(e)}', 500)

@videos_bp.route('/<video_id>', methods=['DELETE'])
@token_required
def delete_video(video_id):
    """Deletar vídeo"""
    try:
        video = Video.query.get(video_id)
        
        if not video:
            return error_response('Vídeo não encontrado', 404)
        
        if video.creator_id != request.user_db_id:
            return error_response('Você não tem permissão para deletar este vídeo', 403)
        
        db.session.delete(video)
        db.session.commit()
        
        return success_response(None, 'Vídeo deletado com sucesso')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Erro ao deletar vídeo: {str(e)}', 500)
