from app import db

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