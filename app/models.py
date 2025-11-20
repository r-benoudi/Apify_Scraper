from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    director = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'director': self.director,
            'rating': self.rating
        }

class Manga(db.Model):
    __tablename__ = 'mangas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    author = db.Column(db.String(100), nullable=True)
    volumes = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'author': self.author,
            'volumes': self.volumes,
            'status': self.status
        }

class Anime(db.Model):
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    studio = db.Column(db.String(100), nullable=True)
    episodes = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'studio': self.studio,
            'episodes': self.episodes,
            'status': self.status
        }
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # "user" or "admin"
    role = db.Column(db.String(10), default="user")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

    
