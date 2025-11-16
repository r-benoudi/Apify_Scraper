from flask import Blueprint, render_template
from app.models import Movie, Manga, Anime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    movies = Movie.query.all()
    mangas = Manga.query.all()
    anime = Anime.query.all()
    
    items1 = [m.to_dict() for m in movies]
    items2 = [m.to_dict() for m in mangas]
    items3 = [a.to_dict() for a in anime]
    
    return render_template('index.html', 
                         items1=items1, 
                         items2=items2, 
                         items3=items3)