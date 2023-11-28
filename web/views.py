import json
from datetime import datetime

from bson import json_util
from flask import Blueprint, request

import db
import functions.analyzer as an
import functions.audio_to_text as att
import functions.uploader as dwn

bp = Blueprint("bp", __name__)


@bp.route("/describe", methods=["POST"])
def upload():
    # video_id = str(db.add_new_video(request.json))

    audio_details = dwn.download_audio(request.json["source"], request.json["url"])
    audio_extend_details = att.split_audio_to_chunks(audio_details)
    final_audio_details = an.analyze_text_via_gpt(audio_extend_details)
    response = final_audio_details['gpt_response']

    # response = {'summary_score': dummy_returner.summary_score, 'summary_text': dummy_returner.summary_text,
    #             'timestamp_generated': str(dummy_returner.timestamp_generated), 'video_id': str(video_id)}
    # db.create_result_record(parse_json(response))
    # TODO: Test for other sources
    return {
        "title": audio_details["title"],
        "author": audio_details["author"],
        "published": audio_details["published"],
        "length": audio_details["length"],
        "type": audio_details["type"],
        "url": audio_details["url"],
        "analysis": response,
        "analysis_time": datetime.now()
    }


@bp.route("/find", methods=["GET"])
def find_results_by_title():
    args = request.args
    results = db.get_search_results(args.get("title"))
    return parse_json(results)
    # return "Hello"


def parse_json(data):
    return json.loads(json_util.dumps(data))
