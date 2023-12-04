import openai
import os
import json
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

    if audio_details["type"] == "Local":
        if audio_details["length"] > 180000:
            text_to_send = f"""
            Na początku filmu autor powiedział: {audio_details["first_words"]}.
            W trakcie filmu padają zdania: {audio_details["middle_words"]}.
            Na koncu filmu autor powiedział: {audio_details["last_words"]}.
            """

        else:
            text_to_send = f"""
            W trakcie filmu padają zdania: {audio_details["text"]}.
            """

    else:
        if audio_details["length"] > 180000:
            text_to_send = f"""
            Wiemy ze film ma tagi: {audio_details["tags"]}.
            Wiemy ze opis filmu to: {audio_details["title"]}.
            Na początku filmu autor powiedział: {audio_details["first_words"]}.
            W trakcie filmu padają zdania: {audio_details["middle_words"]}.
            Na koncu filmu autor powiedział: {audio_details["last_words"]}.
            """

        else:
            text_to_send = f"""
            W kilku zdaniach opowiedz mi co myslisz o pewnym filmie,
            czy uważasz, że jest pozytywny czy negatywny? 
            odpowiedź zacznij słowami 'Ten film opowiada/jest o'
            Wiemy ze film ma tagi: {audio_details["tags"]}.
            Wiemy ze opis filmu to: {audio_details["title"]}.
            W trakcie filmu padają zdania: {audio_details["text"]}.
            Jeśli nie możesz nic powiedzieć o filmie, napisz, że film ma za mało informacji żeby go opisać
            oraz powiedz, że może film moze ma samą muzykę jeśli nie padają żadne zdania, albo są one niezrozumiałe
            """

    openai.Model.list()
    prompt1 = """
    twoim zadaniem jest streszczenie opinii autora o produkcie 
    opis nie powinien uwzględniać elementów filmu nie odnoszących się do produktu
    jeżeli autor podał ocenę, przeskaluj ją do zakresu 0-100, jeżeli nie podał podaj ocenę na podstawie jego sentymentu.
    ODPOWIEDZI UDZIEL W FORMACIE JSON ZGODNIE Z PRZYKŁADEM:
    {ocena: 50, opis: "Ten film opowiada o..."}
    jeżeli nie da się opisać filmu zamiast odpowiedzi napisz "BŁĄD"
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system", "content": prompt1},
            {"role": "user", "content": f"{text_to_send}"},
            {
                "role": "system",
                "content": "PAMIĘTAJ O FORMACIE ODPOWIEDZI, NIE DODAWAJ NIC INNEGO",
            },
        ],
    )
    try:
        possibly_json = response["choices"][0]["message"]["content"]
        output = json.loads(possibly_json)
        audio_details["gpt_response"] = output["opis"]
        audio_details["gpt_score"] = output["ocena"]
    except Exception as _:
        # gpt fucked up
        audio_details["gpt_score"] = None  # todo replace with something more reliable
        audio_details["gpt_response"] = "nie udało się skrócić tekstu"

    return audio_details


audio_details = {""}
