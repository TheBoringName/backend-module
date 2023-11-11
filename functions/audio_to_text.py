import os
import azure.cognitiveservices.speech as speechsdk
import time
import uuid
import random
from pydub import AudioSegment
from dotenv import load_dotenv

import multiprocessing
from queue import Empty

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

def process_audio_chunk(chunk_info, result_queue, id):
    audio_chunk_filename, text_type = chunk_info
    text = transcribe_chunks_to_text(audio_chunk_filename)
    result_queue.put((audio_chunk_filename, text, text_type, id))

def split_audio_to_chunks(audio_details):

    audio = AudioSegment.from_file(audio_details['audio_name'])
    audio_details['text'] = ""
    audio_details['first_words'] = ""
    audio_details['last_words'] = ""
    audio_details['middle_words'] = ""

    chunk_length = 15000
    seven_minutes = 450000
    one_minute = 60000

    num_moments = len(audio) // seven_minutes
    moments = []

    if num_moments > 0:
        for _ in range(num_moments):
            random_chunk = random.randint(one_minute // chunk_length, (len(audio) // chunk_length)-4) * chunk_length
            moments.append(random_chunk)


    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(0, len(audio), chunk_length):

        if not os.path.exists("/tmp/" + audio_details["title"].replace(" ", "")):
            os.makedirs("/tmp/" + audio_details["title"].replace(" ", ""))

        temp_wav_name = "/tmp/" + audio_details["title"].replace(" ", "") + "/" + str(uuid.uuid4()) + ".wav"
        audio_chunk = audio[i:i + chunk_length]
        audio_chunk.export(temp_wav_name, format="wav")

        if (i + chunk_length <= 60000):
            process = multiprocessing.Process(target=process_audio_chunk, args=((temp_wav_name, "first_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

        elif len(audio) - (i + chunk_length) <= 60000:
            process = multiprocessing.Process(target=process_audio_chunk, args=((temp_wav_name, "last_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

        elif i in moments or i-20000 in moments:
            process = multiprocessing.Process(target=process_audio_chunk, args=((temp_wav_name, "middle_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

    for process in processes:
        process.join()

    try:
        results = []
        while True:
            audio_chunk_filename, text, type_text, type_id = result_queue.get_nowait()
            results.append((type_id, audio_chunk_filename,type_text, text))

    except Empty:
        pass

    results.sort(key=lambda x: x[0])

    for result in results:
        audio_details[result[2]] += f" {result[3]}"

    return audio_details