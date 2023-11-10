import os
import azure.cognitiveservices.speech as speechsdk
import time
import uuid
import random
from pydub import AudioSegment
from dotenv import load_dotenv

#------------------------------------#
#             AZURE CREDS            #
#------------------------------------#

load_dotenv()
subscription_key = os.getenv("AZURE_TOKEN")
service_region = os.getenv("AZURE_REGION")



#------------------------------------#
#              FUNCTIONS             #
#------------------------------------#

def transcribe_chunks_to_text(audio_chunk):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_chunk)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    
def split_audio_to_chunks(audio_details):
    temp_wav_name = "/tmp/" + str(uuid.uuid4()) + ".wav"

    audio = AudioSegment.from_file(audio_details['audio_name'])
    audio_details['text'] = ""
    audio_details['first_words'] = ""
    audio_details['last_words'] = ""
    audio_details['middle_words'] = ""

    chunk_length = 20000
    ten_minutes = 600000

    num_moments = len(audio) // ten_minutes
    moments = []
    moments_idx = 1

    if num_moments > 0:
        for _ in range(num_moments):
            random_chunk = random.randint(ten_minutes // chunk_length, (len(audio) // chunk_length)-3) * chunk_length
            moments.append(random_chunk)

    for i in range(0, len(audio), chunk_length):

        audio_chunk = audio[i:i + chunk_length]
        audio_chunk_filename = temp_wav_name
        audio_chunk.export(audio_chunk_filename, format="wav")


        if (i + chunk_length <= 40000) or (len(audio) - (i + chunk_length) <= 40000) or i in moments or i - 20000 in moments:
            time.sleep(5)
        
        if i + chunk_length <= 60000:
            text = transcribe_chunks_to_text(audio_chunk_filename)
            audio_details['text'] += f" {text}"
            audio_details['first_words'] += f" {text}"

        elif len(audio) - (i + chunk_length) <= 60000:
            text = transcribe_chunks_to_text(audio_chunk_filename)
            audio_details['text'] += f" {text}"
            audio_details['last_words'] += f" {text}"

        elif i in moments or i-20000 in moments:
            text = transcribe_chunks_to_text(audio_chunk_filename)
            audio_details['text'] += f" {text}"
            audio_details['middle_words'] += f"Zdanie {moments_idx}:  '{text}'"
            moments_idx += 1

#        else:
#            audio_details['text'] += f" {transcribe_chunks_to_text(audio_chunk_filename)}"

    return audio_details

