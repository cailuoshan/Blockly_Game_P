from . import main
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from flask import request, render_template
import json
from config import game_levels
from ..models import db, Score, User

score_dict = {}
level_dict = {}
current_key_list = []


@main.route('/record', methods=['POST'])
@login_required
def record():
    data = request.json
    key_list: list = data['key_list']

    global score_dict, level_dict, current_key_list

    if len(key_list) == 0:
        score_dict = {}
        level_dict = {}
        current_key_list = []
        scores = Score.query.filter(Score.username==current_user.username).all()
        for score in scores:
            db.session.delete(score)
        db.session.commit()

    parse_key_list(key_list)

    return 'data recorded.'


def parse_key_list(key_list):
    current_key_str = ' '.join(current_key_list)
    if len(key_list) > len(current_key_list):
        new_key_list = list(set(key_list) - set(current_key_list))
        new_key: str = new_key_list[0]
        current_key_list.append(new_key)
        current_key_str = ' '.join(current_key_list)

        for game in game_levels.keys():
            if new_key.find(game) != -1:
                level_list = add_level_list(game, new_key)
                if len(level_list) == game_levels.get(game):
                    time_list = score_dict.setdefault(game, [])
                    time_list.append(datetime.now())

                    assert len(time_list) == 2
                    time_cost = (time_list[1] - time_list[0]).seconds
                    username = current_user.username
                    score = Score(
                        username=username,
                        game_name=game,
                        time_cost=time_cost
                    )
                    db.session.add(score)
                    db.session.commit()
                break
    elif len(key_list) == len(current_key_list):
        for game in game_levels.keys():
            if current_key_str.find(game) == -1:
                time_list = score_dict.setdefault(game, [])
                time_list.clear()
                time_list.append(datetime.now())


def add_level_list(game, new_key):
    level = new_key.replace(game, '')
    level_list = level_dict.setdefault(game, [])
    level_list.append(level)
    return level_list


@main.route('/show_scores', methods=['GET'])
def show_scores():
    data = request.args
    game = data.get('game')
    if game in game_levels.keys():
        scores = Score.query. \
            filter(Score.game_name == game) \
            .order_by(Score.time_cost).all()
        scores_tuple = ((index + 1, score) for index, score in enumerate(scores))
        response = render_template(
            'scores.html',
            scores=scores_tuple,
            game=game
        )
    elif game == 'all':
        users = User.query.filter(User.confirmed == True).all()
        total_score_dict = {}
        for user in users:
            total_scores = Score.query.filter(Score.username == user.username).all()
            if len(total_scores) == len(game_levels.keys()):
                total_score_dict.setdefault(user.username, 0)
                for score in total_scores:
                    total_score_dict[user.username] += score.time_cost
        sorted_scores = sorted(total_score_dict.items(), key=lambda x: x[1])
        score_list = []
        for username, time_cost in sorted_scores:
            total_score = TotalScore(username=username, time_cost=time_cost)
            score_list.append(total_score)
        scores_tuple = ((index + 1, score) for index, score in enumerate(score_list))

        response = render_template(
            'scores.html',
            scores=scores_tuple,
            game='全部'
        )

    else:
        response = render_template('404.html')

    return response


class TotalScore:
    def __init__(self, username, time_cost):
        self.username = username
        self.time_cost = time_cost
