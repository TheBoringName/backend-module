# backend-repository

## Database schema
<p align="center">
    <img src="assets/db_schema.png"/>
</p>

## Fields definition

### Video 
- _id: Unique identifier for the video,
- title: Title of the video,   
- duration: Duration of the video in seconds,
- source: URL or file path of the video,
- publication_date: Date and time when the video was published as a timestamp

### Result
- _id: Unique identifier for the result,
- summary_score: Numeric score summarizing sentiment analysis,
- summary_text: Description of sentiment analysis result,
- summary_state: Sentiment state (Positive, Negative, Neutral),
- timestamp_generated: Date and time when the result was generated as a timestamp,
- video_id: Unique identifier of the associated video

## Sentiment functionalities

### How it works

Script fetches video from user's chosen option. Then video is converted to audio, divided into smaller chunks and uploaded to Azure SpeechToText service. Obtained results are send to Azure AI Language and to GPT-3.5 to get short description and opinion about the video.


#### Used services
- OpenAI GPT-3.5
    - API from OpenAI is used to get short information about the video.
- Azure Speech
    - This service is used to convert audio to text.
- Azure AI Language
    - This API is used to get sentiment analysis about the video.

### Video downloading

Backend allows to download videos from several platfoms:
- Youtube
- Tiktok
- Instagram

User can also upload file from the computer.

All methods can be found in the `downloader.py` file.


### Video to Audio
Due to problems with the new Youtube features (e.g. Audio track) script needs to download original videos (not only audio). 

To do this backend uses the `ffmpeg` lib and the `pydub` package.

### Audio to Text
To analyze the sound and convert it into text, script uses Azure Speech service. Because there are problems with continuous speech transmission (e.g.long pause in speech/long music - longer than 15 seconds) audio is divided into smaller, 20-second chunks.

### Opinion analysis
Using the Azure AI Language module, script sends words spoken in the intro, during and at the end of video. Then, Laguage module analyzes to determine if words in the video have positive, neutral or negative tone.

### Text analysis
For now, full text analysis is performed by the GPT-3.5 engine. Script sends to GPT information about the video tags, name, words spoken in the intro, during and at the end of video. We also limit and filter his statements.

### Backend Written in FLASK
For integration with website, API has been prepared using the FLASK framework.

### Backend Requests
Currently, we are using 4 different endpoints:

```
/describe
```
Allows to send video for the analysis. Request body:
```
"source": "Local/YouTube/TikTok/Instagram"
"url": "<VIDEO_URL>"
```
Note: If the video source is set to local, URL also has to be set to local

<br>

```
/find?title=<SEARCHED_VIDEO_TITLE>
```
Allows to find analyzed video by title. No request body

<br>

```
/history?page=<PAGE_NUMBER>
```
Allows to retrieve all records from db, paged. 10 entries for one page. No request body

<br>

```
/history/list?size=<LIST_SIZE>
```
Allows to retrieve any number of records from database
<br>

### Backend Responses
Responses for each endpoint are the same, concatenating the most important request from database.
Example response:
```
{
    "analysis": "Ten film opowiada o historii Polski, 
    skupiając się na jej trudnościach i przetrwaniu. 
    Przedstawione są cztery powody, dlaczego mamy tendencję 
    do skupiania się na trudnościach Polski w XX wieku.
    Film opowiada również o roli Polski jako "siatki siatkówki"
    Europy i analizuje współdziałanie z Litwą. 
    Pojawiają się informacje o średniowieczu i rozbiorach Polski,
    a także o znaczeniu wyboru Karola Wojtyły na papieża dla Polski.
    Film kończy się ostatecznie opisem Polski jako kraju,
    który przeszedł przez wiele trudności, 
    ale jest w stanie się od nich odbudować.",
    "analysis_date": "2023-12-07 21:29:02.174675",
    "sentiment": "negative",
    "source": "YouTube",
    "title": "History Summarized: Poland",
    "url": "https://www.youtube.com/watch?v=pJmSl148p_I"
}
```

### Requirements for Docker

- Fill `template.env` file and re-name to `.env`

- Build image:
```
docker compose build
```

- Run container:
```
docker compose up
```

- Access to container:
```
docker ps   #get container ID
docker exec -it <container-id> /bin/bash .
```

- Scripts:
All scripts are available in the `/app/functions` directory. For testing, you can run:
```
python3 example_main.py
```



### Requirements for using without Docker 

#### General:
- Fill template.env file and re-name to .env
- create venv and install packages from `requirements.txt` file

#### For Linux:
- Version: **Ubuntu 20.04** or **older** (problems with openssl lib, Azure doesn't support openssl 3.0).
- Download & Install `ffmpeg` lib:
``` 
apt-get update
apt-get install ffmpeg
```

### Credentials
Without a completed `template.env` file, script doesn't work!
```
IG_USERNAME= <instagram_username>
IG_PASSOWRD= <instagram_password>
IG_KEY=<instagram_2fa_secret_key>
AZURE_TOKEN= <azure_service_key>
AZURE_REGION= <azure_service_region>
AZURE_SENTIMENT_KEY=<azure_sentiment_service_key>
AZURE_SENTIMENT_ENDPOINT=<azure_sentiment_service_endpoint>
OPENAI_API= <openai_api_key>
OPENAI_ORG= <openai_organization>

```



