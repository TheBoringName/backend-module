
import openai
import os
from dotenv import load_dotenv

#------------------------------------#
#            OPENAI CREDS            #
#------------------------------------#

load_dotenv()
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API")



#------------------------------------#
#              FUNCTIONS             #
#------------------------------------#

def analyze_text_via_gpt(audio_details):

    text_to_send = f"""
    W kilku zdaniach (mogą być 3-4) opowiedz mi co myslisz o pewnym filmie,
    możesz jeszcze podzielić się wrażeniami twórcy, czy jest pozytywnie czy negatywnie nastawiony,
    odpowiedź zacznij słowami 'Ten film opowiada/jest o'
    Wiemy ze film ma tagi: {audio_details["tags"]}
    Wiemy ze opis filmu to: {audio_details["title"]}
    Na początku filmu autor powiedział: {audio_details["first_words"]}
    Na koncu filmu autor powiedział: {audio_details["last_words"]}
    Jeśli nie możesz nic powiedzieć o filmie, napisz, że film ma za mało informacji żeby go opisać
    """

    openai.Model.list()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{text_to_send}"}
        ]
    )

    audio_details['gpt_response'] = response['choices'][0]['message']['content']


    return audio_details