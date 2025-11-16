from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.movies import movies_bp
    from app.blueprints.mangas import mangas_bp
    from app.blueprints.anime import anime_bp
    from app.blueprints.scraper import scraper_bp  # NOUVEAU

    app.register_blueprint(main_bp)
    app.register_blueprint(movies_bp, url_prefix='/movies')
    app.register_blueprint(mangas_bp, url_prefix='/mangas')
    app.register_blueprint(anime_bp, url_prefix='/anime')
    app.register_blueprint(scraper_bp)  # NOUVEAU , url_prefix='/scraper'

    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app