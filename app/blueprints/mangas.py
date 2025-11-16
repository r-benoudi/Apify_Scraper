from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Manga
from app.utils import export_to_csv

mangas_bp = Blueprint('mangas', __name__)

@mangas_bp.route('/')
def list_mangas():
    search = request.args.get('search', '')
    
    if search:
        items = Manga.query.filter(Manga.title.contains(search)).all()
    else:
        items = Manga.query.all()
    
    items = [m.to_dict() for m in items]
    return render_template('list.html', items=items, category='mangas', title='Mangas')

@mangas_bp.route('/add', methods=['POST'])
def add():
    manga = Manga(
        title=request.form['title'],
        year=int(request.form['year']) if request.form['year'] else None,
        author=request.form['author'] if request.form['author'] else None,
        volumes=int(request.form['volumes']) if request.form['volumes'] else None,
        status=request.form['status'] if request.form['status'] else None
    )
    db.session.add(manga)
    db.session.commit()
    return redirect(url_for('mangas.list_mangas'))

@mangas_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    manga = Manga.query.get_or_404(id)
    manga.title = request.form['title']
    manga.year = int(request.form['year']) if request.form['year'] else None
    manga.author = request.form['author'] if request.form['author'] else None
    manga.volumes = int(request.form['volumes']) if request.form['volumes'] else None
    manga.status = request.form['status'] if request.form['status'] else None
    db.session.commit()
    return redirect(url_for('mangas.list_mangas'))

@mangas_bp.route('/delete/<int:id>')
def delete(id):
    manga = Manga.query.get_or_404(id)
    db.session.delete(manga)
    db.session.commit()
    return redirect(url_for('mangas.list_mangas'))

@mangas_bp.route('/export/<format>')
def export(format):
    items = Manga.query.all()
    
    if format == 'csv':
        headers = ['ID', 'Title', 'Year', 'Author', 'Volumes', 'Status']
        rows = [[i.id, i.title, i.year, i.author, i.volumes, i.status] for i in items]
        return export_to_csv(rows, headers, 'mangas.csv')
    else:
        return jsonify([i.to_dict() for i in items])