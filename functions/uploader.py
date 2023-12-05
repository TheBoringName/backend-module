import os
import re
import uuid
import base64
import io
from dotenv import load_dotenv
from instagrapi import Client
from pydub import AudioSegment
from pytube import YouTube

import functions.tiktok_lib.python_tiktok as pyk

load_dotenv()


def download_audio(source, video_url):
    match source:
        case "YouTube":
            return download_audio_from_youtube(video_url)
        case "Instagram":
            return download_audio_from_instagram(video_url)
        case "TikTok":
            return download_audio_from_tiktok(video_url)
        case "Local":
            return upload_audio_from_local(video_url)
        case _:
            raise ValueError("Invalid source")


# ------------------------------------#
#       YOUTUBE DOWNLOAD AUDIO       #
# ------------------------------------#

def download_audio_from_youtube(video_url):
    video_details = {}
    video_details["url"] = video_url

    ytube = YouTube(video_url)

    video_filter = ytube.streams.filter(progressive=True, type='video', file_extension='mp4').order_by(
        'resolution').desc().first()

    if "shorts" in video_url:
        video_details["tags"] = re.findall(r'#\w+', ytube.title)
        video_details["title"] = re.sub(r'#\w+', '', ytube.title).strip()
    else:
        video_details["tags"] = ytube.keywords
        video_details["title"] = ytube.title

    video_details["author"] = ytube.author
    video_details["length"] = ytube.length
    video_details["published"] = ytube.publish_date
    video_details["type"] = "YouTube"

    video = video_filter.download(output_path="/tmp")
    video_details["audio_name"] = convert_mp4_to_wav(video)

    return video_details


# ------------------------------------#
#        TIKTOK DOWNLOAD AUDIO       #
# ------------------------------------#

def download_audio_from_tiktok(video_url):
    video_details = {}
    video_details["url"] = video_url

    url_without_domain = video_url.replace("https://www.tiktok.com/", "")

    username = url_without_domain.split("/")[0]
    type = re.search(r'[^/]+', url_without_domain.split("/", 1)[1]).group()
    video_id = re.search(r'\d+', url_without_domain).group()

    pyk.save_tiktok(video_url)
    video_info = pyk.get_tiktok_json(video_url)

    video_details["tags"] = re.findall(r'#\w+', video_info["ItemModule"][video_id]["desc"])
    video_details["creator"] = username.replace("@", "")
    video_details["title"] = re.sub(r'#\w+', '', video_info["ItemModule"][video_id]["desc"]).strip()
    video_details["type"] = "Instagram"

    video_mp4_name = f"{username}_{type}_{video_id}.mp4"

    video_details["audio_name"] = convert_mp4_to_wav(video_mp4_name)

    return video_details


# ------------------------------------#
#      INSTAGRAM DOWNLOAD AUDIO      #
# ------------------------------------#

def download_audio_from_instagram(video_url):
    video_details = {}
    video_details["url"] = video_url

    cl = Client()
    cl.login(os.getenv("IG_USERNAME"), os.getenv("IG_PASSOWRD"))

    video_data = cl.media_pk_from_url(video_url)
    video_info = cl.media_info(video_data)

    video_info.caption_text = video_info.caption_text.replace("\n", "").replace(".", "")

    video_details["tags"] = re.findall(r'#\w+', video_info.caption_text)
    video_details["creator"] = video_info.user.username
    video_details["title"] = re.sub(r'#\w+', '', video_info.caption_text).strip()
    video_details["type"] = "TikTok"

    video = cl.video_download(video_data)
    video_details["audio_name"] = convert_mp4_to_wav(video)

    return video_details


# ------------------------------------#
#         LOCAL UPLOAD AUDIO         #
# ------------------------------------#

def upload_audio_from_local(video_path):
    video_details = {}
    video_details["url"] = video_path
    video_details["type"] = "Local"
    video_details["audio_name"] = convert_mp4_to_wav(video_path)

    return video_details


# ------------------------------------#
#        VIDEO-AUDIO CONVERTER       #
# ------------------------------------#

def convert_mp4_to_wav(video_path):
    wav_name = "/tmp/" + str(uuid.uuid4()) + ".wav"
    binary_audio = base64.b64decode(video_path)
    audio = AudioSegment.from_file(io.BytesIO(binary_audio), format="mp4")
    audio = audio.set_channels(1)
    audio.export(wav_name, format="wav")

    os.remove(video_path)
    return wav_name
