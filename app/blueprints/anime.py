from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Anime
from app.utils import export_to_csv

anime_bp = Blueprint('anime', __name__)

@anime_bp.route('/')
def list_anime():
    search = request.args.get('search', '')
    
    if search:
        items = Anime.query.filter(Anime.title.contains(search)).all()
    else:
        items = Anime.query.all()
    
    items = [a.to_dict() for a in items]
    return render_template('list.html', items=items, category='anime', title='Anime')

@anime_bp.route('/add', methods=['POST'])
def add():
    anime = Anime(
        title=request.form['title'],
        year=int(request.form['year']) if request.form['year'] else None,
        studio=request.form['studio'] if request.form['studio'] else None,
        episodes=int(request.form['episodes']) if request.form['episodes'] else None,
        status=request.form['status'] if request.form['status'] else None
    )
    db.session.add(anime)
    db.session.commit()
    return redirect(url_for('anime.list_anime'))

@anime_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    anime = Anime.query.get_or_404(id)
    anime.title = request.form['title']
    anime.year = int(request.form['year']) if request.form['year'] else None
    anime.studio = request.form['studio'] if request.form['studio'] else None
    anime.episodes = int(request.form['episodes']) if request.form['episodes'] else None
    anime.status = request.form['status'] if request.form['status'] else None
    db.session.commit()
    return redirect(url_for('anime.list_anime'))

@anime_bp.route('/delete/<int:id>')
def delete(id):
    anime = Anime.query.get_or_404(id)
    db.session.delete(anime)
    db.session.commit()
    return redirect(url_for('anime.list_anime'))

@anime_bp.route('/export/<format>')
def export(format):
    items = Anime.query.all()
    
    if format == 'csv':
        headers = ['ID', 'Title', 'Year', 'Studio', 'Episodes', 'Status']
        rows = [[i.id, i.title, i.year, i.studio, i.episodes, i.status] for i in items]
        return export_to_csv(rows, headers, 'anime.csv')
    else:
        return jsonify([i.to_dict() for i in items])