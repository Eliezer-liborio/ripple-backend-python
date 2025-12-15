from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import uuid

db = SQLAlchemy()

class User(db.Model):
    """Modelo de usuário"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    interests = db.Column(db.JSON, nullable=True, default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    created_experiences = db.relationship('Experience', backref='creator', lazy=True, foreign_keys='Experience.creator_id')
    created_videos = db.relationship('Video', backref='creator', lazy=True, foreign_keys='Video.creator_id')
    followers = db.relationship('Follow', backref='follower_user', lazy=True, foreign_keys='Follow.follower_id')
    following = db.relationship('Follow', backref='following_user', lazy=True, foreign_keys='Follow.following_id')
    
    def set_password(self, password):
        """Hash da senha"""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verificar senha"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'bio': self.bio,
            'interests': self.interests,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Experience(db.Model):
    """Modelo de experiência"""
    __tablename__ = 'experiences'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.JSON, nullable=True, default=[])
    duration = db.Column(db.Integer, nullable=False)
    is_live = db.Column(db.Boolean, default=False)
    participants = db.Column(db.Integer, default=0)
    engagement = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    creator_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    videos = db.relationship('Video', backref='experience', lazy=True)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'tags': self.tags,
            'duration': self.duration,
            'is_live': self.is_live,
            'participants': self.participants,
            'engagement': self.engagement,
            'creator_id': self.creator_id,
            'creator_name': self.creator_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Video(db.Model):
    """Modelo de vídeo"""
    __tablename__ = 'videos'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(500), nullable=False)
    thumbnail = db.Column(db.String(500), nullable=True)
    duration = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    creator_name = db.Column(db.String(100), nullable=False)
    experience_id = db.Column(db.String(36), db.ForeignKey('experiences.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'thumbnail': self.thumbnail,
            'duration': self.duration,
            'views': self.views,
            'creator_id': self.creator_id,
            'creator_name': self.creator_name,
            'experience_id': self.experience_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Follow(db.Model):
    """Modelo de relacionamento de seguidores"""
    __tablename__ = 'follows'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    follower_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('follower_id', 'following_id', name='unique_follow'),)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'following_id': self.following_id,
            'created_at': self.created_at.isoformat()
        }
