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