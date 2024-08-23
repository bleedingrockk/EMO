from flask import Flask, render_template, request
import time
# from googleapiclient.discovery import build
# from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_id = None
    if request.method == 'POST':
        api_key = request.form['api_key']
        query = request.form['query']
        video_id = youtube_search(api_key, query)
    return render_template('index.html', video_id=video_id)

def youtube_search(api_key, query, max_results=5):
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    results = []
    for item in search_response.get('items', []):
        video_id = item['id'].get('videoId')
        title = item['snippet'].get('title')
        if video_id:
            results.append((video_id, title))

    return results[0][0] if results else None

if __name__ == '__main__':
    app.run(debug=True)
