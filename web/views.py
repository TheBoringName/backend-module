from flask import Blueprint, request
from bson import json_util

import dummy_returner
import db
import json

bp = Blueprint("bp", __name__)

@bp.route("/describe", methods=["POST"])
def upload():
    video_id = str(db.add_new_video(request.json))
    # //DO SOME STUFF WITH AI
    response = {'summary_score': dummy_returner.summary_score, 'summary_text': dummy_returner.summary_text,
                'timestamp_generated': str(dummy_returner.timestamp_generated), 'video_id': str(video_id)}
    db.create_result_record(parse_json(response))
    return response




@bp.route("/find", methods=["GET"])
def find_results_by_title():
    # args = request.args
    # results = db.get_search_results(args.get("title"))
    # return parse_json(results)
    return "Hello fucker"


def parse_json(data):
    return json.loads(json_util.dumps(data))
