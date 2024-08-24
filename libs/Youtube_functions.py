import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

api_key = 'AIzaSyA_GneRzf-BNyXTf-rogarI-fuVJsvG-YE'

# This function will search the query on youtube and return a list of top 5 similar videos and prompt user to select one and return the video id
def youtube_search(api_key, query, max_results=5):
    # Build the YouTube service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Call the search.list method to perform a search
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    # Collect the search results
    results = []
    for item in search_response.get('items', []):
        video_id = item['id'].get('videoId')
        title = item['snippet'].get('title')
        if video_id:
            results.append((video_id, title))

    return results


# This function will use video ID to get details about the video from youtube
def get_video_details(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_response = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    ).execute()

    video_details = {}
    for item in video_response.get('items', []):
        video_details['title'] = item['snippet'].get('title')
        video_details['description'] = item['snippet'].get('description')
        video_details['view_count'] = item['statistics'].get('viewCount')
        video_details['like_count'] = item['statistics'].get('likeCount')
        video_details['comment_count'] = item['statistics'].get('commentCount')
        video_details['duration'] = item['contentDetails'].get('duration')

    return video_details


def get_captions(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        captions = transcript.fetch()

        captions_list = []
        for caption in captions:
            start = caption['start']
            duration = caption['duration']
            text = caption['text']
            captions_list.append({'start': start, 'duration': duration, 'text': text})

        return captions_list

    except Exception as e:
        return f"Error fetching captions: {str(e)}"
