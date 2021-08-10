from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Note
from . import db
import json

views = Blueprint('views',__name__)



@views.route('/',methods=['GET','POST'])
@login_required
def home():
    
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('El texto ingresado es demasiado corto!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota añadida!', category='success')
    notes = Note.query.all()
    return render_template("home.html", user=current_user, notes=notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})


