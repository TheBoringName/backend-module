import analyzer as an
import audio_to_text as att
import downloader as dwn

if __name__ == "__main__":
    video_url = input("Wprowadź link do filmu youtube: ")
    print("\n")
    print("Rozpoczynam pobieranie filmu...")
    audio_details = dwn.download_audio_from_youtube(video_url)
    print("Pobieranie filmu zakończono")
    print("\n")
    print("Rozpoczynam analize tekstową filmu...")
    audio_extend_details = att.split_audio_to_chunks(audio_details)
    print("Analiza tekstowa filmu zakończona")
    print("\n")
    print("Wysłanie informacji do GPT-3.5...")
    final_audio_details = an.analyze_text_via_gpt(audio_extend_details)
    print("GPT-3.5 Opowiedział na pytanie")
    print("\n\n\n\n\n")
    print("-----PODSUMOWANIE-----")

    text_to_send = f"""
    W kilku zdaniach opowiedz mi co myslisz o pewnym filmie,
    możesz jeszcze podzielić się wrażeniami twórcy, czy jest pozytywnie czy negatywnie nastawiony,
    odpowiedź zacznij słowami 'Ten film opowiada/jest o'
    Wiemy ze film ma tagi: {final_audio_details["tags"]}.
    Wiemy ze opis filmu to: {final_audio_details["title"]}.
    Na początku filmu autor powiedział: {final_audio_details["first_words"]}.
    W trakcie filmu padają zdania: {final_audio_details["middle_words"]}.
    Na koncu filmu autor powiedział: {final_audio_details["last_words"]}.
    Jeśli nie możesz nic powiedzieć o filmie, napisz, że film ma za mało informacji żeby go opisać
    """

    print(f"Wiadomość wysłana do GPT: \n {text_to_send}")
    print("\n\n--------\n\n")
    print(f"Odpowiedź GPT 3.5:\n {final_audio_details['gpt_response']}")

    #https://www.youtube.com/watch?v=ySXPnjStay4