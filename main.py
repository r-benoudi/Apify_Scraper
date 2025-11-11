from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import csv
import json
import io
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///media.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    director = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Float, nullable=True)

class Manga(db.Model):
    __tablename__ = 'mangas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    author = db.Column(db.String(100), nullable=True)
    volumes = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)

class Anime(db.Model):
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    studio = db.Column(db.String(100), nullable=True)
    episodes = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=True)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():

    F = Movie.query.all()
    M = Manga.query.all()
    A = Anime.query.all()
    items1 = [
    {
        "id": m.id,
        "title": m.title,
        "year": m.year,
        "genre": m.genre,
        "director": m.director,
        "rating": m.rating
    }
    for m in F
    ]
    items2 = [
    {
        "id": m.id,
        "title": m.title,
        "year": m.year,
        "author": m.author,
        "volumes": m.volumes,
        "status": m.status
    }
    for m in M
    ]
    items3 = [
    {
        "id": m.id,
        "title": m.title,
        "year": m.year,
        "studio": m.studio,
        "episodes": m.episodes,
        "status": m.status
    }
    for m in A
    ]
    
    return render_template('index.html', items1=items1, items2=items2, items3=items3)




# Movies Routes
@app.route('/movies')
def movies():
    search = request.args.get('search', '')
    if search:
        items = Movie.query.filter(Movie.title.contains(search)).all()
        items = [
        {
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "genre": m.genre,
            "director": m.director,
            "rating": m.rating
        }
        for m in items
        ]
    else:
        items = Movie.query.all()
        items = [
        {
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "genre": m.genre,
            "director": m.director,
            "rating": m.rating
        }
        for m in items
        ]
    return render_template('list.html', items=items, category='movies', title='Movies')

@app.route('/movies/add', methods=['POST'])
def add_movie():
    movie = Movie(
        title=request.form['title'],
        year=int(request.form['year']) if request.form['year'] else None,
        genre=request.form['genre'] if request.form['genre'] else None,
        director=request.form['director'] if request.form['director'] else None,
        rating=float(request.form['rating']) if request.form['rating'] else None
    )
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('movies'))

@app.route('/movies/edit/<int:id>', methods=['POST'])
def edit_movie(id):
    movie = Movie.query.get_or_404(id)
    movie.title = request.form['title']
    movie.year = int(request.form['year']) if request.form['year'] else None
    movie.genre = request.form['genre'] if request.form['genre'] else None
    movie.director = request.form['director'] if request.form['director'] else None
    movie.rating = float(request.form['rating']) if request.form['rating'] else None
    db.session.commit()
    return redirect(url_for('movies'))

@app.route('/movies/delete/<int:id>')
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies'))

@app.route('/movies/export/<format>')
def export_movies(format):
    items = Movie.query.all()
    if format == 'csv':
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerow(['ID', 'Title', 'Year', 'Genre', 'Director', 'Rating'])
        for item in items:
            writer.writerow([item.id, item.title, item.year, item.genre, item.director, item.rating])
        output = io.BytesIO()
        output.write(si.getvalue().encode('utf-8'))
        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='movies.csv')
    else:
        data = [{'id': i.id, 'title': i.title, 'year': i.year, 'genre': i.genre, 
                 'director': i.director, 'rating': i.rating} for i in items]
        return jsonify(data)

# Mangas Routes
@app.route('/mangas')
def mangas():
    search = request.args.get('search', '')
    if search:
        items = Manga.query.filter(Manga.title.contains(search)).all()
        items = [
        {
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "author": m.author,
            "volumes": m.volumes,
            "status": m.status
        }
        for m in items
        ]
    else:
        items = Manga.query.all()
        items = [
        {
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "author": m.author,
            "volumes": m.volumes,
            "status": m.status
        }
        for m in items
        ]
    return render_template('list.html', items=items, category='mangas', title='Mangas')

@app.route('/mangas/add', methods=['POST'])
def add_manga():
    manga = Manga(
        title=request.form['title'],
        year=int(request.form['year']) if request.form['year'] else None,
        author=request.form['author'] if request.form['author'] else None,
        volumes=int(request.form['volumes']) if request.form['volumes'] else None,
        status=request.form['status'] if request.form['status'] else None
    )
    db.session.add(manga)
    db.session.commit()
    return redirect(url_for('mangas'))

@app.route('/mangas/edit/<int:id>', methods=['POST'])
def edit_manga(id):
    manga = Manga.query.get_or_404(id)
    manga.title = request.form['title']
    manga.year = int(request.form['year']) if request.form['year'] else None
    manga.author = request.form['author'] if request.form['author'] else None
    manga.volumes = int(request.form['volumes']) if request.form['volumes'] else None
    manga.status = request.form['status'] if request.form['status'] else None
    db.session.commit()
    return redirect(url_for('mangas'))

@app.route('/mangas/delete/<int:id>')
def delete_manga(id):
    manga = Manga.query.get_or_404(id)
    db.session.delete(manga)
    db.session.commit()
    return redirect(url_for('mangas'))

@app.route('/mangas/export/<format>')
def export_mangas(format):
    items = Manga.query.all()
    if format == 'csv':
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerow(['ID', 'Title', 'Year', 'Author', 'Volumes', 'Status'])
        for item in items:
            writer.writerow([item.id, item.title, item.year, item.author, item.volumes, item.status])
        output = io.BytesIO()
        output.write(si.getvalue().encode('utf-8'))
        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='mangas.csv')
    else:
        data = [{'id': i.id, 'title': i.title, 'year': i.year, 'author': i.author, 
                 'volumes': i.volumes, 'status': i.status} for i in items]
        return jsonify(data)

# Anime Routes
@app.route('/anime')
def anime():
    search = request.args.get('search', '')
    if search:
        items = Anime.query.filter(Anime.title.contains(search)).all()
        items = [
        {
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "studio": m.studio,
            "episodes": m.episodes,
            "status": m.status
        }
        for m in items
        ]
    else:
        items = Anime.query.all()
        items = [
        {
            "id": m.id,
            "title": m.title,
            "year": m.year,
            "studio": m.studio,
            "episodes": m.episodes,
            "status": m.status
        }
        for m in items
        ]
    return render_template('list.html', items=items, category='anime', title='Anime')

@app.route('/anime/add', methods=['POST'])
def add_anime():
    anime = Anime(
        title=request.form['title'],
        year=int(request.form['year']) if request.form['year'] else None,
        studio=request.form['studio'] if request.form['studio'] else None,
        episodes=int(request.form['episodes']) if request.form['episodes'] else None,
        status=request.form['status'] if request.form['status'] else None
    )
    db.session.add(anime)
    db.session.commit()
    return redirect(url_for('anime'))

@app.route('/anime/edit/<int:id>', methods=['POST'])
def edit_anime(id):
    anime = Anime.query.get_or_404(id)
    anime.title = request.form['title']
    anime.year = int(request.form['year']) if request.form['year'] else None
    anime.studio = request.form['studio'] if request.form['studio'] else None
    anime.episodes = int(request.form['episodes']) if request.form['episodes'] else None
    anime.status = request.form['status'] if request.form['status'] else None
    db.session.commit()
    return redirect(url_for('anime'))

@app.route('/anime/delete/<int:id>')
def delete_anime(id):
    anime = Anime.query.get_or_404(id)
    db.session.delete(anime)
    db.session.commit()
    return redirect(url_for('anime'))

@app.route('/anime/export/<format>')
def export_anime(format):
    items = Anime.query.all()
    if format == 'csv':
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerow(['ID', 'Title', 'Year', 'Studio', 'Episodes', 'Status'])
        for item in items:
            writer.writerow([item.id, item.title, item.year, item.studio, item.episodes, item.status])
        output = io.BytesIO()
        output.write(si.getvalue().encode('utf-8'))
        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='anime.csv')
    else:
        data = [{'id': i.id, 'title': i.title, 'year': i.year, 'studio': i.studio, 
                 'episodes': i.episodes, 'status': i.status} for i in items]
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)