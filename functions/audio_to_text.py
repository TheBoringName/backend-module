import os
import azure.cognitiveservices.speech as speechsdk
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
    audio_details['length'] = len(audio)
    audio_details['text'] = ""
    audio_details['first_words'] = ""
    audio_details['last_words'] = ""
    audio_details['middle_words'] = ""

    result_queue = multiprocessing.Queue()


    if len(audio) <= 180000:
        get_text_from_short_audio(audio, result_queue)

    elif len(audio) > 180000 and len(audio) < 600000:
        get_text_from_middle_audio(audio, result_queue)

    else:
        get_text_from_long_audio(audio, result_queue)


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

# ===================================#

def get_text_from_short_audio(audio, result_queue):
    processes = []
    chunk_length = 15000
    for i in range(0, len(audio), chunk_length):
        tmp_folder_name =  "/tmp/" +  str(uuid.uuid4())

        if not os.path.exists(tmp_folder_name):
            os.makedirs(tmp_folder_name)

        tmp_wav_name = tmp_folder_name + "/" + str(uuid.uuid4()) + ".wav"
        audio_chunk = audio[i:i + chunk_length]
        audio_chunk.export(tmp_wav_name, format="wav")

        process = multiprocessing.Process(target=process_audio_chunk, args=((tmp_wav_name, "text"), result_queue, i + chunk_length))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

def get_text_from_middle_audio(audio, result_queue):
    processes = []
    chunk_length = 15000

    for i in range(0, len(audio), chunk_length):
        tmp_folder_name =  "/tmp/" +  str(uuid.uuid4())

        if not os.path.exists(tmp_folder_name):
            os.makedirs(tmp_folder_name)

        tmp_wav_name = tmp_folder_name + "/" + str(uuid.uuid4()) + ".wav"

        audio_chunk = audio[i:i + chunk_length]
        audio_chunk.export(tmp_wav_name, format="wav")

        if (i + chunk_length <= 45000):
            process = multiprocessing.Process(target=process_audio_chunk, args=((tmp_wav_name, "first_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

        elif len(audio) - (i + chunk_length) <= 45000:
            process = multiprocessing.Process(target=process_audio_chunk, args=((tmp_wav_name, "last_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

        elif i >= len(audio) * 0.4 and i <= len(audio) * 0.6:
            process = multiprocessing.Process(target=process_audio_chunk, args=((tmp_wav_name, "middle_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

    for process in processes:
        process.join()

def get_text_from_long_audio(audio, result_queue):
    processes = []
    chunk_length = 15000
    seven_minutes = 450000
    one_minute = 60000

    num_moments = len(audio) // seven_minutes
    moments = []

    if num_moments > 0:
        for _ in range(num_moments):
            random_chunk = random.randint(one_minute // chunk_length, (len(audio) // chunk_length)-4) * chunk_length
            moments.append(random_chunk)


    for i in range(0, len(audio), chunk_length):
        tmp_folder_name =  "/tmp/" +  str(uuid.uuid4())

        if not os.path.exists(tmp_folder_name):
            os.makedirs(tmp_folder_name)

        tmp_wav_name = tmp_folder_name + "/" + str(uuid.uuid4()) + ".wav"

        audio_chunk = audio[i:i + chunk_length]
        audio_chunk.export(tmp_wav_name, format="wav")

        if (i + chunk_length <= 60000):
            process = multiprocessing.Process(target=process_audio_chunk, args=((tmp_wav_name, "first_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

        elif len(audio) - (i + chunk_length) <= 60000:
            process = multiprocessing.Process(target=process_audio_chunk, args=((tmp_wav_name, "last_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

        elif i in moments or i-15000 in moments:
            process = multiprocessing.Process(target=process_audio_chunk, args=((tmp_wav_name, "middle_words"), result_queue, i + chunk_length))
            process.start()
            processes.append(process)

    for process in processes:
        process.join()