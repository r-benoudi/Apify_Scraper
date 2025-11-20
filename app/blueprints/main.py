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

@main_bp.route('/login')
def login():

    return render_template('login.html')

@main_bp.route('/register')
def register():

    return render_template('register.html')

@main_bp.route('/home')
def index2():
    """Page d'accueil avec tous les mangas"""
    # Récupérer tous les mangas depuis la base de données
    mangas = Manga.query.order_by(Manga.id.desc()).limit(12).all()
    
    # Préparer les données pour le template
    manga_list = []
    for manga in mangas:
        manga_list.append({
            'id': manga.id,
            'title': manga.title,
            'rating': getattr(manga, 'rating', '4.2'),
            'status': getattr(manga, 'status', 'OnGoing'),
            'chapters': 50,  # Remplacez par le vrai nombre de chapitres
            'image': f'https://via.placeholder.com/200x280/{generate_color()}/ffffff?text={manga.title[:20]}'
        })
    
    return render_template('home.html', mangas=manga_list)

def generate_color():
    """Génère une couleur aléatoire pour les placeholders"""
    import random
    colors = ['ff69b4', '87ceeb', 'dda0dd', 'ffe4b5', '9370db', 'ffd700', 
              'ff6347', '20b2aa', 'ffa07a', 'cd5c5c', '90ee90', 'f0e68c']
    return random.choice(colors)

@main_bp.route('/manga/<int:id>')
def manga_detail(id):
    """Redirection vers la page de détail du manga"""
    from flask import redirect, url_for
    return redirect(url_for('mangas.manga_detail', id=id))