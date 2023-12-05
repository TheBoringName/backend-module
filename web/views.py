import json
from datetime import datetime

from bson import json_util
from flask import Blueprint, request

import db
import functions.analyzer as an
import functions.audio_to_text as att
import functions.uploader as dwn
import functions.sentiment as st
from flask_cors import cross_origin

bp = Blueprint("bp", __name__)


@bp.route("/describe", methods=["POST"])
@cross_origin()
def upload():
    audio_details = dwn.download_audio(request.json["source"], request.json["url"])
    audio_extend_details = att.split_audio_to_chunks(audio_details)
    final_audio_details = an.analyze_text_via_gpt(audio_extend_details)
    sentiment_value = st.sentiment_analyze_via_azure(audio_extend_details)

    video_data = {
        "title": audio_details["title"],
        # "duration": audio_details["length"],
        # "publication_date": str(audio_details["published"]),
        "source": request.json["source"],
        "url": request.json["url"],
        "sentiment": sentiment_value
    }
    video_id = str(db.add_new_video(video_data))
    response = final_audio_details['gpt_response']
    result = {
        "video_id": video_id,
        "analysis": response,
        "analysis_date": str(datetime.now())
    }
    db.create_result_record(parse_json(result))
    video_data.update(result)
    del video_data['_id']
    del video_data['video_id']
    return video_data


@bp.route("/find", methods=["GET"])
@cross_origin()
def find_results_by_title():
    args = request.args
    results = db.get_search_results(args.get("title"))
    return parse_json(results)


@bp.route("/history", methods=["GET"])
@cross_origin()
def get_history():
    args = request.args
    results = db.get_single_page(args.get("page"))
    return parse_json(results)


@bp.route("/history/list", methods=["GET"])
@cross_origin()
def get_history_list():
    args = request.args
    results = db.get_history_list(args.get("size"))
    return parse_json(results)


def parse_json(data):
    return json.loads(json_util.dumps(data))
