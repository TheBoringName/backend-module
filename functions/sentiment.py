import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv

load_dotenv()
endpoint = os.getenv("AZURE_SENTIMENT_ENDPOINT")
key = os.getenv("AZURE_SENTIMENT_KEY")

def sentiment_analyze_via_azure(audio_details):

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    positive = 0.0
    neutral = 0.0
    negative = 0.0

    if "text" in audio_details:
        result = text_analytics_client.analyze_sentiment(audio_details["text"], show_opinion_mining=True)
        positive = float(result.confidence_scores.positive)
        neutral = float(result.confidence_scores.neutral)
        negative = float(result.confidence_scores.negative)

    else:
        all_text = [audio_details["first_words"], audio_details["middle_words"],  audio_details["last_words"]]
        result = text_analytics_client.analyze_sentiment(all_text, show_opinion_mining=True)
        texts = [text for text in result if not text.is_error]

        for text in enumerate(texts):
            positive += float(text.confidence_scores.positive)
            neutral += float(text.confidence_scores.neutral)
            negative += float(text.confidence_scores.negative)



    if positive > neutral and positive > negative:
        return "positive"
    elif negative > positive and negative > neutral:
        return "negative"
    else:
        return "neutral"



