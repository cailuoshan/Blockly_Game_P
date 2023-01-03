from flask import render_template, redirect
from . import main
from flask_login import login_required


@main.route('/')
@login_required
def index():
    # return render_template('blocky_games/index.html')
    return redirect('http://82.157.249.71/blockly_games')