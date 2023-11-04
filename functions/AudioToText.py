import os
import azure.cognitiveservices.speech as speechsdk
import time
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

load_dotenv()

#------------------------------------#
#             AZURE CREDS            #
#------------------------------------#

subscription_key = os.getenv("AZURE_TOKEN")
service_region = os.getenv("AZURE_REGION")

#------------------------------------#
#              FUNCTIONS             #
#------------------------------------#

def transcribe_audio_to_text(audio_chunk, subscription_key, service_region):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_chunk)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()
    print(speech_recognizer.recognize_once())

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    
def split_audito_to_chunks(audio_filename):
    audio = AudioSegment.from_file(audio_filename)
    transcriptions = ""
    chunk_length = 10000

    for i in range(0, len(audio), chunk_length):
        audio_chunk = audio[i:i + chunk_length]
        audio_chunk_filename = f"temporary_chunk.wav"

        audio_chunk.export(audio_chunk_filename, format="wav")
        time.sleep(5)
        
        transcriptions += f" {transcribe_audio_to_text(audio_chunk_filename)}"

    return transcriptions
