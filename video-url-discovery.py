from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

def fetch_travel_videos(api_key: str, query: str, max_results: int = 10) -> list:
    """Fetches URLs of top travel videos along with metadata.

    Args:
        api_key (str): Your API key for the YouTube Data API.
        query (str): The search query (e.g., "Costa Rica travel").
        max_results (int): Maximum number of results to return.

    Returns:
        list: A list of dictionaries, each containing:
              * url: The video URL
              * creator: The video's content creator
              * date_uploaded: The date the video was uploaded
              * likes: The number of likes on the video
              * dislikes: The number of dislikes on the video
    """

    youtube = build('youtube', 'v3', developerKey=api_key)

    # Initial search to get video IDs
    search_response = youtube.search().list(
        q=query,
        part='id',
        maxResults=max_results,
        order='relevance',
        type='video'
    ).execute()

    video_ids = [result['id']['videoId'] for result in search_response.get('items', [])]

    # Fetch metadata for each video
    results = []
    for video_id in video_ids:
        try:
            metadata_response = youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()

            video_data = metadata_response['items'][0] 

            likes = int(video_data.get('statistics', {}).get('likeCount', 0))  # Convert to integer

            if likes > 100:  # Check if likes exceed 100
                results.append({
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'creator': video_data['snippet']['channelTitle'],
                    'date_uploaded': video_data['snippet']['publishedAt'],
                    'likes': likes, 
                    'dislikes': video_data.get('statistics', {}).get('dislikeCount', 'N/A') 
                })
        except HttpError as e:
            print(f'Error for video {video_id}: {e.resp.status} {e.content}')

    return results 

def read_api_key_from_file(file_path: str = "~/.youtube-api") -> str:
    """
    Read the YouTube Data API key from a file.

    Args:
        file_path (str): The path to the file containing the API key.

    Returns:
        str: The API key.
    """
    file_path = os.path.expanduser(file_path)
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key



# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
if __name__ == '__main__':
    api_key = read_api_key_from_file()

    try:
        videos = fetch_travel_videos(api_key, 'Costa Rica travel 2024',200)
        for url in videos:
            print(url)
    except HttpError as e:
        print(f'An HTTP error occurred: {e.resp.status} {e.content}')
        

videos = fetch_travel_videos(api_key, 'Costa Rica travel')
