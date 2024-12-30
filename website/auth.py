from flask import Blueprint, render_template, redirect, url_for, session
import pandas as pd

auth = Blueprint('auth', __name__)

@auth.route('/dataset/')
def dataset():
    # Check if 'df' is in session
    if 'df' not in session:
        return redirect(url_for('views.home'))

    # Load the dataframe from the session (as JSON)
    df = pd.read_json(session['df'])

    # Check if the dataframe is empty
    if df.empty:
        return redirect(url_for('views.home'))

    return render_template("dataset.html", df=df)
