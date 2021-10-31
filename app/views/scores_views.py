from flask import Blueprint
from flask_jwt_extended import (jwt_required)

from app.actions.scores_actions import get_score_by_id, get_approval_reasons

app_scores = Blueprint('scores', __name__)


@app_scores.route('/scorereasons/<id>', methods=['GET'])
def get_score_by_id(score_id):
    score = get_score_by_id(score_id)
    approval_reasons = get_approval_reasons(score)
    return approval_reasons
