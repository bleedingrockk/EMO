import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
from collections import Counter
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from googleapiclient.discovery import build
from datetime import timedelta
import isodate

api_key = 'AIzaSyA_GneRzf-BNyXTf-rogarI-fuVJsvG-YE'

# This function will search the query on youtube and return a list of top 5 similar videos and prompt user to select one and return the video id
from googleapiclient.discovery import build
import isodate

def youtube_search(api_key, query, max_results=4, initial_results=30):
    # Build the YouTube service
    print("Building YouTube service...")
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Call the search.list method to perform a search, retrieving a larger set of initial results
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=initial_results
    ).execute()

    # Collect the search results
    results = []
    video_ids = []

    for item in search_response.get('items', []):
        video_id = item['id'].get('videoId')
        if video_id:
            video_ids.append(video_id)

    if video_ids:
        # Get video details including duration
        video_response = youtube.videos().list(
            id=','.join(video_ids),
            part='contentDetails'
        ).execute()

        for i, video in enumerate(video_response.get('items', [])):
            duration = video['contentDetails']['duration']
            duration_seconds = isodate.parse_duration(duration).total_seconds()

            # Only consider videos longer than 100 seconds
            if duration_seconds > 100:
                title = search_response['items'][i]['snippet']['title']
                thumbnails = search_response['items'][i]['snippet'].get('thumbnails', {})

                # Select the best available thumbnail
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

                # Append only if the video meets the duration criteria
                results.append((video_ids[i], title, thumbnail_url))
                print(f"Appended result - Video ID: {video_ids[i]}, Title: {title}, Thumbnail: {thumbnail_url}, Duration: {duration_seconds} seconds")

                # Stop once we have enough results
                if len(results) >= max_results:
                    break

    # Final results
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





# This function will use video ID to get captions from the video from youtube
def get_captions(video_id):
    try:
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Process the transcript into a list of dictionaries
        captions_list = [{'text': caption['text']} for caption in transcript]
        
        
    except VideoUnavailable:
        return "The video is unavailable or has no transcript."
    except NoTranscriptFound:
        return "No transcript found for the requested language."
    except Exception as e:
        return f"Error fetching captions: {str(e)}"




# This function will return comments with replies from youtube using video ID
def get_comments_with_replies(video_id, api_key, max_results=100):
    """
    This function retrieves comments for a YouTube video, including replies,
    up to a maximum of 10000 comments.

    Args:
        video_id: The ID of the YouTube video (e.g., "dQw4w9WgXcQ").
        api_key: Your YouTube Data API key.
        max_results: The maximum number of comments to retrieve per page (default: 100).

    Returns:
        A list of dictionaries containing comment text, author name (if available),
        and a list of replies (if any) for each comment, up to 10000 comments total.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)

    all_comments = []
    next_page_token = None
    comment_count = 0  # Track the total number of comments retrieved

    while True:
        comments_response = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results,
            pageToken=next_page_token  # Include pageToken if available
        ).execute()

        items = comments_response.get("items", [])
        for item in items:
            comment_data = item["snippet"]["topLevelComment"]["snippet"]
            comment = {
                "textDisplay": comment_data["textDisplay"],
                "authorDisplayName": comment_data.get("authorDisplayName"),
                "replies": []  # Empty list to store replies
            }
            # Check if replies exist and extract them
            replies = item.get("replies", {}).get("comments", [])
            for reply in replies:
                reply_data = reply["snippet"]
                comment["replies"].append({
                    "textDisplay": reply_data["textDisplay"],
                    "authorDisplayName": reply_data.get("authorDisplayName")
                })
            all_comments.append(comment)
            comment_count += 1  # Update comment count

        next_page_token = comments_response.get("nextPageToken")

        # Stop fetching comments if total count reaches 1000 or there are no more pages
        if comment_count >= 100 or not next_page_token:
            break
    #Returns a list of dictionaries
    return all_comments




#Get list of comments and commentors
def save_comments_as_list(comments_data):
    """
    Convert comments and their replies into separate lists of authors and text.

    Args:
        comments_data: A list of dictionaries containing comment and reply details.

    Returns:
        A tuple containing two lists:
        - A list of authors.
        - A list of comment texts.
    """
    author_list = []
    text_list = []

    for comment in comments_data:
        # Check and save 'authorDisplayName' and 'textDisplay' at the top level
        if 'authorDisplayName' in comment and 'textDisplay' in comment:
            author_list.append(str(comment['authorDisplayName']))
            text_list.append(str(comment['textDisplay']))

        # Check for replies and save 'authorDisplayName' and 'textDisplay' in replies
        if 'replies' in comment:
            for reply in comment['replies']:
                if 'authorDisplayName' in reply and 'textDisplay' in reply:
                    author_list.append(str(reply['authorDisplayName']))
                    text_list.append(str(reply['textDisplay']))

    return author_list, text_list




# Get top commentors

def get_top_commenters(author_list):
    """
    Get the top 10 most common commenters from the list.

    Args:
        author_list: A list of author names.

    Returns:
        A list of tuples containing the top 10 usernames and their counts.
    """
    # Count the occurrences of each username
    username_counts = Counter(author_list)

    # Get the top 10 most common usernames
    top_10_usernames = username_counts.most_common(10)

    return top_10_usernames





# Get Emojis data
import emoji

def extract_and_rank_top_emojis(text_list):
    """
    Extract emojis from a list of strings and return the top 10 most common emojis.

    Args:
        text_list: A list of strings from which to extract emojis.
    
    Returns:
        A list of tuples containing the top 10 most common emojis and their counts.
    """
    emojis_list = []

    # Extract emojis from each text in the list
    for text in text_list:
        emojis_list.extend([e['emoji'] for e in emoji.emoji_list(text)])

    # Count the occurrences of each emoji
    emoji_counts = Counter(emojis_list)

    # Get the top 10 most common emojis
    top_10_emojis = emoji_counts.most_common(10)

    return top_10_emojis




# Fucntion to clean the comments and store them as lists of strings
def clean_string(text):
    
    #Args: A string from which to extract
    # Example cleaning operations: remove punctuation and convert to lowercase
    cleaned_text = text.strip().lower()  # Remove leading/trailing whitespace and convert to lowercase
    cleaned_text = ''.join([c for c in cleaned_text if c.isalnum() or c.isspace()])  # Remove non-alphanumeric characters except spaces
    
    # Split the cleaned text into words
    words = cleaned_text.split()
    
    # Load stop words from nltk
    stop_words = set(stopwords.words('english'))
    
    # Remove stop words
    filtered_words = [word for word in words if word not in stop_words]
    
    # Join the filtered words back into a string
    cleaned_text_without_stopwords = ' '.join(filtered_words)

    return cleaned_text_without_stopwords


def cleaned_strings_list(text_list):

    #Args: A list of strings from which to extract
    # Returns: A cleaned string with punctuation removed and all characters converted to lowercase

    cleaned_list = []
    for text in text_list:
        cleaned_text = clean_string(text)
        cleaned_list.append(cleaned_text)
    return cleaned_list

