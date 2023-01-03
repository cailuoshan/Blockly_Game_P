from ..models import db, Score
from config import game_levels
import random
from . import main

# 在main/__init__.py中最后一行加入from . import后面加入test

user_list = ['A1', 'A2', 'A3', 'A4']

@main.route('/test/generate_fake_scores', methods=['GET'])
def generate_fake_scores():
    count = 0
    for user in user_list:
        for game in game_levels.keys():
            time_cost = random.randint(100, 200)
            score = Score(
                username=user,
                game_name=game,
                time_cost=time_cost
            )
            count += 1
            if count < 25:
                db.session.add(score)
    db.session.commit()
    return 'fake score generated.'

@main.route('/test/delete_fake_scores', methods=['GET'])
def delete_fake_scores():
    scores = Score.query.all()
    for score in scores:
        db.session.delete(score)
    db.session.commit()
    return 'fake score deleted.'