import analyzer as an
import audio_to_text as att
import uploader as dwn

if __name__ == "__main__":
    video_type = input("Wybierz skąd pochodzi film:\n  1] Youtube\n  2] Instagram\n  3] TikTok\n  4] Lokalny Plik\n[Wybierz 1-4]: ")

    if video_type == "1":
        video_url = input("Wprowadź link do filmu na YouTube: ")
        print("\n")
        print("Rozpoczynam pobieranie filmu...")
        audio_details = dwn.download_audio_from_youtube(video_url)
        print("Pobieranie filmu zakończono")

    elif video_type == "2":
        video_url = input("Wprowadź link do filmu na Instagramie: ")
        print("\n")
        print("Rozpoczynam pobieranie filmu...")
        audio_details = dwn.download_audio_from_instagram(video_url)
        print("Pobieranie filmu zakończono")
    
    elif video_type == "3":
        video_url = input("Wprowadź link do filmu na TikToku: ")
        print("\n")
        print("Rozpoczynam pobieranie filmu...")
        audio_details = dwn.download_audio_from_tiktok(video_url)
        print("Pobieranie filmu zakończono")
    
    elif video_type == "4":
        video_path = input("Wprowadź ścieżkę do pliku: ")
        print("\n")
        print("Rozpoczynam pobieranie filmu...")
        audio_details = dwn.upload_audio_from_local(video_path)
        print("Pobieranie filmu zakończono")


    print("\n")
    print("Rozpoczynam analize tekstową filmu...")
    audio_extend_details = att.split_audio_to_chunks(audio_details)
    print("Analiza tekstowa filmu zakończona")
    print("\n")
    print("Wysłanie informacji do GPT-3.5...")
    final_audio_details = an.analyze_text_via_gpt(audio_extend_details)
    print("GPT-3.5 Opowiedział na pytanie")
    print("\n\n--------\n\n")
    print(f"Odpowiedź GPT 3.5:\n {final_audio_details['gpt_response']}")

