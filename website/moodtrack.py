from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import MoodTracker
from . import db
from datetime import datetime

mood = Blueprint('mood', __name__)

@mood.route('/mood-create', methods=['GET', 'POST'])
@login_required
def mood_create():
    if request.method == 'POST':
        mood_entry = request.form.get('mood')
        note = request.form.get('note')
        datetimeori = request.form.get('date')

        # Ensure the date is provided
        if not datetimeori:
            flash("Date is still empty!", category='error')
            return render_template('journalcreate.html')

        try:
            datetimefix = datetime.strptime(datetimeori, '%Y-%m-%d')
        except ValueError:
            flash("Invalid date format! Please use YYYY-MM-DD.", category='error')
            return render_template('journalcreate.html')

        # Check if mood is provided
        if not mood_entry:
            flash("Must include your mood today!", category='error')
        else:
            # Create a new mood entry associated with the logged-in user
            new_mood = MoodTracker(mood=mood_entry, date=datetimefix, note=note, user_id=current_user.id)
            db.session.add(new_mood)
            db.session.commit()
            flash("Mood entry created successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template('journalcreate.html')

@mood.route('/mood-entries')
@login_required  # This decorator ensures the user is logged in
def mood_entries():
    entries = MoodTracker.query.filter_by(user_id=current_user.id).all()
    return render_template('mood_entries2.html', entries=entries)