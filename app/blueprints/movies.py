from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Movie
from app.utils import export_to_csv

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def list_movies():
    search = request.args.get('search', '')
    
    if search:
        items = Movie.query.filter(Movie.title.contains(search)).all()
    else:
        items = Movie.query.all()
    
    items = [m.to_dict() for m in items]
    return render_template('list.html', items=items, category='movies', title='Movies')

@movies_bp.route('/add', methods=['POST'])
def add():
    movie = Movie(
        title=request.form['title'],
        year=int(request.form['year']) if request.form['year'] else None,
        genre=request.form['genre'] if request.form['genre'] else None,
        director=request.form['director'] if request.form['director'] else None,
        rating=float(request.form['rating']) if request.form['rating'] else None
    )
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('movies.list_movies'))

@movies_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    movie = Movie.query.get_or_404(id)
    movie.title = request.form['title']
    movie.year = int(request.form['year']) if request.form['year'] else None
    movie.genre = request.form['genre'] if request.form['genre'] else None
    movie.director = request.form['director'] if request.form['director'] else None
    movie.rating = float(request.form['rating']) if request.form['rating'] else None
    db.session.commit()
    return redirect(url_for('movies.list_movies'))

@movies_bp.route('/delete/<int:id>')
def delete(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies.list_movies'))

@movies_bp.route('/export/<format>')
def export(format):
    items = Movie.query.all()
    
    if format == 'csv':
        headers = ['ID', 'Title', 'Year', 'Genre', 'Director', 'Rating']
        rows = [[i.id, i.title, i.year, i.genre, i.director, i.rating] for i in items]
        return export_to_csv(rows, headers, 'movies.csv')
    else:
        return jsonify([i.to_dict() for i in items])