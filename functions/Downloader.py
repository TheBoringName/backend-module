from pytube import YouTube
from pydub import AudioSegment
import os
import uuid
import pyktok as pyk
import re
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

#------------------------------------#
#          YOUTUBE DOWNLOADER        #
#------------------------------------#

def download_audio_from_youtube(video_url):
    wav_name = str(uuid.uuid4()) + ".wav"
    ytube = YouTube(video_url)
    video_filter = ytube.streams.filter(only_audio=True).first()
    video = video_filter.download(output_path="") 
    wav_name = convert_mp4_to_wav(video)

    return wav_name

#------------------------------------#
#           TIKTOK DOWNLOADER        #
#------------------------------------#

def download_audio_from_tiktok(video_url):
    regex_pattern = r'https://www\.tiktok\.com/(@[A-Za-z0-9_]+)/(\w+)/(\d+)\?'
    match = re.search(regex_pattern, video_url)
    if match:
        username = match.group(1)
        keyword = match.group(2)
        video_id = match.group(3)

    pyk.save_tiktok(video_url, True, "test.csv",'edge')
    video_mp4_name = f"{username}_{keyword}_{video_id}.mp4"
    wav_name = convert_mp4_to_wav(video_mp4_name)
    
    return wav_name

#------------------------------------#
#         INSTAGRAM DOWNLOADER       #
#------------------------------------#

def download_audio_from_instagram(video_url):
    cl = Client()
    cl.login(os.getenv("IG_USERNAME"), os.getenv("IG_PASSOWRD"))

    video_data = cl.media_pk_from_url(video_url)
    video = cl.video_download(video_data)
    wav_name = convert_mp4_to_wav(video)

    return wav_name


#------------------------------------#
#        VIDEO-AUDIO CONVERTER       #
#------------------------------------#

def convert_mp4_to_wav(video_path):
    wav_name = str(uuid.uuid4()) + ".wav"
    audio = AudioSegment.from_file(video_path, format="mp4")
    audio = audio.set_channels(1)
    audio.export(wav_name, format="wav")

    os.remove(video_path)
    return wav_name

