import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound

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
        
        # Attempt to get the highest available thumbnail
        thumbnails = item['snippet'].get('thumbnails', {})
        if 'maxres' in thumbnails:
            thumbnail_url = thumbnails['maxres']['url']
        elif 'standard' in thumbnails:
            thumbnail_url = thumbnails['standard']['url']
        elif 'high' in thumbnails:
            thumbnail_url = thumbnails['high']['url']
        elif 'medium' in thumbnails:
            thumbnail_url = thumbnails['medium']['url']
        else:
            thumbnail_url = thumbnails.get('default', {}).get('url', '')

        if video_id:
            results.append((video_id, title, thumbnail_url))  # Include the thumbnail URL in the results

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
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Process the transcript into a list of dictionaries
        captions_list = [{'text': caption['text']} for caption in transcript]
        
        return captions_list

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except VideoUnavailable:
        return "The video is unavailable or has no transcript."
    except NoTranscriptFound:
        return "No transcript found for the requested language."
    except Exception as e:
        return f"Error fetching captions: {str(e)}"


