from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db
from routes_users import users_bp
from routes_experiences import experiences_bp
from routes_videos import videos_bp
from routes_follows import follows_bp
import os

def create_app(config_name='development'):
    """Factory para criar a aplicação Flask"""
    
    # Criar aplicação
    app = Flask(__name__)
    
    # Carregar configurações
    app.config.from_object(config[config_name])
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Configurar CORS
    CORS(app, origins=app.config['CORS_ORIGIN'])
    
    # Registrar blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(experiences_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(follows_bp)
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'ok',
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        }), 200
    
    # 404 handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Rota não encontrada'}), 404
    
    # 500 handler
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    # Obter ambiente
    env = os.getenv('FLASK_ENV', 'development')
    
    # Criar aplicação
    app = create_app(env)
    
    # Iniciar servidor
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
